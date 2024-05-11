import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)


class MongoDBManager:
    def __init__(self):
        self.host = os.getenv('MONGO_HOST', 'localhost')
        self.port = os.getenv('MONGO_PORT', '27017')
        self.username = os.getenv('MONGO_USER')
        self.password = os.getenv('MONGO_PASSWORD')
        self.db_name = os.getenv('MONGO_DB_NAME')

        self.client = MongoClient(
            host=self.host,
            port=int(self.port),
            username=self.username,
            password=self.password
        )
        self.db = self.client[self.db_name]
        try:
            # Check the connection
            self.client.admin.command('ismaster')
        except ConnectionFailure:
            print("Server not available")

    def insert_document(self, collection_name, document, verbose=False):
        """ Insert a document into a collection """
        if verbose:
            print("Inserting document...")
        collection = self.db[collection_name]
        document_id = collection.insert_one(document).inserted_id
        if verbose:
            print("Document inserted with ID:", document_id)
        return document_id

    def find_document(self, collection_name, query, verbose=False):
        """ Find a document in a collection """
        if verbose:
            print("Finding document...")
        collection = self.db[collection_name]
        document_found = collection.find_one(query)
        if verbose:
            print("Document found:", document_found)
        return document_found

    def find_documents(self, collection_name, query, verbose=False):
        """ Find multiple documents in a collection """
        if verbose:
            print("Finding documents...")
        collection = self.db[collection_name]
        documents_found = list(collection.find(query))
        if verbose:
            print("Documents found:", documents_found)
        return documents_found

    def update_document(self, collection_name, query, new_values, verbose=False):
        """ Update a document in a collection """
        if verbose:
            print("Updating document...")
        collection = self.db[collection_name]
        updated_result = collection.update_one(query, {'$set': new_values})
        update_result = updated_result.modified_count
        if verbose:
            print("Documents updated:", update_result)
        return update_result

    def delete_document(self, collection_name, query, verbose=False):
        """ Delete a document from a collection """
        if verbose:
            print("Deleting document...")
        collection = self.db[collection_name]
        deletion_result = collection.delete_one(query)
        delete_result = deletion_result.deleted_count
        if verbose:
            print("Documents deleted:", delete_result)
        return delete_result


if __name__ == "__main__":
    mongo_manager = MongoDBManager()
