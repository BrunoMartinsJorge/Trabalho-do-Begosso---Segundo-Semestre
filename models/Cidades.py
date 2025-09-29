class Cidades:
    def __init__(self, codigo: int = 0, descricao: str = "", estado: str = ""):
        self.codigo = int(codigo)
        self.descricao = str(descricao)
        self.estado = str(estado)

    def __str__(self):
        return f"codigo: {self.codigo}, descricao: {self.descricao}, estado: {self.estado}"

    def __repr__(self):
        return f"Cidade(codigo={self.codigo}, descricao='{self.descricao}', estado='{self.estado}')"

    def to_dict(self):
        return {"codigo": self.codigo, "descricao": self.descricao, "estado": self.estado}