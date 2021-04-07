from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask import session
from flask import jsonify
import mysql.connector


app= Flask(
    __name__,
    static_folder = "public",
    static_url_path = "/",
    )
app.config["JSON_AS_ASCII"] = False
app.secret_key='aw1/23s/4ax/34j'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/users")
def getuser():
    userdb = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'Skfmarch0306',
        database = 'website'
    )
    cursor = userdb.cursor()
    username=request.args.get('username')
    user_search = (
        "select id,username,name from user where username='%s'"% (username)
    )
    cursor.execute(user_search)
    result=cursor.fetchone()
    if result != None:
        return jsonify (
            data =({
                'id' : result[0],
                'username' : result[1],
                'name' : result[2]
        
            })
        )
        
    else:
        return jsonify(
            data={
                "data":None
            }
        )
    
@app.route("/signup", methods=["post"])
def signup():
    userdb = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'Skfmarch0306',
        database = 'website'
    )
    cursor = userdb.cursor()

    name = request.form['name']
    username = request.form['username']
    password = request.form['password']

    userdetails = ({
        'name' : name,
        'username' : username,
        'password' : password
    })
    
    add_user = (
        "insert into user" 
        "(name, username, password)"
        "values(%s, %s, %s)"
    )
    
    check_user = (
        "select * from user where username ={}".format(username)
    )

    cursor.execute(check_user)
    result = cursor.fetchone()

    if result != None:
        return redirect("/wrong")
    else:
        cursor.execute(add_user, (userdetails["name"], userdetails["username"], userdetails['password']))
        userdb.commit()
        cursor.close()
        userdb.close()
        return redirect('/')

@app.route("/signin", methods=["post"])
def signin():
    userdb = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'Skfmarch0306',
        database = 'website'
    )
    cursor = userdb.cursor()
    
    username = request.form['username']
    password = request.form['password']

    input = (
        username,password
    )
    
    check_login = (
        "select * from user where username ={} and password ={}".format(username,password)
    )
    cursor.execute(check_login )
    result = cursor.fetchone()

    if result is not None:
        user = request.form["username"]
        session['user'] = user
        return render_template("member.html", name = result[1])  
    else:
        return redirect(url_for("error", message="帳號或密碼輸入錯誤"))
        

@app.route("/signout")
def signout():
    session.pop('user',None)
    return redirect(url_for('index'))

@app.route("/member")
def member():
    if "user" in session:
        user = session["user"]
        return render_template("member.html")
    else:
        return render_template("/index.html")

@app.route("/error")
def error():
    message = request.args.get("message","帳號或密碼輸入錯誤")
    return render_template("error.html",message=message)

@app.route("/wrong")
def wrong ():
    return "帳號已經被註冊"
app.run(port = 3000, debug = True)