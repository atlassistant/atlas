TODO
===

This file should help newcomers and contributors to know what are the next big **atlas** steps and where to start.

## Short term

- Unit testing!
- Provides a CLI to expose a tiny web interface which takes training data and interpreter class as an input and outputs trained data with associated checksum. With this interface, it would be fairly easy to expose hosted trainer and use their power to train the model and only use the trained model on lightweight system such as a Rasp ;)
- Handle multiple choices. Skill should be able to ask for limited choices via `atlas/<sid>/dialog/ask { "slot": "slot_name", "text": "Select a choice", "choices": ["one", "two", "three"] }` and the Agent should be able to use fuzzy matching to make user inputs maps on one of them.

## Mid term

- Provides a web admin interface to configure the entire system, from training to skill configuration management with user authentication and so on.

## Long term

- Package and repository management to ease the process of discovering and adding comprehensive and execution skills to our assistant.

## For me

- [ ] Documentation architecture
- [x] Fin UI
- [ ] Checksum interpréteur
- [x] Configuration des skills
- [x] Gestion multi users, passer un ui à l'Agent + la config de l'env pour cet utilisateur
- [-] SDK python (localization support)