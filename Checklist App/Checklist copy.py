##################################################################################
############## Por: Fábio Oliveira   -  Atualizado em: 09/07/2024 ################
##################################################################################

import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import *


## verificar o login ##
def login():
    username = username_entry.get()
    password = password_entry.get()

    conn = sqlite3.connect('checklist.db')
    cursor = conn.cursor()

    ## consulta se o usuário e senha estão na base de dados ##
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()

    conn.close()

     ## busca o ID do usuário para carregar suas tarefas ##
    if user:
        logged_in_user['text'] = f'Usuário logado: {username}'
        load_tasks(user[0]) 
    else:
        messagebox.showerror('Login', 'Usuário ou senha incorretos.')


## registra um novo usuário ##
def register():
    username = username_entry.get()
    password = password_entry.get()

    conn = sqlite3.connect('checklist.db')
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        messagebox.showinfo('Cadastro', 'Cadastro realizado com sucesso.')
    except sqlite3.IntegrityError:
        messagebox.showerror('Cadastro', 'Nome de usuário já existe.')

    conn.close()


## carrega as tarefas do usuário ##
def load_tasks(user_id):
    conn = sqlite3.connect('checklist.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM tasks WHERE user_id=?', (user_id,))
    tasks = cursor.fetchall()

    ## limpa a lista de tarefas ##
    tasks_listbox.delete(0, tk.END)  

    for task in tasks:
        task_description = task[2]
        completed = task[3]
        status = '✔️' if completed else '❌'
        tasks_listbox.insert(tk.END, f'{status} {task_description}')

    conn.close()


## adiciona uma nova tarefa ##
def add_task():
    user_id = get_logged_in_user_id()
    task = new_task_entry.get()
    loja = new_loja.get()
    gerente = new_gerente.get()
 

    conn = sqlite3.connect('checklist.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO tasks (user_id, task, loja, gerente) VALUES (?, ?, ?, ?)', (user_id, task, loja, gerente))
    conn.commit()

    conn.close()

    ## carrega as tarefas após adicionar uma nova ##
    load_tasks(user_id)  


## marca uma tarefa como concluída ##
def complete_task():
    selected_task_index = tasks_listbox.curselection()
    if selected_task_index:
        task_id = selected_task_index[0] + 1  

        conn = sqlite3.connect('checklist.db')
        cursor = conn.cursor()

        cursor.execute('UPDATE tasks SET completed=1 WHERE id=?', (task_id,))
        conn.commit()

        conn.close()

        ## carrega as tarefas após marcar como concluída ##
        load_tasks(get_logged_in_user_id())  


## obtei o ID do usuário logado ##
def get_logged_in_user_id():
    username = logged_in_user['text'].split(': ')[1].strip()

    conn = sqlite3.connect('checklist.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM users WHERE username=?', (username,))
    user_id = cursor.fetchone()[0]

    conn.close()
    return user_id


## interface gráfica ##
root = tk.Tk()
root.title('Checklist')

imagem = PhotoImage(file=r"C:\Users\Performance9\Documents\04. DESENVOLVIMENTO\04.1 PYTHON\Ferramenta de CheckList App\Logo BH WorkSpace.png")
w = Label(root, image=imagem)
w.imagem = imagem
w.pack()


## Widgets para login ##
login_frame = tk.Frame(root)
login_frame.pack()

username_label = tk.Label(login_frame, text='Usuário:')
username_label.grid(row=0, column=0, padx=10, pady=5)
username_entry = tk.Entry(login_frame)
username_entry.grid(row=0, column=1, padx=10, pady=5)

password_label = tk.Label(login_frame, text='Senha:')
password_label.grid(row=1, column=0, padx=10, pady=5)
password_entry = tk.Entry(login_frame, show='*')
password_entry.grid(row=1, column=1, padx=10, pady=5)

login_button = tk.Button(login_frame, text='Login', command=login)
login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

register_button = tk.Button(login_frame, text='Cadastro', command=register)
register_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)


## Widgets para checklist ##
checklist_frame = tk.Frame(root)
checklist_frame.pack()

logged_in_user = tk.Label(checklist_frame, text='Nenhum usuário logado')
logged_in_user.pack(pady=10)

new_loja = tk.Label(checklist_frame, text='Loja')
new_loja.pack()

new_loja = tk.Entry(checklist_frame, width=60)
new_loja.pack()

new_gerente = tk.Label(checklist_frame, text='Gerente')
new_gerente.pack()

new_gerente = tk.Entry(checklist_frame, width=60)
new_gerente.pack()

new_task_entry = tk.Label(checklist_frame, text='Atividade')
new_task_entry.pack()

new_task_entry = tk.Entry(checklist_frame, width=60)
new_task_entry.pack()

add_task_button = tk.Button(checklist_frame, text='Adicionar Tarefa', command=add_task)
add_task_button.pack(pady=10)

tasks_listbox = tk.Listbox(checklist_frame, width=60, height=12)
tasks_listbox.pack()

complete_task_button = tk.Button(checklist_frame, text='Marcar como Concluída', command=complete_task)
complete_task_button.pack(pady=10)


root.mainloop()
