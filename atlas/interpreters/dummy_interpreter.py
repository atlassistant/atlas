from . import Interpreter

class DummyInterpreter(Interpreter):
  """This is a tiny dummy interpreter used for testing.
  """

  def __init__(self):
    super(DummyInterpreter, self).__init__('dummy')
    
  def metadata(self):
    return {
        'sampleGetWeather': ['weatherLocation', 'weatherDate'],
        'reminder': ['date', 'subject', 'message']
    }

  def training(self):
    return [{
      'text': 'will it rain today',
      'intent': 'sampleGetWeather'
    }, {
      'text': "what's the weather like today",
      'intent': 'sampleGetWeather'
    }]

  def parse(self, msg):
    return [{
      'text': msg,
      'intent': 'sampleGetWeather',
      'slots': {
        'weatherDate': '2018-05-20',
      }
    }]