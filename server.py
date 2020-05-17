from flask import Flask, request, render_template, session
from functools import wraps
from client_socket import ClientSender


app = Flask(__name__)
manager = Manager()


def session_decorator(function):
    @wraps(function)
    def session_checker(*args, **kwargs):
        user = session.get('USER')
        if user is None:
            return render_template('home.html')

        return function(*args, **kwargs)

    return session_checker


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/doConnection', methods=['POST'])
@session_decorator
def doConnection():
    data = request.get_json()


if __name__ == '__main__':
    app.run()
