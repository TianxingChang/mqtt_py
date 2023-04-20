import paho.mqtt.client as mqtt
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Connect to the MongoDB instance
uri = "mongodb+srv://terry:Createx032024@cleansensecluster.mdrztnb.mongodb.net/?retryWrites=true&w=majority"
mongo_client = MongoClient(uri, server_api=ServerApi('1'))
current_db = mongo_client["test"]
current_collection = current_db["current"]

# Define a callback function to handle incoming messages


def on_message(client, userdata, message):
    print(
        f"Received message on topic {message.topic}: {message.payload.decode()}")
    cursor = current_collection.find({})
    for document in cursor:
        print(document)


# Create an MQTT client instance
client = mqtt.Client()

# Set the callback function
client.on_message = on_message

client.connect("broker.emqx.io", 1883)
client.subscribe("ustoilet_isdworks!")

# Start the MQTT client loop to handle incoming messages
client.loop_forever()
