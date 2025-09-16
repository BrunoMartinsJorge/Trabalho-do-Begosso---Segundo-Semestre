class FaturamentoModalidadeDto:
    def __init__(self, descricao: str, nome_professor: str, cidade_professor: str, valor_faturado: float):
        self.descricao = descricao
        self.nome_professor = nome_professor
        self.cidade_professor = cidade_professor
        self.valor_faturado = valor_faturado

    def to_dict(self):
        return {
            "descricao": self.descricao,
            "nome_professor": self.nome_professor,
            "cidade_professor": self.cidade_professor,
            "valor_faturado": float(self.valor_faturado)
        }