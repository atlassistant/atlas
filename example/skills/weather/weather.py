from atlas_sdk import SkillClient, Intent, Slot, Env, Request
import time
from dateutil.parser import parse as dateParse

def get_forecasts(request):
  """
  :type request: Request

  """

  date = request.slot('date', converter=dateParse)

  if not date:
    return request.ask('date', _('For when do you want the forecast?')) # pylint: disable=E0602
  
  location = request.slot('city')

  if not location:
    return request.ask('city', _('For where do you want the forecast?')) # pylint: disable=E0602

  request.show(_("Well, I'm on it!")) # pylint: disable=E0602

  time.sleep(3) # Simulate fetching

  # Do something with the key
  api_key = request.env('WEATHER_API_KEY') # pylint: disable=W0612

  request.show(_("It's kinda sunny!"), 
    cards=[{
      "media": "https://image.flaticon.com/icons/svg/890/890347.svg",
      "header": "24°C",
      "subhead": date.strftime("%A %d %B"),
      "text": "Looks like it's sunny outside!"
    }, {
      "media": "https://image.flaticon.com/icons/svg/890/890347.svg",
      "header": "22°C",
      "subhead": date.strftime("%A %d %B"),
      "text": "Looks like it's sunny outside!"
    }], terminate=True)  # pylint: disable=E0602

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
