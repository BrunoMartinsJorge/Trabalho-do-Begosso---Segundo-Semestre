from typing import List, Any


class ArvoreBinaria:

    def __init__(self, esquerda=-1, direita=-1, info=0, index=0):
        self.esquerda = int(esquerda)
        self.direita = int(direita)
        self.info = int(info)
        self.index = int(index)

    def __str__(self):
        return f"Esquerda: {self.esquerda}, Direita: {self.direita}, Codigo: {self.info}, Localizacao: {self.index}"

    @staticmethod
    def __ver_se_existe_na_lista(lista_codigo, codigo_atual):
        return codigo_atual in lista_codigo

    @staticmethod
    def leitura_exaustiva_generica(indices: List["ArvoreBinaria"], lista: List[Any]):
        usados = set()
        while len(usados) < len(lista):
            menor = None
            for registro in indices:
                codigo = registro.info
                if not ArvoreBinaria.__ver_se_existe_na_lista(usados, codigo):
                    if menor is None or codigo < menor.info:
                        menor = registro
            if menor:
                print(lista[menor.index])
                usados.add(menor.info)
