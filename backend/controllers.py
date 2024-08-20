from flask import Flask, jsonify,render_template,request,flash,redirect,url_for

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
            campaigns_list = get_campaigns()
            user_list = get_users()
            if usr:
                if usr.role == 0:
                    # Admin user
                    
                    return redirect(url_for("admin_stats"))
                elif usr.role == 1:
                    if usr.status == 0:
                        flash("Your Account is Flagged . Kindly Contact Admin" , 'danger')
                        return redirect(url_for("user_login"))
                    # Influencer user
                    else:
                        
                        return redirect(url_for("influencer_profile",user_id = usr.id))
                elif usr.role == 2:
                    # Sponsor user
                    if usr.status == 0:
                        flash("Your Account is Flagged . Kindly Contact Admin" , 'danger')
                        return redirect(url_for("user_login"))
                    # Influencer user
                    else:
                        return redirect(url_for("sponsor_profile",user_id = usr.id))
            
            # If user not found or roles are not defined, handle login failure
            else:
                flash("Login Credentials is Wrong. Kindly enter correct details")
                return render_template("new-login.html", msg="failed")

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

            flash("Your Account Is Created Successfully" , 'success')
            return redirect(url_for("inf_signup"))
            
        else:
            flash("Account Is Already Existing . Kindly Sign In" , 'danger')
            return redirect(url_for("inf_signup"))
    return render_template("inf-signup.html")
        


    

@app.route("/spo_register",methods=["GET","POST"])
def spo_signup():
    if request.method == "POST":
            uname = request.form.get("uname")
            email = request.form.get("email")
            fname = request.form.get("fname")
            pwd =  request.form.get("pwd")
            usr = user_table.query.filter_by(user_name = uname).first()
            if not usr:
                    if len(uname) >= 10:
                        flash("username length should be less than 10",'danger')
                        return redirect(url_for('spo_signup'))
                    
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
                    flash("Your Account is created Successfully" , 'success')
                    return redirect(url_for("spo_signup"))
                    
            else:
                    flash("Account is already existing . Kindly sign in" , 'danger')
                    return redirect(url_for("spo_signup"))
                    # return render_template("spo-signup.html",msg = "user is already existing . kindly sign in")
    return render_template("spo-signup.html")

# all-users template
@app.route("/all_users",methods=["GET","POST"])
def all_users():
    user_list = get_users()
    influencers_list = get_influencers()
    sponsors_list = get_sponsors()
    return render_template("admin_templates/admin-all-users.html",user_list = user_list , sponsors_list = sponsors_list ,influencers_list = influencers_list)

# all-campaigns template
@app.route("/all_campaigns")
def all_campaigns():
    campaigns_list = get_campaigns()
    sponsors_list = get_sponsors()
    users_list = get_users()
    return render_template("admin_templates/admin-all-campaigns.html",campaigns_list = campaigns_list,sponsors_list = sponsors_list,users_list = users_list)





# getter functions
def get_campaigns():
    campaigns_list=campaigns.query.all()
    campaigns_dict={}
    for campaign in campaigns_list:
        if campaign.id not in campaigns_dict.keys():
            campaigns_dict[campaign.id]=[campaign.campaign_name,campaign.sponsor_id,campaign.campaign_desc,campaign.campaign_status,campaign.campaign_budget,campaign.campaign_start_date,campaign.campaign_end_date,campaign.campaign_category,campaign.campaign_visibility]
    return dict(campaigns_dict)

def get_users():
    users = user_table.query.all()
    users_dict = {}
    for user in users:
        if user.id not in users_dict.keys():
            users_dict[user.id] = [user.email,user.full_name,user.user_name,user.role,user.status]
    return dict(users_dict)

def get_influencers():
    influencers_data = influencers.query.all()
    inf_dict = {}
    for inf in influencers_data:
        if inf.id not in inf_dict.keys():
            inf_dict[inf.id] = [inf.category,inf.niche,inf.followers_count]
    return dict(inf_dict)

def get_sponsors():
    sponsors_data = sponsors.query.all()
    spo_dict = {}
    for spo in sponsors_data:
        if spo.id not in spo_dict.keys():
            spo_dict[spo.id] = [spo.industry,spo.budget]
    return dict(spo_dict)

# /list/delete/<int:user_id>",methods=["GET","POST"])
# def delete_list(user_id):
#     if request.method=="POST":
#         title=request.form.get("title")
#         list_obj=Lists.query.filter_by(user_id=user_id,title=title).first()
#         db.session.delete(list_obj)
#         db.session.commit()
#         user_info=fetch_user_info(user_id)
#         return render_template("user_dashboard.html",id=user_info.id,name=user_info.user_name,lists=user_info.lists)

