from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#criando a api em flask
app = Flask(__name__)
#criando instancia do SQLAlchemy
app.config['SECRET_KEY'] = 'FSD2323F#$!SAH'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.zpwobyqieyuhhazhdbso:xOTrNC65LJwv4EYA@aws-0-us-west-1.pooler.supabase.com:5432/postgres'

db = SQLAlchemy(app)
db: SQLAlchemy

#definir a tabela postagem
#Id_postagem, titulo, autor
class Postagem(db.Model):
    __tablename__ = 'postagem'
    id_postagem = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String)
    id_autor = db.Column(db.Integer,db.ForeignKey('autor.id_autor'))


#definir a tabela autor
#id_autor, nome, email, senha, postagens, admin
class Autor(db.Model):
    __tablename__ = 'autor'
    id_autor = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    email = db.Column(db.String)
    senha = db.Column(db.String)
    admin = db.Column(db.Boolean)
    #Nesse caso do relationship utilizar o nome da classe que quer relacionar
    postagens = db.relationship('Postagem')
# Comando para criar banco de dados
def inicializar_banco():
    with app.app_context():
        db.drop_all()
        db.create_all()
        #Criando o administrador do banco 
        autor = Autor(nome='Vinicius', email='vinicius.euneri@email.com', senha='123456', admin=True)
        db.session.add(autor)
        db.session.commit()

#Garante que o banco de dados não seja apagado e inicializado quando fecha e abre o programa
if __name__ == '__main__':
    inicializar_banco()

