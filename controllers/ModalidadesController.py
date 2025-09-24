from flask import Blueprint, request, jsonify
from models.Matriculas import Matriculas
from models.Modalidades import Modalidades
from services.ModalidadesService import ModalidadesService

modalidades_bp = Blueprint("modalidade", __name__, url_prefix="/modalidades")

modalidadesService = ModalidadesService()

@modalidades_bp.route("/lista_tabela", methods=["GET"])
def lista_tabela():
    modalidadesService = ModalidadesService()
    lista = modalidadesService.buscar_todos_para_tabela()
    return jsonify([dto.__dict__ for dto in lista])

@modalidades_bp.route("/cadastrar_modalidade", methods=["POST"])
def cadastrar_modalidade():
    data = request.get_json()
    codigo = data['codigo']
    descricao = data['descricao']
    codProfessor = data['professor']
    valorDaAula = data['valorAula']
    limiteAlunos = data['limite']
    return modalidadesService.inserir_modalidade(
        Modalidades(int(codigo), descricao, codProfessor, valorDaAula, limiteAlunos, 0))


@modalidades_bp.route("/buscar_modalidade_por_codigo", methods=["GET"])
def buscar_modalidade_por_codigo():
    codigo = request.args.get("codigo")
    return modalidadesService.buscar_modalidades(int(codigo))


@modalidades_bp.route("/apagar_modalidades_por_codigo", methods=["POST"])
def apagar_modalidade_por_codigo():
    codigo = request.args.get('codigo')
    modalidadesService.excluir_modalidade(int(codigo))
    return "Matricula apagada com sucesso!"

@modalidades_bp.route("/leitura_exaustiva", methods=["GET"])
def leitura_exaustiva():
    return modalidadesService.leitura_exaustiva()

@modalidades_bp.route("/buscar_faturamento", methods=["GET"])
def buscar_faturamento():
    codigo = request.args.get("codigo")
    faturamento_dto = modalidadesService.faturamento_por_modalidade(int(codigo))
    return jsonify({
        "faturamento": faturamento_dto.to_dict()
    }), 200
