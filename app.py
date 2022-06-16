from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import urllib.request, json


# "nome" do aplicativo
app = Flask(__name__)
app.secret_key = "super secret key"  # criar chave: python -c 'import os; print(os.urandom(16))'


# Banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Usuario(db.Model):
	id    = db.Column(db.Integer, primary_key=True)
	nome  = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)

	def __init__(self, nome, email):
		self.nome = nome
		self.email = email

	def __repr__(self):
		return '<Usuario %r>' % self.nome


@app.route('/')
def lista_usuarios():
	return render_template('usuarios.html', usuarios=Usuario.query.all())


@app.route('/inserir', methods=['GET', 'POST'])
def inserir():

	nome = request.form.get('nome')
	email = request.form.get('email')

	if request.method == 'POST':
		if not nome or not email:
			flash("Preencha todos os campos!", "error")
		else:
			usuario = Usuario(nome, email)
			db.session.add(usuario)
			db.session.commit()
			return redirect(url_for('lista_usuarios'))

	return render_template('inserir.html')


@app.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):

	usuario = Usuario.query.filter_by(id=id).first()

	if request.method == 'POST':
		nome = request.form['nome']
		email = request.form['email']

		Usuario.query.filter_by(id=id).update({'nome': nome, 'email': email})
		db.session.commit()
		return redirect(url_for('lista_usuarios'))

	return render_template('editar.html', usuario=usuario)


@app.route('/<int:id>/excluir')
def excluir(id):
	
	usuario = Usuario.query.filter_by(id=id).first()
	db.session.delete(usuario)
	db.session.commit()
	return redirect(url_for('lista_usuarios'))


# o app deve ser executado com: `python app.py` (ao invés de `flask run`)
if __name__== "__main__":
	db.create_all()
	app.run(debug=True)
