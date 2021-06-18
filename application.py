from flask import Flask, make_response, request, render_template, redirect, send_from_directory, jsonify
from py import regras as rg
from py import bd as bd



application = Flask(__name__)



### Partes de login. ###
@application.route("/")
@application.route("/login")
def menu():
    logado = autenticar_login()
    if logado is None:
        return render_template("/login.html", erro = "")
    if logado['tipo']=="admin":
        return redirect('/produtos')
    else:
        return redirect('/produtos')


@application.route("/login", methods = ["POST"])
def login():
    # Extrai os dados do formulário.
    f = request.form
    if "login" not in f or "senha" not in f:
        return ":(", 422
    login = f["login"]
    senha = f["senha"]

    # Faz o processamento.
    logado = bd.db_fazer_login(login, senha)

    # Monta a resposta.
    if logado is None:
        return render_template("login.html", erro = "Algo errado! Verifique os dados digitados.")
    resposta = make_response(redirect("/"))

    # Armazena o login realizado com sucesso em cookies (autenticação).
    resposta.set_cookie("login", login, samesite = "Strict")
    resposta.set_cookie("senha", senha, samesite = "Strict")
    return resposta


@application.route("/logout", methods = ["POST"])
def logout():
    # Monta a resposta.
    resposta = make_response(render_template("login.html", mensagem = "Sessão encerrada. Até logo!"))

    # Limpa os cookies com os dados de login (autenticação).
    resposta.set_cookie("login", "", samesite = "Strict")
    resposta.set_cookie("senha", "", samesite = "Strict")
    return resposta



### Usuarios ###
# Tela de listagem de usuarios.
@application.route("/usuarios")
def listar_usuarios_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    lista = bd.db_listar_usuarios()

    # Monta a resposta.
    return render_template("usuarios.html", logado = logado, usuario = lista, mensagem = '')


@application.route("/cadusuario", methods = ["POST","GET"])
def editar_usuario():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")
    
    
    if request.method == 'POST':
        userid = request.form['userid']
        usuario = bd.db_consultar_usuario(userid)
        
    if request.method == 'GET':
        usuario = {'id_usuario': 'novo', 'nome': '', 'login': '', 'senha': '', 'cpf': '', 'email': '', 'tipo': '', 'telefone': '', 'pix': '', 'banco': '', 'tipo_conta': '', 'agencia': '', 'conta': '', 'cep': '', 'logradouro': '', 'numero': '', 'complemento': '', 'cidade': '', 'uf': ''}


    # Monta a resposta.
    if usuario is None:
        # Faz o processamento.
        lista = bd.db_listar_usuarios()
        return render_template("usuarios.html", logado = logado, produto = lista, mensagem = f"Esse produto não existe."), 404
    return jsonify({'htmlresponse': render_template('form_usuario.html', logado = logado, usuario = usuario)})
    #return render_template("cad_produto.html", logado = logado, produto = produto)


# Tela com o formulário de criação de usuario.
@application.route("/usuarios/novo", methods = ["GET"])
def form_criar_usuario_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    usuario = {'id': 'novo', 'nome': '', 'login': '', 'senha': '', 'tipo': '', 'telefone': ''}

    # Monta a resposta.
    return redirect("#addproduto")
    #return render_template("form_usuario.html", logado = logado, usuario = usuario)
# Tela com o formulário de alteração de usuario existente.
@application.route("/usuarios/<int:id>", methods = ["GET"])
def form_alterar_usuario_api(id):
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    usuario = bd.db_consultar_usuario(id)
    

    # Monta a resposta.
    if usuario is None:
        # Faz o processamento.
        lista = bd.db_listar_usuarios()
        return render_template("usuarios.html", logado = logado, usuarios = lista, mensagem = f"Esse usuario não existe."), 404
    return render_template("form_usuario.html", logado = logado, usuario = usuario)


