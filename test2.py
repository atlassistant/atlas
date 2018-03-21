from transitions import Machine
import json
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    client.publish('/atlas/intents/register', json.dumps({
        'intent': 'weather_forecast',
        'slots': ['location', 'date'],
    }))
    client.subscribe('/atlas/intents/weather_forecast')

def on_message(client, userdata, msg):
    if msg.topic == '/atlas/intents/weather_forecast':
        data = json.loads(msg.payload)

        location = data.get('location')

        if not location:
            return client.publish('/atlas/dialog/ask', json.dumps({
                'param': 'location',
                'text': 'Pour quelle ville ?',
            }))

        print ("Ok, let'go for %s" % location)

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('localhost')
    client.loop_forever()