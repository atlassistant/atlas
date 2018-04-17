Configuration
===

There many things you can configure in atlas via the `.yml` configuration file, here is a complete configuration file.

```yml
# Interpreter related settings
interpreter: 
  # Python type of the interpreter to use when parsing user inputs, every keys defined here will be made available in the interpreter constructor
  type: 'atlas.interpreters.snips_interpreter.SnipsInterpreter'

# Discovery related settings
discovery:
  # Launch a ping discovery request every n seconds
  interval: 10
  # Consider a skill has unregistered after n seconds
  timeout: 30

# Executor related settings
executor:
  # Where to look for skills. Every subfolder with an 'atlas' file in it describing what command should be run would be treated as an atlas skill and the command will be executed
  path: 'example/skills'

# Logs related settings
logs:
  # Log level define
  level: 'INFO'

# Web server related settings
server:
  # Host to bind to
  host: '0.0.0.0'
  # Port to bind to
  port: 5000
  # Set it to true to allow webpack rebuild
  debug: false

# Loader related settings
# You must at least have a "default.ini" and "default.json" in training and env path because it is used by atlas if no one can be found for the given user id (it looks for files with the given uid). It's kind of an anonymous configuration.
loader:
  # Where are stored training files for interpreters
  training_path: 'example/training'
  # Where to store generated trained files for interpreters
  trained_path: 'example/data'
  # Where are stored .ini files which contains user settings
  env_path: 'example/env'

# Broker related settings
broker:
  # Host of the MQTT broker
  host: 'localhost'
  # Port of the MQTT broker
  port: 1883
  # Username to connect to the broker
  username:
  # Password to connect to the broker
  password:
```