# Processa o formulário de criação de usuarios. 
@application.route("/usuarios/novo", methods = ["POST"])
def criar_usuario_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Extrai os dados do formulário.
    nome_usuario = request.form["nome_usuario"]
    login = request.form["login"]
    senha = request.form["senha"]
    cpf = request.form["cpf"]
    email = request.form["email"]
    tipo = request.form["tipo"]
    telefone = request.form["telefone"]
    pix = request.form["pix"]
    banco = request.form["banco"]
    tipo_conta = request.form["tipo_conta"]
    agencia = request.form["agencia"]
    conta = request.form["conta"]
    cep = request.form["cep"]
    logradouro = request.form["logradouro"]
    numero = request.form["numero"]
    complemento = request.form["complemento"]
    cidade = request.form["cidade"]
    uf = request.form["uf"]

    # Faz o processamento.
    usuario = rg.criar_usuario(nome_usuario, login, senha, cpf, email, tipo, telefone, pix, banco, tipo_conta, agencia, conta, cep, logradouro, numero, complemento, cidade, uf)

    # Monta a resposta.
    mensagem = f"O usuario {nome_usuario} foi criado com sucesso!."
    # Faz o processamento.
    lista = bd.db_listar_usuarios()
    mensagem = mensagem
    return redirect('/usuarios')

# Processa o formulário de alteração de usuarios.
@application.route("/usuarios/<int:id_usuario>", methods = ["POST"])
def editar_usuario_api(id_usuario):
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Extrai os dados do formulário.
    nome_usuario = request.form["nome_usuario"]
    login = request.form["login"]
    senha = request.form["senha"]
    cpf = request.form["cpf"]
    email = request.form["email"]
    tipo = request.form["tipo"]
    telefone = request.form["telefone"]
    pix = request.form["pix"]
    banco = request.form["banco"]
    tipo_conta = request.form["tipo_conta"]
    agencia = request.form["agencia"]
    conta = request.form["conta"]
    cep = request.form["cep"]
    logradouro = request.form["logradouro"]
    numero = request.form["numero"]
    complemento = request.form["complemento"]
    cidade = request.form["cidade"]
    uf = request.form["uf"]

    # Faz o processamento.
    status, usuario = rg.editar_usuario(id_usuario, nome_usuario, login, senha, cpf, email, tipo, telefone, pix, banco, tipo_conta, agencia, conta, cep, logradouro, numero, complemento, cidade, uf)
    lista = bd.db_listar_usuarios()

    # Monta a resposta.
    if status == 'não existe':
        mensagem = "Esse usuario nem mesmo existia mais."
        return render_template("usuarios.html", logado = logado, usuarios = lista, mensagem = mensagem), 404
    mensagem = f"O usuario {nome_usuario} com o id {id_usuario} foi editado com sucesso."
    lista = bd.db_listar_usuarios()
    return redirect('/usuarios')

# Processa o botão de excluir um usuarios.
@application.route("/usuarios/excluir<int:id_usuario>", methods = ["DELETE"])
def deletar_usuario_api(id_usuario):
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    usuario = rg.apagar_usuario(id_usuario)
    lista = bd.db_listar_usuarios()

    # Monta a resposta.
    if usuario is None:
        return render_template("usuarios.html", logado = logado, usuarios = lista, mensagem = "Esse usuario nem mesmo existia mais."), 404
    mensagem = f"O usuario com o id {id_usuario} foi excluído."
    lista = bd.db_listar_usuarios()
    return redirect('/usuarios')



### Produtos ###
# Lista de Produtos #
@application.route("/produtos")
def listar_produtos_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    lista = bd.db_listar_produtos()

    # Monta a resposta.
    
    return render_template("produtos.html", logado = logado, produto = lista, mensagem = '')


