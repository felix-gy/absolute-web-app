from flask import Flask, render_template, request, redirect, url_for
from config import config
from psycopg2 import connect
from dotenv import load_dotenv
from os import environ

load_dotenv()

app = Flask(__name__)

host = environ.get('DB_HOST')
port = environ.get('DB_PORT')
dbname = environ.get('DB_NAME')
user = environ.get('DB_USER')
password = environ.get('DB_PASSWORD')


def get_connection():
    conn = connect(host=host, port=port, dbname=dbname,
                   user=user, password=password)
    return conn


@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template("home.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form['email'])
        print(request.form['password'])
        return render_template('dashboard.html')
    else:
        return render_template('auth/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)',
                    (username, email, password))
        conn.commit()
        cur.close()
        conn.close()
        print(user, email, password)
        return redirect(url_for('home'))
    else:
        return render_template('auth/register.html')


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.config.from_object(config["development"])
    app.run()
