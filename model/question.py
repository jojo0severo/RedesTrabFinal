

class Question:
    """
    Classe que armazena as informações referentes a apenas una pergunta, como a alternativa correta, a pergunta
    e as alternativas.
    """
    def __init__(self, title, alternatives, correct_alternative):
        self.title = title
        self.alternatives = alternatives
        self.correct_alternative = correct_alternative