# Tela com o formulário de criação de produto.
@application.route("/produtos/novo", methods = ["GET"])
def form_criar_produto_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    produto = {'id_produto': 'novo', 'nome_produto': '', 'status':'', 'preco_atual': '', 'ingredientes': '', 'prazo_validade':'', 'descricao':''}

    # Monta a resposta.
    #redirect('produtos.html' + '#addprodutos')
    return jsonify({'htmlresponse': render_template('cad_produto.html', logado = logado, produto = produto)})
    #return render_template("produtos.html#addproduto", logado = logado, produto = produto)


# Tela com o formulário de alteração de produto existente.
@application.route("/produtos/<int:id_produto>", methods = ["GET"])
def form_alterar_produto_api(id_produto):
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    produto = bd.db_consultar_produto(id_produto)
    

    # Monta a resposta.
    if produto is None:
        # Faz o processamento.
        lista = bd.db_listar_produtos()
        return render_template("produtos.html", logado = logado, produto = lista, mensagem = f"Esse produto não existe."), 404
    return jsonify({'htmlresponse': render_template('produtoseditar.html', produto = produto)})
    #return render_template("cad_produto.html", logado = logado, produto = produto)


@application.route("/editarproduto", methods = ["POST","GET"])
def editar_produto():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")


    if request.method == 'POST':
        userid = request.form['userid']
        produto = bd.db_consultar_produto(userid)
        
    if request.method == 'GET':
        produto = {'id_produto': 'novo', 'nome_produto': '', 'status':'', 'preco_atual': '', 'prazo_validade':'', 'descricao':''}


    # Monta a resposta.
    if produto is None:
        # Faz o processamento.
        lista = bd.db_listar_produtos()
        return render_template("produtos.html", logado = logado, produto = lista, mensagem = f"Esse produto não existe."), 404
    return jsonify({'htmlresponse': render_template('cad_produto.html', produto = produto)})
    #return render_template("cad_produto.html", logado = logado, produto = produto)


@application.route("/editarprodutoinativo", methods = ["POST","GET"])
def editar_produtoinativo():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")


    if request.method == 'POST':
        userid = request.form['userid']
        produto = bd.db_consultar_produto(userid)
        
    if request.method == 'GET':
        produto = {'id_produto': 'novo', 'nome_produto': '', 'status':'', 'preco_atual': '', 'prazo_validade':'', 'descricao':''}


    # Monta a resposta.
    if produto is None:
        # Faz o processamento.
        lista = bd.db_listar_produtos()
        return render_template("produtosinativos.html", logado = logado, produto = lista, mensagem = f"Esse produto não existe."), 404
    return jsonify({'htmlresponse': render_template('cad_produtoinativo.html', produto = produto)})
    #return render_template("cad_produto.html", logado = logado, produto = produto)


# Processa o formulário de criação de produto.
@application.route("/produtos/novo", methods = ["POST"])
def criar_produto_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Extrai os dados do formulário.
    nome_produto = request.form["nome_produto"]
    status = request.form["status"]
    preco_atual = request.form["preco_atual"]
    prazo_validade = request.form["prazo_validade"]
    descricao = request.form["descricao"]

    # Faz o processamento.
    produto = rg.criar_produto(nome_produto, status, preco_atual, prazo_validade, descricao)

    # Monta a resposta.
    mensagem = f"O Produto {nome_produto} foi criado com o id {produto['id_produto']}."
    lista = bd.db_listar_produtos()
    return render_template("produtos.html", logado = logado, produto = lista, mensagem = mensagem)


