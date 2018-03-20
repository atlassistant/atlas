from transitions import Machine
import re
import logging
import json

class Agent(object):

    def __init__(self, data):
        self._log = logging.getLogger('shaun')
        self._intent = None
        self._param = None
        self.bag = {}
        self.requirements = { k: [a for a, b in v.items() if b['required'] == True] for k, v in data.items() }

        ask_states = ['%s__ask__%s' % (k, v) for k, d in data.items() for v in d.keys() if d[v]['required'] == True]
        intent_states = list(data.keys())
        states = ['asleep'] + intent_states + ask_states

        self._log.info('Registering states: \n\t%s' % "\n\t".join(states))
        
        self.machine = Machine(model=self, states=states, initial='asleep', send_event=True, before_state_change='save_environment')

        self.machine.add_transition('asleep', '*', 'asleep')

        for intent in intent_states:
            self._log.info('Registering state %s' % intent)
            self.machine.add_transition(intent, '*', intent, unless='check_slots', after='call_action')

        for ask in ask_states:
            (intent, _) = self._parse(ask)

            self._log.info('Registering transition %s -> %s' % (intent, ask))

            self.machine.add_transition(intent, '*', ask, conditions='check_slots', after='ask_for_slot')

    def save_environment(self, event):
        (intent, param) = self._parse(event.transition.dest)

        self._intent = intent if intent is not None else event.transition.dest
        self._param = param

        self._log.debug('Saving env with intent: %s - param: %s' % (self._intent, self._param))

    def reset(self):
        self._log.info('Resetting environment')
        self._intent = None
        self._param = None
        self.bag = {}
        self.to_asleep()

    def call_action(self, event):
        self._log.info('Calling the action "%s" now!' % event.transition.dest)
        self.reset() # Should I?

    def ask_for_slot(self, event):
        self._log.info('Requiring "%s" slot value' % self._param)

    def _parse(self, str):
        r = re.search('(.*)__ask__(.*)', str)

        if r:
            return (r.group(1), r.group(2))
        
        return (None, None)

    def check_slots(self, event):
        dest = event.transition.dest

        (intent, param) = self._parse(dest)

        if intent and param:
            return self.bag.get(param) == None

        return any([self.bag.get(k) == None for k in self.requirements[dest]])

    def next(self, data=None):
        if data and self._param:
            self._log.info('Setting data "%s" with value %s' % (self._param, data))
            self.bag[self._param] = data

        self.trigger(self._intent)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    with open('data.json') as f:
        data = json.load(f)

    agt = Agent(data)

    # print (agt.machine.events.keys())

    # agt.bag['location'] = 'Paris'
    agt.trigger('weather_forecast')

    agt.next('Paris')

    # agt.next('Today')
