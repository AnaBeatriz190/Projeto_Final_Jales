from flask import *
import sqlite3 as sqlite
import DB

app = Flask(__name__)
app.secret_key = 'chavesupersecretashhhhh'

@app.route("/", methods=['GET'])
def raiz():
    DB.criar_tabelas()
    return render_template('cadastro.html')

@app.route('/cadastro', methods=['POST'])
def inserindo_dados():
    nome = request.form['nome']
    matricula = request.form['matricula']
    senha = request.form['senha']
    DB.inserirUsuario(nome, matricula, senha)
    
    return render_template('admin_lista_alunos.html')

@app.route('/listar_dados')
def listando():
    listaDB = DB.listarUsuario()
    return render_template('lista.html', lista=listaDB)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        matricula = request.form['matricula']
        senha = request.form['senha']
        
        if validar_login(matricula, senha):
            session['matricula'] = matricula  
            
            return render_template('home.html', matricula=matricula)
        else:
            flash('Matrícula ou senha incorretos!', 'error')
            return render_template('login.html')
    return render_template('login.html')

def validar_login(matricula, senha):
    conn = sqlite.connect('DB.sqlite')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM usuarios WHERE matricula = ? AND senha = ?', (matricula, senha))
    user = cursor.fetchone()
    
    conn.close()
    
    if user:
        return True
    return False

@app.route('/home', methods=['GET'])
def home():
    if 'matricula' in session:  
        return render_template('home.html', matricula=session['matricula'])
    else:
        return render_template('login.html') 

@app.route('/logout')
def logout():
    session.pop('matricula', None) 
    return render_template('login.html')



@app.route('/reservar_marmita', methods=['POST'])
def reservando_marmita():
    matricula = request.form['matricula']
    senha = request.form['senha']
    
    conn = sqlite.connect('DB.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT id_usuario FROM usuarios WHERE matricula = ?', (matricula,))
    usuario = cursor.fetchone()
    if usuario:
        id_usuario = usuario[0]
        DB.reservar_marmita(id_usuario)
    
    conn.close()
    
    return render_template('home.html', matricula=matricula)

if __name__ == "__main__":
    app.run(debug=True)
