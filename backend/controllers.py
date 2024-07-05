from flask import Flask,render_template,request

from flask import current_app as app # current running app
from .models import *
@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login",methods=["GET",'POST'])
def user_login():
    #return render_template("login.html")
    if request.method == "POST":
        uname = request.form.get("uname")
        pwd = request.form.get("pwd")
        usr = user_table.query.filter_by(user_name = uname,
                                      pwd=pwd).first()
        if usr != None and usr.role == 0:
            return render_template("admin-dashboard.html")
        elif usr and usr.role == 1:
            return render_template("inf-dashboard.html",influencer = usr.user_name)
        else:
            return render_template("login.html",msg ="Invalid Credentials")    

    return render_template("login.html",msg ="")

@app.route("/inf_register",methods=["GET","POST"])
def inf_signup():
    if request.method == "POST":
        uname = request.form.get("uname")
        email = request.form.get("email")
        fname = request.form.get("fname")
        pwd =  request.form.get("pwd")
        usr = user_table.query.filter_by(user_name = uname).first()
        if not usr:
            new_user = user_table(user_name = uname,email = email,full_name = fname,pwd = pwd,role = 1)
            db.session.add(new_user)
            db.session.commit()
            
            # adding into influencer table
            # id is the foreign key
            category = request.form.get("category")
            niche = request.form.get("niche")
            followers_count = request.form.get("followers_count")
            
            new_infuencer = influencers(id = new_user.id,category = category,niche = niche,followers_count = followers_count)
            db.session.add(new_infuencer)
            db.session.commit()

            return render_template("inf-signup.html",msg = "account created successfully. Kindly login!!!")
            
        else:
            return render_template("inf-signup.html",msg = "user is already existing . kindly sign in")
    return render_template("inf-signup.html",msg= "")
        


    

@app.route("/spo_register",methods=["GET","POST"])
def spo_signup():
    if request.method == "POST":
            uname = request.form.get("uname")
            email = request.form.get("email")
            fname = request.form.get("fname")
            pwd =  request.form.get("pwd")
            usr = user_table.query.filter_by(user_name = uname).first()
            if not usr:
                    new_user = user_table(user_name = uname,email = email,full_name = fname,pwd = pwd,role = 2)
                    db.session.add(new_user)
                    db.session.commit()
                    
                    # adding into sponsor table
                    # id is the foreign key
                    industry = request.form.get("industry")
                    budget = request.form.get("budget")
                    
                    new_sponsor = sponsors(id = new_user.id,industry = industry,budget = budget)
                    db.session.add(new_sponsor)
                    db.session.commit()

                    return render_template("spo-signup.html",msg = "account created successfully. Kindly login!!!")
                    
            else:
                    return render_template("spo-signup.html",msg = "user is already existing . kindly sign in")
    return render_template("spo-signup.html",msg = "")