from flask import Flask, request, render_template, jsonify,redirect,json
#from client_socket import Client

app = Flask(__name__)
client = None
subject = ""
room = ""
rooms_list = ["Sala A","Sala B"]
people = {"joao","Hellen"}
user = "Carlo"


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/room', methods=['POST'])
def room():
    global subject, room

    if request.get_json().get("subject") is None:
        room = request.get_json().get("room")
    else:
        subject = request.get_json().get("subject")
        
        
    print("assunto: {}".format(subject))
    print("sala: {}".format(room))
    
    return jsonify('Ok')


@app.route('/subject', methods=['GET'])
def subjects_page():
    
    subjects = ["Assunto A","Assunto B","Assunto C"]#client.subject
    print(subjects)
    print(type(subjects))
    return render_template('subjects.html',subjects = subjects)

@app.route('/rooms', methods=['GET'])
def rooms():
    global subject,rooms_list
    return render_template('rooms.html',groups = rooms_list,subject=[subject])

@app.route('/room', methods=['GET'])
def return_room():
    global room, people, user
    print("sala: {}".format(room))
    if user in people:
        people.add(user+str(range(99)))
    people.add(user)
    return render_template('room.html',groups = people ,room = [room],subject=[subject])

@app.route('/new-room', methods=['GET'])
def new_room():
    return render_template('new_room.html')

@app.route('/new-room', methods=['POST'])
def register_group():
    global rooms_list
    new_room = request.get_json().get("new_room")
    print(new_room)
    rooms_list.append(new_room)
    
    return jsonify('Ok')

@app.route('/doConnection/', methods=['POST'])
def do_connection():
    # global client

    # client = Client()
    # client.send(str(request.get_json()).encode('utf-8'))
    # subjects = client.send('{"event": "getSubjects", "json": {}}'.encode('utf-8'))

    # client.subject = json.loads(subjects)["data"]
    return jsonify('Ok')




if __name__ == '__main__':
    app.run()
