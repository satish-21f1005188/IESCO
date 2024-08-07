from flask import Flask,render_template,request,flash,redirect,url_for
from datetime import datetime
from flask import current_app as app # current running app
from .models import *

#sponsor-dashboard functions

# sponsor profile
@app.route("/sponsor/profile/<int:user_id>", methods=["GET", "POST"])
def sponsor_profile(user_id):
    user = user_table.query.filter_by(id=user_id).first()
    sponsor = sponsors.query.filter_by(id=user_id).first()
    sponsor_info = get_sponsor_info(user_id)
    # return render_template("spo-profile.html", user=user, sponsor=sponsor)
    return render_template("sponsor_templates/sponsor-profile.html",sponsor_info = sponsor_info,id = user_id)

@app.route("/sponsor/campaigns/<int:user_id>", methods=["GET", "POST"])
def sponsor_campaigns(user_id):
    
    sponsor_info = get_sponsor_info(user_id)
    campaigns_list = get_sponsor_campaigns(user_id)
    days_left_list = {}
    for campaign_id in campaigns_list.keys():
        campaign = campaigns.query.filter_by(id=campaign_id).first()
        days_left_list[campaign_id] = days_left(campaign)
    return render_template("sponsor_templates/sponsor-campaigns.html",id = user_id,campaigns_list = campaigns_list,sponsor_info = sponsor_info,days_left_list = days_left_list)

# Just for routing 
@app.route("/sponsor/new_campaign/<int:user_id>", methods=["GET", "POST"])
def new_campaign(user_id):
    sponsor_info = get_sponsor_info(user_id)
    return render_template("sponsor_templates/new-campaign.html",id = user_id,campaigns_list = campaigns,sponsor_info = sponsor_info)


# Editing campaign
@app.route("/sponsor/edit_campaign/<int:campaign_id>", methods=["GET", "POST"])
def edit_campaign(campaign_id):
    campaign = campaigns.query.filter_by(id=campaign_id).first()
    if request.method == "POST":
        campaign_name = request.form['editCampaignName']
        campaign_description = request.form['editCampaignDescription']
        campaign_budget = request.form['editCampaignBudget']
        campaign_start_date = request.form['editCampaignStartDate']
        campaign_end_date = request.form['editCampaignEndDate']

        campaign_start_date = datetime.strptime(campaign_start_date, '%Y-%m-%d').date()
        campaign_end_date = datetime.strptime(campaign_end_date, '%Y-%m-%d').date()

        campaign.campaign_name = campaign_name
        campaign.campaign_desc = campaign_description
        campaign.campaign_budget = campaign_budget
        campaign.campaign_start_date = campaign_start_date
        campaign.campaign_end_date = campaign_end_date

        db.session.commit()
        flash("Campaign updated successfully",'success')
        return redirect(url_for('sponsor_campaigns',user_id=campaign.sponsor_id))
    return render_template("sponsor_templates/edit-campaign.html",campaign=campaign)


# New campaign creation
@app.route("/sponsor/create_campaign/<int:sponsor_id>", methods=["GET", "POST"])
def create_campaign(sponsor_id):
    if request.method == "POST":
        campaign_name = request.form['campaignName']
        campaign_description = request.form['campaignDescription']
        campaign_budget = request.form['campaignBudget']
        campaign_start_date = request.form['campaignStartDate']
        campaign_end_date = request.form['campaignEndDate']

        campaign_start_date = datetime.strptime(campaign_start_date, '%Y-%m-%d').date()
        campaign_end_date = datetime.strptime(campaign_end_date, '%Y-%m-%d').date()
        sponsor = sponsors.query.filter_by(id=sponsor_id).first()
        if sponsor:
            new_campaign = campaigns(campaign_name=campaign_name,campaign_desc=campaign_description,campaign_status=1,campaign_budget=campaign_budget,campaign_start_date=campaign_start_date,campaign_end_date=campaign_end_date,sponsor_id=sponsor_id)
            db.session.add(new_campaign)
            db.session.commit()
            flash("Campaign created successfully",'success')
            flash("Manage Campaigns under Yours Campaigns section",'success')
            return redirect(url_for('sponsor_campaigns',user_id=sponsor_id))

# Deleting campaign
@app.route("/sponsor/delete_campaign/<int:campaign_id>", methods=["GET", "POST"])
def delete_campaign(campaign_id):
    campaign = campaigns.query.filter_by(id=campaign_id).first()
    sponsor_id = campaign.sponsor_id
    db.session.delete(campaign)
    db.session.commit()
    flash("Campaign deleted successfully",'success')
    return redirect(url_for('sponsor_campaigns',user_id=sponsor_id))
        
# days left for campaign
def days_left(campaign):
    current_date = datetime.now().date()
    end_date = campaign.campaign_end_date
    days_left = (end_date - current_date).days
    return days_left

def get_sponsor_campaigns(user_id):
    campaigns_list = campaigns.query.filter_by(sponsor_id=user_id).all()
    campaigns_dict={}
    for campaign in campaigns_list:
        if campaign.id not in campaigns_dict.keys():
            campaigns_dict[campaign.id]=[campaign.campaign_name,campaign.sponsor_id,campaign.campaign_desc,campaign.campaign_status,campaign.campaign_budget,campaign.campaign_start_date,campaign.campaign_end_date]
    return dict(campaigns_dict)

def get_sponsor_info(user_id):
    user = user_table.query.filter_by(id=user_id).first() #user_table data
    sponsor = sponsors.query.filter_by(id=user_id).first() #sponsor table data
    user_info = {}
    user_info[user_id] = [user.email,user.full_name,user.user_name,user.pwd,user.role,user.status]
    user_info[user_id].append(sponsor.industry)
    user_info[user_id].append(sponsor.budget)
    return dict(user_info)

