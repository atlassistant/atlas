atlas
===

⚠️ This is an early version, so API may change in the future if this is needed! I'll try not to do so unless if there's no other possibilities.

**atlas** is a totally open-source assistant written in Python. It is totally interopable since it uses the MQTT protocol to communicate with third party skills.

It manages dialog states with the help of the [transitions](https://github.com/pytransitions) library and parses natural language with [snips](https://github.com/snipsco/snips-nlu). If snips doesn't fit your needs, you can subclass the `Interpreter` class and make your own 😉

Have a look at the [📚 documentation folder](documentation).

## Installation

*pip maybe...*

*Docker too...*

`git clone` this repository and run `python setup.py install`.

If you want an optimal development workflow, you will also need to `git clone https://github.com/atlassistant/atlas-sdk atlas_sdk` and install it using [its own instructions](https://github.com/atlassistant/atlas-sdk).

### NLU backends

Once installed, **atlas** will not have any dependency with a NLU backend. So you may want to install it yourself. Once done, don't forget to use the appropriated interpreter in the `atlas.yml` configuration file.

For example, if you use [snips-nlu](https://github.com/snipsco/snips-nlu), you must install it with `pip install snips-nlu` and use

```yml
interpreter: 
  type: 'atlas.interpreters.snips_interpreter.SnipsInterpreter'
```

in the atlas configuration file.

## Quickstart

Those quick steps use Snips as the NLU backend.

- Once installed, you must configure it using a [configuration file](documentation/CONFIGURATION.md).
- Drop your training files (appropriate for your backend) into the `<loader.training_path>`, you may use a tool such as [tracy](https://github.com/YuukanOO/tracy) to generates it.
- Drop your configuration files into the `<loader.env_path>`.
- Drop some skills scripts inside `<executor.path>`, each one should be in its own subfolder with an `atlas` file containing the command to run to executes your skill
- Start a MQTT broker, such as [mosquitto](https://mosquitto.org/)
- Start atlas with `atlas -c <your_configuration_file_path>.yml`
- Go to the `<server.url>` in your favorite browser to access the exposes PWA! (you may use another channel if you prefer)
- That's it!

## Contributing

Contribution are welcome! 

You're a developer or just want to know where this project is heading to? Have a look at the [extended TODO](TODO.md) file.

You want to support **atlas** by giving some money? Head over to Liberapay with this tiny button [![Donate using Liberapay](https://liberapay.com/assets/widgets/donate.svg)](https://liberapay.com/YuukanOO/donate), thanks ❤️!