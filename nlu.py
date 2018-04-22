from snips_nlu import load_resources, SnipsNLUEngine
from snips_nlu.builtin_entities import BuiltinEntityParser
from snips_nlu.nlu_engine.utils import resolve_slots
import io, json

with open('./example/training/default.json') as f:
  data = json.load(f)

load_resources('fr')
engine = SnipsNLUEngine()

engine.fit(data)

parsed = engine.parse("Quel temps va t-il faire demain et mardi")

# meta = engine._dataset_metadata['slot_name_mappings']

# language = engine._dataset_metadata["language_code"]
# entities = engine._dataset_metadata["entities"]
                
#print (engine.intent_parsers[1].slot_fillers['sampleGetWeather'].get_slots('today'))

r = dict()

for slot in parsed['slots']:
  name = slot['slotName']
  value = slot['value']['value']

  if name in r:
    if r[name] is not list:
      r[name] = [r[name]]

    r[name].append(value)
  else:
    r[name] = value

print (r)


# p = BuiltinEntityParser('en')
# print(p.parse('5 degree'))