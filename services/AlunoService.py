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
        self.cidade_service = CidadeService()

    def __ler_arquivo(self) -> list[dict]:
        if not os.path.exists(self.path_dados):
            return []
        try:
            with open(self.path_dados, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def __salvar_arquivo(self, alunos: list[dict]) -> None:
        with open(self.path_dados, "w", encoding="utf-8") as f:
            json.dump(alunos, f, indent=4, ensure_ascii=False)

    def excluir_aluno(self, codigo: int) -> None:
        alunos = self.__ler_arquivo()
        novos_alunos = [a for a in alunos if int(a["codigo"]) != codigo]

        if len(alunos) == len(novos_alunos):
            raise ObjectNotExistsException(f"Aluno {codigo} não encontrado!")

        self.__salvar_arquivo(novos_alunos)

    def __verificar_se_codigo_existe(self, alunos: list[dict], novo_aluno: Alunos) -> None:
        if any(novo_aluno.codigo == int(a["codigo"]) for a in alunos):
            raise ObjectExistsException(f"Aluno com código {novo_aluno.codigo} já existe!")

    def inserir_aluno(self, novo_aluno: Alunos) -> Alunos:
        alunos = self.__ler_arquivo()
        self.__verificar_se_codigo_existe(alunos, novo_aluno)

        alunos.append(novo_aluno.to_dict())
        self.__salvar_arquivo(alunos)
        return novo_aluno

    def buscar_todos_alunos(self) -> list[Alunos]:
        return [Alunos(**a) for a in self.__ler_arquivo()]

    def buscar_aluno(self, codigo: int) -> dict:
        aluno_dict = next((a for a in self.__ler_arquivo() if int(a["codigo"]) == codigo), None)
        if not aluno_dict:
            raise ObjectNotExistsException(f"Aluno {codigo} não encontrado!")

        cidade = self.cidade_service.buscar_cidade(int(aluno_dict["codCidade"]))
        imc = self.calcular_imc(aluno_dict["peso"], aluno_dict["altura"])

        return {
            "aluno": aluno_dict,
            "cidade": cidade.to_dict(),
            "imc": imc
        }

    @staticmethod
    def calcular_imc(peso, altura) -> str:
        imc: float = float(peso) / (float(altura) ** 2)
        if imc < 18.5:
            return f"IMC = {imc:.2f} - Abaixo do peso"
        elif imc < 25:
            return f"IMC = {imc:.2f} - Peso normal"
        elif imc < 30:
            return f"IMC = {imc:.2f} - Sobrepeso"
        return f"IMC = {imc:.2f} - Obesidade"
