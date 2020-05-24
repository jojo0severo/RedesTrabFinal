

class Quiz:
    def __init__(self, name, questions):
        self.name = name
        self.questions = questions
        self.answers = []
        self.counter = 0

    def next_question(self):
        if self.counter == len(self.questions):
            return False

        next_question = self.questions[self.counter]
        self.counter += 1

        return next_question

    def add_answer(self, answer):
        self.answers.append(str(self.questions[self.counter-1].correct_alternative) == answer)

    def points(self):
        return sum([1 if ans else 0 for ans in self.answers])
