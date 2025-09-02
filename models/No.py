class No:
    def __init__(self, codigo: int, index: int = 0):
        self.codigo = int(codigo)   # valor do nó
        self.index = int(index)      # posição no arquivo/lista
        self.esquerda: "No" | None = None
        self.direita: "No" | None = None

    def __repr__(self):
        return f"No(codigo={self.codigo}, loc={self.index})"