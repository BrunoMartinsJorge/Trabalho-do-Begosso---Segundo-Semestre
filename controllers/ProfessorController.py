from flask import Blueprint, request, jsonify
from models.Professores import Professores

from services.ProfessorService import ProfessoresService

professor_bp = Blueprint("professor", __name__, url_prefix="/professores")

professor = ProfessoresService()

@professor_bp.route("/cadastrar_profesor", methods=["POST"])
def cadastrar_profesor():
    data = request.get_json()
    codigo = data['codigo']
    nome = data['nome']
    telefone = data['telefone']
    endereco = data['endereco']
    codCidade = data['codigo_cidade']
    return professor.inserir_professor(Professores(int(codigo), nome, telefone, endereco, int(codCidade)))


@professor_bp.route("/buscar_professor_por_codigo", methods=["GET"])
def buscar_profesor_por_codigo():
    codigo = request.args.get("codigo")
    return professor.buscar_professor(int(codigo))


@professor_bp.route("/apagar_profesor_por_codigo", methods=["POST"])
def apagar_profesor_por_codigo():
    codigo = request.args.get("codigo")
    professor.excluir_professor(int(codigo))
    return "Cidade apagada com sucesso!"


@professor_bp.route("/listar_todos", methods=["GET"])
def leitura_exaustiva():
    return professor.buscar_professores_tabela()
