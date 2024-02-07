import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import *
from tkinter import ttk, messagebox
from pandastable import Table, TableModel
import locale
from datetime import datetime
#from reportlab.lib.pagesizes import letter
#from reportlab.lib import colors
import os
from openpyxl import Workbook
#from reportlab.pdfgen import canvas

# Configurar a formatação da moeda para o Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Função para exportar para Excel em fase de teste
#def exportar_para_excel(df, nome_arquivo):
    #writer = pd.ExcelWriter(nome_arquivo, engine='xlsxwriter')
    #df.to_excel(writer, index=False, sheet_name='Dados')
    #writer.save()
    #messagebox.showinfo('Sucesso', f'DataFrame exportado para {nome_arquivo}')

# Função para exportar para PDF em fase de teste
#def exportar_para_pdf(df, nome_arquivo):
    #c = canvas.Canvas(nome_arquivo, pagesize=letter)

    # Choose specific columns to include in the PDF
    #columns_to_export = ['Produto', 'Quantidade_Vendida', 'Preco_Unitario', 'Categoria']

    # Filter DataFrame to include only the chosen columns
    #df_to_export = df[columns_to_export]

    # Convert 'Preco_Unitario' to numeric (assuming it contains numbers)
    #df_to_export['Preco_Unitario'] = pd.to_numeric(df_to_export['Preco_Unitario'], errors='coerce')

    # Drop rows with NaN values
    #df_to_export = df_to_export.dropna()

    # Convert the DataFrame to a list of lists for the TableModel
    #tabela_pdf = [df_to_export.columns.tolist()] + df_to_export.values.tolist()

    #table = Table(tabela_pdf)
    #table.setStyle([('GRID', (0, 0), (-1, -1), 1, colors.black)])
    #width, height = letter
    #table.wrapOn(c, width, height)
    #table.drawOn(c, 30, height - 150)
    #c.save()
    #messagebox.showinfo('Sucesso', f'DataFrame exportado para {nome_arquivo}')



def obter_dados():
    produto = entrada_produto.get().strip()

    if not produto:
        return None

    quantidade_vendida = int(entrada_quantidade.get())
    preco_unitario = float(entrada_preco.get())
    categoria = entrada_categoria.get().strip()

    return {'Produto': produto, 'Quantidade_Vendida': quantidade_vendida, 'Preco_Unitario': preco_unitario,
            'Categoria': categoria}

def validar_dados(dados):
    try:
        quantidade_vendida = int(dados['Quantidade_Vendida'])
        preco_unitario = float(dados['Preco_Unitario'])

        if quantidade_vendida <= 0 or preco_unitario <= 0:
            raise ValueError('Erro: A quantidade vendida e o preço unitário devem ser positivos.')
    except ValueError:
        raise ValueError('Erro: Insira valores válidos para quantidade vendida e preço unitário.')

def exibir_estatisticas(df):
    if not df.empty:
        messagebox.showinfo('DataFrame Atualizado', f'{df}\n\nResumo Estatístico:\n{df.describe()}')
    else:
        messagebox.showinfo('DataFrame Vazio', 'DataFrame vazio. Nenhuma estatística para exibir.')

def criar_visualizacoes(df):
    if not df.empty:
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        sns.scatterplot(data=df, x='Quantidade_Vendida', y='Preco_Unitario', hue='Categoria')
        plt.title('Relação entre Quantidade Vendida e Preço Unitário por Categoria')
        plt.xlabel('Quantidade Vendida')
        plt.ylabel('Preço Unitário')

        plt.subplot(1, 2, 2)
        sns.boxplot(data=df, x='Categoria', y='Preco_Unitario')
        plt.title('Distribuição de Preços por Categoria')
        plt.xlabel('Categoria')
        plt.ylabel('Preço Unitário')
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(8, 6))
        sns.histplot(df['Preco_Unitario'], bins=20, kde=True)
        plt.title('Distribuição de Preços Unitários')
        plt.xlabel('Preço Unitário')
        plt.ylabel('Frequência')
        plt.show()

        plt.figure(figsize=(8, 6))
        sns.countplot(data=df, x='Categoria')
        plt.title('Contagem de Produtos por Categoria')
        plt.xlabel('Categoria')
        plt.ylabel('Contagem')
        plt.show()

    else:
        print('DataFrame vazio. Nada para visualizar.')