#admin-all-users functions
# flag user
@app.route("/all_users/flag_user/<int:user_id>", methods=["GET", "POST"])
def flag_user(user_id):
    if request.method == "POST":
        # Query the user by ID
        usr = user_table.query.filter_by(id=user_id).first()
        if usr:
            # Flag the user
            usr.status = 0
            if usr.role == 2:
                campaigns_list = campaigns.query.filter_by(sponsor_id=user_id).all()
                for campaign in campaigns_list:
                    campaign.campaign_status = 0
                    
            db.session.commit()
            flash('User has been flagged successfully!', 'danger')
        else:
            flash('User not found.', 'danger')  # Optional: Handle user not found case

        # Redirect back to the all users page
        return redirect(url_for('all_users'))  # Change 'all_users' to the correct view function name

    # Handle GET request if necessary (you might want to return some error or a message)
    return redirect(url_for('all_users'))  # Redirect to avoid rendering directly


#revoke user

@app.route("/all_users/revoke_user/<int:user_id>", methods=["GET", "POST"])
def revoke_user(user_id):
    if request.method == "POST":
        # Query the user by ID
        usr = user_table.query.filter_by(id=user_id).first()
        if usr:
            # Flag the user
            usr.status = 1
            if usr.role == 2:
                campaigns_list = campaigns.query.filter_by(sponsor_id=user_id).all()
                for campaign in campaigns_list:
                    campaign.campaign_status = 1
            db.session.commit()
            flash('User has been revoked successfully!', 'success')
        else:
            flash('User not found.', 'danger')  # Optional: Handle user not found case

        # Redirect back to the all users page
        return redirect(url_for('all_users'))  # Change 'all_users' to the correct view function name

    # Handle GET request if necessary (you might want to return some error or a message)
    return redirect(url_for('all_users'))  # Redirect to avoid rendering directly

# all-users-functions end

#all-campaigns functions
# flag campaign
@app.route("/all_campaigns/flag_campaign/<int:campaign_id>", methods=["GET", "POST"])
def flag_campaign(campaign_id):
    if request.method == "POST":
        # Query the campaign by ID
        camp = campaigns.query.filter_by(id=campaign_id).first()
        if camp:
            # Flag the campaign
            camp.campaign_status = 0
            db.session.commit()
            flash('Campaign has been flagged successfully!', 'danger')
        else:
            flash('Campaign not found.', 'danger')
        return redirect(url_for('all_campaigns'))
    return redirect(url_for('all_campaigns'))

#revoke campaign
@app.route("/all_campaigns/revoke_campaign/<int:campaign_id>", methods=["GET", "POST"])
def revoke_campaign(campaign_id):
    if request.method == "POST":
        # Query the campaign by ID
        camp = campaigns.query.filter_by(id=campaign_id).first()
        if camp:
            # Flag the campaign
            camp.campaign_status = 1
            db.session.commit()
            flash('Campaign has been revoked successfully!', 'success')
        else:
            flash('Campaign not found.', 'danger')
        return redirect(url_for('all_campaigns'))
    return redirect(url_for('all_campaigns'))


# admin stats

def get_user_data():
    user_roles = db.session.query(user_table.role, db.func.count(user_table.id)).group_by(user_table.role).all()
    user_roles_list = [{"role": role, "count": count} for role, count in user_roles if role in [ 1, 2]]
    return user_roles_list  # Return as a list of dictionaries

def get_campaign_data():
    campaign_status = db.session.query(campaigns.campaign_status, db.func.count(campaigns.id)).group_by(campaigns.campaign_status).all()
    campaign_status_list = [{"status": status, "count": count} for status, count in campaign_status]
    return campaign_status_list  # Return as a list of dictionaries

def get_campaign_by_category():
    campaign_category = db.session.query(campaigns.campaign_category, db.func.count(campaigns.id)).group_by(campaigns.campaign_category).all()
    campaign_category_list = [{"category": category, "count": count} for category, count in campaign_category]
    return campaign_category_list  # Return as a list of dictionaries

def total_users():
    total_users = user_table.query.count()
    return total_users

def total_campaigns():
    total_campaigns = campaigns.query.count()
    return total_campaigns

def total_influencers():

    total_influencers = influencers.query.count()
    return total_influencers

def total_sponsors():   
    total_sponsors = sponsors.query.count()
    return total_sponsors

def total_active_users():
    total_active_users = user_table.query.filter_by(status=1).count()
    return total_active_users

def total_active_campaigns():
    total_active_campaigns = campaigns.query.filter_by(campaign_status=1).count()
    return total_active_campaigns
@app.route("/admin_stats")
def admin_stats():
    user_data = get_user_data()
    campaign_data = get_campaign_data()
    campaign_by_category_data = get_campaign_by_category()
    inf_spo_ratio = round(total_influencers() / total_sponsors(), 1)
    return render_template("admin_templates/admin-dashboard.html", user_data=user_data,campaign_data=campaign_data,campaign_category_data=campaign_by_category_data
                           ,total_users=total_users(),total_campaigns=total_campaigns(),
                           total_influencers=total_influencers(),total_sponsors=total_sponsors(),
                           total_active_users=total_active_users(),total_active_campaigns=total_active_campaigns(),
                           inf_spo_ratio = inf_spo_ratio)




