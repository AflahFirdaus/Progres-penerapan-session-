# Import Flask
from flask import Flask, render_template, session, request, redirect, url_for
from flask_mysqldb import MySQL

# Main app
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'trixs_db'  

mysql = MySQL(app)

app.secret_key = '!@#$%'


# Set route default
@app.route('/index')
def index():
    if 'is_logged_in' in session:
        cur = mysql.connection.cursor()
        cur.execute("Select * FROM tb_produk")
        data = cur.fetchall()
        cur.close()
        return render_template("index.html", tb_produk=data)
    else:
        return redirect(url_for('login'))

@app.route('/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST' and 'inpEmail' in request.form and 'inpPass' in request.form:
        email = request.form['inpEmail']
        passwd = request.form['inpPass']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tb_user where email = %s and password = %s", (email, passwd))
        result = cur.fetchone()
        if result:
            session['is_logged_in'] = True
            session['username'] = result[1]
            return redirect(url_for('index'))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('is_logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/daftar', methods = ['GET', 'POST'])
def daftar():
    if request.method == 'POST' and 'inpUsername' in request.form and 'inpEmail' in request.form and 'inpPass' in request.form:
        username = request.form['inpUsername']
        passwd = request.form['inpPass']
        email = request.form['inpEmail']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tb_user(username, email, password) VALUES (%s, %s, %s)",(username, email, passwd))
        mysql.connection.commit()
        cur.close()

        session['is_logged_in'] = True
        session['username'] = email
        return redirect(url_for('index'))
    else:
        return render_template('daftar.html')

@app.route("/produk1")
def produk1():
    return render_template("produk1.html")

# Debung, untuk automatic update server
if __name__ == "__main__":
    app.run(debug=True)