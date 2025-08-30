class Modalidades:
    def __init__(self, codigo, descricao, codProfessor, valorDaAula, limiteAlunos, totalMatriculas):
        self.codigo = int(codigo)
        self.descricao = str(descricao)
        self.codProfessor = int(codProfessor)
        self.valorDaAula = int(valorDaAula)
        self.limiteAlunos = int(limiteAlunos)
        self.totalMatriculas = int(totalMatriculas)

    def __str__(self):
        return f"{self.codigo};{self.descricao};{self.codProfessor};{self.valorDaAula};{self.limiteAlunos};{self.totalMatriculas};"