def exportar_para_csv(df, nome_arquivo):
    df.to_csv(nome_arquivo, index=False)
    messagebox.showinfo('Sucesso', f'DataFrame exportado para {nome_arquivo}')

def salvar_e_fechar():
    global df
    dados = obter_dados()
    if dados:
        try:
            validar_dados(dados)
            preco_formatado = locale.currency(dados['Preco_Unitario'], grouping=True)
            novo_dado = {'Produto': dados['Produto'], 'Quantidade_Vendida': dados['Quantidade_Vendida'],
                         'Preco_Unitario': preco_formatado, 'Categoria': dados['Categoria']}
            df = pd.concat([df, pd.DataFrame([novo_dado])], ignore_index=True)
            exportar_para_csv(df, 'dados_produtos.csv')
            messagebox.showinfo('Sucesso', 'Dados salvos com sucesso!')
            exibir_estatisticas(df)
            criar_visualizacoes(df)
        except ValueError as e:
            messagebox.showerror('Erro', str(e))

def exibir_tabela():
    top = Toplevel()
    top.title("Visualização da Tabela")

    frame = Frame(top)
    frame.pack(padx=10, pady=10)

    pt = Table(frame, dataframe=df, showtoolbar=True, showstatusbar=True)
    pt.show()

def encerrar_programa():
    root.destroy()

def exportar_e_encerrar():
    exportar_para_csv(df, 'dados_produtos.csv')
    encerrar_programa()