# Processa o formulário de alteração de produto.
@application.route("/produtos/<int:id_produto>", methods = ["POST"])
def editar_produto_api(id_produto):
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Extrai os dados do formulário.
    nome_produto = request.form["nome_produto"]
    status = request.form["status"]
    preco_atual = request.form["preco_atual"]
    prazo_validade = request.form["prazo_validade"] 
    descricao = request.form["descricao"]


    # Faz o processamento.
    lista = bd.db_listar_produtos()
    status, produto = rg.editar_produto(id_produto, nome_produto, status, preco_atual, prazo_validade, descricao)
    

    # Monta a resposta.
    if status == 'não existe':
        mensagem = "Esse produto nem mesmo existia mais."
        return render_template("produtos.html", logado = logado, produtos = lista, mensagem = mensagem), 404
    
    mensagem = f"O produto {nome_produto} com o id {id_produto} foi editado com sucesso."
    #return render_template("produtos.html", logado = logado, produto = lista, mensagem = mensagem)
    #return jsonify({'htmlresponse': render_template('produtos.html', logado = logado, produto = produto, mensagem = mensagem)})
    return redirect("/produtos")
    #return render_template("produtos.html", logado = logado, produto = lista, mensagem = mensagem)

# Processa o formulário de alteração de produto.
@application.route("/produtos/inativos/<int:id_produto>", methods = ["POST"])
def editar_produtoinativo_api(id_produto):
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Extrai os dados do formulário.
    nome_produto = request.form["nome_produto"]
    status = request.form["status"]
    preco_atual = request.form["preco_atual"]
    prazo_validade = request.form["prazo_validade"] 
    descricao = request.form["descricao"]


    # Faz o processamento.
    lista = bd.db_listar_produtos()
    status, produto = rg.editar_produto(id_produto, nome_produto, status, preco_atual, prazo_validade, descricao)
    

    # Monta a resposta.
    if status == 'não existe':
        mensagem = "Esse produto nem mesmo existia mais."
        return render_template("produtos.html", logado = logado, produtos = lista, mensagem = mensagem), 404
    
    mensagem = f"O produto {nome_produto} com o id {id_produto} foi editado com sucesso."
    #return render_template("produtos.html", logado = logado, produto = lista, mensagem = mensagem)
    #return jsonify({'htmlresponse': render_template('produtos.html', logado = logado, produto = produto, mensagem = mensagem)})
    return redirect('/produtos/inativos')
    #return render_template("produtos.html", logado = logado, produto = lista, mensagem = mensagem)

# Lista de Produtos Inativos #
@application.route("/produtos/inativos")
def listar_produtosinativos_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    lista = bd.db_listar_produtosinativos()

    # Monta a resposta.
    return render_template("produtosinativos.html", logado = logado, produto = lista, mensagem = '')




### vendas ###
# Lista de vendas #
@application.route("/vendas")
def listar_vendas_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    lista = bd.db_listar_vendas()

    # Monta a resposta.
    
    return render_template("vendas.html", logado = logado, vendas = lista)


# Tela com o formulário de criação de vendas.
@application.route("/vendas/novo", methods = ["GET"])
def form_criar_vendas_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    produto = {'id_produto': 'novo', 'nome': '', 'status':'', 'preco_atual': '', 'ingredientes': '', 'prazo_validade':'', 'descricao':''}

    # Monta a resposta.
    #redirect('produtos.html' + '#addprodutos')
    return jsonify({'htmlresponse': render_template('cad_produto.html', logado = logado, produto = produto)})
    #return render_template("produtos.html#addproduto", logado = logado, produto = produto)


# Tela com o formulário de alteração de vendas existente.
@application.route("/vendas/<int:id_vendas>", methods = ["GET"])
def form_alterar_vendas_api(id_produto):
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    produto = bd.db_consultar_produto(id_produto)
    

    # Monta a resposta.
    if produto is None:
        # Faz o processamento.
        lista = bd.db_listar_produtos()
        return render_template("produtos.html", logado = logado, produto = lista, mensagem = f"Esse produto não existe."), 404
    return jsonify({'htmlresponse': render_template('produtoseditar.html', produto = produto)})
    #return render_template("cad_produto.html", logado = logado, produto = produto)


