class ListaModalidadesDto:
    def __init__(self, codigo=0, descricao='', professor='', valorAula=0.0, limite=0, totalMatriculados=0):
        self.codigo = codigo
        self.descricao = descricao
        self.professor = professor
        self.valorAula = valorAula
        self.limite = limite
        self.totalMatriculados = totalMatriculados

    def __str__(self):
        return f"{self.codigo};{self.descricao};{self.professor};{self.valorAula};{self.limite};{self.totalMatriculados}"

    def __repr__(self):
        return (f"Cidade(codigo={self.codigo}, descricao='{self.descricao}', professor='{self.professor}', valorAula='{self.valorAula}', limite='{self.limite}', "
                f"totalMatriculados='{self.totalMatriculados}')")

    def to_dict(self):
        return {"codigo": self.codigo, "descricao": self.descricao, "professor": self.professor,
                "valorAula": self.valorAula, "limite": self.limite, "totalMatriculados": self.totalMatriculados}
