from bson import ObjectId
from src.database import NoSQLDatabase
from src.decorators import handler_id_retrieve, handler_id_retrieve_list, handler_nosql_id
from src.utils import IRepository


class NoSQLRepository(IRepository):
    def __init__(self, db, collection, model):
        self.db: NoSQLDatabase = db
        self.collection = self.db.db_name[collection]
        self.model = model

    @handler_id_retrieve
    def create(self, data):
        obj = self.collection.insert_one(data)
        obj = self.collection.find_one({"_id": obj.inserted_id})
        return obj

    @handler_id_retrieve_list
    def get_all(self, filters=None):
        if filters:
            return self.collection.find(filters)
        return self.collection.find()

    @handler_id_retrieve_list
    def get_all_for_user(self, user_id):
        return self.collection.find({"owner_id": ObjectId(user_id)})

    @handler_nosql_id
    @handler_id_retrieve
    def get(self, id=None, filters=None):
        if filters:
            return self.collection.find_one(filters)
        return self.collection.find_one({"_id": ObjectId(id)})


    @handler_nosql_id
    @handler_id_retrieve
    def update(self, id, data):
        obj = self.collection.find_one({"_id": ObjectId(id)})
        if not obj:
            return None
        for key, value in data.items():
            obj[key] = value
        obj = self.collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": obj}, return_document=True)
        return obj
