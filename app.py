from flask import Flask, render_template, flash, request 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate 

# Création d'un instance flask 
app = Flask(__name__)

## Ajout de la base de données
## Ancienne bdd SQLite
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Nouvelle bdd mySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password123@localhost/users'

# Clé secrète 
app.config['SECRET_KEY'] = "mot de passe à ne pas partager"

# Initialiter la base de données 
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Création d'un modèle 
class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(120), nullable = False, unique = True)
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.name

# Création d'une classe UserForm (formulaire)
class UserForm(FlaskForm):
    name = StringField("Nom", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    submit = SubmitField("Submit")


# Création d'une classe Form (formulaire)
class NamerForm(FlaskForm):
    name = StringField("Quel est votre nom ?", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Création d'une route 
@app.route('/')
def index():
    first_name = "Mat"
    stuff = "<strong>Voici du text</strong>"
    pizza = ["pizza 1", "pizza 2", "pizza 3"]
    return render_template('index.html', first_name=first_name, stuff=stuff, pizza=pizza)

# Route Name
@app.route('/user/<string:name>')
def user(name):
    return render_template('user.html', user_name=name)
# Par convention, on utilise le même nom : user_name=name > name=name

## Création d'un page d'erreur customisée 
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404 #", +code erreur obligatoire avec errorhandler "

# Internal error server
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


# Page "name"
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    # Validation du formulaire 
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Enregistrement réussi")
    return render_template('name.html', 
        name = name, 
        form = form)

# Page ajout d'un utilisateur 
@app.route('/user/add', methods = ['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first() # test si l'adresse mail existe déjà dans la bdd, ne devrait rien renvoyer si pas d'adresse dans la bdd
        if user is None:
            user = Users(name = form.name.data, email = form.email.data, favorite_color = form.favorite_color.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form = form, name = name, our_users = our_users)

# Route update (MAJ infos utilisateur)
@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form[ 'name' ]
        name_to_update.email = request.form[ 'email' ]
        name_to_update.favorite_color = request.form[ 'favorite_color' ]
        try:
            db.session.commit()
            flash("Utilisateur mis à jour !")
            return render_template("update.html", 
                form = form, 
                name_to_update = name_to_update,
                id=id)
        except:
            flash("Erreur, essayer encore")
            return render_template("update.html", 
                form = form, 
                name_to_update = name_to_update,
                id=id)
    else: 
        return render_template("update.html", 
                form = form, 
                name_to_update = name_to_update,
                id=id)


# Suppression utilisateur
@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("Utilisateur supprimé")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html", form = form, name = name, our_users = our_users)
    except:
        flash("Erreur, attention")
        return render_template("add_user.html", form = form, name = name, our_users = our_users)
