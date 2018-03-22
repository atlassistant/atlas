from . import Interpreter

class DummyInterpreter(Interpreter):

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
                
            }
        }]