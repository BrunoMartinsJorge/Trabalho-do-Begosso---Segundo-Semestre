class RelatorioGeralModalidadeDto:
    def __init__(self, modalidade='', cidadeProfessor='', professor='', valorFaturado=0.0):
        self.modalidade = modalidade
        self.cidadeProfessor = cidadeProfessor
        self.professor = professor
        self.valorFaturado = valorFaturado

    def __str__(self):
        return f"{self.modalidade};{self.cidadeProfessor};{self.professor};{self.valorFaturado}"

    def __repr__(self):
        return f"Cidade(modalidade={self.modalidade}, cidadeProfessor='{self.cidadeProfessor}', professor='{self.professor}'. valorFaturado='{self.valorFaturado}')"

    def to_dict(self):
        return {"modalidade": self.modalidade, "cidadeProfessor": self.cidadeProfessor, "professor": self.professor,
                "valorFaturado": self.valorFaturado}
