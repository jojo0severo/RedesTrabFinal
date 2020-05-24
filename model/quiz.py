

class Quiz:
    """
    Esta classe armazena as informações referentes a um quiz completo como o id do assunto e as questões.
    """

    def __init__(self, subject_id, questions):
        self.subject_id = subject_id
        self.questions = questions
