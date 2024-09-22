from pymongo.mongo_client import MongoClient
import os

class DatabaseConnection:
    def __init__(self, uri=str(os.getenv('URI')), db_name="air-canvas", collection_name="users"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def get_db(self):
        return self.db
    
    def validate_data(self, data, schema):
        for field, field_type in schema.items():
            if field not in data:
                raise ValueError(f"Missing field: {field}")
            
            if isinstance(field_type, dict):
                self.validate_data(data[field], field_type)
            elif not isinstance(data[field], field_type):
                raise ValueError(f"Field {field} is not of type {field_type.__name__}")

    def insert_document(self, document):
        schema = {
            'name': str,
            'password': str,
            'email': str
            }
        self.validate_data(document, schema)
        result = self.collection.insert_one(document)
        return result.inserted_id