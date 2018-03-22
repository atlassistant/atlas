from transitions import Machine
import json
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    client.subscribe('atlas/intents/weather_forecast')

def on_message(client, userdata, msg):
    if msg.topic == 'atlas/intents/weather_forecast':
        data = json.loads(msg.payload)

        location = data.get('location')
        date = data.get('date')
        id = data['__id']

        if not location:
            return client.publish('atlas/%s/dialog/ask' % id, json.dumps({
                'slot': 'location',
                'text': 'Pour quelle ville veux-tu la météo ?',
            }))

        if not date:
            return client.publish('atlas/%s/dialog/ask' % id, json.dumps({
                'slot': 'date',
                'text': 'Pour quelle date veux-tu la météo ?',
            })) 

        print ("Ok, let'go for %s" % location)

        client.publish('atlas/%s/dialog/terminate' % id)

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('localhost')
    client.loop_forever()