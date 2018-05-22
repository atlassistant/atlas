from atlas_sdk import SkillClient, Intent, Slot, Request

def turn_lights(request, switch):
  """
  :type request: Request

  """

  # If multiple values are found for the same slot, you will receive a list
  rooms = request.slot('room')

  if not rooms:
    return request.ask(_('For which room?'), slot='room') # pylint: disable=E0602

  if type(rooms) is not list:
    rooms = [rooms]

  request.show(_('Turning lights %s in %s') % (switch, ', '.join(rooms)), terminate=True) # pylint: disable=E0602

def turn_lights_on(request):
  turn_lights(request, 'on')

def turn_lights_off(request):
  turn_lights(request, 'off')

if __name__ == '__main__':
  lights_skill = SkillClient(
    name='lights',
    version='1.0.0',
    author='Julien LEICHER',
    description='Lights skill example',
    intents=[
      Intent('turnLightOn', turn_lights_on, [Slot('room')]),
      Intent('turnLightOff', turn_lights_off, [Slot('room')]),
    ],
  )

  lights_skill.run()
