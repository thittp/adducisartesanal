from contextlib import closing
import mysql.connector

###############################################
#### Funções auxiliares de banco de dados. ####
###############################################

# Converte uma linha em um dicionário.
def row_to_dict(description, row):
    if row is None: return None
    d = {}
    for i in range(0, len(row)):
        d[description[i][0]] = row[i]
    return d

# Converte uma lista de linhas em um lista de dicionários.
def rows_to_dict(description, rows):
    result = []
    for row in rows:
        result.append(row_to_dict(description, row))
    return result

####################################
#### Definições básicas de BD. ####
####################################
### Partes de login. ###
#def conectar():
#    return mysql.connector.connect(host="adducis.ch3noq1jgsa1.us-east-2.rds.amazonaws.com",user="adducis",password= "654artesanais",database="Usuarios")


def conectar():
    return mysql.connector.connect(host="localhost",user="root",password= "692107Thi",database="adducisartesanal")

def db_fazer_login(login, senha):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT * FROM usuario WHERE login = %s AND senha = %s;", (login, senha))
        return row_to_dict(cur.description, cur.fetchone())


def db_consultar_usuario(id_usuario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT * FROM usuario WHERE id_usuario = (%s)", [id_usuario])
        return row_to_dict(cur.description, cur.fetchone())


### Cadastro de usuarios. ###
def db_listar_usuarios():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT * FROM usuario")
        return rows_to_dict(cur.description, cur.fetchall())


def db_criar_usuario(nome_usuario, login, senha, cpf, email, tipo, telefone, pix, banco, tipo_conta, agencia, conta, cep, logradouro, numero, complemento, cidade, uf):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO usuario (nome_usuario, login, senha, cpf, email, tipo, telefone, pix, banco, tipo_conta, agencia, conta, cep, logradouro, numero, complemento, cidade, uf) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [nome_usuario, login, senha, cpf, email, tipo, telefone, pix, banco, tipo_conta, agencia, conta, cep, logradouro, numero, complemento, cidade, uf])
        id_usuario = cur.lastrowid
        con.commit()
        return {'id_usuario': id_usuario, 'nome_usuario': nome_usuario, 'login': login, 'senha': senha, 'cpf': cpf, 'email': email, 'tipo': tipo, 'telefone': telefone, 'pix': pix, 'banco':banco, 'tipo_conta': tipo_conta, 'agencia': agencia, 'conta': conta, 'cep': cep, 'logradouro': logradouro, 'numero': numero, 'complemento': complemento, 'cidade': cidade, 'uf': uf}

def db_editar_usuario(id_usuario, nome_usuario, login, senha, cpf, email, tipo, telefone, pix, banco, tipo_conta, agencia, conta, cep, logradouro, numero, complemento, cidade, uf):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE usuario SET nome_usuario = %s, login = %s, senha = %s, cpf = %s, email = %s, tipo = %s, telefone = %s, pix = %s, banco = %s, tipo_conta = %s, agencia = %s, conta = %s, cep = %s, logradouro = %s, numero = %s, complemento = %s, cidade = %s, uf = %s WHERE id_usuario = %s", [nome_usuario, login, senha, cpf, email, tipo, telefone, pix, banco, tipo_conta, agencia, conta, cep, logradouro, numero, complemento, cidade, uf, id_usuario])
        con.commit()
        return {'id_usuario': id_usuario, 'nome_usuario': nome_usuario, 'login': login, 'senha': senha, 'cpf': cpf, 'email': email, 'tipo': tipo, 'telefone': telefone, 'pix': pix, 'banco': banco, 'tipo_conta': tipo_conta, 'agencia': agencia, 'conta': conta, 'cep': cep,  'logradouro': logradouro, 'numero': numero, 'complemento': complemento, 'cidade': cidade, 'uf': uf}


