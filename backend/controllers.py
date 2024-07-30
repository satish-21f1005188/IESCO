from flask import Flask,render_template,request

from flask import current_app as app # current running app
from .models import *
@app.route("/")
def home():
    return render_template("new-login.html")

@app.route("/login", methods=["GET", "POST"])
def user_login():
   
    
    if request.method == "POST":
            uname = request.form.get("uname")
            pwd = request.form.get("pwd")
            
            # Query the database for the user
            usr = user_table.query.filter_by(user_name=uname, pwd=pwd).first()
            
            if usr:
                if usr.role == 0:
                    # Admin user
                    campaigns_list = get_campaigns()
                    user_list = get_users()
                    return render_template("admin-dashboard.html", campaigns_list=campaigns_list, user_list=user_list)
                elif usr.role == 1:
                    # Influencer user
                    return render_template("inf-dashboard.html", influencer=usr.user_name)
                elif usr.role == 2:
                    # Sponsor user
                    return render_template("spo-dashboard.html", sponsor=usr.user_name)
            
            # If user not found or roles are not defined, handle login failure
            else:
                msg = 'Login failed. Please check your credentials.'
                return render_template("new-login.html", msg=msg)

    if request.method == "GET":
    
        # Render the login page with the appropriate message
        return render_template("new-login.html",msg = "")

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


@app.route("/all_users",methods=["GET","POST"])
def all_users():
    user_list = get_users()
    return render_template("admin-all-users.html",user_list = user_list)







# getter functions
def get_campaigns():
    campaigns_list=campaigns.query.all()
    campaigns_dict={}
    for campaign in campaigns_list:
        if campaign.id not in campaigns_dict.keys():
            campaigns_dict[campaign.id]=[campaign.campaign_name,campaign.campaign_desc,campaign.campaign_status,campaign.campaign_budget,campaign.campaign_start_date,campaign.campaign_end_date]
    return campaigns_dict

def get_users():
    users = user_table.query.all()
    users_dict = {}
    for user in users:
        if user.id not in users_dict.keys():
            users_dict[user.id] = [user.email,user.full_name,user.user_name,user.role]
    return users_dict
