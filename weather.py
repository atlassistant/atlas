from transitions import Machine
import json
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    client.subscribe('atlas/intents/sampleGetWeather')

def on_message(client, userdata, msg):
    if msg.topic == 'atlas/intents/sampleGetWeather':
        data = json.loads(msg.payload)

        location = data.get('weatherLocation')
        date = data.get('weatherDate')
        id = data['__id']

        if not location:
            return client.publish('atlas/%s/dialog/ask' % id, json.dumps({
                'slot': 'weatherLocation',
                'text': 'Pour quelle ville veux-tu la météo ?',
            }))

        if not date:
            return client.publish('atlas/%s/dialog/ask' % id, json.dumps({
                'slot': 'weatherDate',
                'text': 'Pour quelle date veux-tu la météo ?',
            })) 

        
        client.publish('atlas/%s/dialog/show' % id, json.dumps({
            'text': 'Ok, je recherche la météo de %s pour %s' % (location, date)
        }))
        client.publish('atlas/%s/dialog/terminate' % id)

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('localhost')
    client.loop_forever()