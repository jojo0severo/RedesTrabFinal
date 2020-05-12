import sqlite3
from controller.manager import Manager


class Loader:
    @property
    def manager(self):
        manager = Manager()

        conn = sqlite3.connect('data/database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name, question.id, question FROM subject LEFT JOIN question;')
        names = cursor.fetchall()

        for name, question_id, question in names:
            manager._add_subject(name)

        return manager
