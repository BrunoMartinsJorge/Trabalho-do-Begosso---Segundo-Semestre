from flask import Blueprint, request, jsonify
from models.Professores import Professores

from services.ProfessorService import ProfessoresService

professor_bp = Blueprint("professor", __name__, url_prefix="/professores")

professor = ProfessoresService()


@professor_bp.route("/cadastrar_profesor", methods=["POST"])
def cadastrar_profesor():
    codigo = request.form['codigo']
    nome = request.form['nome']
    telefone = request.form['telefone']
    endereco = request.form['endereco']
    codCidade = request.form['codCidade']
    return professor.inserir_professor(Professores(int(codigo), nome, telefone, endereco, int(codCidade)))


@professor_bp.route("/buscar_profesor_por_codigo", methods=["GET"])
def buscar_profesor_por_codigo():
    codigo = request.args.get("codigo")
    return professor.buscar_professor(int(codigo))


@professor_bp.route("/apagar_profesor_por_codigo", methods=["POST"])
def apagar_profesor_por_codigo():
    codigo = request.form['codigo']
    professor.excluir_professor(int(codigo))
    return "Cidade apagada com sucesso!"


@professor_bp.route("/leitura_exaustiva", methods=["GET"])
def leitura_exaustiva():
    return professor.leitura_exaustiva()
