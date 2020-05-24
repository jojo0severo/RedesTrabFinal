import sys
from flask import Flask, request, render_template, jsonify, url_for
from manager.manager import Manager

args = sys.argv[1:]
flask_port, host, port, server_host, server_port, buffer_size = 5000, '127.0.0.1', 60001, '127.0.0.1', 65000, 4096
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
    return render_template('home.html', flask_port=flask_port)


@app.route('/subjects', methods=['GET', 'POST'])
def subjects():
    if request.method == 'POST':
        data = request.get_json()
        manager.connect_user(data)
        manager.recover_subjects()

        return jsonify(url_for('subjects'))

    recovered_subjects = manager.get_subjects()
    return render_template('subjects.html', subjects=recovered_subjects, flask_port=flask_port)


@app.route('/groups', methods=['GET', 'POST'])
def groups():
    if request.method == 'POST':
        data = request.get_json()
        manager.recover_groups(data)

        return jsonify(url_for('groups'))

    recovered_groups = manager.get_groups()
    user = manager.get_user()
    return render_template('groups.html',
                           flask_port=flask_port,
                           rooms=recovered_groups,
                           subject=user['subject']['name'],
                           subject_id=user['subject']['id'])


@app.route('/group', methods=['GET', 'POST'])
def group():
    if request.method == 'POST':
        data = request.get_json()
        manager.enter_group(data)

        return jsonify(url_for('group'))

    recovered_group = manager.get_group()
    user = manager.get_user()
    return render_template('group.html',
                           flask_port=flask_port,
                           group_id=user['group']['id'],
                           subject=user['subject']['name'],
                           group_name=recovered_group['name'],
                           people=recovered_group['users'])


@app.route('/newGroup', methods=['GET', 'POST'])
def new_group():
    if request.method == 'POST':
        data = request.get_json()
        manager.create_group(data)

        return jsonify(url_for('group'))

    return render_template('new_group.html', flask_port=flask_port)


@app.route('/leave', methods=['POST'])
def leave():
    manager.leave_group()

    return jsonify(url_for('groups'))


@app.route('/start', methods=['POST'])
def start():
    resp = manager.start_match()
    if resp:
        return jsonify(url_for('questions'))

    return jsonify('wait')


@app.route('/questions', methods=['GET', 'POST'])
def questions():
    if request.method == 'POST':
        data = request.get_json()
        manager.add_previous_answer(data)

        if manager.quiz.counter == 4:
            manager.end_match()
            return jsonify(url_for('end_match'))

        return jsonify(url_for('questions'))

    question = manager.get_question()

    if question is not None:
        return render_template('questions.html',
                               flask_port=flask_port,
                               question_title=question['title'],
                               alternatives=question['alternatives'])
    else:
        return render_template('questions.html',
                               flask_port=flask_port)


@app.route('/endGame', methods=['GET', 'POST'])
def end_match():
    resp = manager.get_results()
    if resp:
        return render_template('endgame.html', flask_port=flask_port, message=manager.get_message(), hide=True)

    return render_template('endgame.html', flask_port=flask_port, message='Waiting', hide=False)


if __name__ == '__main__':
    app.run(port=flask_port)
