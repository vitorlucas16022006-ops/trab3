import tkinter as tk
from tkinter import ttk, messagebox
import os

ARQUIVO = "clientes.txt"

# =========================
# Classes
# =========================
class Cliente:
    def __init__(self, nome, renda, cpf):
        self.nome = nome
        self.renda = renda
        self.cpf = cpf

    # CLIENTE PREMIUM
    def eh_premium(self):
        return self.renda > 15000

    # CLIENTE VIP BLACK
    def eh_vip(self):
        return self.renda > 100000


class Investimento:
    def __init__(self, tipo, lucro):
        self.tipo = tipo
        self.lucro = lucro


# =========================
# Janela Principal
# =========================
root = tk.Tk()
root.title("Sistema Bancário")
root.geometry("900x600")
root.config(bg="#1e1e1e")


# =========================
# FUNÇÕES
# =========================
def cadastrar_cliente():
    nome = input_nome.get()
    cpf = input_cpf.get()
    renda = input_renda.get()

    if nome == "" or cpf == "" or renda == "":
        messagebox.showwarning("Aviso", "Preencha todos os campos.")
        return

    # VALIDAR CPF
    if not cpf.isdigit() or len(cpf) != 11:
        messagebox.showerror(
            "Erro",
            "CPF inválido. Digite 11 números."
        )
        return

    try:
        renda = float(renda)

    except ValueError:
        messagebox.showerror("Erro", "Renda inválida.")
        return

    # VERIFICAR CPF DUPLICADO
    if os.path.exists(ARQUIVO):

        with open(ARQUIVO, "r") as arquivo:

            for linha in arquivo.readlines():

                dados = linha.strip().split(";")

                if len(dados) == 3 and dados[1] == cpf:
                    messagebox.showerror(
                        "Erro",
                        "CPF já cadastrado."
                    )
                    return

    with open(ARQUIVO, "a") as arquivo:
        arquivo.write(f"{nome};{cpf};{renda}\n")

    messagebox.showinfo("Sucesso", "Cliente cadastrado!")

    input_nome.delete(0, tk.END)
    input_cpf.delete(0, tk.END)
    input_renda.delete(0, tk.END)


def listar_clientes():

    lista_clientes.delete(*lista_clientes.get_children())

    if not os.path.exists(ARQUIVO):
        return

    with open(ARQUIVO, "r") as arquivo:

        for linha in arquivo.readlines():

            dados = linha.strip().split(";")

            if len(dados) != 3:
                continue

            lista_clientes.insert(
                "",
                tk.END,
                values=(dados[0], dados[1], dados[2])
            )


def acessar_app():

    cpf_busca = input_busca.get()

    if not os.path.exists(ARQUIVO):
        messagebox.showerror("Erro", "Nenhum cliente encontrado.")
        return

    with open(ARQUIVO, "r") as arquivo:

        for linha in arquivo.readlines():

            dados = linha.strip().split(";")

            if len(dados) != 3:
                continue

            nome, cpf, renda_str = dados

            try:
                renda = float(renda_str)

            except ValueError:
                continue

            if cpf == cpf_busca:

                cliente = Cliente(nome, renda, cpf)

                janela = tk.Toplevel(root)
                janela.title("Aplicativo do Cliente")
                janela.geometry("500x500")
                janela.config(bg="#2b2b2b")

                titulo = tk.Label(
                    janela,
                    text="APP DE INVESTIMENTOS",
                    bg="#2b2b2b",
                    fg="white",
                    font=("Arial", 18, "bold")
                )

                titulo.pack(pady=15)

                info = f"""
Cliente: {cliente.nome}
CPF: {cliente.cpf}
Renda: R$ {cliente.renda:,.2f}
"""

                tk.Label(
                    janela,
                    text=info,
                    bg="#2b2b2b",
                    fg="white",
                    font=("Arial", 12)
                ).pack()

                # =========================
                # CLIENTE VIP BLACK
                # =========================
                if cliente.eh_vip():

                    tk.Label(
                        janela,
                        text="ÁREA VIP BLACK",
                        bg="#2b2b2b",
                        fg="gold",
                        font=("Arial", 16, "bold")
                    ).pack(pady=10)

                    investimentos_vip = [

                        Investimento(
                            "Bitcoin Internacional",
                            25000
                        ),

                        Investimento(
                            "Fundos Milionários",
                            40000
                        ),

                        Investimento(
                            "Carteira Global",
                            55000
                        ),

                        Investimento(
                            "Private Equity",
                            80000
                        )
                    ]

                    for inv in investimentos_vip:

                        btn = tk.Button(
                            janela,
                            text=f"{inv.tipo} | Lucro: R$ {inv.lucro}",
                            bg="gold",
                            fg="black",
                            width=38,
                            height=2,
                            command=lambda i=inv:
                            messagebox.showinfo(
                                "INVESTIMENTO VIP",
                                f"Você escolheu:\n{i.tipo}\n\nLucro esperado: R$ {i.lucro}"
                            )
                        )

                        btn.pack(pady=8)

                # =========================
                # CLIENTE PREMIUM
                # =========================
                elif cliente.eh_premium():

                    tk.Label(
                        janela,
                        text="Área Premium",
                        bg="#2b2b2b",
                        fg="#00ff88",
                        font=("Arial", 14, "bold")
                    ).pack(pady=10)

                    investimentos = [

                        Investimento(
                            "Renda Fixa",
                            1200
                        ),

                        Investimento(
                            "Ações",
                            3500
                        ),

                        Investimento(
                            "Fundos Imobiliários",
                            2800
                        )
                    ]

                    for inv in investimentos:

                        btn = tk.Button(
                            janela,
                            text=f"{inv.tipo} | Lucro: R$ {inv.lucro}",
                            bg="#00aa66",
                            fg="white",
                            width=35,
                            height=2,
                            command=lambda i=inv:
                            messagebox.showinfo(
                                "Investimento",
                                f"Você escolheu {i.tipo}\nLucro esperado: R$ {i.lucro}"
                            )
                        )

                        btn.pack(pady=8)

                # =========================
                # CLIENTE COMUM
                # =========================
                else:

                    tk.Label(
                        janela,
                        text="Cliente sem acesso premium",
                        bg="#2b2b2b",
                        fg="orange",
                        font=("Arial", 12, "bold")
                    ).pack(pady=15)

                    anuncios = [

                        "Cartão sem anuidade",

                        "Seguro de vida",

                        "Empréstimo consignado"
                    ]

                    for anuncio in anuncios:

                        tk.Button(
                            janela,
                            text=anuncio,
                            width=30,
                            bg="#444",
                            fg="white"
                        ).pack(pady=5)

                return

    messagebox.showerror("Erro", "Cliente não encontrado.")


