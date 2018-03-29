from . import Interpreter
from snips_nlu import load_resources, SnipsNLUEngine
from snips_nlu.builtin_entities import BuiltinEntityParser
import io, json

class SnipsInterpreter(Interpreter):
    
    def __init__(self, **kwargs):
        super(SnipsInterpreter, self).__init__('en')

        # TODO replace those ugly test code!

        load_resources('en')

        try:
            with open('trained.json') as f:
                self._engine = SnipsNLUEngine.from_dict(json.load(f))
        except FileNotFoundError:
            self._engine = SnipsNLUEngine()

            with open('sample_dataset.json') as f:
                self._engine.fit(json.load(f))

            with open('trained.json', mode='w') as f:
                json.dump(self._engine.to_dict(), f)

        self._entity_parser = BuiltinEntityParser('en')

    def get_metadata(self):
        meta = self._engine._dataset_metadata['slot_name_mappings']

        return { k: list(v.keys()) for k, v in meta.items() }

    def parse_entity(self, msg, intent, slot):
        parsed = self._entity_parser.parse(msg)

        if parsed:
            return parsed[0]['entity']['value']

        return msg

    def parse(self, msg):
        parsed = self._engine.parse(msg)

        # TODO safely retrieve values

        return [{
            'text': msg,
            'intent': parsed['intent']['intentName'],
            'slots': { s['slotName']: s['value']['value'] for s in parsed['slots'] }
        }]