from pymongo import MongoClient
from elasticsearch import Elasticsearch
from flask import (Flask, request, redirect, render_template, flash, session, url_for, jsonify)
from werkzeug.security import generate_password_hash, check_password_hash
from os import getenv

client = MongoClient(host=getenv('MONGODB_HOSTNAME'), port=27017, username=getenv('MONGODB_USERNAME'), password=getenv('MONGODB_PASSWORD'))
db = client.searchapp

es = Elasticsearch(getenv('ELASTIC_HOST'))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/")
def index():
	return render_template('index.html')

@app.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
    
        if not username:
            error = 'Nome de usuário é obrigatório.'
        elif not password:
            error = 'Senha é obrigatória.'

        if error is None:
            users = db.users

            if not users.find_one({"username": username}):
                users.insert_one({"username": username, "password": generate_password_hash(password)})
                
                return redirect(url_for('login'))
            else:
                error = 'Nome de usuário já existe.'

        flash(error)

    return render_template('signup.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
    
        if not username:
            error = 'Nome de usuário é obrigatório.'
        elif not password:
            error = 'Senha é obrigatória.'

        if error is None:
            users = db.users
            user = users.find_one({"username": username})

            if user:
                if not check_password_hash(user['password'], password):
                    error = 'Senha incorreta.'
            else:
                error = 'Nome de usuário incorreto.'
            
            if error is None:
                session.clear()
                session['logged_in'] = True
                #session['user_id'] = user['id']
                return redirect(url_for('index'))
            
            flash(error)

    return render_template('login.html')

@app.route("/search/cnpj", methods=('GET', 'POST'))
def cnpj():
    if request.method == 'POST':
        query = {
            "query": {
                "match": {
                    "CNPJ BASICO": request.form['search']
                }
            }
        }

        res = es.search(index="empresas", body=query)

        return jsonify(res)

    return render_template('search.html', col="CNPJ")

@app.route("/search/razao-social", methods=('GET', 'POST'))
def razao_social():
    if request.method == 'POST':
        query = {
            "query": {
                "match": {
                    "RAZAO SOCIAL": request.form['search']
                }
            }
        } 

        res = es.search(index="empresas", body=query)

        return jsonify(res)

    return render_template('search.html', col="razão social")

@app.route("/search/endereco", methods=('GET', 'POST'))
def endereco():
    if request.method == 'POST':

        addr_type, addr = request.form['search'].split(" ", maxsplit=1)
        addr, number = request.form['search'].rsplit(" ", maxsplit=1)

        query = {
            "query": {
                "bool": {
                    "should": [
                        {
                            "match": {
                                "TIPO DE LOGRADOURO": addr_type
                            }
                        },
                        {
                            "match": {
                                "LOGRADOURO": addr
                            }
                        },
                        {
                            "match": {
                                "NUMERO": number
                            }
                        }
                    ]
                }
            }
        }


        res = es.search(index="estabelecimentos", body=query)

        return jsonify(res)

    return render_template('search.html', col="endereço")

@app.route("/search/telefone", methods=('GET', 'POST'))
def telefone():
    if request.method == 'POST':
        query = {
            "query": {
                "multi_match": {
                    "query": request.form['search'],
                    "fields": ["TELEFONE 1", "TELEFONE 2"]
                }
            }
        }

        res = es.search(index="estabelecimentos", body=query)

        return jsonify(res)

    return render_template('search.html', col="telefone")