@application.route("/editarvendas", methods = ["POST","GET"])
def editar_vendas():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")


    if request.method == 'POST':
        userid = request.form['userid']
        vendas = bd.db_consultar_vendas(userid)
        
    if request.method == 'GET':
        vendas = {'id_vendas': 'novo', 'data_venda': '', 'canal_venda':'', 'desconto_venda': ''}
        produto = bd.db_listar_produtos()


    # Monta a resposta.
    if vendas is None:
        # Faz o processamento.
        lista = bd.db_listar_vendas()
        return render_template("vendas.html", logado = logado, produto = lista, mensagem = f"Esse produto não existe."), 404
    return jsonify({'htmlresponse': render_template('cad_vendas.html', vendas = vendas, produto = produto)})
    





### insumo ###
@application.route("/insumo")
def listar_insumo_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    lista = bd.db_listar_insumo()

    # Monta a resposta.
    return render_template("insumo.html", logado = logado, insumo = lista)


@application.route("/cadinsumo", methods = ["POST","GET"])
def editar_insumo():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")


    if request.method == 'POST':
        userid = request.form['userid']
        insumo = bd.db_consultar_insumo(userid)
        
    if request.method == 'GET':
        insumo = {'id_insumo': 'novo', 'nome_insumo': '', 'unidade_medida': ''}
        


    # Monta a resposta.
    if insumo is None:
        # Faz o processamento.
        insumo = bd.db_listar_insumo()
        return render_template("insumo.html", logado = logado, insumo = insumo, mensagem = f"Esse produto não existe."), 404
    return jsonify({'htmlresponse': render_template('cad_insumo.html', insumo = insumo)})







# Tela com o formulário de alteração de insumo existente.
@application.route("/insumo/<int:id_insumo>", methods = ["GET"])
def form_alterar_insumo_api(id_insumo):
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    insumo = bd.db_consultar_insumo(id_insumo)
    

    # Monta a resposta.
    if insumo is None:
        return render_template("insumo.html", logado = logado, mensagem = f"Esse insumo não existe."), 404
    return render_template("cad_insumo.html", logado = logado, insumo = insumo)


# Processa o formulário de criação de insumo. 
@application.route("/insumo/novo", methods = ["POST"])
def criar_insumo_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Extrai os dados do formulário.
    nome_insumo = request.form["nome_insumo"]
    unidade_medida = request.form["unidade_medida"]

    # Faz o processamento.
    insumo = rg.criar_insumo(nome_insumo, unidade_medida)

    # Monta a resposta.
    mensagem = f"O Insumo foi criado com o id."
    insumo = bd.db_listar_insumo()
    
    return redirect('/insumo')
    #redirect('/insumo')


# Processa o formulário de alteração de insumo.
@application.route("/insumo/<int:id_insumo>", methods = ["POST"])
def editar_insumo_api(id_insumo):
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Extrai os dados do formulário.
    nome_insumo = request.form["nome_insumo"]
    unidade_medida = request.form["unidade_medida"]

    # Faz o processamento.
    lista = bd.db_listar_insumo()
    # Faz o processamento.
    status, insumo = rg.editar_insumo(id_insumo, nome_insumo, unidade_medida)

    # Monta a resposta.
    if status == 'não existe':
        mensagem = "Esse insumo nem mesmo existia mais."
        return render_template("insumo.html", logado = logado, mensagem = mensagem), 404
    mensagem = f"O insumo {nome_insumo} com o id {id_insumo} foi editado."
    lista = bd.db_listar_insumo()
    return redirect('/insumo')
    #return render_template("insumo.html", logado = logado, insumo = lista, mensagem = mensagem)


### insumos inativos###
@application.route("/insumo/inativos")
def listar_insumoinativos_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    lista = bd.db_listar_insumoinativos()

    # Monta a resposta.
    return render_template("insumoinativos.html", logado = logado, insumo = lista)



### compra ###
@application.route("/insumo/compra")
def listar_compra_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    lista = bd.db_listar_compra()

    # Monta a resposta.
    return render_template("compra.html", logado = logado, compra = lista, mensagem = '')


