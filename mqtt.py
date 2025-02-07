import paho.mqtt.client as paho
from paho.mqtt.client import MQTTMessage, Client
from mqtt_utils import device_message, object_from_json
import json

mqtt_client = paho.Client()

def mqtt_on_connect(client, userdata, flags, rc):
    if (rc == 0):
        print("Successfully connecting to local MQTT broker!")
    else:
        print(f"Failed to connect to MQTT broker! rc: {rc}")
    return

def mqtt_on_message(client: Client, userdata, msg: MQTTMessage):
    topic = msg.topic
    data = msg.payload.decode()
    print(f'Received message on topic "{topic}" with the payload: {data}')
    
    message: device_message = object_from_json(data)

    match message.type:
        case "info":
            print(F"Info message received from device")
        case _:
            print(F"Unknown type of message received from device")

    return

def mqtt_initialize_callbacks():
    """Sets callbacks to be used by the MQTT client"""

    mqtt_client.on_connect = mqtt_on_connect
    mqtt_client.on_message = mqtt_on_message
    return

def mqtt_subscribe_to_all():
    """Subscribe to necessary MQTT topics"""

    # Read from file and subscribe based on array
    return

def mqtt_connect():
    """Initialize connection to local MQTT broker"""

    mqtt_initialize_callbacks()
    mqtt_client.connect('localhost', 1883)
    mqtt_client.loop_start()
    mqtt_subscribe_to_all()
    return

