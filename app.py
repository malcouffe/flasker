from flask import Flask, render_template

# Création d'un instance flask 
app = Flask(__name__)

# Création d'une route 

@app.route('/')
def index():
    first_name = "Mat"
    stuff = "<strong>Voici du text</strong>"
    pizza = ["pizza 1", "pizza 2", "pizza 3"]
    return render_template('index.html', first_name=first_name, stuff=stuff, pizza=pizza)

@app.route('/user/<string:name>')
def user(name):
    return render_template('user.html', user_name=name)
# Par convention, on utilise le même nom : user_name=name > name=name

# Création d'un page d'erreur customisée 

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404 #", +code erreur obligatoire avec errorhandler "

# Internal error server
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500
