#bibliotecas
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import unicodedata
from backend import ler_produtos, salvar_produto_backend, excluir_produto, ler_responsavel, editar_produto, ler_produtos

#janela principal
janela = Tk()
janela.title("Sistema de Cadastro - Adega")
janela.geometry("800x500")
janela.config(bg="#6DA096")

#titulo
tit = Label(janela, text="Adega - Stockify")
tit.config(font=("Impact", 20, "italic", "bold"), fg="#58877E", bg="#EDEDED")
tit.pack(fill="x", pady=20)

#tabela 
tree = ttk.Treeview(janela, columns=("ID", "Nome", "Marca", "Qtd", "Preço", "Tipo"), show="headings")

for coluna, texto, largura in [
    ("ID", "ID", 30),
    ("Nome", "Produto", 60),
    ("Marca", "Marca", 60),
    ("Qtd", "Qtd", 35),
    ("Preço", "Preço (R$)", 75),
    ("Tipo", "Tipo", 60)
]:
    tree.heading(coluna, text=texto)
    tree.column(coluna, width=largura)

tree.place(relx=0.23, rely=0.15, relwidth=0.75, relheight=0.75)

#funçao listar
def listar_func():
    produtos = ler_produtos()
    tree.delete(*tree.get_children())
    if not produtos:
        messagebox.showinfo("Aviso", "Nenhum produto encontrado.")
        return
    for p in produtos:
        try:
            id_produto, nome, marca, quantidade, preco, tipo = p
            tree.insert("", "end",
                        values=(id_produto, nome, marca, quantidade, f"R$ {float(preco):.2f}", tipo))
        except:
            continue

#janela de cadastro de produto
def abrir_cadas():
    cad = Toplevel()
    cad.title("Cadastrar Produto")
    cad.geometry("450x350")
    cad.config(bg="#6DA096")
    cad.grab_set()
    cad.resizable(False, False)
    #campos
    labels = ["Produto:", "Marca:", "Quantidade:", "Preço:", "Tipo:", "Funcionário:", "Data:"]
    entradas = {}
    y = 20
    for texto in labels:
        Label(cad, text=texto, bg="#C0C0C0",
              font=("arial", 10, "italic", "bold")).place(x=20, y=y)

        if texto == "Data:":
            ent = Entry(cad, state="readonly")
        else:
            ent = Entry(cad)

        ent.place(x=125, y=y)
        ent.config(bg="#ffffff", font=("Verdana", 10, "italic", "bold"))
        entradas[texto] = ent
        y += 40
    #data atual
    data_atual = datetime.now().strftime("%d/%m/%Y")
    entradas["Data:"].config(state="normal")
    entradas["Data:"].insert(0, data_atual)
    entradas["Data:"].config(state="readonly")
    #botao salvar
    Button(cad,text="Salvar",bg="#C0C0C0",fg="black",command=lambda: salvar_produto_ui(entradas, cad)).place(x=330, y=320)
    #botao cancelar
    Button(
        cad,
        text="Cancelar",
        bg="#C0C0C0",
        fg="black",
        command=cad.destroy).place(x=380, y=320)

#salvar produto
def salvar_produto_ui(campos, janela_cad):
    nome = campos["Produto:"].get().strip()
    marca = campos["Marca:"].get().strip()
    quantidade = campos["Quantidade:"].get().strip()
    preco = campos["Preço:"].get().strip()
    tipo = campos["Tipo:"].get().strip()
    funcionario = campos["Funcionário:"].get().strip()
    data = campos["Data:"].get().strip()

    #tratamento de erros
    if not nome or not marca or not quantidade or not preco or not tipo or not funcionario:
        messagebox.showerror("ERRO", "Preencha todos os campos.")
        return
    try:
        quantidade = int(quantidade)
    except:
        messagebox.showerror("ERRO", "Quantidade deve ser número inteiro.")
        return
    try:
        preco = float(preco)
    except:
        messagebox.showerror("ERRO", "Preço inválido.")
        return

    #chamando funçao do backend
    salvar_produto_backend(nome, marca, quantidade, preco, tipo, funcionario, data)

    listar_func()  #atualizando a tabela
    janela_cad.destroy()
    messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")

#excluir produto
def excluir():
    item= tree.selection()
    if not item:
        messagebox.showwarning('Aviso','Selecione um produto para excluir.')
        return
    valores= tree.item(item,'values')
    id_produto = valores[0]
    sucesso= excluir_produto(id_produto)
    if sucesso:
        messagebox.showinfo('Sucesso','Produto excluído com sucesso!')
        listar_func()
    else:
        messagebox.showerror('Erro', 'Não foi possivel excluir o produto')

#editar produto
def editar_produtoo():
    item = tree.selection()
    if not item:
        messagebox.showwarning("Aviso", "Selecione um produto para editar.")
        return

    valores = tree.item(item, "values")
    id_produto, nome, marca, quantidade, preco, tipo = valores
    preco = preco.replace("R$ ", "").replace(",", ".")
    
    edit = Toplevel()
    edit.title("Editar Produto")
    edit.geometry("450x350")
    edit.config(bg="#6DA096")
    edit.grab_set()
    edit.resizable(False, False)
    campos = {}
    labels = ["Produto:", "Marca:", "Quantidade:", "Preço:", "Tipo:"]
    valores_iniciais = [nome, marca, quantidade, preco, tipo]
    y = 20
    for texto, valor in zip(labels, valores_iniciais):
        Label(edit, text=texto, bg="#C0C0C0",
              font=("arial", 10, "italic", "bold")).place(x=20, y=y)
        ent = Entry(edit)
        ent.place(x=125, y=y)
        ent.insert(0, valor)
        campos[texto] = ent
        y += 40
    Button(edit,text="Salvar",bg="#C0C0C0",command=lambda: salvar_edicao(id_produto, campos, edit)).place(x=330, y=300)
    Button(edit, text="Cancelar", bg="#C0C0C0", command=edit.destroy).place(x=380, y=300)

