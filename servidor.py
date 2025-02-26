from flask import *
import DB
import historicoDB.sqlite
app = Flask(__name__)

@app.route("/", methods = ['GET'])
def raiz():
    DB.criar_tabelas()
    return render_template('cadastro.html')

@app.route('/cadastro', methods=['POST'])
def inserindo_dados():
    nome = request.form['nome']
    matricula = request.form['matricula']
    senha = request.form['senha']
    DB.inserirUsuario(nome, matricula, senha)
    lista = DB.listarUsuario()
    return render_template('lista.html', lista=lista)

@app.route('/listar_dados')
def listando():
    listaDB = DB.listarUsuario()
    return render_template('lista.html', lista=listaDB)



app.run(debug=True)