import json
import os
from typing import List, Any

from flask import jsonify

from exceptions.ObjectExistsException import ObjectExistsException
from exceptions.ObjectNotExistsException import ObjectNotExistsException
from models.ArvoresBinaria import ArvoreBinaria
from models.Modalidades import Modalidades


class ModalidadesService:

    def __init__(self):
        self.arvore_binaria: List[ArvoreBinaria] = []
        self.pasta_archives = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'archives')
        os.makedirs(self.pasta_archives, exist_ok=True)
        self.path_dados = os.path.join(self.pasta_archives, "modalidades.txt")

    def __verificar_se_codigo_existe(self, Modalidades: List[Any], nova_modalidade: Modalidades) -> None:
        for modalidade in Modalidades:
            if nova_modalidade.codigo == int(modalidade['codigo']):
                raise ObjectExistsException(f"Modalidade com código {nova_modalidade.codigo} já existe!")

    @staticmethod
    def inserir_modalidade(nova_modalidade: Modalidades) -> Any:
        pasta_archives = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'archives')
        path_modalidades = os.path.join(pasta_archives, "Modalidades.txt")
        os.makedirs(pasta_archives, exist_ok=True)

        if os.path.exists(path_modalidades):
            with open(path_modalidades, "r", encoding="utf-8") as arquivo:
                try:
                    modalidades = json.load(arquivo)
                except json.JSONDecodeError:
                    modalidades = []
        else:
            modalidades = []

        ModalidadesService.__verificar_se_codigo_existe(ModalidadesService, modalidades, nova_modalidade)

        modalidades.append(nova_modalidade.to_dict())

        with open(path_modalidades, "w", encoding="utf-8") as arquivo:
            json.dump(modalidades, arquivo, indent=4, ensure_ascii=False)

        modalidades = [Modalidades(**d) for d in modalidades]
        return jsonify([c.to_dict() for c in modalidades]), 201

    def buscar_todas_modalidades(self) -> list[Modalidades]:
        modalidades = []
        with open(self.path_dados, "r", encoding="utf-8") as arquivo:
            dados_json = json.load(arquivo)

        for d in dados_json:
            modalidade = Modalidades(
                codigo=int(d["codigo"]),
                descricao=d["descricao"],
                codProfessor=d["codProfessor"],
                valorDaAula=d["valorDaAula"],
                limiteAlunos=d["limiteAlunos"],
                totalMatriculas=d["totalMatriculas"]
            )
            modalidades.append(modalidade)
        return modalidades

    @staticmethod
    def buscar_modalidades(codigo: int) -> Modalidades:
        pasta_archives = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'archives')
        path_modalidades = os.path.join(pasta_archives, "Modalidades.txt")
        os.makedirs(pasta_archives, exist_ok=True)
        modalidades = []
        with open(path_modalidades, "r", encoding="utf-8") as arquivo:
            modalidades = json.load(arquivo)
        modalidade_achada = None
        for modalidade in modalidades:
            if codigo == int(modalidade['codigo']):
                modalidade_achada = modalidade
        if modalidade_achada is None:
            raise ObjectNotExistsException("Modalidade não encontrado!")
        return modalidade_achada

    def excluir_modalidade(self, codigo: int) -> None:
        indices, raiz = self.carregar_arvore_binaria()
        dados: List[Modalidades] = self.buscar_todas_modalidades()

        if not indices or not dados:
            return

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
        dados_json = [modalidade.__dict__ for modalidade in dados]
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
        dados = self.buscar_todas_modalidades()
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
        return [modalidade.__dict__ for modalidade in dados_ordenados]

    def carregar_arvore_binaria(self) -> ArvoreBinaria:
        return ArvoreBinaria.construir_arvore(self.buscar_todas_modalidades())
