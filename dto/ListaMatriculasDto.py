class ListaMatriculasDto:
    def __init__(self, codigo=0, nomeAluno='', descricao='', qtdAulas=0, valorPagar=0.0):
        self.codigo = codigo
        self.nomeAluno = nomeAluno
        self.descricao = descricao
        self.qtdAulas = qtdAulas
        self.valorPagar = valorPagar

    def __str__(self):
        return f"{self.codigo};{self.nomeAluno};{self.descricao};{self.qtdAulas};{self.valorPagar}"

    def __repr__(self):
        return (f"Cidade(codigo={self.codigo}, nomeAluno='{self.nomeAluno}', descricao='{self.descricao}', "
                f"qtdAulas='{self.qtdAulas}, valorPagar='{self.valorPagar})')")

    def to_dict(self):
        return {"codigo": self.codigo, "nomeAluno": self.nomeAluno, "descricao": self.descricao,
                "qtdAulas": self.qtdAulas, "valorPagar": self.valorPagar}
