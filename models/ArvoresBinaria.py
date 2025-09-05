from typing import List, Any


class ArvoreBinaria:
    def __init__(self, esquerda: int = -1, direita: int = -1, info: int = 0, index: int = 0):
        self.esquerda = int(esquerda)
        self.direita = int(direita)
        self.info = int(info)
        self.index = int(index)

    def __repr__(self):
        return f"ArvoreBinaria({self.esquerda}, {self.direita}, {self.info}, {self.index})"

    @staticmethod
    def construir_arvore(dados: List[Any]):
        def get_codigo(item):
            if isinstance(item, dict):
                if 'codigo' in item:
                    return int(item['codigo'])
                if 'Codigo' in item:
                    return int(item['Codigo'])
                raise KeyError("Chave 'codigo' não encontrada no dict")
            if hasattr(item, 'codigo'):
                return int(getattr(item, 'codigo'))
            if hasattr(item, 'Codigo'):
                return int(getattr(item, 'Codigo'))
            raise AttributeError("Objeto não possui atributo 'codigo' ou 'Codigo'")

        codigos = [get_codigo(d) for d in dados]

        nos = [ArvoreBinaria(esquerda=-1, direita=-1, info=cod, index=i)
               for i, cod in enumerate(codigos)]

        if not nos:
            return nos, -1

        draiz = 0

        for novo_idx in range(1, len(nos)):
            current = draiz
            while True:
                if nos[novo_idx].info < nos[current].info:

                    if nos[current].esquerda == -1:
                        nos[current].esquerda = novo_idx
                        break
                    else:
                        current = nos[current].esquerda
                else:
                    if nos[current].direita == -1:
                        nos[current].direita = novo_idx
                        break
                    else:
                        current = nos[current].direita

        return nos, draiz
