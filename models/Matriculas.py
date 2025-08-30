class Matriculas:
    def __init__(self, codigo, codAluno, codModalidade, quantidadeAulas):
        self.codigo = codigo
        self.codAluno = codAluno
        self.codModalidade = codModalidade
        self.quantidadeAulas = quantidadeAulas

    def __str__(self):
        return f"{self.codigo},{self.codAluno},{self.codModalidade};{self.quantidadeAulas}"
