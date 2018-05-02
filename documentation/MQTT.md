MQTT Topics
===

Here is a list and required body for all MQTT messages. There are some common concepts you need to know:

- `cid`: represents the conversation id, generated at each intent request
- `sid`: represents a channel id (or session id)
- `uid`: represents the user id

Every json property prefixed by a double underscore are considered as metadata.

## atlas/discovery/ping

Send a discovery request.

```json
{
  "version": "Version of the atlas server which sent this ping",
  "started_at": "datetime.utcnow().isoformat() at which it was started"
}
```

## atlas/discovery/pong

Send a discovery response.

```json
{
  "name": "Name of the skill",
  "author": "Author of the skill",
  "description": "Description of the skill",
  "version": "Version of the skill",
  "intents": {
    "intent_name": ["slot_name"]
  },
  "env": {
    "A_PARAMETER": "type"
  }
}
```

## atlas/{sid}/channel/create

Creates an agent for this channel.

```json
{
  "uid": "User identifier"
}
```

## atlas/{sid}/channel/created

Inform the channel that an agent has been succesfuly created.

```json
{
  "lang": "Language of the interpreter for this channel"
}
```   

## atlas/{sid}/channel/destroy

Destroy a channel.

## atlas/{sid}/channel/destroyed

Inform the channel that it has been destroyed by atlas.

## atlas/{sid}/channel/show

Show a message to the channel. In the future more properties will be added to handle more complex UI.

```json
{
  "text": "Message to show"
}
```

## atlas/{sid}/channel/ask

Ask for a slot value. In the future more properties will be added to handle more complex UI.

```json
{
  "text": "Question to ask"
}
```

## atlas/{sid}/channel/work

Inform the channel that a work has started.

## atlas/{sid}/channel/terminate

Inform the channel that a work has ended.

## atlas/intents/{intent_name}

Run a skill associated with an intent.

```json
{
  "__cid": "conversation_id",
  "__sid": "session_id",
  "__uid": "user_id",
  "__lang": "user language code",
  "__version": "atlas version",
  "__env": {
    "A_PARAMETER": "User configurated value"
  },
  "slot_name": "Slot value",
  "another_slot": ["If multiple values for the same slot are found", "They will be passed as an array"]
}
```

## atlas/{sid}/dialog/parse

Parses a message. The message to parse should be included as a raw payload.

## atlas/{sid}/dialog/ask

Ask for a slot value. Additional properties will be transfered directly to the channel.

```json
{
  "__cid": "conversation_id",
  "slot": "slot_name",
  "text": "Question to ask"
}
```

## atlas/{sid}/dialog/show

Show a message to the channel by forwarding it.

```json
{
  "__cid": "conversation_id",
  "text": "Message to show"
}
```

## atlas/{sid}/dialog/terminate

Terminates a dialog.

```json
{
  "__cid": "conversation_id",
}
```
