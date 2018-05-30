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

  confirmation = request.slot('confirmation').first().value
  text = request.slot('text').first().value

  if confirmation:
    if confirmation == yes:
      return request.show(_("Ok! I'll search the web for %s") % text, terminate=True) # pylint: disable=E0602
    elif confirmation == no:
      return request.terminate()

  return request.ask('confirmation', [
    _('Do you want me to search for "%s"?') % text, # pylint: disable=E0602
    _('Should I search the web for "%s" ?') % text, # pylint: disable=E0602
  ], choices=[yes, no])

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