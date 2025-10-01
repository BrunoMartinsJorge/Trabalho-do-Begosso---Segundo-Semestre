from typing import List, Any

from flask import jsonify

from controllers.AlunoController import alunoService
from dto.RelatorioGeralModalidadeDto import RelatorioGeralModalidadeDto
from dto.RelatorioMatriculaDto import RelatorioMatriculaDto
from services.AlunoService import AlunoService
from services.MatriculasService import MatriculasService
from services.ModalidadesService import ModalidadesService


class RelatorioService:
    def __init__(self):
        self.modalidadeService = ModalidadesService()
        self.matriculasService = MatriculasService()
        self.alunoService = AlunoService()

    def listar_relatorio_matriculas(self) -> Any:
        listaDto: Any = []
        listaMatriculas = self.matriculasService.leitura_exaustiva()
        for matricula in listaMatriculas:
            alunoMatricula = self.alunoService.buscar_aluno(int(matricula['codAluno']))
            dadosMatricula = self.matriculasService.buscar_matricula(int(matricula['codigo']))
            modalidade = self.modalidadeService.buscar_modalidades(int(matricula['codModalidade']))
            matriculaDto = RelatorioMatriculaDto(
                int(matricula['codigo']),
                alunoMatricula['aluno']['nome'],
                alunoMatricula['cidade']['nome'],
                modalidade['modalidade']['descricao'],
                modalidade['info']['professor'],
                float(dadosMatricula['valorPagar']),
            )
            listaDto.append(matriculaDto)
        qtdAlunos = self.matriculasService.quantidade_alunos_matriculados()
        return jsonify({
            "matriculas": [dto.__dict__ for dto in listaDto],
            'qtdAlunos': qtdAlunos
        })

    def gerar_relatorio_modalidade(self, codigo: int) -> Any:
        listaMatriculas = self.matriculasService.buscar_matriculas_modalidades(codigo)
        modalidade = self.modalidadeService.buscar_modalidades(codigo)
        valor_total: float = 0.0
        if len(listaMatriculas) > 0:
            for matricula in listaMatriculas:
                dadosMatricula = self.matriculasService.buscar_matricula(int(matricula['codigo']))
                valor_total += float(dadosMatricula['valorPagar'])
            if valor_total == 0:
                return None
            return RelatorioGeralModalidadeDto(
                modalidade['modalidade']['descricao'],
                modalidade['info']['professor'],
                modalidade['info']['cidade'],
                valor_total
            )
        else: return None