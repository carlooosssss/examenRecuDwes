from itertools import product
from math import prod
from flask import Flask, flash, request, render_template, url_for, redirect
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from flask_login import login_user, login_required, LoginManager, logout_user, current_user
import os
from werkzeug.security import generate_password_hash
from flask_wtf.csrf import CSRFProtect

from models.ModelUser import ModelUser

load_dotenv()

app = Flask(__name__)

CSRFProtect(app)

app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

db = MySQL(app)

login_manager = LoginManager(app)

@login_manager.user_loader
def get_by_id(id):
    return ModelUser.get_by_id(db, id)

@app.route('/', methods=['GET'])
def welcome():
    
    return render_template("welcome.html")

@app.route('/login', methods=['POST','GET'])
def login():
    
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')
    
        logged_user = ModelUser.login(db,username, password)

        if logged_user:
            if logged_user.password:

                login_user(logged_user)

                return redirect(url_for('home'))
            else:
                flash("Contraseña incorrecta")
                return redirect(url_for('login'))


        else:
            flash("Usuario no encontrado")
            return redirect(url_for('login'))
        
    else: 
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        return render_template('login.html')

    
@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        hashed_password = generate_password_hash(password)

        cur = db.connection.cursor()

        sql = ("INSERT INTO users (username, password) VALUES (%s, %s)")

        cur.execute(sql, (username, hashed_password))

        db.connection.commit()

        flash("Usuario registrado correctamente")
        return redirect(url_for('home'))
    else:
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/tienda')
def tienda():

    cur = db.connection.cursor()

    sql = ("SELECT * FROM productos")

    cur.execute(sql)

    productos = cur.fetchall()

    cur = db.connection.cursor()

    sql = ("SELECT * FROM carrito")

    cur.execute(sql)

    carrito = cur.fetchall()

    print(carrito)

    return render_template("tienda.html", productos = productos, carrito = carrito)


@app.route('/addProduct/<id>')
def addProduct(id):

    cur = db.connection.cursor()

    sql = ("SELECT * FROM productos WHERE id = %s")

    cur.execute(sql, id)

    producto = cur.fetchone()
    
    producto_carrito = list(producto)

    cur = db.connection.cursor()

    sql = ("INSERT INTO carrito (id, nombre, precio, user_id) VALUES (%s, %s, %s,%s)")

    cur.execute(sql, (producto_carrito[0],producto_carrito[1] ,producto_carrito[2], current_user.id))

    db.connection.commit()
    
    return redirect(url_for('tienda'))
    

@app.route('/deleteProduct/<id>')
def deleteProduct(id):   
    
    cur = db.connection.cursor()

    sql = ("DELETE FROM carrito WHERE id = %s")

    cur.execute(sql, (id,))

    db.connection.commit()
    
    return redirect(url_for('tienda'))

if __name__ == '__main__':
    app.run(debug=True)