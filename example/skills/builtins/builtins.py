from atlas_sdk import SkillClient, Intent, Request

def cancel(request):
  """
  :type request: Request
  """
  
  request.show(_('Copy that! Command aborted'), terminate=True) # pylint: disable=E0602

if __name__ == '__main__':
  skill = SkillClient(
    name='builtins',
    version='1.0.0',
    author='Julien LEICHER',
    description='Handle built-ins operations',
    intents=[
      Intent('atlas/cancel', cancel),
    ],
  )

  skill.run()