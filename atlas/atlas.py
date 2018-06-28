from atlas_sdk.runnable import Runnable

class Atlas(Runnable):
  
  def run(self):
    print ('launching atlas')

  def cleanup(self):
    print ('cleaning stuff up')