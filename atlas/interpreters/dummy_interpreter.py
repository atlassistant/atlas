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

  def training(self):
    return [{
      'text': 'will it rain today',
      'intent': 'weather_forecast'
    }, {
      'text': "what's the weather like today",
      'intent': 'weather_forecast'
    }]

  def parse(self, msg):
    return [{
      'text': msg,
      'intent': 'weather_forecast',
      'slots': {
        'date': 'tomorrow',
        'location': ['one', 'two', 'three']
      }
    }, {
      'text': msg,
      'intent': 'reminder',
      'slots': {
        'subject': 'Sortir les poubelles',
        'date': 'tomorrow'
      } 
    }]