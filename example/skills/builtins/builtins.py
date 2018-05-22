from atlas_sdk import SkillClient, Intent, Request

def cancel(request):
  """
  :type request: Request
  """
  
  request.show(_('Copy that! Command aborted'), terminate=True) # pylint: disable=E0602

def fallback(request):
  """
  :type request: Request
  """

  yes = _('Yes') # pylint: disable=E0602
  no = _('No') # pylint: disable=E0602

  if request.choice == yes:
    return request.show(_("Ok! I'll search the web for %s") % request.slot('text'), terminate=True) # pylint: disable=E0602
  elif request.choice == no:
    return request.terminate()

  return request.ask(_('Do you want me to search for %s?') % request.slot('text'), choices=[yes, no]) # pylint: disable=E0602

if __name__ == '__main__':
  skill = SkillClient(
    name='builtins',
    version='1.0.0',
    author='Julien LEICHER',
    description='Handle built-ins operations',
    intents=[
      Intent('atlas/cancel', cancel),
      Intent('atlas/fallback', fallback),
    ],
  )

  skill.run()