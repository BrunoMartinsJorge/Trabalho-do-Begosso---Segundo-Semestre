class Aluno:
    def __init__(self, codigo=0, nome=0, codCidade=0, nascimento=0, peso=0, altura=0, status=0):
        self.codigo = int(codigo)
        self.nome = str(nome)
        self.codCidade = int(codCidade)
        self.nascimento = str(nascimento)
        self.peso = int(peso)
        self.altura = int(altura)
        self.status = int(status)

    def __str__(self):
        return f"{self.codigo};{self.nome};{self.codCidade};{self.nascimento};{self.peso};{self.altura};{self.status}"

    def adicionarAluno(self):
        aluno = Aluno()
        aluno.nome = str(input(print("Digite o nome do aluno")
                               ))
        aluno.codCidade = int(input(print("Digite o codigo da cidade")))
        aluno.nascimento = str(input(print("Digite a data de nascimento do aluno")))
        aluno.peso = int(input("Digite o peso do aluno"))
        aluno.altura = int(input("Digite o altura do aluno"))
        return aluno

    def calcularIMC(self):
        return float(self.peso) / float(self.altura)
