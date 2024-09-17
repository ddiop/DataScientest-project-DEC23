import os
import random

import pymongo
from dotenv import load_dotenv
from pymongo import MongoClient


from pymongo.errors import ConnectionFailure
load_dotenv()


class MongoDBConnection:
    def __init__(self):


        mongo_url = "mongodb://root:example@mongo:27017/"
        self.client = MongoClient(mongo_url)
        print("Connected successfully!")



    def insert_documents(self, db_name, collection_name, document):
        try:
            # Connexion à la base de données

            client = self.client
            db = client[db_name]
            collection = db[collection_name]

            # Insertion du document
            result = collection.insert_many(document)

            print("save doc to database ",db)

            return result
        except pymongo.errors.BulkWriteError as e:
            # Gestion de l'erreur
            for error in e.details['writeErrors']:
                if error['code'] == 11000:  # Erreur de clé en double
                    print("Document already exists:", error['errmsg'])
                else:
                    print("Other error:", error['errmsg'])
        except Exception as e:
            print("An error occurred:", e)

    def get_documents_by_country(self, db_name, collection_name, country):
        # Connexion à la base de données
        client = self.client
        db = client[db_name]
        collection = db[collection_name]

        try:
            documents = list(collection.find({"name": country}))
            print(documents)
            return documents
        except Exception as e:
            print(f"Error while retrieving documents from MongoDB: {e}")
            return []



