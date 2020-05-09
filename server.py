from flask import Flask, request, render_template, jsonify
from client_socket import Client

app = Flask(__name__)
client = None


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/doConnection/', methods=['POST'])
def do_connection():
    global client

    client = Client()
    client.send(request.get_json().encode('utf-8'))

    return jsonify('Ok')


if __name__ == '__main__':
    app.run()
