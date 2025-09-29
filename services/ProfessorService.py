import json
import os
from typing import Any, List

from flask import jsonify

from dto.ListaProfessores import ListaProfessores
from exceptions.ObjectNotExistsException import ObjectNotExistsException
from models.ArvoresBinaria import ArvoreBinaria
from models.Professores import Professores
from exceptions.ObjectExistsException import ObjectExistsException
from services.CidadeService import CidadeService


class ProfessoresService:

    def __init__(self):
        self.arvore_binaria: List[ArvoreBinaria] = []
        self.pasta_archives = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'archives')
        os.makedirs(self.pasta_archives, exist_ok=True)
        self.path_dados = os.path.join(self.pasta_archives, "professores.txt")

    def __verificar_se_codigo_existe(self, professores: List[Any], novo_professor: Professores) -> None:
        for professor in professores:
            if novo_professor.codigo == int(professor['codigo']):
                raise ObjectExistsException(f"Professor com código {novo_professor.codigo} já existe!")

    @staticmethod
    def inserir_professor(novo_professor: Professores) -> Any:
        pasta_archives = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'archives')
        path_professores = os.path.join(pasta_archives, "professores.txt")  # padronizado em minúsculo
        os.makedirs(pasta_archives, exist_ok=True)
        if os.path.exists(path_professores):
            with open(path_professores, "r", encoding="utf-8") as arquivo:
                try:
                    professores_json = json.load(arquivo)
                except json.JSONDecodeError:
                    professores_json = []
        else:
            professores_json = []
        for p in professores_json:
            if novo_professor.codigo == int(p["codigo"]):
                raise ObjectExistsException(f"Professor com código {novo_professor.codigo} já existe!")
        professores_json.append(novo_professor.to_dict())
        with open(path_professores, "w", encoding="utf-8") as arquivo:
            json.dump(professores_json, arquivo, indent=4, ensure_ascii=False)

        return jsonify(professores_json), 201

    def buscar_professores_tabela(self) -> list[dict]:
        professores = self.leitura_exaustiva()
        lista_professores: list[dict] = []

        for professor in professores:
            cidade = CidadeService.buscar_cidade(CidadeService, int(professor['codCidade']))
            cidade_estado = cidade['descricao'] + ' - ' + cidade['estado']

            professor_elemento = ListaProfessores(
                int(professor['codigo']),
                professor['nome'],
                professor['endereco'],
                professor['telefone'],
                cidade_estado
            )
            lista_professores.append(professor_elemento.to_dict())
        return lista_professores

    def __buscar_todos_professores(self) -> list[Professores]:
        professores = []
        with open(self.path_dados, "r", encoding="utf-8") as arquivo:
            dados_json = json.load(arquivo)

        for d in dados_json:
            professor = Professores(
                codigo=int(d["codigo"]),
                nome=d["nome"],
                endereco=d["endereco"],
                telefone=d["telefone"],
                codCidade=int(d["codCidade"])
            )
            professores.append(professor)
        return professores

    @staticmethod
    def buscar_professor(codigo: int) -> Any:
        pasta_archives = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'archives')
        path_professores = os.path.join(pasta_archives, "Professores.txt")
        os.makedirs(pasta_archives, exist_ok=True)
        professores = []
        with open(path_professores, "r", encoding="utf-8") as arquivo:
            professores = json.load(arquivo)
        professor_achado = None
        for professor in professores:
            if codigo == int(professor['codigo']):
                professor_achado = professor
        if professor_achado is None:
            raise ObjectNotExistsException("Professor não encontrado com código " + str(codigo))
        cidade = CidadeService.buscar_cidade(CidadeService, professor_achado['codCidade'])
        info_cidade = {
            "nome": cidade['descricao'],
            "estado": cidade['estado'],
        }
        professor = {
            "professor": professor_achado,
            "cidade": info_cidade
        }
        return professor

    def excluir_professor(self, codigo: int) -> None:
        indices, raiz = self.carregar_arvore_binaria()
        dados: List[Professores] = self.__buscar_todos_professores()

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
        dados_json = [professor.__dict__ for professor in dados]
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
        dados = self.__buscar_todos_professores()
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
        return [professor.__dict__ for professor in dados_ordenados]

    def buscar_professor_por_modalidade(self, cod_professor: int) -> Professores | None:
        lista_professores: List[Professores] = self.__buscar_todos_professores()
        for professor in lista_professores:
            if professor.codigo == cod_professor:
                return professor
        return None

    def carregar_arvore_binaria(self) -> ArvoreBinaria:
        return ArvoreBinaria.construir_arvore(self.__buscar_todos_professores())
