class DB_requests:

    def insert_data_to_collection(collection, data):
        filter = {'_id': data['_id']}
        new_values = {"$set": data}
        collection.update_one(filter, new_values, upsert=True)
