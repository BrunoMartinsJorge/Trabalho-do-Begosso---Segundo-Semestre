class Professores:
    def __init__(self, codigo=0, nome=0, endereco=0, telefone=0, codCidade=0):
        self.codigo = int(codigo)
        self.nome = str(nome)
        self.endereco = int(endereco)
        self.telefone = int(telefone)
        self.codCidade = int(codCidade)

    def __str__(self):
        return f"{self.codigo};{self.nome};{self.endereco};{self.telefone};{self.codCidade}"
