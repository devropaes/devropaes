#Este projeto foi desenvolvido  para o controle interno de uma empresa
# e é responsável por analisar os perfis de acessos de seus funcionários
# existentes em seu sistema e definir se a combinação de perfis, para um
# mesmo usuário, pode apresentar algum conflito de interesse.
# Um conflito de interesse é quando o usuário pode se aproveitar dos acessos
# que possui para praticar uma fraude.

#Passo 1
#Importação de Bibliotecas
import tkinter as tk # a criação da interface gráfica (Tkinter)
from tkinter import messagebox #exibição de caixas de diálogo (messagebox)
import csv #manipulação de arquivos CSV (csv)
import os #manipulação de arquivos do sistema (os)
from sqlalchemy import create_engine, Column, Integer, String # manipulação de banco de dados SQLite (SQLAlchemy).
from sqlalchemy.orm import sessionmaker #simplifica a criação e o gerenciamento de sessões SQLAlchemy (sessionmaker)
from sqlalchemy.ext.declarative import declarative_base #é uma ferramenta poderosa que torna mais fácil criar e
# gerenciar modelos de banco de dados usando SQLAlchemy(declarative_base)

#Passo 2
# Configurei o banco de dados SQLite chamado "site.db" usando o SQLAlchemy.
# O parâmetro echo=True permite a exibição de saídas de depuração.
engine = create_engine('sqlite:///site.db', echo=True)
Base = declarative_base()

#Passo 3
# Definição das Tabelas do Banco de Dados:
# Defini três classes que representam tabelas no banco de dados:
# Sistema, Perfil Acesso, e MatrizSoD. Cada classe corresponde a uma
# tabela no banco de dados e define seus campos (colunas) e tipos de dados.
# Configuração do banco de dados SQLite
#Abri o terminal do PyCharm. (Você pode encontrá-lo no menu superior indo para "View"
# (Visualizar) -> "Tool Windows" (Janelas de Ferramentas) -> "Terminal").
#No terminal, digite o seguinte comando e pressione Enter: instale pip install sqlalchemy
class Sistema(Base):
    __tablename__ = 'sistema'
    id = Column(Integer, primary_key=True)
    codigo = Column(String(15), unique=True, nullable=False)
    nome = Column(String(20), nullable=False)

class PerfilAcesso(Base):
    __tablename__ = 'perfil_acesso'
    id = Column(Integer, primary_key=True)
    codigo_sistema = Column(String(15), nullable=False)
    nome = Column(String(20), nullable=False)
    descricao = Column(String(200), nullable=False)

class MatrizSoD(Base):
    __tablename__ = 'matriz_sod'
    id = Column(Integer, primary_key=True)
    codigo_sistema_1 = Column(String(15), nullable=False)
    codigo_sistema_2 = Column(String(15), nullable=False)
    codigo_perfil_1 = Column(String(20), nullable=False)
    codigo_perfil_2 = Column(String(20), nullable=False)

# Função para Verificar Conflitos na Matriz SoD:
# A função verificar_conflito é definida para verificar se há conflitos
# entre sistemas e perfis de acesso selecionados na interface gráfica.
def verificar_conflito():
    sistema1 = sistema1_var.get()
    perfil1 = perfil1_var.get()
    sistema2 = sistema2_var.get()
    perfil2 = perfil2_var.get()

    if sistema1 == sistema2 and perfil1 == perfil2:
        messagebox.showerror("Conflito de Interesse", "Os perfis selecionados têm conflito de interesse.")
    else:
        messagebox.showinfo("Sem Conflito", "Não há conflito de interesse entre os perfis selecionados.")

# Função para cadastrar sistemas no banco de dados
def cadastrar_sistema():
    sistema = sistema_entry.get().strip()
    nome_sistema = sistema_nome_entry.get().strip()

    if not sistema or not nome_sistema:
       messagebox.showerror("Erro de Cadastro", "O código e o nome do sistema são obrigatórios.")
    else:
        # Cadastrar o sistema no banco de dados
        session = Session()
        novo_sistema = Sistema(codigo=sistema, nome=nome_sistema)
        session.add(novo_sistema)
        session.commit()
        session.close()

        messagebox.showinfo("Cadastro de Sistema", "Sistema cadastrado com sucesso.")

