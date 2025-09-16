class ListaProfessores:
    def __init__(self, codigo=0, nome='', endereco='', telefone=None, cidade=''):
        self.codigo = int(codigo)
        self.nome = str(nome)
        self.endereco = endereco
        self.telefone = telefone
        self.cidade = str(cidade)

    def __str__(self):
        return f"{self.codigo};{self.nome};{self.endereco};{self.telefone};{self.cidade}"

    def __repr__(self):
        return f"Cidade(codigo={self.codigo}, nome='{self.nome}', endereco='{self.endereco}'. telefone='{self.telefone}', cidade='{self.cidade}')"

    def to_dict(self):
        return {"codigo": self.codigo, "nome": self.nome, "endereco": self.endereco, "telefone": self.telefone,
                "cidade": self.cidade}
