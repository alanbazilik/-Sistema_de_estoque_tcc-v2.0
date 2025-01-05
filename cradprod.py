import customtkinter as ctk
import cv2
from pyzbar.pyzbar import decode
import psycopg2
from tkinter import messagebox, ttk


# Função para abrir conexão com o banco de dados
def abrir_conexao():
    return psycopg2.connect(
        dbname="produtos_db",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )


# Inicializar banco de dados
def init_db():
    conn = abrir_conexao()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS produtos (
                        id SERIAL PRIMARY KEY,
                        descricao TEXT NOT NULL,
                        quantidade INTEGER NOT NULL,
                        valor REAL NOT NULL,
                        codigo_barras TEXT UNIQUE NOT NULL)''')
    conn.commit()
    conn.close()


# Função para salvar produto
def salvar_produto(descricao, quantidade, valor, codigo_barras):
    if not descricao or not quantidade or not valor or not codigo_barras:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
        return

    try:
        conn = abrir_conexao()
        cursor = conn.cursor()

        # Verificar se o código de barras já existe
        cursor.execute("SELECT * FROM produtos WHERE codigo_barras = %s", (codigo_barras,))
        produto_existente = cursor.fetchone()

        if produto_existente:
            messagebox.showinfo("Aviso", f"O produto já está cadastrado no estoque:\n\n"
                                         f"Descrição: {produto_existente[1]}\n"
                                         f"Quantidade: {produto_existente[2]}\n"
                                         f"Valor: R$ {produto_existente[3]:.2f}")
        else:
            cursor.execute("INSERT INTO produtos (descricao, quantidade, valor, codigo_barras) VALUES (%s, %s, %s, %s)",
                           (descricao, quantidade, valor, codigo_barras))
            conn.commit()
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            listar_produtos()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar o produto: {e}")
    finally:
        conn.close()


# Função para alterar produto
def alterar_produto(descricao, quantidade, valor, codigo_barras):
    if not descricao or not quantidade or not valor or not codigo_barras:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
        return

    try:
        conn = abrir_conexao()
        cursor = conn.cursor()
        cursor.execute("UPDATE produtos SET descricao=%s, quantidade=%s, valor=%s WHERE codigo_barras=%s",
                       (descricao, quantidade, valor, codigo_barras))
        conn.commit()
        messagebox.showinfo("Sucesso", "Produto alterado com sucesso!")
        listar_produtos()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao alterar o produto: {e}")
    finally:
        conn.close()


# Função para deletar produto
def deletar_produto(codigo_barras):
    if not codigo_barras:
        messagebox.showerror("Erro", "O código de barras do produto deve ser informado!")
        return

    try:
        conn = abrir_conexao()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produtos WHERE codigo_barras=%s", (codigo_barras,))
        conn.commit()
        messagebox.showinfo("Sucesso", "Produto deletado com sucesso!")
        listar_produtos()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao deletar o produto: {e}")
    finally:
        conn.close()


# Função para ativar scanner com verificação de produto no estoque
def ativar_scanner(entry_codigo):
    cap = cv2.VideoCapture("http://192.168.1.103:4747/video")  # URL do DroidCam
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        for barcode in decode(frame):
            codigo = barcode.data.decode("utf-8")
            entry_codigo.delete(0, ctk.END)
            entry_codigo.insert(0, codigo)

            # Verificar se o código de barras já existe no banco de dados
            try:
                conn = abrir_conexao()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM produtos WHERE codigo_barras = %s", (codigo,))
                produto = cursor.fetchone()

                if produto:
                    messagebox.showinfo("Aviso", f"O produto já está cadastrado no estoque:\n\n"
                                                 f"Descrição: {produto[1]}\n"
                                                 f"Quantidade: {produto[2]}\n"
                                                 f"Valor: R$ {produto[3]:.2f}")
                else:
                    messagebox.showinfo("Info", "Código de barras não cadastrado. Preencha os dados para cadastrar.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao verificar produto: {e}")
            finally:
                conn.close()

            cap.release()
            cv2.destroyAllWindows()
            return

        cv2.imshow("Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# Função para preencher os campos ao clicar na tabela
def preencher_campos(event):
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item[0], "values")
        entry_descricao.delete(0, ctk.END)
        entry_descricao.insert(0, item[1])

        entry_quantidade.delete(0, ctk.END)
        entry_quantidade.insert(0, item[2])

        entry_valor.delete(0, ctk.END)
        entry_valor.insert(0, item[3])

        entry_codigo.delete(0, ctk.END)
        entry_codigo.insert(0, item[4])


# Função para listar produtos
def listar_produtos():
    for item in tree.get_children():
        tree.delete(item)

    try:
        conn = abrir_conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtos")
        produtos = cursor.fetchall()

        for produto in produtos:
            tree.insert("", "end", values=produto)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao listar produtos: {e}")
    finally:
        conn.close()


# Função para limpar o campo de código de barras
def limpar_codigo_barras():
    entry_codigo.delete(0, ctk.END)

# Configurar interface gráfica
ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("Cadastro de Produtos")
app.geometry("800x700")

# Campos de entrada
ctk.CTkLabel(app, text="Descrição:").pack(pady=5, fill="x", padx=20)
entry_descricao = ctk.CTkEntry(app, width=300)
entry_descricao.pack(pady=5, fill="x", padx=20)

ctk.CTkLabel(app, text="Quantidade:").pack(pady=5, fill="x", padx=20)
entry_quantidade = ctk.CTkEntry(app, width=300)
entry_quantidade.pack(pady=5, fill="x", padx=20)

ctk.CTkLabel(app, text="Valor:").pack(pady=5, fill="x", padx=20)
entry_valor = ctk.CTkEntry(app, width=300)
entry_valor.pack(pady=5, fill="x", padx=20)

# Frame para organizar o botão e a caixa de entrada lado a lado
frame_codigo = ctk.CTkFrame(app)
frame_codigo.pack(pady=10, fill="x", padx=20)

# Caixa de entrada para código de barras
ctk.CTkLabel(frame_codigo, text="Código de Barras:").pack(side="left", pady=5)

entry_codigo = ctk.CTkEntry(frame_codigo, width=300)
entry_codigo.pack(side="left", pady=5, padx=10)

# Botão para limpar o campo de código de barras
btn_limpar = ctk.CTkButton(frame_codigo, text="Limpar", command=limpar_codigo_barras, width=100)
btn_limpar.pack(side="left", pady=5)


# Botões
btn_scanner = ctk.CTkButton(app, text="Ativar Scanner", command=lambda: ativar_scanner(entry_codigo))
btn_scanner.pack(pady=10, fill="x", padx=20)

btn_salvar = ctk.CTkButton(app, text="Salvar Produto",
                           command=lambda: salvar_produto(
                               entry_descricao.get(),
                               int(entry_quantidade.get()),
                               float(entry_valor.get()),
                               entry_codigo.get()))
btn_salvar.pack(pady=10, fill="x", padx=20)

btn_alterar = ctk.CTkButton(app, text="Alterar Produto",
                            command=lambda: alterar_produto(
                                entry_descricao.get(),
                                int(entry_quantidade.get()),
                                float(entry_valor.get()),
                                entry_codigo.get()))
btn_alterar.pack(pady=10, fill="x", padx=20)

btn_deletar = ctk.CTkButton(app, text="Deletar Produto",
                            command=lambda: deletar_produto(entry_codigo.get()))
btn_deletar.pack(pady=10, fill="x", padx=20)



# Tabela para exibir produtos
frame_tabela = ctk.CTkFrame(app)
frame_tabela.pack(pady=10, fill="both", expand=True)

tree = ttk.Treeview(frame_tabela, columns=("ID", "Descrição", "Quantidade", "Valor", "Código de Barras"), show="headings")
tree.pack(fill="both", expand=True)

tree.heading("ID", text="ID")
tree.heading("Descrição", text="Descrição")
tree.heading("Quantidade", text="Quantidade")
tree.heading("Valor", text="Valor")
tree.heading("Código de Barras", text="Código de Barras")

# Configurar evento para clique duplo na tabela
tree.bind("<Double-1>", preencher_campos)

listar_produtos()


app.mainloop()