# Função para cadastrar perfis de acesso no banco de dados
def cadastrar_perfil():
    sistema = sistema_perfil_var.get().strip()
    perfil = perfil_entry.get().strip()
    descricao = descricao_entry.get().strip()

    if not sistema or not perfil or not descricao:
        messagebox.showerror("Erro de Cadastro", "O sistema, nome do perfil e descrição são obrigatórios.")
    else:
        # Cadastrar o perfil de acesso no banco de dados
        session = Session()
        novo_perfil = PerfilAcesso(codigo_sistema=sistema, nome=perfil, descricao=descricao)
        session.add(novo_perfil)
        session.commit()
        session.close()

        messagebox.showinfo("Cadastro de Perfil de Acesso", "Perfil de acesso cadastrado com sucesso.")


# Função para exportar dados para CSV
def exportar_csv():
    sistemas = Session().query(Sistema).all()
    perfis = Session().query(PerfilAcesso).all()
    matriz_sod = Session().query(MatrizSoD).all()

    with open('dados.csv', 'w', newline='') as arquivo_csv:
        writer = csv.writer(arquivo_csv)
        writer.writerow(['Sistema', 'Nome do Sistema'])
        for sistema in sistemas:
            writer.writerow([sistema.codigo, sistema.nome])

        writer.writerow(['Codigo do Sistema', 'Nome do Perfil', 'Descrição do Perfil'])
        for perfil in perfis:
            writer.writerow([perfil.codigo_sistema, perfil.nome, perfil.descricao])

        writer.writerow(['Codigo do Sistema 1', 'Codigo do Sistema 2', 'Codigo do Perfil 1', 'Codigo do Perfil 2'])
        for sod in matriz_sod:
            writer.writerow([sod.codigo_sistema_1, sod.codigo_sistema_2, sod.codigo_perfil_1, sod.codigo_perfil_2])

    messagebox.showinfo("Exportar para CSV", "Dados exportados para 'dados.csv'.")

# Função para importar dados de um arquivo CSV
def importar_csv():
    arquivo_csv = 'dados.csv'
    if os.path.exists(arquivo_csv):
        with open(arquivo_csv, 'r') as arquivo_csv:
            reader = csv.reader(arquivo_csv)
            next(reader)  # Ignora a linha de cabeçalho
            for row in reader:
                if len(row) == 2:  # Dados de sistemas
                    sistema = Sistema(codigo=row[0], nome=row[1])
                    session = Session()
                    session.add(sistema)
                    session.commit()
                    session.close()
                elif len(row) == 3:  # Dados de perfis
                    perfil = PerfilAcesso(codigo_sistema=row[0], nome=row[1], descricao=row[2])
                    session = Session()
                    session.add(perfil)
                    session.commit()
                    session.close()
                elif len(row) == 4:  # Dados da Matriz SoD
                    sod = MatrizSoD(codigo_sistema_1=row[0], codigo_sistema_2=row[1], codigo_perfil_1=row[2], codigo_perfil_2=row[3])
                    session = Session()
                    session.add(sod)
                    session.commit()
                    session.close()
        messagebox.showinfo("Importar CSV", "Dados importados com sucesso.")
    else:
        messagebox.showerror("Importar CSV", "O arquivo 'dados.csv' não foi encontrado.")

# Configuração do banco de dados e criação da tabela
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Criação da janela principal
root = tk.Tk()
root.title("Matriz SoD")

# Frames para os diferentes elementos da aplicação- (Frames são contêineres retangulares
# usados para organizar e agrupar elementos em uma interface gráfica).
frame_sod = tk.Frame(root)
frame_sod.pack(pady=10)

frame_sistema = tk.Frame(root)
frame_sistema.pack(pady=10)

