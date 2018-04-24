Example setup
===

## Usage

### With Docker

- `docker-compose up`
- Wait for the skills to be registered and access `http://localhost:5000`

### Without Docker

- Install the snips backend with `pip install snips-nlu`
- Launch a MQTT broker such as **mosquitto**
- Launch atlas with `atlas -c atlas.local.yml` inside this directory
- Wait for the skills to be registered and access `http://localhost:5000`

And try saying something such as `turn lights on in the kitchen and in the living room`, `turn lights on` or `will it rain on tuesday`.

## Folders explanation

- `training`: Contains training data for the interpreter
- `env`: Contains user configuration
- `skills`: Contains skills executed by the executor
- `data`: Contains trained data to speed up the loading time
