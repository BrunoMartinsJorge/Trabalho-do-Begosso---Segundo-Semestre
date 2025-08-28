from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def formulario():
    return render_template('index.html')

@app.route('/salvar_dados', methods=['POST'])
def salvar_dados():
    nome = request.form['nome']
    email = request.form['email']

    dados = f"Nome: {nome}, Email: {email}\n"

    with open('dados.txt', 'a') as arquivo:
        arquivo.write(dados)
    return "Dados salvos com sucesso!"

if __name__ == '__main__':
    app.run(debug=True)