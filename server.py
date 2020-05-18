from flask import Flask, request, render_template, jsonify,redirect,json
import time
import sys
sys.setrecursionlimit(100000)
#from client_socket import Client

app = Flask(__name__)
client = None
subject = ""
room = ""
rooms_list = {"Sala A","Sala B"}
people = {"joao","Hellen"}
user = "Carlo"
type_client = ""
questions = [{ 
        "questionTitle": "Pergunta 1",
        "alternatives": ["Resposta 1", "Resposta 2", "Resposta 3", "Resposta 4"],
        "correctAlternative": 2
    },{ 
        "questionTitle": "Pergunta 2",
        "alternatives": ["Resposta2 1", "Resposta2 2", "Resposta2 3", "Resposta2 4"],
        "correctAlternative": 2
    }]
current_question = 0
correct_enswers = 0
winner = True
game_started = False
game_done = False


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
    from random import randint
    global room, people, user
    
    if user.upper().strip() in [i.upper().strip() for i in people]:
        sufix = randint(0,99)
        people.add(user+str(sufix))
    people.add(user)
    return render_template('room.html',groups = people ,room = [room],subject=[subject])

@app.route('/new-room', methods=['GET'])
def new_room():
    return render_template('new_room.html')

@app.route('/new-room', methods=['POST'])
def register_group():
    from random import randint
    
    global rooms_list
    
    new_room = request.get_json().get("new_room")
    if new_room.upper().strip() in [i.upper().strip().strip() for i in rooms_list]:
        sufix = randint(0,99)
        rooms_list.add(new_room + str(sufix))
    else:
        rooms_list.add(new_room)
    
    return jsonify('Ok')

def start_game():
    global questions, current_question, type_client, winner, game_done
    
    if current_question < len(questions):
    
        question = questions[current_question]
        question_title = question.get("questionTitle")
        answers = question.get("alternatives")

        current_question += 1
        return render_template('question.html',pergunta = [question_title], respostas = answers)
    else:
        if game_done:
            if winner:
                return render_template('winner.html')
            else:
                return render_template('loser.html')
        else:
            time.sleep(1)
            game_done = True
            return start_game()
    
@app.route('/question', methods=['GET'])
def get_question():
    global game_started
    
    if type_client == "host":
        print("envio de msg para comecar o jogo")
        return start_game()
    else:
        print("Verificar se o jogo esta ativo")
        
        game_on = game_started
        if game_on == False:
            time.sleep(1)
            game_started = True
            return get_question()
        else:
            return start_game()
        
@app.route('/answer', methods=['POST'])
def send_answer():
    global questions, current_question, correct_enswers
    
    question = questions[current_question - 1]
    correct_answer_index = question.get("correctAlternative")
    correct_answer = question["alternatives"][correct_answer_index]
    client_answer = request.get_json().get("answer")
    
    if client_answer == correct_answer:
        correct_enswers = correct_enswers + 1
    
    print(correct_enswers)
    
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
