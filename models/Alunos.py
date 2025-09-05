class Alunos:
    def __init__(self, codigo=0, nome=0, codCidade=0, nascimento=0, peso=0, altura=0):
        self.codigo = int(codigo)
        self.nome = str(nome)
        self.codCidade = int(codCidade)
        self.nascimento = str(nascimento)
        self.peso = int(peso)
        self.altura = int(altura)

    def __str__(self):
        return f"{self.codigo};{self.nome};{self.codCidade};{self.nascimento};{self.peso};{self.altura}"

    def calcularIMC(self):
        return float(self.peso) / float(self.altura)

    def __repr__(self):
        return f"Aluno(codigo={self.codigo}, nome='{self.nome}', codCidade='{self.codCidade}', nascimento='{self.nascimento}', peso='{self.peso}', altura='{self.altura}'"

    def to_dict(self):
        return {"codigo": self.codigo, "nome": self.nome, "codCidade": self.codCidade, "nascimento": self.nascimento,
                "peso": self.peso, "altura": self.altura}
