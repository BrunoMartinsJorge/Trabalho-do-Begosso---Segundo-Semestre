from typing import List, Any


class ArvoreBinaria:
    def __init__(self, esquerda=0, direita=0, info=0, index=0):
        self.esquerda = int(esquerda)
        self.direita = int(direita)
        self.info = int(info)
        self.index = int(index)

        def __str__():
            return f"{self.esquerda};{self.direita};{self.info};{self.index}"

        def __ver_se_existe_na_lista(lista_codigo, codigo_atual):
            tem = False
            for codigo in lista_codigo:
                if codigo_atual == codigo:
                    tem = True
                    break
            return tem

        @staticmethod
        def leitura_exaustiva_generica(indices: List[ArvoreBinaria], lista: List[Any]):
            usados = set()
            while len(usados) < len(lista):
                menor = None
                for registro in indices:
                    codigo = registro.info
                    if not __ver_se_existe_na_lista(usados, codigo):
                        if menor is None or codigo < menor.info:
                            menor = registro
                if menor:
                    print(lista[menor.index])
                    usados.add(menor.info)
