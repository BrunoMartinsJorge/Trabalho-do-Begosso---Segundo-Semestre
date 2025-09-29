import json
import os
from typing import List

from dto.ListaMatriculasDto import ListaMatriculasDto
from exceptions.ObjectNotExistsException import ObjectNotExistsException
from models.Matriculas import Matriculas
from models.ArvoresBinaria import ArvoreBinaria
from exceptions.ObjectExistsException import ObjectExistsException
from services.AlunoService import AlunoService
from services.ModalidadesService import ModalidadesService

class MatriculasService:
    def __init__(self):
        self.arvore_binaria: List[ArvoreBinaria] = []
        self.pasta_archives = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'archives')
        os.makedirs(self.pasta_archives, exist_ok=True)
        self.path_dados = os.path.join(self.pasta_archives, "matriculas.txt")
        self.aluno_service = AlunoService()

    def __ler_arquivo(self) -> list[dict]:
        if not os.path.exists(self.path_dados):
            return []
        try:
            with open(self.path_dados, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def __salvar_arquivo(self, matriculas: list[dict]) -> None:
        with open(self.path_dados, "w", encoding="utf-8") as f:
            json.dump(matriculas, f, indent=4, ensure_ascii=False)

    def __verificar_se_codigo_existe(self, matriculas: list[dict], nova: Matriculas) -> None:
        if any(nova.codigo == int(m["codigo"]) for m in matriculas):
            raise ObjectExistsException(f"Matrícula {nova.codigo} já existe!")

    def inserir_matricula(self, nova: Matriculas) -> Matriculas:
        matriculas = self.__ler_arquivo()
        self.__verificar_se_codigo_existe(matriculas, nova)

        MatriculasService.__verificar_se_modalidade_tem_vagas(nova.codModalidade)

        matriculas.append(nova.to_dict())
        self.__salvar_arquivo(matriculas)

        ModalidadesService().atualizar_modalidade(nova.codModalidade, "SOMAR")
        return nova

    def buscar_todas_matriculas(self) -> list[Matriculas]:
        return [Matriculas(**m) for m in self.__ler_arquivo()]

    def buscar_matricula(self, codigo: int) -> ListaMatriculasDto:
        matricula_dict = next((m for m in self.__ler_arquivo() if int(m["codigo"]) == codigo), None)
        if not matricula_dict:
            raise ObjectNotExistsException(f"Matrícula {codigo} não encontrada!")

        infos = self.__buscar_infos_matricula(
            int(matricula_dict["codAluno"]),
            int(matricula_dict["codModalidade"]),
            int(matricula_dict["quantidadeAulas"])
        )

        return ListaMatriculasDto(
            codigo,
            infos["aluno"]["nome"],
            infos["modalidade"],
            matricula_dict["quantidadeAulas"],
            float(infos["valor"])
        )
