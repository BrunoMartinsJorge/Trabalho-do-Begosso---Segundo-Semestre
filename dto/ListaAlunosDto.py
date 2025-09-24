class ListaAlunos:
    def __init__(self, codigo=0, nome='', dataNascimento='', cidade=None):
        self.codigo = int(codigo)
        self.nome = str(nome)
        self.dataNascimento = dataNascimento
        self.cidade = str(cidade)

    def __str__(self):
        return f"{self.codigo};{self.nome};{self.dataNascimento};{self.cidade}"

    def __repr__(self):
        return f"Cidade(codigo={self.codigo}, nome='{self.nome}', dataNascimento='{self.dataNascimento}', cidade='{self.cidade}')"

    def to_dict(self):
        return {"codigo": self.codigo, "nome": self.nome, "dataNascimento": self.dataNascimento,
                "cidade": self.cidade}
