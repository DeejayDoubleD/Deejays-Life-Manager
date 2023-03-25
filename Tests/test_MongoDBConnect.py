from typing import Any

import pytest
from bson import ObjectId
from pymongo import results, errors
from pymongo.results import InsertOneResult

from DatabaseConnects.MongoDBConnect import MongoDBConnect

# Define positive test data
TEST_HOST: str = "localhost"
TEST_PORT: int = 27017
TEST_DB_NAME: str = "test_db"
TEST_COLLECTION_NAME: str = "test_collection"
TEST_DOCUMENT: dict[str, Any] = {"test_key": "test_value", "age": 30}

# Define test data for error testing

TEST_DOCUMENT_FALSE_SCHEMA: dict[str, Any] = {"false_test_key": "test_value", "age": 30}
FALSE_TEST_PORT: int = 270171
FALSE_TEST_HOST: str = "false_host"

# Define tests


def test_insert_one_document_positive():
    """
    Tests if the function 'insert_one_document' inserts a given document properly
    """
    mongo: MongoDBConnect = MongoDBConnect(TEST_HOST, TEST_PORT, TEST_DB_NAME)
    inserted_id: InsertOneResult = mongo.insert_one_document(TEST_COLLECTION_NAME, TEST_DOCUMENT)
    assert isinstance(inserted_id, results.InsertOneResult)


def test_insert_one_document_false_schema():
    """
    Tests, if the function 'insert_one_document' raises an exception when the document failed the schema validation
    """
    mongo: MongoDBConnect = MongoDBConnect(TEST_HOST, TEST_PORT, TEST_DB_NAME)
    with pytest.raises(errors.WriteError):
        mongo.insert_one_document(TEST_COLLECTION_NAME, TEST_DOCUMENT_FALSE_SCHEMA)


def test_insert_one_document_false_port_and_host():
    """
    Tests, if the function 'insert_one_document' raises an exception when the mongodb isn't accessible because of a
    false port and hostname
    """
    mongo: MongoDBConnect = MongoDBConnect(FALSE_TEST_HOST, FALSE_TEST_PORT, TEST_DB_NAME)
    with pytest.raises(errors.ServerSelectionTimeoutError):
        mongo.insert_one_document(TEST_COLLECTION_NAME, TEST_DOCUMENT_FALSE_SCHEMA)


def test_find_one_document_positive():
    mongo: MongoDBConnect = MongoDBConnect(TEST_HOST, TEST_PORT, TEST_DB_NAME)
    document: dict[str, Any] = mongo.find_one_document(TEST_COLLECTION_NAME, 'test_key', TEST_DOCUMENT['test_key'])
    assert document['test_key'] == TEST_DOCUMENT['test_key']


def test_find_one_document_false_port_and_host():
    """
    Tests, if the function 'find_one_document' raises an exception when the mongodb isn't accessible because of a
    false port and hostname
    """
    mongo: MongoDBConnect = MongoDBConnect(FALSE_TEST_HOST, FALSE_TEST_PORT, TEST_DB_NAME)
    with pytest.raises(errors.ServerSelectionTimeoutError):
        mongo.find_one_document(TEST_COLLECTION_NAME, 'test_key', TEST_DOCUMENT['test_key'])


def test_update_one_document_positive():
    mongo: MongoDBConnect = MongoDBConnect(TEST_HOST, TEST_PORT, TEST_DB_NAME)

    update_document: dict[str, Any] = mongo.find_one_document(TEST_COLLECTION_NAME,
                                                              'test_key', TEST_DOCUMENT['test_key'])
    update_id: ObjectId = update_document['_id']
    update_data: dict[str, int] = {"age": 31}

    modified_count: int = mongo.update_one_document(TEST_COLLECTION_NAME, update_id, update_data)
    assert modified_count == 1
    updated_document: dict[str, any] = mongo.find_one_document(TEST_COLLECTION_NAME, 'age', 31)
    assert updated_document["age"] == update_data["age"]


def test_update_one_document_false_port_and_host():
    """
    Tests, if the function 'update_one_document' raises an exception when the mongodb isn't accessible because of a
    false port and hostname
    """
    mongo: MongoDBConnect = MongoDBConnect(FALSE_TEST_HOST, FALSE_TEST_PORT, TEST_DB_NAME)

    with pytest.raises(errors.ServerSelectionTimeoutError):
        update_document: dict[str, Any] = mongo.find_one_document(TEST_COLLECTION_NAME,
                                                                  'test_key', TEST_DOCUMENT['test_key'])
        update_id: ObjectId = update_document['_id']
        update_data: dict[str, int] = {"age": 31}
        mongo.update_one_document(TEST_COLLECTION_NAME, update_id, update_data)


def test_delete_one_document_positive():
    mongo: MongoDBConnect = MongoDBConnect(TEST_HOST, TEST_PORT, TEST_DB_NAME)
    delete_document: dict[str, Any] = mongo.find_one_document(TEST_COLLECTION_NAME,
                                                              'test_key', TEST_DOCUMENT['test_key'])
    delete_id: ObjectId = delete_document['_id']

    deleted_count: int = mongo.delete_one_document(TEST_COLLECTION_NAME, delete_id)
    assert deleted_count == 1
    document: dict[str, Any] = mongo.find_one_document(TEST_COLLECTION_NAME, '_id', delete_id)
    assert document is None


def test_delete_one_document_false_port_and_host():
    """
    Tests, if the function 'delete_one_documentt' raises an exception when the mongodb isn't accessible because of a
    false port and hostname
    """
    mongo: MongoDBConnect = MongoDBConnect(FALSE_TEST_HOST, FALSE_TEST_PORT, TEST_DB_NAME)

    with pytest.raises(errors.ServerSelectionTimeoutError):
        delete_document: dict[str, Any] = mongo.find_one_document(TEST_COLLECTION_NAME,
                                                                  'test_key', TEST_DOCUMENT['test_key'])
        delete_id: ObjectId = delete_document['_id']
        mongo.delete_one_document(TEST_COLLECTION_NAME, delete_id)
