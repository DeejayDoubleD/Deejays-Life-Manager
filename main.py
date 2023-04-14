from flask import Flask, request, render_template, Response, redirect
from flask_bcrypt import Bcrypt

from Handler.LoginHandler import LoginHandler
from DatabaseConnects.MongoDBConnect import MongoDBConnect


MONGODB_HOST: str = 'localhost'
MONGODB_PORT: int = 27017
MONGODB_DATABASE: str = 'DeejaysLifeManager-Dev'


app: Flask = Flask(__name__, template_folder='templates')
flask_bcrypt: Bcrypt = Bcrypt(app)
mongo_db: MongoDBConnect = MongoDBConnect(MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE)


@app.route("/login", methods=['GET', 'POST'])
def login_user() -> Response | str:
    """
    Gets the username and password from the form and logs the user in with the login_handler module

    :return: Response 200 if username and password ist correct, else redirect response to login page | login
    form render template
    """
    if request.method == 'POST':
        login_handler: LoginHandler = LoginHandler(mongo_db, flask_bcrypt)
        username: str = request.form['username']
        password: str = request.form['password']

        logged_in: bool = login_handler.login_user(username, password)

        if logged_in is True:
            return Response('{"detail": "You have logged in successfully!"}', status=200,
                            mimetype='application/json')
        else:
            return redirect(request.referrer)

    return render_template('Login-Form.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