@application.route("/cadcompra", methods = ["POST","GET"])
def editar_compra():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")


    if request.method == 'POST':
        userid = request.form['userid']
        compra = bd.db_consultar_compra(userid)
        
    if request.method == 'GET':
        compra = {'id_compra': 'novo', 'data_compra': '', 'valor_compra': ''}

    insumo = bd.db_listar_insumo()
    itemcompra = bd.db_listar_itemcompra()
    # Monta a resposta.
    if compra is None:
        # Faz o processamento.
        compra = bd.db_listar_compra()
        return render_template("compra.html", logado = logado, compra = compra, mensagem = f"Esse produto não existe."), 404
    return jsonify({'htmlresponse': render_template('cad_compra.html', logado = logado, compra = compra, insumo = insumo, itemcompra = itemcompra)})




# Tela com o formulário de criação de compra.
@application.route("/insumo/compra/novo", methods = ["GET"])
def form_criar_compra_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
  
    compra = {'id_compra': 'novo', 'data_compra': '', 'preco_compra': ''}

    # Monta a resposta.
    return render_template("cad_compra.html", logado = logado, compra = compra)


# Tela com o formulário de alteração de compra existente.
@application.route("/insumo/compra/<int:id_compra>", methods = ["GET"])
def form_alterar_compra_api(id_compra):
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    compra = bd.db_consultar_compra(id_compra)
    

    # Monta a resposta.
    if compra is None:
        return render_template("compra.html", logado = logado, mensagem = f"Esse insumo não existe."), 404
    return render_template("cad_compra.html", logado = logado, compra = compra)


# Processa o formulário de alteração de compra.

@application.route("/insumo/compra/novo", methods = ["POST"])
def criar_compra_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Extrai os dados do formulário.
    data_compra = request.form["data_compra"]
    valor_compra = request.form["valor_compra"]
    id_insumo = request.form["id_insumo"]
    quantidade = request.form["quantidade"]
    data_vencimento = request.form["data_vencimento"]
    valor_unitario = request.form["valor_unitario"]

    # Faz o processamento.
    compra = rg.criar_compra(data_compra, valor_compra)
    itemcompra = rg.criar_itemcompra(compra['id_compra'], id_insumo, quantidade, data_vencimento, valor_unitario)
    addinsumo = rg.editar_addinsumo(itemcompra['id_insumo'], itemcompra['quantidade'])
    # Monta a resposta.
    mensagem = f"O aluno  foi criado com o id ."
    return redirect('/insumo/compra')

### itemcompra ###
@application.route("/insumo/compra/item<int:id_compra>",  methods = ["POST"])
def listar_itemcompra_api(id_compra):
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    compra = bd.db_consultar_compra(id_compra)
    itemcompra = bd.db_listar_item()

    # Monta a resposta.
    return render_template("item_compra.html", logado = logado, compra = compra, itemcompra = itemcompra)


# Tela com o formulário de criação de item.
@application.route("/insumo/compra/item<int:id_compra>/novo", methods = ["GET"])
def form_criar_item_api(id_compra):
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
  
    item = {'id_item': 'novo', 'id_compra': '', 'id_insumo': '', 'data_vencimento': '', 'quantidade_insumo': '', 'unidade_medida': '', 'preco_insumo': ''}
    insumo = bd.db_listar_insumo()

    # Monta a resposta.
    return render_template("cad_itemcompra.html", logado = logado, item = item, insumo = insumo)



### estoque ###
@application.route("/estoque")
def listar_estoque_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    lista = bd.db_listar_estoque()

    # Monta a resposta.
    return render_template("estoque.html", logado = logado, produto = lista)



#Fabricação#
@application.route("/fabricacao")
def listar_fabricacao_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    lista = bd.db_listar_fabricacao()

    # Monta a resposta.
    return render_template("fabricacao.html", logado = logado, fabricacao = lista)



