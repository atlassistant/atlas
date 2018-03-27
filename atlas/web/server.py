from flask import Flask, render_template
from flask_restful import Api, Resource
import logging, subprocess, os

app = Flask('atlas.web', static_folder='./public')
api = Api(app)

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

class Server:
    """Web server for the atlas interface.
    """

    def __init__(self, config):
        """Constructs a new Server with the given config.

        :param config: Configuration of the web server
        :type config: ServerConfig

        """

        self._log = logging.getLogger('atlas.server')
        self._config = config

        api.add_resource(HelloWorld, '/hello')

    def run(self):
        """Starts the web server.
        """
        
        # When in a debug mode, start webpack in watch mode automatically
        # This help makes the development easier
        if self._config.debug:
            p = subprocess.Popen('npm run start', cwd=os.path.dirname(__file__), shell=True)
            self._log.info('Started webpack')

        self._log.info('Starting web server on %s:%s' % (self._config.host, self._config.port))
        app.run(self._config.host, self._config.port)#, debug=self._config.debug)

        # And terminate the process once done
        if self._config.debug:
            p.terminate()
            self._log.info('Stopped webpack')