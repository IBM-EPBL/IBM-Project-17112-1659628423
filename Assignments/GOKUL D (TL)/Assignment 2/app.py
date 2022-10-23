from flask import Flask, render_template, redirect, url_for, request
import ibm_db

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=2d46b6b4-cbf6-40eb-bbce-6251e6ba0300.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32328;SECURITY=SSL;SSLServerCertificate=abc.crt;UID=cqk12082;PWD=yUYWG68g3jEqz9xT",'','')
print(conn)
print("Connection Successful")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method=='POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        sql = "insert into users values(?,?,?)"
        prep_stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(prep_stmt,1,name)
        ibm_db.bind_param(prep_stmt,2,email)
        ibm_db.bind_param(prep_stmt,3,password)
        ibm_db.execute(prep_stmt)
        return redirect(url_for('log_in'))
    else:
        return render_template("signup.html")

@app.route('/login', methods=['GET', 'POST'])
def log_in():
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        sql = "select * from users where email=? and password=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        dic = ibm_db.fetch_assoc(stmt)
        print(dic)
        if dic:
            return redirect(url_for('home'))
    else:
        return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)
