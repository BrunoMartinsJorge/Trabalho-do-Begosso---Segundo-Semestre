from flask import Flask, render_template, request

from controllers.CidadesController import cidade_bp
from controllers.AlunoController import aluno_bp
from controllers.MatriculasController import matriculas_bp
from controllers.ModalidadesController import modalidades_bp
from controllers.ProfessorController import professor_bp
from exceptions.ExceptionHandler import register_error_handlers
from services.AlunoService import AlunoService
from services.CidadeService import CidadeService
from services.MatriculasService import MatriculasService
from services.ModalidadesService import ModalidadesService
from services.ProfessorService import ProfessoresService

app = Flask(__name__)

app.register_blueprint(cidade_bp)
app.register_blueprint(aluno_bp)
app.register_blueprint(matriculas_bp)
app.register_blueprint(modalidades_bp)
app.register_blueprint(professor_bp)

register_error_handlers(app)

@app.route('/')
def formulario():
    return render_template('index.html')

@app.route('/alunos')
def alunos_router():
    alunoService = AlunoService()
    return render_template('Alunos.html', alunos=alunoService.buscar_todos_alunos())

@app.route('/cidades')
def cidades_router():
    cidadesService = CidadeService()
    return render_template('Cidades.html', cidades=cidadesService.buscar_todas_cidades(), arvores=cidadesService.carregar_arvore_binaria())

@app.route('/modalidades')
def modalidades_router():
    modalidadesServices = ModalidadesService()
    return render_template('Modalidades.html', modalidades=modalidadesServices.buscar_todas_modalidades())

@app.route('/professores')
def professores_router():
    professoresService = ProfessoresService()
    return render_template('Professores.html', professores=professoresService.buscar_todos_professores())

@app.route('/matriculas')
def matriculas_router():
    matriculasService = MatriculasService()
    return render_template('Matriculas.html', matriculas=matriculasService.buscar_todas_matriculas())

if __name__ == '__main__':
    app.run(debug=True)
