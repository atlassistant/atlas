from flask import Flask, render_template
import logging

class ServerConfig:
    """Holds settings related to the web server.
    """

    def __init__(self, host='localhost', port=5000):
        """Constructs a new ServerConfig.

        :param host: Host to bind to
        :type host: str
        :param port: Port to bind to
        :type port: int

        """

        self.host = host
        self.port = port

app = Flask('atlas.web', static_folder='./web/dist', template_folder='./web')

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

    # TODO structure!
    @app.route('/')
    def index():
        return 'hello'

    def run(self):
        """Starts the web server.
        """

        self._log.info('Starting web server on %s:%s' % (self._config.host, self._config.port))
        app.run(self._config.host, self._config.port)