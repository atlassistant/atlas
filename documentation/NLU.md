Natural Language Understanding
===

**NLU** is provided by `Interpreter` subclasses. I already provide a `SnipsInterpreter` that parses sentences with the [snips-nlu](https://github.com/snipsco/snips-nlu) python library.

Whatever backend you are using, there some built-in features in **atlas** that extend NLU possibilities.

## Reserved intent names

They are some specific intent names that you should not take for your custom actions but should train to handle some specific case in the **atlas** core.

These are:

- `cancel`: Used to cancel an ongoing command

## Parametric intent name

When you're using the same pattern in your training examples for different intents, you may have some issue retrieving the correct one when inferring.

For example, when doing this kind of stuff:

- `turnOnLight`: `Turn lights on`, `Lights on`
- `turnOffLight`: `Turn lights off`, `Lights off`
- `turnOnFan`: `Turn the fan on`, `Fan on please`

and so on, the NLU may predict incorrectly the user intent because of pattern similarities.

For this purpose, you can create generic training sample and intent and extract entities such as `toggler` (on / off) and `entityType` (lights / fan / ...). But each entity type will need its own atlas `Skill`, registered for a specific entity (imagine a Hue skill to control Philips Hue devices) and a specific intent name, not the generic one.

That's where **Parametric intent name** comes to the rescue. If you define an intent such as `turn{toggler}{entityType}`, each `{placeholder}` will be replaced by the extracted slot value and the appropriate skill will be triggered.