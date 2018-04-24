Example setup
===

## Usage

- Install the snips backend with `pip install snips-nlu`
- Launch a MQTT broker such as **mosquitto**
- Launch atlas with `atlas` inside this directory
- Wait for the skills to be registered and access `http://localhost:5000`

And try saying something such as `turn lights on in the kitchen and in the living room`, `turn lights on` or `will it rain tomorrow`.

## Folders

- `training`: Contains training data for the interpreter
- `env`: Contains user configuration
- `skills`: Contains skills executed by the executor
- `data`: Contains trained data to speed up the loading time

## Known limitations

When a skill ask for a slot value, it only handle one value and not an array of value. I'm on it!