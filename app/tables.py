from pymongo import mongo_client

client = mongo_client('localhost', 27017)

current_db = client['pyloungedb']

collection_notif = current_db['notifications']