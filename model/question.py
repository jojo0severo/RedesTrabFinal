

class Question:
    """
    Classe que armazena as informações referentes a uma pergunta.
    Como a pergunta, as alternativas e a alternativa correta.
    """

    def __init__(self, title, alternatives, correct_alternative):
        self.title = title
        self.alternatives = alternatives
        self.correct_alternative = correct_alternative
