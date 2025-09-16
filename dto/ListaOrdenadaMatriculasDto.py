class ListaOrdenadaMatriculasDto:
    def __init__(self, codigo: int, nome_aluno: str, nome_cidade_aluno: str, descricao_modalidade: str,
                 nome_professor: str, valor_pago: float):
        self.codigo = codigo
        self.nome_aluno = nome_aluno
        self.nome_cidade_aluno = nome_cidade_aluno
        self.descricao_modalidade = descricao_modalidade
        self.nome_professor = nome_professor
        self.valor_pago = valor_pago

