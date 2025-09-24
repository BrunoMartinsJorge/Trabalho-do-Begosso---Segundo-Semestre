from flask import Blueprint, request, jsonify

from services.RelatorioService import RelatorioService

relatorio_bp = Blueprint("relatorio", __name__, url_prefix="/relatorio")

relatorioService = RelatorioService()

@relatorio_bp.route("/listar-relatorio-matriculas", methods=["GET"])
def listar_relatorio_matriculas():
    codigo = request.args.get("codigo")
    lista = relatorioService.listar_relatorio_matriculas(int(codigo))
    return jsonify([dto.__dict__ for dto in lista])
