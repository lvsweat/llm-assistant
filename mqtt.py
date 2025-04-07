import paho.mqtt.client as paho
from paho.mqtt.client import MQTTMessage, Client
from mqtt_utils import device_message, object_from_json
import json

def empty_function(msg: str):
    pass

mqtt_client = paho.Client()
on_message_postcall = empty_function

def mqtt_on_connect(client, userdata, flags, rc):
    if (rc == 0):
        print("Successfully connected to local MQTT broker!")
    else:
        print(f"Failed to connect to MQTT broker! rc: {rc}")
    return

def mqtt_on_message(client: Client, userdata, msg: MQTTMessage):
    topic = msg.topic
    data = msg.payload.decode()
    print(f'Received message on topic "{topic}" with the payload: {data}')
    
    message: device_message = object_from_json(data, device_message)

    llm_message = ""

    match message.data:
        case "info":
            print(f"Info message received from device")
        case "connection":
            print(f"Connection message received from device with the following data:")
            print(message.data)
            connected = message.data.get("connected")
            device_name = message.data.get("deviceName")
            if (connected == True):
                llm_message = f"Repeat the following exactly with nothing else. A device named {device_name} has just connected via MQTT."
        case _:
            print(f"Unknown type of message received from device")
    on_message_postcall(llm_message)
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

