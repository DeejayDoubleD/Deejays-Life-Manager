from flask_bcrypt import Bcrypt
from DatabaseConnects.MongoDBConnect import MongoDBConnect
from pymongo.errors import ServerSelectionTimeoutError


class LoginHandler:

    def __init__(self, mongo_db: MongoDBConnect, flask_bcrypt: Bcrypt):
        self.mongo_db = mongo_db
        self.flask_bcrypt = flask_bcrypt

    def login_user(self, username: str, password: str):
        check_username = self.check_username(username)
        check_password = self.check_password(username, password)

        if check_username is True and check_password is True:
            return True
        else:
            return False

    def check_username(self, username: str):
        try:
            check_username = self.mongo_db.find_one_document('User', 'username', username)
        except ServerSelectionTimeoutError as error_message:
            raise error_message
        
        if check_username is None:
            return False
        else:
            return True

    def check_password(self, username: str, password: str):
        try:
            check_password = self.mongo_db.find_one_document('User', 'username', username)
        except ServerSelectionTimeoutError as error_message:
            raise error_message

        if check_password is not None and self.flask_bcrypt.check_password_hash(check_password['password'], password) \
                is True:
            return True
        else:
            return False
