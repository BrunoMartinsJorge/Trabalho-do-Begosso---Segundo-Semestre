from typing import List, Any

from controllers.AlunoController import alunoService
from dto.RelatorioMatriculaDto import RelatorioMatriculaDto
from services.AlunoService import AlunoService
from services.MatriculasService import MatriculasService
from services.ModalidadesService import ModalidadesService


class RelatorioService:
    def __init__(self):
        self.modalidadeService = ModalidadesService()
        self.matriculasService = MatriculasService()
        self.alunoService = AlunoService()

    def listar_relatorio_matriculas(self, codigo) -> Any:
        listaDto: Any = []
        listaMatriculas = self.matriculasService.buscar_matriculas_modalidades(codigo)
        for matricula in listaMatriculas:
            alunoMatricula = self.alunoService.buscar_aluno(int(matricula['codAluno']))
            dadosMatricula = self.matriculasService.buscar_matricula(int(matricula['codigo']))
            modalidade = self.modalidadeService.buscar_modalidades(codigo)
            matriculaDto = RelatorioMatriculaDto(
                int(matricula['codigo']),
                alunoMatricula['aluno']['nome'],
                alunoMatricula['cidade']['nome'],
                modalidade['modalidade']['descricao'],
                modalidade['info']['professor'],
                float(dadosMatricula['valorPagar']),
            )
            listaDto.append(matriculaDto)
        return listaDto