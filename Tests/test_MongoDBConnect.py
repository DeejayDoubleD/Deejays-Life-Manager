import pytest
from pymongo import results, errors

from DatabaseConnects.MongoDBConnect import MongoDBConnect

# Define positive test data
TEST_HOST = "localhost"
TEST_PORT = 27017
TEST_DB_NAME = "test_db"
TEST_COLLECTION_NAME = "test_collection"
TEST_DOCUMENT = {"test_key": "test_value", "age": 30}

# Define test data for error testing

TEST_DOCUMENT_FALSE_SCHEMA = {"false_test_key": "test_value", "age": 30}
FALSE_TEST_PORT = 270171
FALSE_TEST_HOST = "false_host"

# Define tests
def test_insert_one_document_positive():
    mongo = MongoDBConnect(TEST_HOST, TEST_PORT, TEST_DB_NAME)
    inserted_id = mongo.insert_one_document(TEST_COLLECTION_NAME, TEST_DOCUMENT)
    assert isinstance(inserted_id, results.InsertOneResult)


def test_insert_one_document_false_schema():
    mongo = MongoDBConnect(TEST_HOST, TEST_PORT, TEST_DB_NAME)
    with pytest.raises(errors.WriteError):
        mongo.insert_one_document(TEST_COLLECTION_NAME, TEST_DOCUMENT_FALSE_SCHEMA)


def test_insert_one_document_false_port_and_host():
    mongo = MongoDBConnect(FALSE_TEST_HOST, FALSE_TEST_PORT, TEST_DB_NAME)
    with pytest.raises(errors.ServerSelectionTimeoutError):
        mongo.insert_one_document(TEST_COLLECTION_NAME, TEST_DOCUMENT_FALSE_SCHEMA)


def test_find_one_document_positive():
    mongo = MongoDBConnect(TEST_HOST, TEST_PORT, TEST_DB_NAME)
    document = mongo.find_one_document(TEST_COLLECTION_NAME, 'test_key', TEST_DOCUMENT['test_key'])
    assert document['test_key'] == TEST_DOCUMENT['test_key']


def test_update_one_document_positive():
    mongo = MongoDBConnect(TEST_HOST, TEST_PORT, TEST_DB_NAME)

    update_document = mongo.find_one_document(TEST_COLLECTION_NAME, 'test_key', TEST_DOCUMENT['test_key'])
    update_id = update_document['_id']
    update_data = {"age": 31}

    modified_count = mongo.update_one_document(TEST_COLLECTION_NAME, update_id, update_data)
    assert modified_count == 1
    updated_document = mongo.find_one_document(TEST_COLLECTION_NAME, 'age', 31)
    assert updated_document["age"] == update_data["age"]


def test_delete_one_document_positive():
    mongo = MongoDBConnect(TEST_HOST, TEST_PORT, TEST_DB_NAME)
    delete_document = mongo.find_one_document(TEST_COLLECTION_NAME, 'test_key', TEST_DOCUMENT['test_key'])
    delete_id = delete_document['_id']

    deleted_count = mongo.delete_one_document(TEST_COLLECTION_NAME, delete_id)
    assert deleted_count == 1
    document = mongo.find_one_document(TEST_COLLECTION_NAME, '_id', delete_id)
    assert document is None
