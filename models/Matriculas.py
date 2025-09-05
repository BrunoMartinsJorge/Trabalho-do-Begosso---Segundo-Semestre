class Matriculas:
    def __init__(self, codigo, codAluno, codModalidade, quantidadeAulas):
        self.codigo = codigo
        self.codAluno = codAluno
        self.codModalidade = codModalidade
        self.quantidadeAulas = quantidadeAulas

    def __str__(self):
        return f"{self.codigo},{self.codAluno},{self.codModalidade};{self.quantidadeAulas}"

    def __repr__(self):
        return f"Cidade(codigo={self.codigo}, codAluno='{self.codAluno}', codModalidade='{self.codModalidade}', quantidadeAulas='{self.quantidadeAulas}')"

    def to_dict(self):
        return {"codigo": self.codigo, "codAluno": self.codAluno, "codModalidade": self.codModalidade,
                "quantidadeAulas": self.quantidadeAulas}
