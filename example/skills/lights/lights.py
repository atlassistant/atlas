from atlas_sdk import SkillClient, Intent, Slot, Request

def turn_lights(request):
  """
  :type request: Request

  """

  # If multiple values are found for the same slot, you will receive a list
  rooms = request.slot('room')

  if not rooms:
    return request.ask('room', _('For which room?')) # pylint: disable=E0602

  if type(rooms) is not list:
    rooms = [rooms]

  request.show(_('Turning lights on in %s') % ', '.join(rooms), terminate=True) # pylint: disable=E0602

if __name__ == '__main__':
  lights_skill = SkillClient(
    name='lights',
    version='1.0.0',
    author='Julien LEICHER',
    description='Lights skill example',
    intents=[
      Intent('sampleTurnOnLight', turn_lights, [Slot('room')])
    ],
  )

  lights_skill.run()
