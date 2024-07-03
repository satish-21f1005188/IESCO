from flask import Flask,render_template,request

from flask import current_app as app # current running app
from models import *
@app.route("/")
def home():
    return "<h2>Fuck you ,im routing here"

@app.route("/login",methods=["GET",'POST'])
def user_login():
    #return render_template("login.html")
    if request.method == "POST":
        uname = request.form.get("uname")
        pwd = request.form.get("pwd")
        usr = table_1.query.filter_by(user_name = uname,
                                      pwd=pwd).first()
        if usr != None and usr.role == 0:
            pass
            

    return render_template("login.html")

@app.route("/register",methods=["GET","POST"])
def user_signup():
    return render_template("sign_up.html")