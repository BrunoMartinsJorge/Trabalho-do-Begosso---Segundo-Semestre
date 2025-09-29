from flask import Blueprint, request, jsonify

from models.Alunos import Alunos
from models.Cidades import Cidades
from services.AlunoService import AlunoService

aluno_bp = Blueprint("aluno", __name__, url_prefix="/alunos")

alunoService = AlunoService()

@aluno_bp.route("/cadastrar_aluno", methods=["POST"])
def cadastrar_aluno():
    data = request.get_json()
    codigo = data["codigo"]
    nome = data["nome"]
    codCidade = data["codigo_cidade"]
    data_nascimento = data["nascimento"]
    peso = data["peso"]
    altura = float(data["altura"])
    return alunoService.inserir_aluno(Alunos(int(codigo), nome, codCidade, data_nascimento, peso, altura))

@aluno_bp.route("/calcular_imc", methods=["GET"])
def calcular_imc():
    codigo = request.args.get("codigo")
    try:
        codigo_int = int(codigo)
    except (TypeError, ValueError):
        return {"erro": f"Código inválido: {codigo}"}, 400
    return jsonify(alunoService.calcular_imc(AlunoService, codigo_int))

@aluno_bp.route("/buscar_aluno_por_codigo", methods=["GET"])
def buscar_aluno_por_codigo():
    codigo = request.args.get("codigo")
    try:
        codigo_int = int(codigo)
    except (TypeError, ValueError):
        return {"erro": f"Código inválido: {codigo}"}, 400

    aluno = alunoService.buscar_aluno(codigo_int)
    return jsonify(aluno)

@aluno_bp.route("/apagar_alunos_por_codigo", methods=["POST"])
def apagar_aluno_por_codigo():
    codigo = request.args.get("codigo")
    alunoService.excluir_aluno(int(codigo))
    return "Cidade apagada com sucesso!"

@aluno_bp.route("/buscar_todos", methods=["GET"])
def leitura_exaustiva():
    alunos = alunoService.buscar_todos_alunos()
    alunos_dict = [aluno.to_dict() for aluno in alunos]
    return jsonify(alunos_dict)

