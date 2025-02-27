from flask import Flask, request, render_template, redirect, url_for, flash, session
import sqlite3 as sqlite
import DB

app = Flask(__name__)
app.secret_key = 'chavesupersecretashhhhh'

@app.route("/", methods=['GET'])
def raiz():
    return render_template('login.html')

@app.route('/cadastro', methods=['POST', 'GET'])
def inserindo_dados():
    if request.method == 'POST':

        nome = request.form['nome']
        matricula = request.form['matricula']
        senha = request.form['senha']
        DB.inserirUsuario(nome, matricula, senha)
        return render_template('home.html')
    else:
        return render_template('cadastro.html')
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
        return render_template('escolher_almoco.html', matricula=session['matricula'])
    else:
        return render_template('login.html') 

@app.route('/logout')
def logout():
    session.pop('matricula', None) 
    return render_template('login.html')

@app.route('/escolher_almoco', methods=['POST'])
def escolhendo():
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
    
    return render_template('escolher_almoco.html', matricula=matricula)

@app.route('/lista', methods = ['POST'])
def listando():
    alunos = DB.listarUsuario()
    return render_template('admin_lista_alunos.html', alunos=alunos)


if __name__ == "__main__":
    app.run(debug=True)
