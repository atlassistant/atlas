TODO
===

This file should help newcomers and contributors to know what are the next big **atlas** steps and where to start.

## Short term

- Unit testing!
- Make `parse_entity` retrieve a list of slots if needed in the snips interpreter
- Provides a CLI to expose a tiny web interface which takes training data and interpreter configuration as an input and outputs trained data with associated checksum. With this interface, it would be fairly easy to expose hosted trainer and use their power to train the model and only use the trained model on lightweight system such as a Rasp ;)
- Add support for complex UI, such as cards in the Progressive Web App.

## Mid term

- Provides a web admin interface to configure the entire system, from training to skill configuration management with user authentication and so on.

## Long term

- Package and repository management to ease the process of discovering and adding comprehensive and execution skills to our assistant.
