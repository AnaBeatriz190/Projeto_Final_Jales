from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3 as sqlite

app = Flask(__name__)
app.secret_key = 'supersecretkey'


#DDL
def criar_tabelas():
    conn = sqlite.connect('DB.sqlite')
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')
    cursor.execute(''' 
                   CREATE TABLE IF NOT EXISTS usuarios (
                       id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                       nome TEXT NOT NULL,
                       matricula TEXT NOT NULL,
                       senha TEXT NOT NULL
                   )
                   ''')
    cursor.execute('''        
                   CREATE TABLE IF NOT EXISTS reserva_marmita (
                       id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
                       id_usuario INTEGER NOT NULL,
                       hora_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                       FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
                   )
                   ''')

    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS lista (
                        id_lista INTEGER PRIMARY KEY AUTOINCREMENT,
                        quantidade_disponivel INTEGER NOT NULL,
                        data_lista,
                        hora_liberacao TIME
                    )
                    ''')
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS historico (
                        id_usuario INTEGER NOT NULL,
                        hora_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                        acao TEXT
                    )
                   ''')
    conn.commit()
    conn.close()


#DML
def inserirUsuario(nome, matricula, senha):
    conn = sqlite.connect('DB.sqlite')
    cursor = conn.cursor()
    
    try:
        conn.begin() 
        cursor.execute('''INSERT INTO usuarios (nome, matricula, senha) VALUES (?, ?, ?)''', 
                       (nome, matricula, senha))
        conn.commit() 
    except Exception as e:
        conn.rollback() 
        flash(f'Ocorreu um erro: {str(e)}', 'error')
    finally:
        conn.close()

def listarUsuario():
    conn = sqlite.connect('DB.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios order by id_usuario desc')
    dados = cursor.fetchall()
    usuarios = []
    for dado in dados:
        usuarios.append(dado)
    conn.close()
    return usuarios



def reservar_marmita(id_usuario):
    conn = sqlite.connect('DB.sqlite')
    cursor = conn.cursor()
    
    try:
        conn.begin()  
        cursor.execute('''INSERT INTO reserva_marmita (id_usuario) VALUES (?)''', (id_usuario,))
        conn.commit() 
    except Exception as e:
        conn.rollback() 
        flash(f'Ocorreu um erro ao reservar a marmita: {str(e)}', 'error')
    finally:
        conn.close()


#DQL

def validar_login(matricula, senha):
    conn = sqlite.connect('DB.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE matricula = ? AND senha = ?', (matricula, senha))
    user = cursor.fetchone()
    conn.close()
    return user is not None


#DCL
def criarAdmin():
    conn = sqlite.connect('DB.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
                    GRANT SELECT, INSERT, UPDATE
                    ON reserva_marmita.*
                    TO gerente;

                   ''')
    user = cursor.fetchone()
    conn.close()
    return user is not None

if __name__ == "__main__":
    app.run(debug=True)


#######################################################################################################################

def criar_triggers():
    conn = sqlite.connect('DB.sqlite')
    cursor = conn.cursor()

    
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS verificar_e_atualizar_lista
        BEFORE INSERT ON reserva_marmita
        FOR EACH ROW
        WHEN (SELECT quantidade_disponivel FROM lista ORDER BY id_lista DESC LIMIT 1) > 0
        BEGIN
            UPDATE lista
            SET quantidade_disponivel = quantidade_disponivel - 1
            WHERE id_lista = (SELECT id_lista FROM lista ORDER BY id_lista DESC LIMIT 1);
        END;
    ''')

    
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS historico_gatilho
        AFTER INSERT ON reserva_marmita
        FOR EACH ROW
        BEGIN
            INSERT INTO historicoDB (id_usuario, hora_reserva, acao)
            VALUES (NEW.id_usuario, NEW.hora_reserva, 'Reserva Adicionada');
        END;
    ''')

    conn.commit()
    conn.close()


criar_triggers()
#NÃO TEM COMO CRIAR PROCEDIMENTOS NO SQLITE EM SI, ENTÃO FIZ EM PYTHON E TORCER PRA PIEDADE DE JALES.

def procedimento_usuario_criado(id_usuario, nome, matricula):
    
    print(f"Usuário criado: ID={id_usuario}, Nome={nome}, Matrícula={matricula}")
def procedimento_lista_mostrada():
    print("Lista mostrada:")




