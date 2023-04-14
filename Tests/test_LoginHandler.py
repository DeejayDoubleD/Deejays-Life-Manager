from typing import Any

import pytest
from pymongo.errors import ServerSelectionTimeoutError
from Handler.LoginHandler import LoginHandler
from DatabaseConnects.MongoDBConnect import MongoDBConnect
from main import flask_bcrypt

# Define positive test data
TEST_HOST: str = "localhost"
TEST_PORT: int = 27017
TEST_DB_NAME: str = "test_db"
TEST_COLLECTION_NAME: str = "User"
TEST_DOCUMENT: dict[str, Any] = {'username': 'test_user', 'password': flask_bcrypt.generate_password_hash('test_pw')
                                 .decode('utf-8')}
TEST_DATABASE = MongoDBConnect(TEST_HOST, TEST_PORT, TEST_DB_NAME)
TEST_LOGINHANDLER: LoginHandler = LoginHandler(TEST_DATABASE, flask_bcrypt)
TEST_USER = TEST_DATABASE.insert_one_document(TEST_COLLECTION_NAME, TEST_DOCUMENT)


# Define negative test data
FALSE_USERNAME: str = 'false_username'
FALSE_PASSWORD: str = 'false_password'
FALSE_TEST_HOST: str = "false_host"
FALSE_TEST_PORT: int = 0000
FALSE_TEST_DATABASE = MongoDBConnect(FALSE_TEST_HOST, FALSE_TEST_PORT, TEST_DB_NAME)
FALSE_TEST_LOGINHANDLER: LoginHandler = LoginHandler(FALSE_TEST_DATABASE, flask_bcrypt)


def test_login_user_positive():
    """
    Tests if the function 'login_user' returns True when given a correct username and password
    """
    user_logged_in: bool = TEST_LOGINHANDLER.login_user(TEST_DOCUMENT['username'], 'test_pw')
    assert user_logged_in is True


def test_login_user_false_username_and_password():
    """
    Tests if the function 'login_user' returns False when given an incorrect username and password
    """
    user_logged_in: bool = TEST_LOGINHANDLER.login_user(FALSE_USERNAME, FALSE_PASSWORD)
    assert user_logged_in is False


def test_login_user_false_no_database_connection():
    """
    Tests if the function 'login_user' raises an exception when the mongodb isn't accessible because of a
    false port and hostname
    """
    with pytest.raises(ServerSelectionTimeoutError):
        FALSE_TEST_LOGINHANDLER.login_user(TEST_DOCUMENT['username'], 'test_pw')


def test_check_username_positive():
    """
    Tests if the function 'check_username' returns True when given a correct username
    """
    check_username: bool = TEST_LOGINHANDLER.check_username(TEST_DOCUMENT['username'])
    assert check_username is True


def test_check_username_false_username():
    """
    Tests if the function 'check_username' returns False when given an incorrect username
    """
    check_username: bool = TEST_LOGINHANDLER.check_username(FALSE_USERNAME)
    assert check_username is False


def test_check_username_no_database_connection():
    """
    Tests if the function 'check_username' raises an exception when the mongodb isn't accessible because of a
    false port and hostname
    """
    with pytest.raises(ServerSelectionTimeoutError):
        FALSE_TEST_LOGINHANDLER.check_username(TEST_DOCUMENT['username'])


def test_check_password_positive():
    """
    Tests if the function 'check_password' returns True when given a correct password
     """
    check_password: bool = TEST_LOGINHANDLER.check_password(TEST_DOCUMENT['username'], 'test_pw')
    assert check_password is True


def test_check_password_false_password():
    """
    Tests if the function 'check_password' returns False when given an incorrect password
    """
    check_password: bool = TEST_LOGINHANDLER.check_password(TEST_DOCUMENT['username'], FALSE_PASSWORD)
    assert check_password is False
    TEST_DATABASE.delete_one_document(TEST_COLLECTION_NAME, TEST_USER.inserted_id)


def test_check_password_no_database_connection():
    """
    Tests if the function 'check_password' raises an exception when the mongodb isn't accessible because of a
    false port and hostname
    """
    with pytest.raises(ServerSelectionTimeoutError):
        FALSE_TEST_LOGINHANDLER.check_password(TEST_DOCUMENT['username'], 'test_pw')
