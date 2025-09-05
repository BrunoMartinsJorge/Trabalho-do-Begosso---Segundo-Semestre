from flask import Blueprint, request, jsonify
from models.Matriculas import Matriculas
from models.Modalidades import Modalidades
from services.ModalidadesService import ModalidadesService

modalidades_bp = Blueprint("modalidade", __name__, url_prefix="/modalidades")

modalidadesService = ModalidadesService()


@modalidades_bp.route("/cadastrar_modalidade", methods=["POST"])
def cadastrar_modalidade():
    codigo = request.form['codigo']
    descricao = request.form['descricao']
    codProfessor = request.form['codProfessor']
    valorDaAula = request.form['valorDaAula']
    limiteAlunos = request.form['limiteAlunos']
    totalMatriculas = request.form['totalMatriculas']
    return modalidadesService.inserir_modalidade(
        Modalidades(int(codigo), descricao, codProfessor, valorDaAula, limiteAlunos, totalMatriculas))


@modalidades_bp.route("/buscar_modalidade_por_codigo", methods=["GET"])
def buscar_modalidade_por_codigo():
    codigo = request.args.get("codigo")
    return modalidadesService.buscar_modalidades(int(codigo))


@modalidades_bp.route("/apagar_modalidades_por_codigo", methods=["POST"])
def apagar_modalidade_por_codigo():
    codigo = request.form['codigo']
    modalidadesService.excluir_modalidade(int(codigo))
    return "Matricula apagada com sucesso!"


@modalidades_bp.route("/leitura_exaustiva", methods=["GET"])
def leitura_exaustiva():
    return modalidadesService.leitura_exaustiva()
