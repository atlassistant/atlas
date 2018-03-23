from snips_nlu import load_resources, SnipsNLUEngine
from snips_nlu.builtin_entities import BuiltinEntityParser
from snips_nlu.nlu_engine.utils import resolve_slots
import io, json

with open('./sample_dataset.json') as f:
  data = json.load(f)

load_resources('en')
engine = SnipsNLUEngine()

engine.fit(data)

parsed = engine.parse("tomorrow", "sampleGetWeather")

# meta = engine._dataset_metadata['slot_name_mappings']

# language = engine._dataset_metadata["language_code"]
# entities = engine._dataset_metadata["entities"]
                
#print (engine.intent_parsers[1].slot_fillers['sampleGetWeather'].get_slots('today'))

p = BuiltinEntityParser('en')
print(p.parse('5 degree'))