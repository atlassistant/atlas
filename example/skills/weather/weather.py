from atlas_sdk import SkillClient, Intent, Slot, Env, Request
import time
from dateutil.parser import parse as dateParse

def get_forecasts(request):
  """
  :type request: Request

  """

  yes = _('Yes') # pylint: disable=E0602
  no = _('No') # pylint: disable=E0602

  if request.choice == yes:
    date = request.slot('date', converter=dateParse)

    if not date:
      return request.ask(_('For when do you want the forecast?'), slot='date') # pylint: disable=E0602

    location = request.slot('city')

    if not location:
      return request.ask(_('For where do you want the forecast?'), slot='city') # pylint: disable=E0602

    time.sleep(3)

    # Do something with the key
    api_key = request.env('WEATHER_API_KEY') # pylint: disable=W0612

    request.show(_("Well, I'll try to find the forecasts for %s on %s") % (location, date), terminate=True)  # pylint: disable=E0602
  elif request.choice == no:
    return request.show(_('You have dismissed the command'), terminate=True) # pylint: disable=E0602

  return request.ask(_('Do you confirm the command?'), choices=[yes, no]) # pylint: disable=E0602

if __name__ == '__main__':
  weather_skill = SkillClient(
    name='weather',
    version='1.0.0',
    author='Julien LEICHER',
    description='Gives some weather forecasts',
    intents=[
      Intent('weatherForecast', get_forecasts, [Slot('date'), Slot('city')])
    ],
    env=[Env('WEATHER_API_KEY')]
  )

  weather_skill.run()