# Função para simular uma venda
def realizar_venda():
    produto_selecionado = combo_produtos.get()
    quantidade_vendida = int(entry_quantidade_venda.get())

    if produto_selecionado and quantidade_vendida > 0:
        try:
            # Atualiza o DataFrame com a venda
            df.loc[df['Produto'] == produto_selecionado, 'Quantidade_Vendida'] += quantidade_vendida

            # Adiciona uma nova entrada para a venda no histórico
            historico_vendas.append({'Produto': produto_selecionado, 'Quantidade_Vendida': quantidade_vendida,
                                     'Data_Venda': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

            messagebox.showinfo('Sucesso', 'Venda realizada com sucesso!')
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao realizar a venda: {str(e)}')
    else:
        messagebox.showwarning('Aviso', 'Selecione um produto e insira uma quantidade válida para a venda.')


# Função para ver_tabelas_anteriores
def ver_tabelas_anteriores():
    # Verificar se há tabelas anteriores
    arquivos_csv = [f for f in os.listdir() if f.endswith('.csv') and f.startswith('dados_produtos')]

    if not arquivos_csv:
        messagebox.showinfo('Informação', 'Nenhuma tabela anterior encontrada.')
        return

    # Criar uma nova janela para exibir a tabela anterior
    top = Toplevel()
    top.title("Tabelas Anteriores")

    # Adicionar uma tabela Pandas para cada arquivo CSV
    for arquivo_csv in arquivos_csv:
        arquivo_label = Label(top, text=f'Tabela: {arquivo_csv}')
        arquivo_label.pack()

        tabela_frame = Frame(top)
        tabela_frame.pack(padx=10, pady=10)

        df_anterior = pd.read_csv(arquivo_csv)
        pt = Table(tabela_frame, dataframe=df_anterior, showtoolbar=True, showstatusbar=True)
        pt.show()

def adicionar_produto():
    dados = obter_dados()
    global df
    if dados:
        try:
            validar_dados(dados)
            preco_formatado = locale.currency(dados['Preco_Unitario'], grouping=True)
            novo_dado = {'Produto': dados['Produto'], 'Quantidade_Vendida': dados['Quantidade_Vendida'],
                         'Preco_Unitario': preco_formatado, 'Categoria': dados['Categoria']}
            df = pd.concat([df, pd.DataFrame([novo_dado])], ignore_index=True)
            exportar_para_csv(df, 'dados_produtos.csv')
            messagebox.showinfo('Sucesso', 'Produto adicionado com sucesso!')
            exibir_estatisticas(df)
            criar_visualizacoes(df)
            atualizar_combobox()
        except ValueError as e:
            messagebox.showerror('Erro', str(e))


def remover_produto():
    global df
    produto_selecionado = combo_produtos.get()
    if produto_selecionado:
        confirmacao = messagebox.askyesno('Confirmação', f'Tem certeza que deseja remover o produto "{produto_selecionado}"?')
        if confirmacao:
            df = df[df['Produto'] != produto_selecionado]
            exportar_para_csv(df, 'dados_produtos.csv')
            messagebox.showinfo('Sucesso', 'Produto removido com sucesso!')
            exibir_estatisticas(df)
            criar_visualizacoes(df)
            atualizar_combobox()
    else:
        messagebox.showwarning('Aviso', 'Selecione um produto para remover.')


def editar_produto():
    produto_selecionado = combo_produtos.get()
    if produto_selecionado:
        # TODO: Implementar a edição de produto
        messagebox.showinfo('Informação', 'Funcionalidade de edição ainda não implementada.')
    else:
        messagebox.showwarning('Aviso', 'Selecione um produto para editar.')


def atualizar_combobox():
    produtos_disponiveis = df['Produto'].unique()
    combo_produtos['values'] = produtos_disponiveis

def exibir_historico(historico):
    top = Toplevel()
    top.title("Histórico")

    if not historico:
        Label(top, text="Nenhum histórico disponível.").pack(padx=10, pady=10)
    else:
        for i, entry in enumerate(historico, start=1):
            texto = f"{i}. {entry['Produto']} - {entry.get('Quantidade_Vendida', entry.get('Qualificacao'))} - {entry.get('Data_Venda', entry.get('Data_Qualificacao'))}"
            Label(top, text=texto).pack(padx=10, pady=5)



# Função para qualificar um produto
def qualificar_produto():
    produto_selecionado = combo_produtos.get()
    qualificacao = combo_qualificacao.get()

    if produto_selecionado and qualificacao:
        try:
            # Atualiza o DataFrame com a qualificação
            df.loc[df['Produto'] == produto_selecionado, 'Qualificacao'] = qualificacao

            # Adiciona uma nova entrada para a qualificação no histórico
            historico_qualificacoes.append({'Produto': produto_selecionado, 'Qualificacao': qualificacao,
                                            'Data_Qualificacao': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

            messagebox.showinfo('Sucesso', 'Produto qualificado com sucesso!')
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao qualificar o produto: {str(e)}')
    else:
        messagebox.showwarning('Aviso', 'Selecione um produto e uma qualificação.')

# Interface gráfica
root = Tk()
root.title("Cadastro e Vendas de Produtos")

# Criar e organizar a interface gráfica

frame_entrada = Frame(root, padx=20, pady=20)
frame_entrada.pack(padx=10, pady=10)
rotulos_entrada = ['Produto', 'Quantidade_Vendida', 'Preco_Unitario', 'Categoria']
entrada_variaveis = [StringVar() for _ in rotulos_entrada]

# Variáveis para armazenar os dados inseridos
entrada_produto = entrada_variaveis[0]
entrada_quantidade = entrada_variaveis[1]
entrada_preco = entrada_variaveis[2]
entrada_categoria = entrada_variaveis[3]

for i, rotulo in enumerate(rotulos_entrada):
    Label(frame_entrada, text=rotulo + ":").grid(row=i, column=0, sticky=E, pady=5)
    Entry(frame_entrada, textvariable=entrada_variaveis[i]).grid(row=i, column=1, padx=10, pady=5)

Button(frame_entrada, text="Salvar", command=salvar_e_fechar).grid(row=len(rotulos_entrada), column=0, columnspan=2, pady=10)
Button(frame_entrada, text="Cancelar", command=encerrar_programa).grid(row=len(rotulos_entrada) + 1, column=0, columnspan=2, pady=10)

# Inicializar DataFrame vazio
df = pd.DataFrame()

# Adicionar botão para exibir tabela
Button(root, text="Exibir Tabela", command=exibir_tabela).pack(pady=10)

# Adicionar botão para ver tabelas anteriores
Button(root, text="Ver Tabelas Anteriores", command=ver_tabelas_anteriores).pack(pady=10)

# Adicionar botão para exportar e encerrar
Button(root, text="Exportar e Encerrar", command=exportar_e_encerrar).pack(pady=10)

# Adicionar botão para exportar para Excel
#btn_exportar_excel = Button(root, text="Exportar para Excel", command=lambda: exportar_para_excel(df, 'dados_produtos.xlsx'))
#btn_exportar_excel.pack(padx=10, pady=10)

# Adicionar botão para exportar para PDF
#btn_exportar_pdf = Button(root, text="Exportar para PDF", command=lambda: exportar_para_pdf(df, 'dados_produtos.pdf'))
#btn_exportar_pdf.pack(padx=10, pady=10)


# Adicionar separador
ttk.Separator(root, orient=HORIZONTAL).pack(fill=X, padx=10, pady=10)

# Adicionar seção para realizar vendas e qualificações
frame_vendas_qualificacoes = Frame(root, padx=20, pady=20)
frame_vendas_qualificacoes.pack(padx=10, pady=10)

# Opções para seleção de produtos
if 'Produto' in df.columns:
    produtos_disponiveis = df['Produto'].unique()
else:
    produtos_disponiveis = []

combo_produtos = ttk.Combobox(frame_vendas_qualificacoes, values=produtos_disponiveis)
combo_produtos.grid(row=0, column=0, padx=10, pady=5, sticky=W)
combo_produtos.set('Selecione o Produto')

# Entrada para quantidade na venda
Label(frame_vendas_qualificacoes, text="Quantidade na Venda:").grid(row=1, column=0, padx=10, pady=5, sticky=W)
entry_quantidade_venda = Entry(frame_vendas_qualificacoes)
entry_quantidade_venda.grid(row=1, column=1, padx=10, pady=5, sticky=W)

# Botão para realizar venda
btn_realizar_venda = Button(frame_vendas_qualificacoes, text="Realizar Venda", command=realizar_venda)
btn_realizar_venda.grid(row=2, column=0, columnspan=2, pady=10)

# Adicionar separador
ttk.Separator(root, orient=HORIZONTAL).pack(fill=X, padx=10, pady=10)

# Adicionar seção para qualificar produtos
# Opções para seleção de qualificação
qualificacoes_disponiveis = ['Ótimo', 'Bom', 'Regular', 'Ruim']
combo_qualificacao = ttk.Combobox(frame_vendas_qualificacoes, values=qualificacoes_disponiveis)
combo_qualificacao.grid(row=3, column=0, padx=10, pady=5, sticky=W)
combo_qualificacao.set('Selecione a Qualificação')

# Botão para qualificar produto
btn_qualificar_produto = Button(frame_vendas_qualificacoes, text="Qualificar Produto", command=qualificar_produto)
btn_qualificar_produto.grid(row=4, column=0, columnspan=2, pady=10)

# Adicionar botão para adicionar produto
btn_adicionar_produto = Button(root, text="Adicionar Produto", command=adicionar_produto)
btn_adicionar_produto.pack(side=LEFT, padx=10, pady=10)


# Adicionar botão para remover produto
btn_remover_produto = Button(root, text="Remover Produto", command=remover_produto)
btn_remover_produto.pack(side=LEFT, padx=10, pady=10)


# Adicionar botão para editar produto
btn_editar_produto = Button(root, text="Editar Produto", command=editar_produto)
btn_editar_produto.pack(side=LEFT, padx=10, pady=10)


# Adicionar separador
separador = ttk.Separator(root, orient=HORIZONTAL)
separador.pack(side=LEFT, padx=10, pady=10)


# Adicionar seção para histórico de vendas e qualificações
frame_historico = Frame(root, padx=20, pady=20)
frame_historico.pack(side=LEFT, padx=10, pady=10)

# Botão para exibir histórico de vendas
Button(frame_historico, text="Exibir Histórico de Vendas", command=lambda: exibir_historico(historico_vendas)).grid(row=0, column=0, pady=5, sticky=W)

# Botão para exibir histórico de qualificações
Button(frame_historico, text="Exibir Histórico de Qualificações", command=lambda: exibir_historico(historico_qualificacoes)).grid(row=1, column=0, pady=5, sticky=W)

# Inicializar históricos
historico_vendas = []
historico_qualificacoes = []



root.mainloop()