def db_deletar_usuario(id_usuario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("DELETE FROM usuario WHERE id_usuario = %s", [id_usuario])
        con.commit()



### produtos ###
def db_listar_produtos():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT * FROM produto WHERE status = 'A'")
        return rows_to_dict(cur.description, cur.fetchall())


def db_criar_produto(nome_produto, status, preco_atual, prazo_validade, descricao):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO produto (nome_produto, status, preco_atual, prazo_validade, descricao) VALUES (%s, %s, %s, %s, %s)", [nome_produto, status, preco_atual, prazo_validade, descricao])
        id_produto = cur.lastrowid
        con.commit()
        return {'id_produto': id_produto, 'nome_produto': nome_produto, 'status': status, 'preco_atual': preco_atual, 'prazo_validade': prazo_validade, 'descricao': descricao}


def db_consultar_produto(id_produto):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT * FROM produto WHERE id_produto = (%s)", [id_produto])
        return row_to_dict(cur.description, cur.fetchone())


def db_editar_produto(id_produto, nome_produto, status, preco_atual, prazo_validade, descricao):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE produto SET nome_produto = %s, status = %s, preco_atual = %s, prazo_validade = %s, descricao = %s WHERE id_produto = %s", [nome_produto, status, preco_atual, prazo_validade, descricao, id_produto])
        con.commit()
        return {'id_produto': id_produto, 'nome_produto': nome_produto, 'status': status, 'preco_atual':preco_atual, 'prazo_validade':prazo_validade, 'descricao':descricao}


def db_listar_produtosinativos():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT * FROM produto WHERE status = 'I'")
        return rows_to_dict(cur.description, cur.fetchall())



### vendas ###
def db_listar_vendas():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT * FROM venda")
        return rows_to_dict(cur.description, cur.fetchall())

def db_consultar_vendas(id_venda):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT * FROM venda WHERE id_venda = (%s)", [id_venda])
        return row_to_dict(cur.description, cur.fetchone())




### insumo ###
def db_listar_insumo():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT * FROM insumo")
        return rows_to_dict(cur.description, cur.fetchall())


def db_criar_insumo(nome_insumo, unidade_medida):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO insumo (nome_insumo, unidade_medida) VALUES (%s, %s)", [nome_insumo, unidade_medida])
        id_insumo = cur.lastrowid
        con.commit()
        return {'id_insumo': id_insumo, 'nome_insumo': nome_insumo, 'unidade_medida': unidade_medida}


def db_editar_insumo(id_insumo, nome_insumo, unidade_medida):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE insumo SET nome_insumo = %s, unidade_medida = %s WHERE id_insumo = %s", [nome_insumo, unidade_medida, id_insumo])
        con.commit()
        return {'id_insumo': id_insumo, 'nome_insumo': nome_insumo, 'unidade_medida': unidade_medida}

def db_editar_addinsumo(id_insumo, quantidade):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE insumo SET quantidade = quantidade + %s WHERE id_insumo = %s", [quantidade, id_insumo])
        con.commit()
        return {'id_insumo': id_insumo, 'quantidade': quantidade}



def db_consultar_insumo(id_insumo):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT * FROM insumo WHERE id_insumo = (%s)", [id_insumo])
        return row_to_dict(cur.description, cur.fetchone())





### compra ###
def db_listar_compra():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT * FROM compra")
        return rows_to_dict(cur.description, cur.fetchall())


def db_criar_compra(data_compra, valor_compra):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO compra (data_compra, valor_compra) VALUES (%s, %s)", [data_compra, valor_compra])
        id_compra = cur.lastrowid
        con.commit()
        return {'id_compra': id_compra, 'data_compra': data_compra, 'valor_compra': valor_compra}


def db_consultar_compra(id_compra):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT * FROM compra WHERE id_compra = (%s)", [id_compra])
        return row_to_dict(cur.description, cur.fetchone())


def db_editar_compra(id_compra, data_compra, valor_compra):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE compra SET data_compra = %s, valor_compra = %s WHERE id_compra = %s", [data_compra, valor_compra, id_compra])
        con.commit()
        return {'id_compra': id_compra, 'data_compra': data_compra, 'valor_compra': valor_compra}



### itemcompra ###
def db_listar_itemcompra():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT * FROM itemcompra")
        return rows_to_dict(cur.description, cur.fetchall())

def db_criar_itemcompra(id_compra, id_insumo, quantidade, data_vencimento, valor_unitario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO itemcompra (id_compra, id_insumo, quantidade, data_vencimento, valor_unitario) VALUES (%s, %s, %s, %s, %s)", [id_compra, id_insumo, quantidade, data_vencimento, valor_unitario])
        id_item = cur.lastrowid
        con.commit()
        return {'id_item': id_item, 'id_compra': id_compra, 'id_insumo': id_insumo, 'quantidade': quantidade, 'data_vencimento': data_vencimento, 'valor_unitario': valor_unitario}





### estoque ###
def db_listar_estoque():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT P.id_produto, P.nome, sum(F.quantidade) - sum(V.quantidade) AS quantidade FROM produto as P LEFT JOIN itemfabricacao AS F ON P.id_produto = F.id_produto LEFT JOIN itensvendas AS V ON P.id_produto = V.id_produto GROUP BY P.id_produto")
        return rows_to_dict(cur.description, cur.fetchall())



### fabricacao ###
def db_listar_fabricacao():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT * FROM fabricacao")
        return rows_to_dict(cur.description, cur.fetchall())


def db_criar_fabricacao(data_fabricacao):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO fabricacao (data_fabricacao) VALUES (%s)", [data_fabricacao])
        id_fabricacao = cur.lastrowid
        con.commit()
        return {'id_fabricacao': id_fabricacao, 'data_fabricacao': data_fabricacao}


def db_consultar_fabricacao(id_fabricacao):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT * FROM fabricacao WHERE id_fabricacao = (%s)", [id_fabricacao])
        return row_to_dict(cur.description, cur.fetchone())


def db_editar_fabricacao(id_fabricacao, data_fabricacao):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE fabricacao SET data_fabricacao = %s WHERE id_fabricacao = %s", [data_fabricacao, id_fabricacao])
        con.commit()
        return {'id_fabricacao': id_fabricacao, 'data_fabricacao': data_fabricacao}



### itemfabricacao ###
def db_listar_itemfabricacao():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT * FROM itemfabricacao")
        return rows_to_dict(cur.description, cur.fetchall())

def db_criar_itemfabricacao(id_fabricacao, id_insumo, quantidade, data_vencimento, valor_unitario):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO itemfabricacao (id_fabricacao, id_insumo, quantidade, data_vencimento, valor_unitario) VALUES (%s, %s, %s, %s, %s)", [id_fabricacao, id_insumo, quantidade, data_vencimento, valor_unitario])
        id_item = cur.lastrowid
        con.commit()
        return {'id_item': id_item, 'id_fabricacao': id_fabricacao, 'id_insumo': id_insumo, 'quantidade': quantidade, 'data_vencimento': data_vencimento, 'valor_unitario': valor_unitario}





def db_editar_addproduto(id_produto, quantidade):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("UPDATE produto SET quantidade = quantidade + %s WHERE id_produto = %s", [quantidade, id_produto])
        con.commit()
        return {'id_produto': id_produto, 'quantidade': quantidade}

### Caixa ###
def db_listar_saldo():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT date_format(X.data_registro, '%d/%m/%Y') as 'Data', format(coalesce(sum(X.valor_entrada),0)-(coalesce(sum(X.valor_saida),0)), 2) as ValorDia FROM caixa as X GROUP BY X.data_registro")
        return rows_to_dict(cur.description, cur.fetchall())


def db_listar_entradas():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT date_format(V.data_venda, '%d/%m/%Y') as 'Data', CONCAT('R$ ', Replace(FORMAT(sum(V.preco_venda), 2), '.', ',')) AS Valor FROM venda as V GROUP BY V.data_venda")
        return rows_to_dict(cur.description, cur.fetchall())


def db_listar_saidas():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT date_format(C.data_compra, '%d/%m/%Y') as 'Data', CONCAT('R$ ', Replace(FORMAT(sum(C.valor_compra), 2), '.', ',')) AS Valor FROM compra as C GROUP BY C.data_compra")
        return rows_to_dict(cur.description, cur.fetchall())
