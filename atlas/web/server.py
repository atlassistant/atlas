from flask import Flask, request, render_template, send_file
from flask_restful import Api, Resource
from flask_socketio import SocketIO, Namespace, emit
import logging, subprocess, os
from ..version import __version__
from atlas_sdk import BrokerConfig, ChannelClient

app = Flask('atlas.web', static_folder='./public', template_folder='./public')
app.config['TEMPLATES_AUTO_RELOAD'] = True

api = Api(app)
socketio = SocketIO(app)

@app.route('/')
def index():
  # TODO language from user settings

  return render_template('index.html', lang=request.args.get('lang', 'en-US'), version=__version__)

@app.route('/sw.js')
def serve_service_worker():
  return send_file('public/sw.js')

class ServerConfig:
  """Holds settings related to the web server.
  """

  def __init__(self, broker_config, url=None, host='localhost', port=5000, debug=True):
    """Constructs a new ServerConfig.

    :param broker_config: Broker config used by the web server for websocket channels
    :type broker_config: BrokerConfig
    :param host: Host to bind to
    :type host: str
    :param port: Port to bind to
    :type port: int
    :param debug: Determines if we should run the web & webpack watch command
    :type debug: bool

    """

    self.url = url or 'http://%s:%d' % (host, port)
    self.host = host
    self.port = port
    self.debug = debug
    self.broker = broker_config

class HelloWorld(Resource):
  def get(self):
    return {'hello': 'world'}

class Server:
  """Web server for the atlas interface.
  """

  def __init__(self, config):
    """Constructs a new Server with the given config.

    :param config: Configuration of the web server
    :type config: ServerConfig

    """

    self._log = logging.getLogger('atlas.server')
    self._channels = {}
    self._config = config

    api.add_resource(HelloWorld, '/hello')

    socketio.on_event('connect', self.on_connect)
    socketio.on_event('disconnect', self.on_disconnect)
    socketio.on_event('parse', self.on_parse)

  def on_connect(self):
    """Called when a connection has been made by a websocket.
    """

    client_id = request.sid

    channel = ChannelClient(client_id, 1337, # TODO Replace with a true user id
      on_ask=lambda d, _: socketio.emit('ask', d, room=client_id),
      on_show=lambda d, _: socketio.emit('show', d, room=client_id),
      on_terminate=lambda: socketio.emit('terminate', room=client_id),
      on_work=lambda: socketio.emit('work', room=client_id),
    )
    
    self._channels[client_id] = channel

    channel.start(self._config.broker)

  def on_disconnect(self):
    """Called when a websocket has disconnected.
    """

    self._channels[request.sid].stop()

    del self._channels[request.sid]

  def on_parse(self, data):
    """Called when a websocket client wants to parse data.

    :param data: Data received
    :type data: str

    """

    self._channels[request.sid].parse(data)

  def run(self):
    """Starts the web server.
    """
        
    # When in a debug mode, start webpack in watch mode automatically
    # This help makes the development easier
    if self._config.debug:
      p = subprocess.Popen('npm run start', cwd=os.path.dirname(__file__), shell=True)
      self._log.info('Started webpack')

    self._log.info('🌐 Starting web server on %s:%s, public url is %s' % (self._config.host, self._config.port, self._config.url))
    # app.run(self._config.host, self._config.port)#, debug=self._config.debug)

    socketio.run(app, self._config.host, self._config.port)

    # And terminate the process once done
    if self._config.debug:
      p.terminate()
      self._log.info('Stopped webpack')