from db import db

class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), nullable=True)
    pagamento = db.Column(db.String(30))
    total = db.Column(db.Integer)