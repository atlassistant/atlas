atlas
===

**atlas** is a totally open-source assistant written in Python. It is totally interopable since it uses the MQTT protocol to communicate with third party skills.

It manages dialog states with the help of the [transitions](https://github.com/pytransitions) library and parses natural language with [snips](https://github.com/snipsco/snips-nlu). If snips doesn't fit your needs, you can subclass the `Interpreter` class and make your own 😉

Have a look at the [📚 documentation folder](documentation).

## Installation

*pip maybe...*

`git clone` this repository and run `pip install -r requirements.txt`.

For development, you will also need to `git clone https://github.com/atlassistant/atlas-sdk atlas_sdk` and install it using [its instruction](https://github.com/atlassistant/atlas-sdk).

### NLU backends

Once installed, **atlas** will not have any dependency with a NLU backend. So you may want to install it yourself. Once done, don't forget to use the appropriated interpreter in the `atlas.yml` configuration file.

For example, if you use [snips](https://github.com/snipsco/snips-nlu), you must install it with `pip install snips-nlu` and use

```yml
interpreter: 
  type: 'atlas.interpreters.snips_interpreter.SnipsInterpreter'
```

in the atlas configuration file.

## Launching

Have a look at the [example](example) folder for available configurations and launch **atlas** with the following command `python -m atlas.cli.main -c your_configuration.yml`.

If you want to test your skill, you can launch a tiny client CLI with `python -m atlas.cli.client <client_id>`.