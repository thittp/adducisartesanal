from py import bd as bd


##########################################
#### Definições de regras de negócio. ####
##########################################

def criar_usuario(nome_usuario, login, senha, cpf, email, tipo, telefone, pix, banco, tipo_conta, agencia, conta, cep, logradouro, numero, complemento, cidade, uf):
    return bd.db_criar_usuario(nome_usuario, login, senha, cpf, email, tipo, telefone, pix, banco, tipo_conta, agencia, conta, cep, logradouro, numero, complemento, cidade, uf)


def editar_usuario(id_usuario, nome_usuario, login, senha, cpf, email, tipo, telefone, pix, banco, tipo_conta, agencia, conta, cep, logradouro, numero, complemento, cidade, uf):
    usuario = bd.db_consultar_usuario(id_usuario)
    if usuario is None:
        return 'não existe', None
    bd.db_editar_usuario(id_usuario, nome_usuario, login, senha, cpf, email, tipo, telefone, pix, banco, tipo_conta, agencia, conta, cep, logradouro, numero, complemento, cidade, uf)
    return 'alterado', usuario


def apagar_usuario(id_usuario):
    usuario = bd.db_consultar_usuario(id_usuario)
    if usuario is not None: bd.db_deletar_usuario(id_usuario)
    return usuario


# produto
def criar_produto(nome_produto, status, preco_atual, prazo_validade, descricao):
    return bd.db_criar_produto(nome_produto, status, preco_atual, prazo_validade, descricao)


def editar_produto(id_produto, nome_produto, status, preco_atual, prazo_validade, descricao):
    produto = bd.db_consultar_produto(id_produto)
    if produto is None:
        return 'não existe', None
    bd.db_editar_produto(id_produto, nome_produto, status, preco_atual, prazo_validade, descricao)
    return 'alterado', produto



# insumo
def criar_insumo(nome_insumo, unidade_medida):
    return bd.db_criar_insumo(nome_insumo, unidade_medida)


def editar_insumo(id_insumo, nome_insumo, unidade_medida):
    insumo = bd.db_consultar_insumo(id_insumo)
    if insumo is None:
        return 'não existe', None
    bd.db_editar_insumo(id_insumo, nome_insumo, unidade_medida)
    return 'alterado', insumo


def editar_addinsumo(id_insumo, quantidade):
    insumo = bd.db_consultar_insumo(id_insumo)
    if insumo is None:
        return 'não existe', None
    bd.db_editar_addinsumo(id_insumo, quantidade)
    return 'alterado', insumo


### compra ###
def criar_compra(data_compra, valor_compra):
    return bd.db_criar_compra(data_compra, valor_compra)


def editar_compra(id_compra, data_compra, valor_compra):
    compra = bd.db_consultar_compra(id_compra)
    if compra is None:
        return 'não existe', None
    bd.db_editar_compra(id_compra, data_compra, valor_compra)
    return 'alterado', compra

def criar_itemcompra(id_compra, id_insumo, quantidade, data_vencimento, valor_unitario):
    return bd.db_criar_itemcompra(id_compra, id_insumo, quantidade, data_vencimento, valor_unitario)


def item_compra(id_compra, data_compra):
    compra = bd.db_consultar_compra(id_compra)
    if compra is None:
        return 'não existe', None
    return 'alterado', compra


### fabricacao ###
def criar_fabricacao(data_fabricacao):
    return bd.db_criar_fabricacao(data_fabricacao)


def editar_fabricacao(id_fabricacao, data_fabricacao):
    fabricacao = bd.db_consultar_fabricacao(id_fabricacao)
    if fabricacao is None:
        return 'não existe', None
    bd.db_editar_fabricacao(id_fabricacao, data_fabricacao)
    return 'alterado', fabricacao

def criar_itemfabricacao(id_fabricacao, id_insumo, quantidade, data_vencimento, valor_unitario):
    return bd.db_criar_itemfabricacao(id_fabricacao, id_insumo, quantidade, data_vencimento, valor_unitario)


def editar_addproduto(id_produto, quantidade):
    produto = bd.db_consultar_produto(id_produto)
    if produto is None:
        return 'não existe', None
    bd.db_editar_addproduto(id_produto, quantidade)
    return 'alterado', produto


