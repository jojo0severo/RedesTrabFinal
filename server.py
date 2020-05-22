import sys
from flask import Flask, request, render_template, jsonify, url_for
from manager.manager import Manager


args = sys.argv[1:]
flask_port, host, port, server_host, server_port, buffer_size = 5000, '127.0.0.1', 9001, '127.0.0.1', 65000, 4096
try:
    flask_port = int(args[0])
    host = args[1]
    port = int(args[2])
    server_host = args[3]
    server_port = int(args[4])
    buffer_size = int(args[5])
except:
    pass

app = Flask(__name__)
manager = Manager(host=host, port=port, server_host=server_host, server_port=server_port, buffer_size=buffer_size)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/subjects', methods=['GET', 'POST'])
def subjects():
    if request.method == 'POST':
        data = request.get_json()
        manager.connect_user(data)
        manager.recover_subjects()

        return jsonify(url_for('subjects'))

    recovered_subjects = manager.get_subjects()
    return render_template('subjects.html', subjects=recovered_subjects)


@app.route('/groups', methods=['GET', 'POST'])
def groups():
    if request.method == 'POST':
        data = request.get_json()
        manager.recover_groups(data)

        return jsonify(url_for('groups'))

    recovered_groups = manager.get_groups()
    user = manager.get_user()
    return render_template('groups.html', rooms=recovered_groups, subject=user['subject']['name'])


@app.route('/group', methods=['GET', 'POST'])
def group():
    if request.method == 'POST':
        data = request.get_json()
        manager.enter_group(data)

        return jsonify(url_for('group'))

    recovered_group = manager.get_group()
    user = manager.get_user()
    return render_template('group.html',
                           subject=user['subject']['name'],
                           group_name=recovered_group['name'],
                           people=recovered_group['users'])


@app.route('/new_group', methods=['GET', 'POST'])
def new_group():
    if request.method == 'POST':
        data = request.get_json()
        manager.create_group(data)

        return jsonify(url_for('group'))

    return render_template('new_group.html')


@app.route('/start')
def start():
    return jsonify('ok')


@app.route('/leave', methods=['POST'])
def leave():
    manager.leave_group()

    return jsonify(url_for('groups'))


if __name__ == '__main__':
    app.run()