def salvar_edicao(id_produto, campos, janela_edit):

    nome = campos["Produto:"].get().strip()
    marca = campos["Marca:"].get().strip()
    quantidade = campos["Quantidade:"].get().strip()
    preco = campos["Preço:"].get().strip()
    tipo = campos["Tipo:"].get().strip()

    try:
        quantidade = int(quantidade)
        preco = float(preco)
    except:
        messagebox.showerror("Erro", "Quantidade ou preço inválidos.")
        return

    sucesso = editar_produto(id_produto, nome, marca, quantidade, preco, tipo)

    if sucesso:
        listar_func()
        messagebox.showinfo("Sucesso", "Produto atualizado!")
        janela_edit.destroy()
    else:
        messagebox.showerror("Erro", "Falha ao editar produto.")

# Função para normalizar textos 
def normalizar(txt):
    return ''.join(c for c in unicodedata.normalize('NFD', txt)
                   if unicodedata.category(c) != 'Mn').lower()
# Barra de pesquisa
entry_pesquisa = Entry(janela, font=("Verdana", 10))
entry_pesquisa.place(relx=0.01, rely=0.54, relwidth=0.18, relheight=0.05)

# Função pesquisar
def pesquisar():
    busca = normalizar(entry_pesquisa.get().strip())
    if not busca:
        messagebox.showwarning("Aviso", "Digite algo para pesquisar.")
        return
    produtos = ler_produtos()
    tree.delete(*tree.get_children())
    encontrado = False

    for p in produtos:
        id_produto, nome, marca, quantidade, preco, tipo = p
        dados = f"{id_produto} {nome} {marca} {tipo}"  # Pesquisa em múltiplos campos
        dados_norm = normalizar(dados)

        if busca in dados_norm:
            tree.insert("", "end",
                        values=(id_produto, nome, marca, quantidade, f"R$ {float(preco):.2f}", tipo))
            encontrado = True

    if not encontrado:
        messagebox.showinfo("Resultado", "Nenhum resultado encontrado.")

# Botão de pesquisa 
Button(janela, text="Pesquisar", bg="#C0C0C0", command=pesquisar).place(relx=0.01, rely=0.60, relwidth=0.18, relheight=0.05)

def abrir_historico():
    hist = Toplevel()
    hist.title("Histórico de Cadastros")
    hist.geometry("600x400")
    hist.config(bg="#6DA096")
    hist.grab_set()  # bloqueia a principal até fechar

    # título
    Label(
        hist,
        text="Histórico de Cadastros",
        font=("Impact", 18),
        bg="#EDEDED",
        fg="#58877E").pack(fill="x", pady=10)

    # tabela
    tree_hist = ttk.Treeview(
        hist,
        columns=("ID", "Funcionário", "Produto", "Data", "ID do Produto"),
        show="headings")

    tree_hist.heading("ID", text="ID")
    tree_hist.heading("Funcionário", text="Funcionário")
    tree_hist.heading("Produto", text="Produto")
    tree_hist.heading("Data", text="Data")
    tree_hist.heading("ID do Produto", text="ID do Produto")

    tree_hist.column("ID", width=40)
    tree_hist.column("Funcionário", width=150)
    tree_hist.column("Produto", width=150)
    tree_hist.column("Data", width=100)
    tree_hist.column("ID do Produto", width=100)

    tree_hist.pack(expand=True, fill="both", padx=10, pady=10)

    # carregar dados
    dados = ler_responsavel()

    if not dados:
        messagebox.showinfo("Aviso", "Nenhum histórico encontrado.")
        return

    for item in dados:
        try:
            id_hist, funcionario, produto, data, id_produto = item
            tree_hist.insert("", "end", values=(id_hist, funcionario, produto, data, id_produto))
        except:
            continue

#botoes laterais
Button(janela, text="Visualizar Produtos", bg="#C0C0C0",command=listar_func).place(relx=0.01, rely=0.16, relwidth=0.18, relheight=0.06)
Button(janela, text="Adicionar Produto", bg="#C0C0C0",command=abrir_cadas).place(relx=0.01, rely=0.23, relwidth=0.18, relheight=0.06)
Button(janela, text="Editar Produto", bg="#C0C0C0",command=editar_produtoo).place(relx=0.01, rely=0.30, relwidth=0.18, relheight=0.06)
Button(janela, text="Remover Produto", bg="#C0C0C0",command=excluir).place(relx=0.01, rely=0.37, relwidth=0.18, relheight=0.06)
Button(janela, text="Histórico de Cadastros", bg="#C0C0C0",command=abrir_historico).place(relx=0.01, rely=0.44, relwidth=0.18, relheight=0.06)
Button(janela, text="Pesquisar", bg="#C0C0C0", command=pesquisar).place(relx=0.01, rely=0.60, relwidth=0.18, relheight=0.05)
Button(janela, text="Sair da aplicação", bg="#C0C0C0",command=janela.destroy).place(relx=0.01, rely=0.92, relwidth=0.18, relheight=0.06)

#inicia a interface
janela.mainloop()
