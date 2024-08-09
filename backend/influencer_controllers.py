from flask import Flask,render_template,request,flash,redirect,url_for
from datetime import datetime
from flask import current_app as app # current running app
from .models import *
from .controllers import *


# routing to influencer profile
@app.route("/influencer/profile/<int:user_id>", methods=["GET", "POST"])
def influencer_profile(user_id):
    influencer_info = get_influencer_info(user_id)
    return render_template("influencers_templates/influencer-profile.html",influencer_info = influencer_info,id = user_id)




def get_influencer_info(user_id):
    influencer = influencers.query.filter_by(id=user_id).first()
    user = user_table.query.filter_by(id=user_id).first()
    influencer_info = {}
    influencer_info[user_id] = [
        user.full_name,
        user.email,
        user.user_name,
        influencer.category,
        influencer.niche,
        influencer.followers_count,
        user.pwd ]
    return dict(influencer_info)

# editing influencer profile

@app.route("/influencer/edit_profile/<int:influencer_id>", methods=["GET", "POST"])
def edit_influencer_profile(influencer_id):
    if request.method == "POST":
        name = request.form['editProfileName']
        email = request.form['editProfileEmail']
        username = request.form['editProfileUserName']
        category = request.form['editProfileCategory']
        niche = request.form['editProfileNiche']
        followers_count = request.form['editProfileFollowersCount']
        password = request.form['editProfilePassword'] 
        confirm_password = request.form['editProfileConfirmPassword']

        influencer = influencers.query.filter_by(id=influencer_id).first()
        user_table_data = user_table.query.filter_by(id=influencer_id).first()
        
        if user_table.query.filter_by(user_name=username).first() and user_table.query.filter_by(user_name=username).first().id != influencer_id:
            flash("Username already exists",'danger')
            return redirect(url_for('influencer_profile',user_id=influencer_id))
        elif password != confirm_password:
            flash("Passwords do not match",'danger')
            return redirect(url_for('influencer_profile',user_id=influencer_id))
        user_table_data.full_name = name
        user_table_data.email = email
        user_table_data.user_name = username
        influencer.category = category
        influencer.niche = niche
        influencer.followers_count = followers_count
        user_table_data.pwd = password
        db.session.commit()
        flash("Profile updated successfully",'success')
        return redirect(url_for('influencer_profile',user_id=influencer_id))
    

# all - campaigns
@app.route("/influencer/campaigns/<int:influencer_id>", methods=["GET", "POST"])
def influencers_all_campaigns(influencer_id):
    campaigns_list = get_campaigns()
    influencer_info = get_influencer_info(influencer_id)
    return render_template(
        "influencers_templates/influencer-all-campaigns.html", 
        campaigns_list=campaigns_list, 
        id=influencer_id, 
        influencer_info=influencer_info
    )

@app.route("/influencer/search/<int:influencer_id>", methods=["GET", "POST"])
def influencer_search_campaigns(influencer_id):
    campaigns_list = get_campaigns_by_ad_request_status(influencer_id)
    influencer_info = get_influencer_info(influencer_id)
    filtered_campaigns_list = {}

    if request.method == "POST":
        category = request.form['category']
        for campaign_id, details in campaigns_list.items():
            campaign = campaigns.query.filter(
                campaigns.id == campaign_id, 
                campaigns.campaign_status == 1
            ).first()

            if campaign and campaign.campaign_category == category:
                filtered_campaigns_list[campaign_id] = details

    return render_template(
        "influencers_templates/influencer-all-campaigns.html", 
        id=influencer_id, 
        influencer_info=influencer_info, 
        campaigns_list=filtered_campaigns_list
    )

def check_ad_request_exists(influencer_id, campaign_id):
    return adRequests.query.filter_by(influencer_id=influencer_id, campaign_id=campaign_id).first() is not None

def get_campaigns_by_ad_request_status(influencer_id):
    campaigns_list = get_campaigns()
    for campaign_id, details in campaigns_list.items():
        if check_ad_request_exists(influencer_id, campaign_id):
            details.append("Ad Requested")
        else:
            details.append("No Ad Requested")
        campaign = campaigns.query.filter_by(id=campaign_id).first()
        sponsor = user_table.query.filter_by(id=campaign.sponsor_id).first()
        details.append(sponsor.full_name)
    return campaigns_list
