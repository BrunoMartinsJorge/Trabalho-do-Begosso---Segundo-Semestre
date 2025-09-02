from flask import Flask, render_template, request

from enums.TipoRegistro import TipoRegistroEnum
from models.Cidades import Cidades
from utils.OpereacoesBasicas import OperacoesBasicas

app = Flask(__name__)

@app.route('/')
def formulario():
    return render_template('index.html')

@app.route('/alunos')
def alunos_router():
    return render_template('Alunos.html')

@app.route('/cidades')
def cidades_router():
    return render_template('Cidades.html')

@app.route('/modalidades')
def modalidades_router():
    return render_template('Modalidades.html')

@app.route('/professores')
def professores_router():
    return render_template('Professores.html')

@app.route('/matriculas')
def matriculas_router():
    return render_template('Matriculas.html')


@app.route('/cidades')
def cidades():
    cidades = []
    with open('./archives/Cidades.txt', 'r') as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha:
                continue
            partes = linha.replace(';', ',').split(',')
            info = {}
            for parte in partes:
                if ':' in parte:
                    chave, valor = parte.split(':', 1)
                    info[chave.strip()] = valor.strip()

            cidades.append(info)
    return render_template('cidades.html', cidades=cidades)

@app.route('/salvar_dados', methods=['POST'])
def salvar_dados():
    nome = request.form['nome']
    email = request.form['email']
    dados = f"Nome: {nome}, Email: {email}\n"
    with open('./archives/Matriculas.txt', 'a') as arquivo:
        arquivo.write(dados)
    return "Dados salvos com sucesso!"


@app.route('/adicionar-cidade', methods=['POST'])
def adicionar_cidade():
    codigo = request.form['codigo']
    descricao = request.form['descricao']
    estado = request.form['estado']
    objeto = Cidades(codigo, descricao, estado)
    op = OperacoesBasicas(TipoRegistroEnum.CIDADE)
    op.inserir_dados(objeto)
    return """
    <script>
        alert('Cidade adicionada com sucesso!');
        window.location.href = '/cidades';  // redireciona depois do alert
    </script>
    """


if __name__ == '__main__':
    app.run(debug=True)
