from cmd import Cmd
import sys
from atlas_sdk import ChannelClient, BrokerConfig
from ..agent import generate_hash

class Prompt(Cmd):
  def __init__(self, user_id):
    super(Prompt, self).__init__()

    self.prompt = '> '
    self.uid = user_id
    self.client_id = generate_hash()
    self.client = ChannelClient(self.client_id, self.uid, 
      on_ask=self.show_message, 
      on_show=self.show_message, 
      on_terminate=self.has_terminated,
      on_work=self.on_work
    )
    self.client.start(BrokerConfig())

  def show_message(self, data, raw):
    print (data.get('text'))

  def on_work(self):
    print('-- work has started')
  
  def has_terminated(self):
    print ('-- intent has terminated')

  def default(self, arg):
    self.client.parse(arg)

  def do_exit(self, args):
    self.client.stop()

    raise SystemExit

if __name__ == '__main__':
  prompt = Prompt(sys.argv[1])
  prompt.cmdloop('Welcome %s!' % prompt.uid)