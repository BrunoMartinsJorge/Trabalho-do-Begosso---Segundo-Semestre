import json
import os
from typing import Any, List

from flask import jsonify

from exceptions.ObjectNotExistsException import ObjectNotExistsException
from models.Matriculas import Matriculas
from models.ArvoresBinaria import ArvoreBinaria
from exceptions.ObjectExistsException import ObjectExistsException


class MatriculasService:

    def __init__(self):
        self.arvore_binaria: List[ArvoreBinaria] = []
        self.pasta_archives = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'archives')
        os.makedirs(self.pasta_archives, exist_ok=True)
        self.path_dados = os.path.join(self.pasta_archives, "matriculas.txt")

    def __verificar_se_codigo_existe(self, matriculas: List[Any], nova_matricula: Matriculas) -> None:
        for matricula in matriculas:
            if nova_matricula.codigo == int(matricula['codigo']):
                raise ObjectExistsException(f"Matricula com código {nova_matricula.codigo} já existe!")

    @staticmethod
    def inserir_matricula(nova_matricula: Matriculas) -> Any:
        pasta_archives = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'archives')
        path_matricula = os.path.join(pasta_archives, "Matriculas.txt")
        os.makedirs(pasta_archives, exist_ok=True)

        if os.path.exists(path_matricula):
            with open(path_matricula, "r", encoding="utf-8") as arquivo:
                try:
                    matriculas = json.load(arquivo)
                except json.JSONDecodeError:
                    matriculas = []
        else:
            matriculas = []

        MatriculasService.__verificar_se_codigo_existe(MatriculasService, matriculas, nova_matricula)

        matriculas.append(nova_matricula.to_dict())

        with open(path_matricula, "w", encoding="utf-8") as arquivo:
            json.dump(matriculas, arquivo, indent=4, ensure_ascii=False)

        matriculas = [Matriculas(**d) for d in matriculas]
        return jsonify([c.to_dict() for c in matriculas]), 201

    def buscar_todas_matriculas(self) -> list[Matriculas]:
        matriculas = []
        with open(self.path_dados, "r", encoding="utf-8") as arquivo:
            dados_json = json.load(arquivo)

        for d in dados_json:
            matricula = Matriculas(
                codigo=int(d["codigo"]),
                codAluno=d["codAluno"],
                codModalidade=d["codModalidade"],
                quantidadeAulas=d["quantidadeAulas"]
            )
            matriculas.append(matricula)
        return matriculas

    @staticmethod
    def buscar_matricula(codigo: int) -> Matriculas:
        pasta_archives = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'archives')
        path_matricula = os.path.join(pasta_archives, "Matriculas.txt")
        os.makedirs(pasta_archives, exist_ok=True)
        matriculas = []
        with open(path_matricula, "r", encoding="utf-8") as arquivo:
            matriculas = json.load(arquivo)
        matricula_achada = None
        for matricula in matriculas:
            if codigo == int(matricula['codigo']):
                matricula_achada = matricula
        if matricula_achada is None:
            raise ObjectNotExistsException("Matricula não encontrado!")
        return matricula_achada

    def excluir_matricula(self, codigo: int) -> None:
        indices, raiz = self.carregar_arvore_binaria()
        dados: List[Matriculas] = self.buscar_todas_matriculas()

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
        dados_json = [matricula.__dict__ for matricula in dados]
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
        dados = self.buscar_todas_matriculas()
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
        return [matricula.__dict__ for matricula in dados_ordenados]

    def carregar_arvore_binaria(self) -> ArvoreBinaria:
        return ArvoreBinaria.construir_arvore(self.buscar_todas_matriculas())
