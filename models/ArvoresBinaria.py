from typing import List, Any
from models.No import No

class ArvoreBinaria:
    def __init__(self):
        self.raiz = None

    def inserir(self, codigo: int, localizacao: int):
        if self.raiz is None:
            self.raiz = No(codigo, localizacao)
        else:
            self._inserir(self.raiz, codigo, localizacao)

    def _inserir(self, atual: No, codigo: int, localizacao: int):
        if codigo < atual.codigo:
            if atual.esquerda is None:
                atual.esquerda = No(codigo, localizacao)
            else:
                self._inserir(atual.esquerda, codigo, localizacao)
        else:
            if atual.direita is None:
                atual.direita = No(codigo, localizacao)
            else:
                self._inserir(atual.direita, codigo, localizacao)

    def buscar(self, codigo: int) -> No | None:
        return self._buscar(self.raiz, codigo)

    def _buscar(self, atual: No, codigo: int) -> No | None:
        if atual is None:
            return None
        if codigo == atual.codigo:
            return atual
        if codigo < atual.codigo:
            return self._buscar(atual.esquerda, codigo)
        return self._buscar(atual.direita, codigo)

    def em_ordem(self):
        """Percorre em ordem crescente de códigos"""
        def _em_ordem(atual):
            if atual:
                yield from _em_ordem(atual.esquerda)
                yield atual
                yield from _em_ordem(atual.direita)

        yield from _em_ordem(self.raiz)
