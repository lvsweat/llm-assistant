import paho.mqtt.client as paho


mqtt_client = paho.Client()

def mqtt_on_connect(client, userdata, flags, rc):
    if (rc == 0):
        print("Successfully connect to local MQTT broker!")
    else:
        print(f"Failed to connect to MQTT broker! rc: {rc}")
    return

def mqtt_initialize_callbacks():
    """Sets callbacks to be used by the MQTT client"""
    mqtt_client.on_connect = mqtt_on_connect
    return

def mqtt_subscribe_to_all():
    """Subscribe to necessary MQTT topics"""

    return

def mqtt_connect():
    """Initialize connection to local MQTT broker"""

    mqtt_initialize_callbacks()
    mqtt_client.connect('localhost', 1883)
    mqtt_client.loop_start()
    mqtt_subscribe_to_all()
    return

