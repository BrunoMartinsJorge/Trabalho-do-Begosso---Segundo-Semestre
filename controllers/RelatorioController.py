from flask import Blueprint, request, jsonify

from services.RelatorioService import RelatorioService

relatorio_bp = Blueprint("relatorio", __name__, url_prefix="/relatorio")

relatorioService = RelatorioService()

@relatorio_bp.route("/listar-relatorio-matriculas", methods=["GET"])
def listar_relatorio_matriculas():
    lista = relatorioService.listar_relatorio_matriculas()
    return lista

@relatorio_bp.route("/listar-relatorio-modalidades", methods=["GET"])
def listar_relatorio_modalidades():
    codigo = request.args.get("codigo")
    modalidadeRelatorio = relatorioService.gerar_relatorio_modalidade(int(codigo))
    if modalidadeRelatorio is None:
        return jsonify(None)
    return jsonify(modalidadeRelatorio.__dict__)