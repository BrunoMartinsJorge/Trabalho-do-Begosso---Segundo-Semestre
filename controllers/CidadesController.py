from flask import Blueprint, request, jsonify
from models.Cidades import Cidades
from services.CidadeService import CidadeService

cidade_bp = Blueprint("cidade", __name__, url_prefix="/cidades")

cidadeService = CidadeService()

@cidade_bp.route("/cadastrar_cidade", methods=["POST"])
def cadastrar_cidade():
    codigo = request.form['codigo']
    descricao = request.form['descricao']
    estado = request.form['estado']
    return cidadeService.inserir_cidade(Cidades(int(codigo), descricao, estado))


@cidade_bp.route("/buscar_cidade_por_codigo", methods=["GET"])
def buscar_cidade_por_codigo():
    codigo = request.args.get("codigo")
    return cidadeService.buscar_cidade(int(codigo))


@cidade_bp.route("/apagar_cidades_por_codigo", methods=["POST"])
def apagar_cidade_por_codigo():
    codigo = request.form['codigo']
    cidadeService.excluir_cidade(int(codigo))
    return "Cidade apagada com sucesso!"

@cidade_bp.route("/leitura_exaustiva", methods=["GET"])
def leitura_exaustiva():
    return cidadeService.leitura_exaustiva()