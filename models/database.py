from pymongo import MongoClient

class Database:
    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client["your_database_name"]
        self.users_collection = self.db["users"]

    def create_user(self, user):
        result = self.users_collection.insert_one(user)
        return result.inserted_id

    def get_user(self, username):
        user = self.users_collection.find_one({"username": username})
        return user

    def update_user(self, username, updated_data):
        result = self.users_collection.update_one({"username": username}, {"$set": updated_data})
        return result.modified_count

    def delete_user(self, username):
        result = self.users_collection.delete_one({"username": username})
        return result.deleted_count
