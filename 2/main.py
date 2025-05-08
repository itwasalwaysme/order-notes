from flask import Flask, url_for, render_template, request, redirect, flash
from db import db
from models import Cliente
import time

app = Flask(__name__)
app.secret_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///clientes.db"
db.init_app(app)

@app.route("/excluir/<int:id>", methods=['POST', 'GET'])
def excluir(id):
    usuario = db.session.query(Cliente).filter_by(id=id).first()
    db.session.delete(usuario)
    db.session.commit()
    time.sleep(1)
    return redirect(url_for('home'))

@app.route("/excluir2/<int:id>", methods=['POST', 'GET'])
def excluir2(id):
    usuario = db.session.query(Cliente).filter_by(id=id).first()
    db.session.delete(usuario)
    db.session.commit()
    time.sleep(0.20)
    return redirect(url_for('adicionar'))


@app.route("/editar/<int:id>", methods=['GET', 'POST'])
def editar(id):
    usuario = db.session.query(Cliente).filter_by(id=id).first()
    if request.method == "GET":
        return render_template('editar.html', usuario=usuario)
    elif request.method == "POST":
        nome = request.form['nome']
        telefone = request.form['telefone']
        usuario.nome = nome
        usuario.telefone = telefone
        db.session.commit()
        time.sleep(1)
        return redirect(url_for('home'))
    return render_template('home.hmtl')

@app.route("/")
def home():
    usuarios = db.session.query(Cliente).all()
    return render_template('home.html', usuarios=usuarios)

@app.route("/cadastrar", methods=['GET', 'POST'])
def cadastrar():
    if request.method == "GET":
        return render_template('cadastrar.html')
    elif request.method == "POST":
        nome = request.form['nome']
        telefone = request.form['telefone']
        cadastrar = Cliente(nome=nome, telefone=telefone)
        db.session.add(cadastrar)
        db.session.commit()
        time.sleep(0.50)
        return redirect(url_for('home'))
    return render_template("cadastrar.html")

@app.route("/pedidos", methods=['GET', 'POST'])
def adicionar():
    usuarios = db.session.query(Cliente).all()
    if request.method == "GET":
        total_geral = sum(float(usuario.total) for usuario in usuarios if usuario.total)
        return render_template('pedidos.html', usuarios=usuarios, total_geral=total_geral)
    elif request.method == "POST":
        nome = request.form['nomeCliente']
        total = request.form['Total']
        pagamento = request.form['pagamento']
        match pagamento:
            case "1":
                pagamento = "PIX"
            case "2":
                pagamento = "CARTÃO"
            case "3":
                pagamento = "DINHEIRO"
        pedido = Cliente(nome=nome, pagamento=pagamento, total=total)
        db.session.add(pedido)
        db.session.commit()
        return redirect(url_for('adicionar'))
    
@app.route("/editar2/<int:id>", methods=['GET', 'POST'])
def editar_pedido(id):
    usuario = db.session.query(Cliente).filter_by(id=id).first()
    if request.method == "GET":
        return render_template('editar_pedido.html', usuario=usuario)
    elif request.method == "POST":
        nome = request.form['nome']
        pagamento = request.form['pagamento']
        total = request.form['total']
        match pagamento:
            case "1":
                pagamento = "PIX"
            case "2":
                pagamento = "CARTÃO"
            case "3":
                pagamento = "DINHEIRO"
        usuario.nome = nome
        usuario.pagamento = pagamento
        usuario.total = total
        db.session.commit()
        time.sleep(0.30)
        return redirect(url_for('adicionar'))
    return render_template('editar_pedido.html')  

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)