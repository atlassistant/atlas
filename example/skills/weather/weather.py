from atlas_sdk import SkillClient, Intent, Slot, Env, Request
import time

def get_forecasts(request):
  """
  :type request: Request

  """

  date = request.slot('date')

  if not date:
    return request.ask('date', _('For when do you want the forecast?')) # pylint: disable=E0602

  location = request.slot('location')

  if not location:
    return request.ask('location', _('For where do you want the forecast?')) # pylint: disable=E0602

  time.sleep(3)

  api_key = request.env('WEATHER_API_KEY') # pylint: disable=W0612

  request.show(_("Well, I'll try to find the forecasts for %s on %s") % (location, date), terminate=True)  # pylint: disable=E0602

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
