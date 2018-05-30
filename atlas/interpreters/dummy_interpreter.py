from . import Interpreter

class DummyInterpreter(Interpreter):
  """This is a tiny dummy interpreter used for testing.
  """

  def __init__(self):
    super(DummyInterpreter, self).__init__('dummy')
    
  def metadata(self):
    return {
        'weatherForecast': ['city', 'date'],
        'reminder': ['date', 'subject', 'message']
    }

  def training(self):
    return [{
      'text': 'will it rain today',
      'intent': 'weatherForecast'
    }, {
      'text': "what's the weather like today",
      'intent': 'weatherForecast'
    }]

  def parse(self, msg):
    # return []
    return [{
      'text': msg,
      'intent': 'weatherForecast',
      'slots': {
        'date': [{ 'value': '2018-05-20'}],
      }
    }]