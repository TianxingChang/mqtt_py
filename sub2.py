import paho.mqtt.client as mqtt
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json

# Connect to the MongoDB instance
uri = "mongodb+srv://terry:Createx032024@cleansensecluster.mdrztnb.mongodb.net/?retryWrites=true&w=majority"

def on_message(client, userdata, message):
    # insert the received message to mongodb: if no toilet found, insert a new document; otherwise, update the found document
    print(
        f"Received message on topic {message.topic}: {message.payload.decode()}")
    recv_json = json.loads(message.payload.decode())
    recv_id = recv_json["toilet_id"]
    insert_doc = current_collection.find_one({"toilet_id": recv_id})
    if not insert_doc:
        # not found
        current_collection.insert_one(recv_json)
        print(f'insert a new document: {recv_json}')
    else:
        current_collection.update_one(
            {"toilet_id": recv_id}, {"$set": recv_json})
        print(f'update document: {recv_json}')



mongo_client = MongoClient(uri, server_api=ServerApi('1'))
current_db = mongo_client["test"]
current_collection = current_db["current"]

# Create an MQTT client instance
client = mqtt.Client()

# St the callback function
client.on_message = on_message

client.connect("broker.emqx.io", 1883)
client.subscribe("ustoilet_isdworks!")

# Start the MQTT client loop to handle incoming messages
client.loop_forever()
# Define a callback function to handle incoming messages
        



