from flask import *
import sqlite3 as sqlite
import DB

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Chave secreta para sessões

# Rota inicial
@app.route("/", methods=['GET'])
def raiz():
    DB.criar_tabelas()
    return render_template('cadastro.html')

# Rota de Cadastro
@app.route('/cadastro', methods=['POST'])
def inserindo_dados():
    nome = request.form['nome']
    matricula = request.form['matricula']
    senha = request.form['senha']
    DB.inserirUsuario(nome, matricula, senha)
    
    return render_template('admin_lista_alunos.html')

# Rota de Listagem de Dados
@app.route('/listar_dados')
def listando():
    listaDB = DB.listarUsuario()
    return render_template('lista.html', lista=listaDB)

# Rota de Login (Página de Login)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        matricula = request.form['matricula']
        senha = request.form['senha']
        
        # Verificar se as credenciais são válidas
        if validar_login(matricula, senha):
            session['matricula'] = matricula  # Armazenando a matrícula na sessão
            # Ao invés de redirecionar, renderizamos a página diretamente
            return render_template('home.html', matricula=matricula)
        else:
            flash('Matrícula ou senha incorretos!', 'error')  # Mensagem de erro
            return render_template('login.html')  # Retornar para a página de login com erro
    return render_template('login.html')

# Função de validação do login
def validar_login(matricula, senha):
    conn = sqlite.connect('DB.sqlite')
    cursor = conn.cursor()
    
    # Verificar no banco de dados se existe um usuário com a matrícula e senha fornecidos
    cursor.execute('SELECT * FROM usuarios WHERE matricula = ? AND senha = ?', (matricula, senha))
    user = cursor.fetchone()
    
    conn.close()
    
    # Retorna True se o usuário for encontrado, caso contrário, retorna False
    if user:
        return True
    return False

# Rota para a página de Home (após login bem-sucedido)
@app.route('/home', methods=['GET'])
def home():
    if 'matricula' in session:  # Verifica se o usuário está logado
        return render_template('home.html', matricula=session['matricula'])
    else:
        return render_template('login.html')  # Renderiza o login se não estiver logado

# Rota de Logout
@app.route('/logout')
def logout():
    session.pop('matricula', None)  # Remove o usuário da sessão
    # Ao invés de redirecionar, renderizamos a página de login diretamente
    return render_template('login.html')



@app.route('/reservar_marmita', methods=['POST'])
def reservando_marmita():
    matricula = request.form['matricula']
    senha = request.form['senha']
    
    # Inserir o usuário no banco de dados
    
    # Realizar a reserva de marmita
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