frame_perfil = tk.Frame(root)
frame_perfil.pack(pady=10)

# Matriz SoD
#Labels estão sendo criados dentro do frame_sod para exibir rótulos como "Sistema 1", "Perfil 1", "Sistema 2" e "Perfil 2"
#na interface gráfica.
sistema1_label = tk.Label(frame_sod, text="Sistema 1:")
sistema1_label.grid(row=0, column=0)


sistema1_var = tk.StringVar() #Variáveis do tipo StringVar são criadas (sistema1_var, perfil1_var, sistema2_var, perfil2_var) e associadas
# aos campos de entrada correspondentes.
sistema1_entry = tk.Entry(frame_sod, textvariable=sistema1_var) #Entry é usado para permitir que o usuário insira texto na interface gráfica.
sistema1_entry.grid(row=0, column=1)

perfil1_label = tk.Label(frame_sod, text="Perfil 1:")
perfil1_label.grid(row=0, column=2)

perfil1_var = tk.StringVar()
perfil1_entry = tk.Entry(frame_sod, textvariable=perfil1_var)
perfil1_entry.grid(row=0, column=3)

sistema2_label = tk.Label(frame_sod, text="Sistema 2:")
sistema2_label.grid(row=1, column=0)

sistema2_var = tk.StringVar()
sistema2_entry = tk.Entry(frame_sod, textvariable=sistema2_var)
sistema2_entry.grid(row=1, column=1)

perfil2_label = tk.Label(frame_sod, text="Perfil 2:")
perfil2_label.grid(row=1, column=2)

perfil2_var = tk.StringVar()
perfil2_entry = tk.Entry(frame_sod, textvariable=perfil2_var)
perfil2_entry.grid(row=1, column=3)

verificar_button = tk.Button(frame_sod, text="Verificar Conflito", command=verificar_conflito) #Um botão com o texto
# "Verificar Conflito" é criado dentro do frame_sod.
verificar_button.grid(row=2, column=0, columnspan=4)

# Cadastro de Sistemas
sistema_label = tk.Label(frame_sistema, text="Sistema:")
sistema_label.grid(row=0, column=0)

sistema_entry = tk.Entry(frame_sistema)
sistema_entry.grid(row=0, column=1)

sistema_nome_label = tk.Label(frame_sistema, text="Nome do Sistema:")
sistema_nome_label.grid(row=1, column=0)

sistema_nome_entry = tk.Entry(frame_sistema)
sistema_nome_entry.grid(row=1, column=1)

cadastrar_sistema_button = tk.Button(frame_sistema, text="Cadastrar Sistema", command=cadastrar_sistema)
cadastrar_sistema_button.grid(row=2, column=0, columnspan=2)

# Cadastro de Perfis de Acesso
sistema_perfil_label = tk.Label(frame_perfil, text="Sistema:")
sistema_perfil_label.grid(row=0, column=0)

sistema_perfil_var = tk.StringVar()
sistema_perfil_combobox = tk.Entry(frame_perfil, textvariable=sistema_perfil_var)
sistema_perfil_combobox.grid(row=0, column=1)

perfil_label = tk.Label(frame_perfil, text="Perfil:")
perfil_label.grid(row=1, column=0)

perfil_entry = tk.Entry(frame_perfil)
perfil_entry.grid(row=1, column=1)

descricao_label = tk.Label(frame_perfil, text="Descrição:")
descricao_label.grid(row=2, column=0)

descricao_entry = tk.Entry(frame_perfil)
descricao_entry.grid(row=2, column=1)

cadastrar_perfil_button = tk.Button(frame_perfil, text="Cadastrar Perfil", command=cadastrar_perfil)
cadastrar_perfil_button.grid(row=3, column=0, columnspan=2)

# Botões para exportar e importar dados
exportar_csv_button = tk.Button(root, text="Exportar para CSV", command=exportar_csv)
exportar_csv_button.pack(pady=10)

importar_csv_button = tk.Button(root, text="Importar CSV", command=importar_csv)
importar_csv_button.pack()

root.mainloop()

