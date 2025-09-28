import json
import os
from typing import Any, List

from flask import jsonify

from dto.ListaAlunosDto import ListaAlunos
from exceptions.ObjectNotExistsException import ObjectNotExistsException
from models.Alunos import Alunos
from models.ArvoresBinaria import ArvoreBinaria
from exceptions.ObjectExistsException import ObjectExistsException
from services.CidadeService import CidadeService


class AlunoService:

    def __init__(self):
        self.arvore_binaria: List[ArvoreBinaria] = []
        self.pasta_archives = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'archives')
        os.makedirs(self.pasta_archives, exist_ok=True)
        self.path_dados = os.path.join(self.pasta_archives, "alunos.txt")
        self.cidadeService = CidadeService()
        self.cidadeService = CidadeService()

    def __verificar_se_codigo_existe(self, alunos: List[Any], novo_aluno: Alunos) -> None:
        for aluno in alunos:
            if novo_aluno.codigo == int(aluno['codigo']):
                raise ObjectExistsException(f"Aluno com código {novo_aluno.codigo} já existe!")

    def calcular_imc(self, codigo: int) -> Any:
        aluno = self.buscar_aluno(codigo)
        resposta = {
            "nome": aluno['aluno']['nome'],
            "imc": aluno['imc']
        }
        return resposta

    def buscar_alunos_tabela(self) -> list[dict]:
        alunos = self.leitura_exaustiva()
        lista_alunos: list[dict] = []

        for aluno in alunos:
            cidade = CidadeService.buscar_cidade(int(aluno['codCidade']))
            cidade_estado = cidade['descricao'] + ' - ' + cidade['estado']
            aluno_elemento = ListaAlunos(
                int(aluno['codigo']),
                aluno['nome'],
                aluno['nascimento'],
                cidade_estado
            )
            lista_alunos.append(aluno_elemento.to_dict())
        return lista_alunos

    @staticmethod
    def inserir_aluno(novo_aluno: Alunos) -> Any:
        pasta_archives = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'archives')
        path_alunos = os.path.join(pasta_archives, "Alunos.txt")
        os.makedirs(pasta_archives, exist_ok=True)

        if os.path.exists(path_alunos):
            with open(path_alunos, "r", encoding="utf-8") as arquivo:
                try:
                    alunos = json.load(arquivo)
                except json.JSONDecodeError:
                    alunos = []
        else:
            alunos = []

        AlunoService.__verificar_se_codigo_existe(AlunoService, alunos, novo_aluno)

        alunos.append(novo_aluno.to_dict())

        with open(path_alunos, "w", encoding="utf-8") as arquivo:
            json.dump(alunos, arquivo, indent=4, ensure_ascii=False)

        alunos = [Alunos(**d) for d in alunos]
        return jsonify([c.to_dict() for c in alunos]), 201

    def buscar_todos_alunos(self) -> list[Alunos]:
        alunos = []
        with open(self.path_dados, "r", encoding="utf-8") as arquivo:
            dados_json = json.load(arquivo)

        for d in dados_json:
            aluno = Alunos(
                codigo=int(d["codigo"]),
                nome=d["nome"],
                codCidade=d["codCidade"],
                nascimento=d["nascimento"],
                peso=d["peso"],
                altura=d["altura"]
            )
            alunos.append(aluno)
        return alunos

    @staticmethod
    def buscar_aluno(codigo: int) -> Any:
        pasta_archives = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'archives')
        path_alunos = os.path.join(pasta_archives, "Alunos.txt")
        os.makedirs(pasta_archives, exist_ok=True)
        alunos = []
        with open(path_alunos, "r", encoding="utf-8") as arquivo:
            alunos = json.load(arquivo)
        aluno_achado = None
        for aluno in alunos:
            if codigo == int(aluno['codigo']):
                aluno_achado = aluno
        if aluno_achado is None:
            raise ObjectNotExistsException("Aluno não encontrado com ID " + codigo)
        cidade = CidadeService.buscar_cidade(int(aluno_achado["codCidade"]))
        imc = AlunoService.__calcular_imc(aluno_achado["peso"], aluno_achado["altura"])
        info_ciadade = {
            "nome": cidade['descricao'],
            "estado": cidade['estado']
        }
        aluno = {
            "aluno": aluno_achado,
            "cidade": info_ciadade,
            "imc": imc
        }
        return aluno

    @staticmethod
    def __calcular_imc(peso, altura) -> str:
        imc: float = float(peso) / (float(altura) ** 2)
        if imc < 18.5:
            return f'Seu IMC = {imc:.2f} - Abaixo do peso'
        elif 18.5 <= imc < 25:
            return f'Seu IMC = {imc:.2f} - Peso normal'
        elif 25 <= imc < 30:
            return f'Seu IMC = {imc:.2f} - Sobrepeso'
        else:
            return f'Seu IMC = {imc:.2f} - Obesidade'

    def excluir_aluno(self, codigo: int) -> None:
        indices, raiz = self.carregar_arvore_binaria()
        dados: List[Alunos] = self.buscar_todos_alunos()

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
        dados_json = [aluno.__dict__ for aluno in dados]
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
        dados = self.buscar_todos_alunos()
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
        return [aluno.__dict__ for aluno in dados_ordenados]

    def carregar_arvore_binaria(self) -> ArvoreBinaria:
        return ArvoreBinaria.construir_arvore(self.buscar_todos_alunos())
