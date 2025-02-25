import sqlite3 as sqlite

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
                       hora_reserva TEXT NOT NULL
                   )

                   ''')  
    cursor.execute('''        
                   CREATE TABLE IF NOT EXISTS lista (
                       id_lista  INTEGER PRIMARY KEY AUTOINCREMENT,
                       quantidade_disponivel INTEGER NOT NULL,
                       data_lista TEXT NOT NULL,
                       hora_liberacao TEXT NOT NULL
                   )

                   ''')                    
    
    conn.commit()
    conn.close()
    
criar_tabelas()

def inserirUsuario(nome, matricula, senha):
    conn = sqlite.connect('DB.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
                   INSERT INTO usuarios (nome, matricula, senha) VALUES (?, ?, ?)
                   ''', (nome, matricula, senha))
    conn.commit()
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