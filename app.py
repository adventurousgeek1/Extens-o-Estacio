import tkinter as tk
from tkinter import messagebox
import psycopg2

# Função para conectar ao banco de dados PostgreSQL
def conectar_bd():
    try:
        conn = psycopg2.connect(
            host="localhost",  # Alterar para o host do seu banco
            database="informaticasPy",  # Substituir pelo nome do seu banco
            user="postgres",  # Substituir pelo nome de usuário
            password="sua senha"  # Substituir pela senha do seu banco
        )
        return conn
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para inserir os dados no banco de dados
def inserir_produto():
    id_produto = entry_id.get()
    nome_produto = entry_nome.get()
    descricao_produto = entry_descricao.get()
    preco_produto = entry_preco.get()
    quantidade_produto = entry_quantidade.get()
    
    conn = conectar_bd()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            INSERT INTO produtos (id, nome, descricao, preco, quantidade) 
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (id_produto, nome_produto, descricao_produto, preco_produto, quantidade_produto))
            conn.commit()
            
            janela_inserir = tk.Toplevel(root)
            janela_inserir.title("Inserir Produtos")
            janela_inserir.geometry("600x400") 
            
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inserir produto: {e}")
        finally:
            cursor.close()
            conn.close()

# Função para listar os produtos
def listar_produtos():
    conn = conectar_bd()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, descricao, preco, quantidade FROM produtos")
            produtos = cursor.fetchall()

            # Criar uma nova janela para exibir os produtos
            janela_listagem = tk.Toplevel(root)
            janela_listagem.title("Lista de Produtos")
            janela_listagem.geometry("600x400")  # Definir o tamanho da janela

            # Título das colunas
            tk.Label(janela_listagem, text="ID", width=10, anchor='w', padx=5).grid(row=0, column=0)
            tk.Label(janela_listagem, text="Nome", width=20, anchor='w', padx=5).grid(row=0, column=1)
            tk.Label(janela_listagem, text="Descrição", width=30, anchor='w', padx=5).grid(row=0, column=2)
            tk.Label(janela_listagem, text="Preço", width=10, anchor='w', padx=5).grid(row=0, column=3)
            tk.Label(janela_listagem, text="Quantidade", width=10, anchor='w', padx=5).grid(row=0, column=4)

            # Exibir os produtos
            for i, produto in enumerate(produtos):
                for j, dado in enumerate(produto):
                    tk.Label(janela_listagem, text=dado, width=20 if j == 2 else 10, anchor='w', padx=5).grid(row=i+1, column=j)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar produtos: {e}")
        finally:
            cursor.close()
            conn.close()

# Interface gráfica com Tkinter
root = tk.Tk()
root.title("Cadastro de Produtos")
root.geometry("300x305")

# Widgets do Tkinter para cadastrar produto
tk.Label(root, text="ID").grid(row=0, column=0, padx=10, pady=5)
entry_id = tk.Entry(root)
entry_id.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Nome").grid(row=1, column=0, padx=10, pady=5)
entry_nome = tk.Entry(root)
entry_nome.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Descrição").grid(row=2, column=0, padx=10, pady=5)
entry_descricao = tk.Entry(root)
entry_descricao.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Preço").grid(row=3, column=0, padx=10, pady=5)
entry_preco = tk.Entry(root)
entry_preco.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Quantidade").grid(row=4, column=0, padx=10, pady=5)
entry_quantidade = tk.Entry(root)
entry_quantidade.grid(row=4, column=1, padx=10, pady=5)

# Botão para cadastrar o produto
btn_cadastrar = tk.Button(root, text="Cadastrar Produto", command=inserir_produto)
btn_cadastrar.grid(row=5, columnspan=2, padx=10, pady=10)

# Botão para listar produtos
btn_listar = tk.Button(root, text="Listar Produtos", command=listar_produtos)
btn_listar.grid(row=6, columnspan=2, padx=10, pady=10)

root.mainloop()
