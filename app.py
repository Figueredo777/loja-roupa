from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = "chave_secreta"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///loja.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    imagem = db.Column(db.String(100), nullable=True)
    categoria = db.Column(db.String(50), nullable=True)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    destaques = Produto.query.filter_by(categoria="inicio").all()
    return render_template("index.html", destaques=destaques)

@app.route("/masculino")
def masculino():
    produtos = Produto.query.filter_by(categoria="masculino").all()
    return render_template("masculino.html", produtos=produtos)

@app.route("/feminino")
def feminino():
    produtos = Produto.query.filter_by(categoria="feminino").all()
    return render_template("feminino.html", produtos=produtos)

@app.route("/contato")
def contato():
    return render_template("contato.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        usuario = Usuario.query.filter_by(email=email, senha=senha).first()

        if usuario:
            session["usuario_nome"] = usuario.nome
            return redirect(url_for("index"))
        else:
            return render_template("login.html", erro="E-mail ou senha incorretos.")

    return render_template("login.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        existente = Usuario.query.filter_by(email=email).first()
        if existente:
            return render_template("cadastro.html", erro="Este e-mail já está cadastrado.")

        novo = Usuario(nome=nome, email=email, senha=senha)
        db.session.add(novo)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("cadastro.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/carrinho")
def carrinho():
    if "carrinho" not in session:
        session["carrinho"] = []

    itens = []
    total = 0

    for item_id in session["carrinho"]:
        produto = Produto.query.get(item_id)
        if produto:
            itens.append(produto)
            total += produto.preco

    return render_template("carrinho.html", itens=itens, total=total)

@app.route("/adicionar/<int:produto_id>")
def adicionar_carrinho(produto_id):
    if "carrinho" not in session:
        session["carrinho"] = []

    session["carrinho"].append(produto_id)
    session.modified = True

    return redirect(url_for("carrinho"))

@app.route("/remover/<int:produto_id>")
def remover_carrinho(produto_id):
    if "carrinho" in session and produto_id in session["carrinho"]:
        session["carrinho"].remove(produto_id)
        session.modified = True

    return redirect(url_for("carrinho"))

@app.route("/checkout/endereco", methods=["GET", "POST"])
def checkout_endereco():
    if request.method == "POST":
        session["endereco"] = {
            "nome": request.form["nome"],
            "rua": request.form["rua"],
            "numero": request.form["numero"],
            "cidade": request.form["cidade"],
            "estado": request.form["estado"],
            "cep": request.form["cep"]
        }
        return redirect(url_for("checkout_pagamento"))

    return render_template("checkout_endereco.html")

@app.route("/checkout/pagamento", methods=["GET", "POST"])
def checkout_pagamento():
    if request.method == "POST":
        session["pagamento"] = request.form["metodo"]
        return redirect(url_for("checkout_resumo"))

    return render_template("checkout_pagamento.html")

@app.route("/checkout/resumo")
def checkout_resumo():
    itens = []
    total = 0

    for item_id in session.get("carrinho", []):
        produto = Produto.query.get(item_id)
        if produto:
            itens.append(produto)
            total += produto.preco

    pagamento = session.get("pagamento")
    endereco = session.get("endereco")

    pix_total = None
    if pagamento == "PIX":
        pix_total = round(total * 0.9, 2)

    parcela_cartao = None
    if pagamento == "Cartão":
        parcela_cartao = round(total / 6, 2)

    return render_template(
        "checkout_resumo.html",
        itens=itens,
        total=total,
        endereco=endereco,
        pagamento=pagamento,
        pix_total=pix_total,
        parcela_cartao=parcela_cartao
    )

@app.route("/checkout/confirmacao")
def checkout_confirmacao():
    pagamento = session.get("pagamento", "Não informado")

    numero_pedido = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(100, 999))

    if pagamento == "PIX":
        status = "Aguardando pagamento via PIX"
    elif pagamento == "Cartão":
        status = "Pagamento aprovado (simulado)"
    else:
        status = "Em processamento"

    session["carrinho"] = []

    return render_template(
        "checkout_confirmacao.html",
        pagamento=pagamento,
        numero_pedido=numero_pedido,
        status=status
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)