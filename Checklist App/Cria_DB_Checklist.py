import sqlite3

# Função para criar o banco de dados
def create_db():
    conn = sqlite3.connect('checklist.db')
    cursor = conn.cursor()

    # Tabela de usuários
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                    )''')

    # Tabela de tarefas
    cursor.execute('''CREATE OR ALTER TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        task TEXT NOT NULL,
                        completed INTEGER DEFAULT 0,
                        date TEXT,
                        loja TEXT NOT NULL,
                        gerente TEXT NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )''')

    conn.commit()
    conn.close()

# Chamar a função para criar o banco de dados (executar apenas uma vez)
create_db()
