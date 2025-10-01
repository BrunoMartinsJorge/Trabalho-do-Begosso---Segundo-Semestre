import json
import os
from typing import Any, List

from flask import jsonify

from exceptions.ObjectNotExistsException import ObjectNotExistsException
from models.ArvoresBinaria import ArvoreBinaria
from models.Cidades import Cidades
from exceptions.ObjectExistsException import ObjectExistsException


class CidadeService:

    def __init__(self):
        self.arvore_binaria: List[ArvoreBinaria] = []
        self.pasta_archives = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'archives')
        os.makedirs(self.pasta_archives, exist_ok=True)
        self.path_dados = os.path.join(self.pasta_archives, "cidades.txt")

    def __verificar_se_codigo_existe(self, cidades: List[Any], nova_cidade: Cidades) -> None:
        for cidade in cidades:
            if nova_cidade.codigo == int(cidade['codigo']):
                raise ObjectExistsException(f"Cidade com código {nova_cidade.codigo} já existe!")

    def inserir_cidade(self, nova_cidade: Cidades) -> Any:
        pasta_archives = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'archives')
        path_cidades = os.path.join(pasta_archives, "Cidades.txt")
        os.makedirs(pasta_archives, exist_ok=True)

        if os.path.exists(path_cidades):
            with open(path_cidades, "r", encoding="utf-8") as arquivo:
                try:
                    cidades = json.load(arquivo)
                except json.JSONDecodeError:
                    cidades = []
        else:
            cidades = []

        self.__verificar_se_codigo_existe(cidades, nova_cidade)

        cidades.append(nova_cidade.to_dict())

        with open(path_cidades, "w", encoding="utf-8") as arquivo:
            json.dump(cidades, arquivo, indent=4, ensure_ascii=False)

    def buscar_todas_cidades(self) -> list[Cidades]:
        cidades = []
        with open(self.path_dados, "r", encoding="utf-8") as arquivo:
            dados_json = json.load(arquivo)

        for d in dados_json:
            cidade = Cidades(
                codigo=int(d["codigo"]),
                descricao=d["descricao"],
                estado=d["estado"]
            )
            cidades.append(cidade)
        return cidades

    def buscar_cidade(self, codigo: int) -> Cidades:
        pasta_archives = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'archives')
        path_cidades = os.path.join(pasta_archives, "Cidades.txt")
        os.makedirs(pasta_archives, exist_ok=True)

        cidades = []
        with open(path_cidades, "r", encoding="utf-8") as arquivo:
            cidades = json.load(arquivo)

        cidade_achada = None
        for cidade in cidades:
            if codigo == int(cidade['codigo']):
                cidade_achada = cidade

        if cidade_achada is None:
            raise ObjectNotExistsException("Cidade não encontrada!")

        return cidade_achada

    def excluir_cidade(self, codigo: int) -> None:
        indices, raiz = self.carregar_arvore_binaria()
        dados: List[Cidades] = self.buscar_todas_cidades()

        if not indices or not dados:
            return None

        def encontrar_minimo(index):
            while indices[index].esquerda != -1:
                index = indices[index].esquerda
            return index

        def remover(atual_index, codigo):
            if atual_index == -1:
                return -1
            no = indices[atual_index]
            if codigo < no.info:
                no.esquerda = remover(no.esquerda, codigo)
            elif codigo > no.info:
                no.direita = remover(no.direita, codigo)
            else:
                if no.esquerda == -1 and no.direita == -1:
                    return -1
                if no.esquerda == -1:
                    return no.direita
                if no.direita == -1:
                    return no.esquerda
                min_index = encontrar_minimo(no.direita)
                no.info = indices[min_index].info
                no.index = indices[min_index].index
                no.direita = remover(no.direita, indices[min_index].info)
            return atual_index

        nova_raiz = remover(raiz, codigo)

        # Esses ':' servem substitui todos os elementos da lista existente com os novos elementos. Parecendo um ponteiro(Mesmo que em Pitão não tenha)
        dados[:] = [c for c in dados if c.codigo != codigo]
        indices[:] = [n for n in indices if n is not None]

        for i, no in enumerate(indices):
            if no.esquerda != -1 and no.esquerda >= len(indices):
                no.esquerda = -1
            if no.direita != -1 and no.direita >= len(indices):
                no.direita = -1
            if no.index >= len(dados):
                no.index = len(dados) - 1 if dados else -1

        with open(self.path_dados, "r+") as f:
            f.truncate(0)

        dados_json = [cidade.__dict__ for cidade in dados]
        with open(self.path_dados, "w", encoding="utf-8") as f:
            json.dump(dados_json, f, ensure_ascii=False, indent=4)

        return nova_raiz

    def __ver_se_existe_na_lista(self, lista_codigo, codigo_atual):
        tem = False
        for codigo in lista_codigo:
            if codigo_atual == codigo:
                tem = True
                break
        return tem

    def leitura_exaustiva(self):
        dados = self.buscar_todas_cidades()
        indices = self.carregar_arvore_binaria()
        usados = set()
        dados_ordenados = []

        while len(usados) < len(dados):
            menor = None
            for registro in indices[0]:
                codigo = registro.info
                if not self.__ver_se_existe_na_lista(usados, codigo):
                    if menor is None or codigo < menor.info:
                        menor = registro
            if menor:
                usados.add(menor.info)
                dados_ordenados.append(dados[menor.index])

        return [cidade.__dict__ for cidade in dados_ordenados]

    def carregar_arvore_binaria(self) -> ArvoreBinaria:
        return ArvoreBinaria.construir_arvore(self.buscar_todas_cidades())
