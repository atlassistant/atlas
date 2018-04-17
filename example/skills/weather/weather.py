from atlas_sdk import SkillClient, Intent, Slot, Env, Request
import time

def get_forecasts(request):
  """
  :type request: Request

  """

  date = request.slot('date')

  if not date:
    return request.ask('date', 'Pour quelle date veux-tu la météo ?')

  location = request.slot('location')

  if not location:
    return request.ask('location', 'Pour quel endroit veux-tu la météo ?')

  time.sleep(3)

  request.show('Très bien, je recherche la météo pour %s le %s avec la clé %s' % (location, date, request.env('WEATHER_API_KEY')), terminate=True)

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
