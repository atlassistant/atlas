from . import Interpreter

class DummyInterpreter(Interpreter):
  """This is a tiny dummy interpreter used for testing.
  """

  def __init__(self):
    super(DummyInterpreter, self).__init__('dummy')
    
  def metadata(self):
    return {
        'weather_forecast': ['location', 'date'],
        'reminder': ['date', 'subject', 'message']
    }

  def parse(self, msg):
    return [{
      'text': msg,
      'intent': 'weather_forecast',
      'slots': {
        'date': 'tomorrow'
      }
    }, {
      'text': msg,
      'intent': 'reminder',
      'slots': {
        'subject': 'Sortir les poubelles',
        'date': 'tomorrow'
      } 
    }]