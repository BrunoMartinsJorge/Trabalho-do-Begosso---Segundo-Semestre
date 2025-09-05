from flask import Blueprint, request, jsonify
from models.Cidades import Cidades
from services.AlunoService import AlunoService

aluno_bp = Blueprint("aluno", __name__, url_prefix="/alunos")

alunoService = AlunoService()

@aluno_bp.route("/cadastrar_aluno", methods=["POST"])
def cadastrar_aluno():
    codigo = request.form['codigo']
    descricao = request.form['descricao']
    estado = request.form['estado']
    return alunoService.inserir_aluno(Cidades(int(codigo), descricao, estado))


@aluno_bp.route("/buscar_aluno_por_codigo", methods=["GET"])
def buscar_aluno_por_codigo():
    codigo = request.args.get("codigo")
    return alunoService.buscar_aluno(int(codigo))


@aluno_bp.route("/apagar_alunos_por_codigo", methods=["POST"])
def apagar_aluno_por_codigo():
    codigo = request.form['codigo']
    alunoService.excluir_aluno(int(codigo))
    return "Cidade apagada com sucesso!"

@aluno_bp.route("/leitura_exaustiva", methods=["GET"])
def leitura_exaustiva():
    return alunoService.leitura_exaustiva()