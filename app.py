from flask import Flask, jsonify, request, make_response
from estrutura_banco_dados import Autor, Postagem, app, db
import jwt
import json
from datetime import datetime, timedelta
from functools import wraps

def token_obrigatorio(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        #Verificação se o token foi enviado
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'mensagem':'Token não foi incluido'}, 401)
        #Depois de pegar o token, verificação se o token e valido no BD
        try:
            resultado = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            autor = Autor.query.filter_by(id_autor=resultado['id_autor']).first()
        except Exception as error:
            print(error)
            return jsonify({'mensagem': 'Token é invalido'}, 401)
        return f(autor, *args, **kwargs)
    return decorated


@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Login invalido', 401, {'WWW-Authenticate': 'Basic realm="Login obrigatório"'})
    usuario = Autor.query.filter_by(nome=auth.username).first()
    if not usuario:
        return make_response('Login invalido', 401, {'WWW-Authenticate': 'Basic realm="Login obrigatório"'})
    if auth.password == usuario.senha:
        token = jwt.encode({'id_autor': usuario.id_autor, 'exp': datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token':token})
    return make_response('Login inválido', 401, {'WWW-Authenticate': 'Basic realm="Login obrigatório"'})

@app.route('/')
@token_obrigatorio
def obter_postagens(autor):
    postagens= Postagem.query.all()
    list_postagem = []

    for postagem in postagens:
        postagem_atual = {}
        postagem_atual['titulo'] = postagem.titulo
        postagem_atual['id_autor'] = postagem.id_autor
        list_postagem.append(postagem_atual)
    return jsonify({'postagens':list_postagem})

@app.route('/postagem/<int:id_postagem>', methods=['GET'])
@token_obrigatorio
def obter_postagem_id(autor, id_postagem):
    postagem = Postagem.query.filter_by(id_postagem=id_postagem).first()
    postagem_atual = {}

    try:
        postagem_atual['titulo'] = postagem.titulo
    except:
        pass
    return jsonify({'postagem':postagem_atual})

@app.route('/postagem', methods=['POST'])
@token_obrigatorio
def nova_postagem(autor):
    new_post = request.get_json()
    postagem = Postagem(titulo=new_post['titulo'], id_autor=new_post['id_autor'])
    db.session.add(postagem)
    db.session.commit()

    return jsonify({'mensagem':'Postagem criada com sucesso!'})

@app.route('/postagem/<int:id_postagem>', methods=['PUT'])
@token_obrigatorio
def atualizar_post(autor, id_postagem):
    post_atualizado = request.get_json()
    postagem = Postagem.query.filter_by(id_postagem=id_postagem).first()
    try:
        postagem.titulo = post_atualizado['titulo']
    except:
        pass
    try:
        postagem.id_autor = post_atualizado['id_autor']
    except:
        pass
    
    db.session.commit()
    return jsonify({'mensagem':'Postagem atualizada com sucesso!'})

@app.route('/postagem/<int:id_postagem>', methods=['DELETE'])
@token_obrigatorio
def deletar_postagem(autor, id_postagem):
    postagem_excluida = Postagem.query.filter_by(id_postagem=id_postagem).first()
    if not postagem_excluida:
        return jsonify({'mensagem':'Postagem não existe'})
    db.session.delete(postagem_excluida)
    db.session.commit()

    return jsonify({'mensagem':'Postagem deletada com sucesso!'})

@app.route('/autores')
@token_obrigatorio
def obter_autores(autor):
    autores = Autor.query.all()
    lista_autores = []
    for autor in autores:
        autor_atual = {}
        autor_atual['nome'] = autor.nome
        autor_atual['email'] = autor.email
        autor_atual['id_autor'] = autor.id_autor
        lista_autores.append(autor_atual)
    return jsonify({'mensagem':lista_autores})

@app.route('/autores/<int:id_autor>', methods=['GET'])
@token_obrigatorio
def obter_autor_por_id(autor, id_autor):
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    autor_atual = {}

    try:
        autor_atual['nome'] = autor.nome
    except:
        pass 
    try:
        autor_atual['email'] = autor.email
    except:
        pass
    try:
        autor_atual['id_autor'] = autor.id_autor
    except:
        pass

    return jsonify({'mensagem': autor_atual})

@app.route('/autores', methods=['POST'])
@token_obrigatorio
def adicionar_autor(autor):
    novo_autor = request.get_json()
    autor = Autor(nome=novo_autor['nome'], senha=novo_autor['senha'], email=novo_autor['email'])
    db.session.add(autor)
    db.session.commit()

    return jsonify({'mensagem': 'Autor adicionado com sucesso!'})

@app.route('/autores/<int:id_autor>', methods=['PUT'])
@token_obrigatorio
def atualizar_autor(autor, id_autor):
    autor_atualizado = request.get_json()
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    try:
        autor.nome = autor_atualizado['nome']
    except:
        pass
    try:
        autor.senha = autor_atualizado['senha']
    except:
        pass
    try:
        autor.email = autor_atualizado['email']
    except:
        pass

    db.session.commit()
    return jsonify({'mensagem':'Autor atualizado com sucesso!'})

@app.route('/autores/<int:id_autor>', methods=['DELETE'])
@token_obrigatorio
def deletar_autor(autor, id_autor):
    deletar_autor = Autor.query.filter_by(id_autor=id_autor).first()
    if not deletar_autor:
        return jsonify({'mensagem':'Esse autor não existe!'})
    db.session.delete(deletar_autor)
    db.session.commit()

    return jsonify({'mensagem': 'Autor deletado com sucesso'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
resultado = jwt.decode(token, app.config['SECRET_KEY'],algorithms=['HS256'])