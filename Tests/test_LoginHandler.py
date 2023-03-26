from typing import Any
from Handler.LoginHandler import LoginHandler
from DatabaseConnects.MongoDBConnect import MongoDBConnect
from main import flask_bcrypt

# Define test data
TEST_HOST: str = "localhost"
TEST_PORT: int = 27017
TEST_DB_NAME: str = "test_db"
TEST_COLLECTION_NAME: str = "User"
TEST_DOCUMENT: dict[str, Any] = {'username': 'test_user', 'password': flask_bcrypt.generate_password_hash('test_pw')
                                 .decode('utf-8')}
FALSE_USERNAME: str = 'false_username'
FALSE_PASSWORD: str = 'false_password'

test_database = MongoDBConnect(TEST_HOST, TEST_PORT, TEST_DB_NAME)
test_loginhandler: LoginHandler = LoginHandler(test_database, flask_bcrypt)
test_user = test_database.insert_one_document(TEST_COLLECTION_NAME, TEST_DOCUMENT)


def test_login_user_positive():

    user_logged_in: bool = test_loginhandler.login_user(TEST_DOCUMENT['username'], 'test_pw')
    assert user_logged_in is True


def test_login_user_false_username_and_password():
    user_logged_in: bool = test_loginhandler.login_user(FALSE_USERNAME, FALSE_PASSWORD)
    assert user_logged_in is False


def test_check_username_positive():
    check_username: bool = test_loginhandler.check_username(TEST_DOCUMENT['username'])
    assert check_username is True


def test_check_username_false_username():
    check_username: bool = test_loginhandler.check_username(FALSE_USERNAME)
    assert check_username is False


def test_check_password_positive():
    check_password: bool = test_loginhandler.check_password(TEST_DOCUMENT['username'], 'test_pw')
    assert check_password is True


def test_check_password_false_password():
    check_password: bool = test_loginhandler.check_password(TEST_DOCUMENT['username'], FALSE_PASSWORD)
    assert check_password is False
    test_database.delete_one_document(TEST_COLLECTION_NAME, test_user.inserted_id)
