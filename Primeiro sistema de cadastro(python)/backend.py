import os
from datetime import datetime

#arquivos txt
arquivo_produto = "dados/produtos.txt"
arquivo_cadastro = "dados/cadastros.txt"

#leitura dos arquivo produto
def ler_produtos(): 
    produtos = []
    try:
        with open(arquivo_produto, 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    partes = [p.strip() for p in linha.split(',')]
                    produtos.append(partes)
    except FileNotFoundError:
        pass
    return produtos

def ler_responsavel(): 
    cadastro = []
    try:
        with open(arquivo_cadastro, 'r', encoding='utf-8') as c:
            for linha in c:
                linha = linha.strip()
                if linha:
                    partes = [p.strip() for p in linha.split(',')]
                    if len(partes) == 5:
                        id_hist = partes[0]
                        funcionario = partes[1]
                        produto = partes[2]
                        data = partes[3]
                        id_produto = partes[4]
                        cadastro.append((id_hist,funcionario, produto, data, id_produto))
                    
    except FileNotFoundError:
        pass
    return cadastro

#gereção de novos ids
def gerar_novo_id_produto(): #id produto
    try:
        with open(arquivo_produto, "r", encoding="utf-8") as f:
            linhas = [l.strip() for l in f if l.strip()]
        if linhas:
            ids = [int(l.split(",")[0]) for l in linhas]
            return max(ids) + 1
    except FileNotFoundError:
        pass
    return 1
def gerar_novo_id_cadastro(): #id cadastro
    try:
        with open(arquivo_cadastro, "r", encoding="utf-8") as f:
            linhas = [l.strip() for l in f if l.strip()]
        if linhas:
            ids = [int(l.split(",")[0]) for l in linhas]
            return max(ids) + 1
    except FileNotFoundError:
        pass
    return 1

#função salvar produto
def salvar_produto_backend(nome, marca, quantidade, preco, tipo, funcionario, data):
    novo_id = gerar_novo_id_produto()
    novo_id_cad = gerar_novo_id_cadastro()
    linha_produto = f"{novo_id}, {nome}, {marca}, {quantidade}, {preco}, {tipo}\n" #criando linha produto
    linha_cadastro = f"{novo_id_cad}, {funcionario}, {nome}, {data}, {novo_id}\n" #criando linha cadastro
    with open(arquivo_produto, "a", encoding="utf-8") as f: #salvando no arquivo de produtos
        f.write(linha_produto)
    with open(arquivo_cadastro, "a", encoding="utf-8") as c: # salva no arquivo de cadastros
        c.write(linha_cadastro)
    return True

#funçao excluir produto
def excluir_produto(id_produto):
    try:
        id_produto=int(id_produto) #convertendo o id para inteiro
    except ValueError:
        return False
    try:
        with open('dados/produtos.txt', 'r', encoding= 'utf-8') as f:
            linhas= f.readlines() #lendo todas as linhas do arquivo txt
        linhas_filtradas= [linha for linha in linhas if int(linha.split(',')[0].strip()) !=id_produto] #filtrando as linhas e mantendo as que não tem o id informado
        if len(linhas_filtradas) == len(linhas):
            return False 
        with open('dados/produtos.txt','w', encoding='utf-8') as f: #reescreve o arquivo sem o produto
            f.writelines(linhas_filtradas)
        return True
    except FileNotFoundError:
        return False
    
    #funçao editar produto
def editar_produto(id_produto,nome,marca,quantidade,preco,tipo):
    try:
        id_produto= int(id_produto)
    except:
        return False
    try:
        with open(arquivo_produto, 'r', encoding= 'utf-8') as f:
            linhas= f.readlines()
        novas_linhas= []
        encontrado = False
        for linha in linhas:
            partes= [p.strip() for p in linha.split(',')]    
            if int(partes[0]) == id_produto:
                nova_linha= f'{id_produto}, {nome}, {marca}, {quantidade}, {preco}, {tipo}\n'
                novas_linhas.append(nova_linha)
                encontrado = True
            else:
                novas_linhas.append(linha)

        if not encontrado:
            return False
        with open (arquivo_produto, 'w', encoding= 'utf-8') as f:
            f.writelines(novas_linhas)
        return True
    except:
        return False
    
