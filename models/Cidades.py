class Cidades:
    def __init__(self, codigo=0, descricao=0, estado=0):
        self.codigo = int(codigo)
        self.descricao = str(descricao)
        self.estado = str(estado)

    def __str__(self):
        return f"Codigo :{self.codigo}, Descricao :{self.descricao}, Estado :{self.estado}"