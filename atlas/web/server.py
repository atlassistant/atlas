from flask import Flask, request
from flask_restful import Api, Resource
from flask_socketio import SocketIO, Namespace, emit
import logging, subprocess, os
from ..broker import BrokerConfig
from ..client import ChannelClient

app = Flask('atlas.web', static_folder='./public')
api = Api(app)
socketio = SocketIO(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

class ServerConfig:
    """Holds settings related to the web server.
    """

    def __init__(self, host='localhost', port=5000, debug=True):
        """Constructs a new ServerConfig.

        :param host: Host to bind to
        :type host: str
        :param port: Port to bind to
        :type port: int
        :param debug: Determines if we should run the web & webpack watch command
        :type debug: bool

        """

        self.host = host
        self.port = port
        self.debug = debug

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class HelloWS(Namespace):

    def __init__(self, config, namespace=None):
        super(HelloWS, self).__init__(namespace)

        self._config = config
        self._channels = {}

    def on_connect(self):
        client_id = request.sid

        channel = ChannelClient(client_id,
            on_ask=lambda d, _: socketio.emit('ask', d, namespace=self.namespace, room=client_id),
            on_show=lambda d, _: socketio.emit('show', d, namespace=self.namespace, room=client_id),
            on_terminate=lambda: socketio.emit('terminate', namespace=self.namespace, room=client_id))
        
        self._channels[client_id] = channel

        channel.start(self._config)

    def on_disconnect(self):
        self._channels[request.sid].stop()

        del self._channels[request.sid]

    def on_parse(self, data):
        self._channels[request.sid].parse(data)

class Server:
    """Web server for the atlas interface.
    """

    def __init__(self, config, broker_config):
        """Constructs a new Server with the given config.

        :param config: Configuration of the web server
        :type config: ServerConfig
        :param broker_config: Broker configuration
        :type broker_config: BrokerConfig

        """

        self._log = logging.getLogger('atlas.server')
        self._config = config

        api.add_resource(HelloWorld, '/hello')
        socketio.on_namespace(HelloWS(broker_config, '/ws'))

    def run(self):
        """Starts the web server.
        """
        
        # When in a debug mode, start webpack in watch mode automatically
        # This help makes the development easier
        if self._config.debug:
            p = subprocess.Popen('npm run start', cwd=os.path.dirname(__file__), shell=True)
            self._log.info('Started webpack')

        self._log.info('Starting web server on %s:%s' % (self._config.host, self._config.port))
        # app.run(self._config.host, self._config.port)#, debug=self._config.debug)

        socketio.run(app, self._config.host, self._config.port)

        # And terminate the process once done
        if self._config.debug:
            p.terminate()
            self._log.info('Stopped webpack')