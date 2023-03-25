import pymongo
from bson import ObjectId
from pymongo import results, errors
from typing import Any


class MongoDBConnect:
    def __init__(self, host, port, database):
        self.client = pymongo.MongoClient(host, port)
        self.database = self.client[database]

    def insert_one_document(self, insert_collection: str, insert_document: dict[str, Any]) -> results.InsertOneResult:
        """
        Inserts the document 'insert_document' in the collection 'insert_collection'.
        :param insert_collection: str = name of the collection where the document should be inserted
        :param insert_document: dict = dict that should be inserted into the collection 'insert_collection'
        :return: insert_message: InsertOneResult = Insert message from MongoDB Database
        """
        try:
            insert_message: results.InsertOneResult = self.database[insert_collection].insert_one(insert_document)

        except errors.WriteError as error_message:
            raise error_message

        except errors.ServerSelectionTimeoutError as error_message:
            raise error_message

        return insert_message

    def find_one_document(self, search_collection, search_key, search_value) -> dict[str, Any] | None:
        """
        Finds a document in the collection 'search_collection' with the search parameters 'search_key'
         and 'search_value'
        :param search_collection: str = collection you want to search in
        :param search_key: str = the key you want to search with
        :param search_value: Any = the value you want to search with
        :return: found_document: dict[str, Any] | None = dict with found document or None when the function cannot find
                 a matching document
        """
        try:
            found_document: dict[str, Any] | None = self.database[search_collection].find_one(
                {search_key: search_value})
        except errors.ServerSelectionTimeoutError as error_message:
            raise error_message

        return found_document

    def update_one_document(self, update_collection: str, update_id: ObjectId, update_data: dict[str, Any]) -> int:
        """
        updates the document with the id 'update_id' in the collection 'update_collection' with the data 'update_data'
        :param update_collection: str = collection where you want to update a document
        :param update_id: ObjectId = id from the document you want to update
        :param update_data: dict[str, Any] = data you want to update the document with
        :return: result.modified_count: int = number of updated documents
        """
        try:
            result: results.UpdateResult = self.database[update_collection].update_one({"_id": update_id},
                                                                                       {"$set": update_data})
        except errors.ServerSelectionTimeoutError as error_message:
            raise error_message

        return result.modified_count

    def delete_one_document(self, delete_collection: str, delete_id: ObjectId) -> int:
        """
        Deletes the document with the id 'delete_id' in the collection 'delete_collection'
        :param delete_collection: int = collection where you want to delete a document
        :param delete_id: ObjectId = id from the document you want to delete
        :return: result.deleted_count: int = number of deleted documents
        """
        try:
            result: results.DeleteResult = self.database[delete_collection].delete_one({"_id": delete_id})

        except errors.ServerSelectionTimeoutError as error_message:
            raise error_message

        return result.deleted_count
