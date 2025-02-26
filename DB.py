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
    procedimento_usuario_criado(nome, matricula, senha)
    
    
def listarUsuario():
    conn = sqlite.connect('DB.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios order by id_usuario desc')
    dados = cursor.fetchall()
    usuarios = []
    for dado in dados:
        usuarios.append(dado)
    conn.close()
    procedimento_lista_mostrada()
    return usuarios


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
#NÃO TEM COMO CRIAR PROCEDIMENTOS NO SQLITE EM SI, ENTÃO FIZEM PYTHON E TORCER PRA PIEDADE DE JALES.

def procedimento_usuario_criado(id_usuario, nome, matricula):
    
    print(f"Usuário criado: ID={id_usuario}, Nome={nome}, Matrícula={matricula}")
def procedimento_lista_mostrada():
    print("Lista mostrada:")




