from atlas_sdk import SkillClient, Intent, Slot, Env, Request, Message

def get_forecasts(request, message):
  """
  :type request: Request
  :type message: Message

  """

  date = message.slot('date')

  if not date:
    return request.ask('date', 'Pour quelle date veux-tu la météo ?')

  location = message.slot('location')

  if not location:
    return request.ask('location', 'Pour quel endroit veux-tu la météo ?')

  request.show('Très bien, je recherche la météo pour %s le %s' % (location, date), terminate=True)

if __name__ == '__main__':
  weather_skill = SkillClient(
    name='weather',
    version='1.0.0',
    author='Julien LEICHER',
    description='Gives some weather forecasts',
    intents=[
      Intent('weather_forecast', get_forecasts, [Slot('date'), Slot('location')])
    ],
    env=[Env('WEATHER_API_KEY')]
  )

  weather_skill.run()
