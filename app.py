from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash  #criptografia de senhas
import yaml
import os

app = Flask(__name__, static_url_path='/static')
Bootstrap(app)

# Configure SQL DB
db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/', methods=['GET', 'POST'])
def index():
    cur = mysql.connection.cursor()
#------------------------------------------------------------------------
    # if cur.execute("INSERT INTO user(user_name) VALUES('Ben')"):
    #     return 'success', 201

#-------------------------------------------------------------------------
    if request.method == 'POST':
        return request.form['password'] #eh onde esta armazenada a senha
        # return 'Succesfully registered'
#-------------------------------------------------------------------------
    # cur.execute("INSERT INTO user VALUES(%s)",['Mike'])  #adding
    # mysql.connection.commit() #for saving the changes

    # result_value = cur.execute("SELECT * FROM user") #fetching data from db
    # if result_value > 0: #it mean there is at least one row
    #     users = cur.fetchall()  #fetching the values to users
    #     return(users[0][0]) #1 index p/ nome_user, 2 p/ a lista de nomes
#-------------------------------------------------------------------------
    fruits = ['apple', 'mango', 'pineaple']
    return render_template('index.html', fruits= fruits) #a parte render_template eh obritoria p/ carregar pagina
#-------------------------------------------------------------------------
    # return redirect(url_for('about')) #redireciona para a outra pagina(about)

@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        try:
            form = request.form
            name = form['name']
            age = form['age']
            cur = mysql.connection.cursor()
            name = generate_password_hash(name) #criptografa p/ o db e p/ receber d volta
            cur.execute("INSERT INTO employee(name, age) VALUES(%s, %s)",(name, age))
            mysql.connection.commit()
            flash('Employee added successfully','success')
        except:
            flash('failed to insert data', 'danger')

    return render_template('about.html')

@app.route('/employees')
def employee():
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM employee")
    if result_value > 0:
        employees = cur.fetchall()

        # return str(check_password_hash(employees[1]['name'], 'john'))

        # session['username'] = employees[0]['name'] #mostra o 1 employee em qualquer lugar do app, no caso o about
    return render_template('employees.html', employees = employees)

@app.route('/css')
def css():
    return render_template('css.html')

@app.errorhandler(404)
def page_not_found(e):
    return 'this page was no found'
    return render_template('page_not_found.html'), 404 # Eh possivel criar uma pagina para erros.


if __name__ == '__main__':
    app.run(debug=True)