# =========================
# MENU SUPERIOR
# =========================
barra_menu = tk.Menu(root)

menu_arquivo = tk.Menu(barra_menu, tearoff=0)

menu_arquivo.add_command(
    label="Listar Clientes",
    command=listar_clientes
)

menu_arquivo.add_separator()

menu_arquivo.add_command(
    label="Sair",
    command=root.quit
)

barra_menu.add_cascade(
    label="Menu",
    menu=menu_arquivo
)

root.config(menu=barra_menu)


# =========================
# TÍTULO
# =========================
titulo = tk.Label(
    root,
    text="SISTEMA BANCÁRIO",
    bg="#1e1e1e",
    fg="white",
    font=("Arial", 24, "bold")
)

titulo.pack(pady=20)


# =========================
# FRAME CADASTRO
# =========================
frame_cadastro = tk.Frame(
    root,
    bg="#2b2b2b",
    padx=20,
    pady=20
)

frame_cadastro.pack(pady=10)

tk.Label(
    frame_cadastro,
    text="Nome:",
    bg="#2b2b2b",
    fg="white"
).grid(row=0, column=0, sticky="w")

input_nome = tk.Entry(frame_cadastro, width=35)
input_nome.grid(row=0, column=1, pady=5)

tk.Label(
    frame_cadastro,
    text="CPF:",
    bg="#2b2b2b",
    fg="white"
).grid(row=1, column=0, sticky="w")

input_cpf = tk.Entry(frame_cadastro, width=35)
input_cpf.grid(row=1, column=1, pady=5)

tk.Label(
    frame_cadastro,
    text="Renda:",
    bg="#2b2b2b",
    fg="white"
).grid(row=2, column=0, sticky="w")

input_renda = tk.Entry(frame_cadastro, width=35)
input_renda.grid(row=2, column=1, pady=5)

btn_cadastrar = tk.Button(
    frame_cadastro,
    text="Cadastrar Cliente",
    command=cadastrar_cliente,
    bg="#00aa66",
    fg="white",
    width=25,
    height=2
)

btn_cadastrar.grid(row=3, columnspan=2, pady=15)


# =========================
# BOTÃO LISTAR
# =========================
btn_listar = tk.Button(
    root,
    text="Listar Clientes",
    command=listar_clientes,
    bg="#007acc",
    fg="white",
    width=25,
    height=2
)

btn_listar.pack(pady=10)


# =========================
# TABELA CLIENTES
# =========================
frame_lista = tk.Frame(root)
frame_lista.pack(pady=10)

colunas = ("Nome", "CPF", "Renda")

lista_clientes = ttk.Treeview(
    frame_lista,
    columns=colunas,
    show="headings",
    height=8
)

for col in colunas:
    lista_clientes.heading(col, text=col)
    lista_clientes.column(col, width=200)

lista_clientes.pack()


# =========================
# ACESSAR APP
# =========================
frame_busca = tk.Frame(root, bg="#1e1e1e")
frame_busca.pack(pady=20)

tk.Label(
    frame_busca,
    text="CPF do Cliente:",
    bg="#1e1e1e",
    fg="white"
).grid(row=0, column=0)

input_busca = tk.Entry(frame_busca, width=30)
input_busca.grid(row=0, column=1, padx=10)

btn_acessar = tk.Button(
    frame_busca,
    text="Acessar Aplicativo",
    command=acessar_app,
    bg="#ffaa00",
    fg="black",
    width=20
)

btn_acessar.grid(row=0, column=2)


# =========================
# EXECUTAR
# =========================
root.mainloop()