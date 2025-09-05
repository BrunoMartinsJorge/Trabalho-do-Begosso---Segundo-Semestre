class Professores:
    def __init__(self, codigo=0, nome=0, endereco=0, telefone=0, codCidade=0):
        self.codigo = int(codigo)
        self.nome = str(nome)
        self.endereco = endereco
        self.telefone = telefone
        self.codCidade = int(codCidade)

    def __str__(self):
        return f"{self.codigo};{self.nome};{self.endereco};{self.telefone};{self.codCidade}"

    def __repr__(self):
        return f"Cidade(codigo={self.codigo}, nome='{self.nome}', endereco='{self.endereco}'. telefone='{self.telefone}', codCidade='{self.codCidade}')"

    def to_dict(self):
        return {"codigo": self.codigo, "nome": self.nome, "endereco": self.endereco, "telefone": self.telefone,
                "codCidade": self.codCidade}
