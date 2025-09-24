from flask import Blueprint, request, jsonify
from models.Matriculas import Matriculas
from services.MatriculasService import MatriculasService

matriculas_bp = Blueprint("matricula", __name__, url_prefix="/matriculas")

matriculaService = MatriculasService()

@matriculas_bp.route("/cadastrar_matricula", methods=["POST"])
def cadastrar_matricula():
    codigo = request.form['codigo']
    codAluno = request.form['codAluno']
    codModalidade = request.form['codModalidade']
    quantidadeAulas = request.form['quantidadeAulas']
    return matriculaService.inserir_matricula(Matriculas(int(codigo), codAluno, codModalidade, quantidadeAulas))


@matriculas_bp.route("/buscar_matricula_por_codigo", methods=["GET"])
def buscar_matricula_por_codigo():
    codigo = request.args.get("codigo")
    return matriculaService.buscar_matricula(int(codigo))


@matriculas_bp.route("/apagar_matricula_por_codigo", methods=["POST"])
def apagar_matricula_por_codigo():
    codigo = request.form['codigo']
    matriculaService.excluir_matricula(int(codigo))
    return "Matricula apagada com sucesso!"

@matriculas_bp.route("/listar_todos", methods=["GET"])
def listar_todos():
    lista = matriculaService.buscar_tabela_matriculas()
    return jsonify([dto.__dict__ for dto in lista])
