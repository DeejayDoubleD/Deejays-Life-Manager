from flask_bcrypt import Bcrypt
from DatabaseConnects.MongoDBConnect import MongoDBConnect
from pymongo.errors import ServerSelectionTimeoutError


class LoginHandler:
    """
    Handles the login authentication and checks if username and password exists and is correct
    """

    def __init__(self, mongo_db: MongoDBConnect, flask_bcrypt: Bcrypt):
        self.mongo_db = mongo_db
        self.flask_bcrypt = flask_bcrypt

    def login_user(self, username: str, password: str) -> bool:
        """
        Checks if the username and password exists and is correct
        :param username: str = username to check
        :param password: str = password to check
        :return: bool = True if username and password exists and is correct, otherwise false
        """
        try:
            check_username: bool = self.check_username(username)
            check_password: bool = self.check_password(username, password)
        except ServerSelectionTimeoutError as error_message:
            raise error_message

        if check_username is True and check_password is True:
            return True
        else:
            return False

    def check_username(self, username: str) -> bool:
        """
        Checks if the given username exists in database collection 'User'
        :param username: str = username to check
        :return: bool = True if username exists, otherwise False
        """
        try:
            check_username: dict[str, any] = self.mongo_db.find_one_document('User', 'username', username)
        except ServerSelectionTimeoutError as error_message:
            raise error_message
        
        if check_username is None:
            return False
        else:
            return True

    def check_password(self, username: str, password: str) -> bool:
        """
        Checks if the given password is correct
        :param username: str = username to find the correct password
        :param password: str = password that has to be checked
        :return: bool = True if password is correct, otherwise False
        """
        try:
            check_password: dict[str, any] = self.mongo_db.find_one_document('User', 'username', username)
        except ServerSelectionTimeoutError as error_message:
            raise error_message

        if check_password is not None and self.flask_bcrypt.check_password_hash(check_password['password'], password) \
                is True:
            return True
        else:
            return False