@application.route("/cadfabricacao", methods = ["POST","GET"])
def editar_fabricacao():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")


    if request.method == 'POST':
        userid = request.form['userid']
        fabricacao = bd.db_consultar_fabricacao(userid)
        
    if request.method == 'GET':
        fabricacao = {'id_fabricacao': 'novo', 'data_fabricacao': ''}
        produto = bd.db_listar_produtos()
        

    # Monta a resposta.
    if fabricacao is None:
        # Faz o processamento.
        fabricacao = bd.db_listar_fabricacao()
        return render_template("fabricacao.html", logado = logado, fabricacao = fabricacao, mensagem = f"Esse produto não existe."), 404
    return jsonify({'htmlresponse': render_template('cad_fabricacao.html', logado = logado, fabricacao = fabricacao, produto = produto)})



# Tela com o formulário de criação de fabricação.
@application.route("/estoque/novafabricacao", methods = ["GET"])
def form_criar_fabricacao_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    fabricacao = {'id_produto': 'novo', 'data_fabricacao': ''}

    # Monta a resposta.
    return render_template("cad_fabricacao.html", logado = logado, fabricacao = fabricacao)


# Tela com o formulário de alteração de fabricacao existente.


# Processa o formulário de criação de fabricacao.
@application.route("/fabricacao/novo", methods = ["POST"])
def criar_fabricacao_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Extrai os dados do formulário.
    data_fabricacao = request.form["data_fabricacao"]
    produto = request.form["produto"]
    quantidade = request.form["quantidade"]



    # Faz o processamento.
    fabricacao = rg.criar_fabricacao(data_fabricacao)
    itemfabricacao = rg.criar_itemfabricacao(fabricacao['id_fabricacao'], produto, quatidade)
    addproduto = rg.editar_addproduto(itemfabricacao[id_produto], itemfabricacao['quantidade'])
    # Monta a resposta.
    mensagem = f"O usuario  foi criado com o id {fabricacao['id_fabricacao']}."
    fabricacao = bd.db_listar_fabricacao()
    return redirect('/fabricacao')


# Processa o formulário de alteração de fabricacao.


# Tela com o formulário de criação de novo item de fabricação.
@application.route("/fabricação/novo", methods = ["GET"])
def form_criar_itemfabricacao_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    itemfabricacao = {'id_item': 'novo', 'id_fabricacao': '', 'id_produto': '', 'quantidade': '', 'prazo_vencimento': ''}

    # Monta a resposta.
    return render_template("cad_itemfabricacao.html", logado = logado, itemfabricacao = itemfabricacao)



### caixa ###
@application.route("/caixa")
def listar_entradas_api():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")

    # Faz o processamento.
    lista = bd.db_listar_saldo()
    lista1 = bd.db_listar_entradas()
    lista2 = bd.db_listar_saidas()

    # Monta a resposta.
    return render_template("caixa.html", logado = logado, saldo = lista, entradas = lista1, saidas = lista2)



## Dasboard ####
@application.route("/dashmaster")
def dashmaster():
    # Autenticação.
    logado = autenticar_login()
    if logado is None:
        return redirect("/")
    if logado['tipo']=="admin":
        return render_template("dashmaster.html", logado = logado, mensagem = "")
    else:
        return render_template("dashvendedor.html", logado = logado, mensagem = "")  



###############################################
#### Coisas internas da controller da API. ####
###############################################
def autenticar_login():
    login = request.cookies.get("login", "")
    senha = request.cookies.get("senha", "")
    return bd.db_fazer_login(login, senha)



########################
#### Inicialização. ####
########################

#if __name__ == "__main__":
#    port = int(os.environ.get("PORT", 5000))
#    app.run(host='0.0.0.0', port=port)



if __name__ == "__main__":
    application.run(debug=True)