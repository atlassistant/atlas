from cmd import Cmd
import sys
from ..client.channel_client import ChannelClient
from ..broker import BrokerConfig

class Prompt(Cmd):
    def __init__(self, client_id):
        super(Prompt, self).__init__()

        self.prompt = '> '
        self.client_id = client_id
        self.client = ChannelClient(self.client_id, on_ask=self.show_message, on_show=self.show_message, on_terminate=self.has_terminated)
        self.client.start(BrokerConfig())

    def show_message(self, data, raw):
        print (data.get('text'))
    
    def has_terminated(self):
        print ('-- intent has terminated')

    def default(self, arg):
        self.client.parse(arg)

    def do_exit(self, args):
        self.client.stop()

        raise SystemExit

if __name__ == '__main__':
    prompt = Prompt(sys.argv[1])
    prompt.cmdloop('Welcome %s!' % prompt.client_id)