import paho.mqtt.client as mqtt
import json

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    client.publish('/atlas/dialog/parse', json.dumps({
        'sid': 'joe',
        'text': 'donne moi la météo'
    }))
    client.disconnect()

if __name__ == '__main__':
    client.on_connect = on_connect
    client.connect('localhost')
    client.loop_forever()