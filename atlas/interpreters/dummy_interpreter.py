from . import Interpreter

class DummyInterpreter(Interpreter):

    def __init__(self, **kwargs):
        super(DummyInterpreter, self).__init__('en')

    def get_metadata(self):
        return {
            'weather_forecast': ['location', 'date'],
            'reminder': ['date', 'subject']
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