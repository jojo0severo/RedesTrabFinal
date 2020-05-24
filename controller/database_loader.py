import sqlite3
import random
from controller.manager import Manager
from controller.id_generator import Generator
from model.subject import Subject
from model.quiz import Quiz
from model.question import Question


class Loader:
    @property
    def manager(self):
        manager = Manager()

        conn = sqlite3.connect('data/database.db')
        cursor = conn.cursor()

        cursor.execute(
            'SELECT subject.id, name, question, correct_alternatives.texto, wrong_alternatives.texto FROM subject '
            'LEFT JOIN question ON subject.id = question.id_subject '
            'LEFT JOIN correct_alternatives ON question.id = correct_alternatives.id_question '
            'LEFT JOIN wrong_alternatives ON question.id = wrong_alternatives.id_question;')

        data = cursor.fetchall()

        for k in range(0, len(data), 12):
            questions = []
            for i in range(k, k + 12, 3):
                _, subject_name, question, correct_answer = data[i][:-1]
                alternatives = []
                for j in range(i, i + 3):
                    alternatives.append(data[j][-1])

                random.shuffle(alternatives)
                right_post = random.randint(0, 3)
                alternatives.insert(right_post, correct_answer)

                questions.append(Question(question, alternatives, right_post))

            subject_id = Generator()
            q = Quiz(subject_id, questions)
            manager.subjects[subject_id] = Subject(subject_id, data[k][1], q)

        return manager


# if __name__ == '__main__':
#     conn = sqlite3.connect('../data/database.db')
#     cursor = conn.cursor()
#
#     cursor.executescript(open('../data/tables.sql', 'r').read())
#
#     cursor.executescript(open('../data/insert_subjects.sql', 'r').read())
#     cursor.executescript(open('../data/insert_questions.sql', 'r').read())
#
#     conn.commit()
