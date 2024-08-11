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
    total_expenditure = sponsor_total_expenditure(user_id)
    total_campaigns = sponsor_total_campaigns(user_id)
    total_ad_requests_completed = sponsor_total_ad_requests_completed(user_id)
    # return render_template("spo-profile.html", user=user, sponsor=sponsor)
    return render_template("sponsor_templates/sponsor-profile.html",sponsor_info = sponsor_info,id = user_id
                           ,total_expenditure = total_expenditure,total_campaigns = total_campaigns,
                           total_ads_completed = total_ad_requests_completed)

# edit sponsor profile
@app.route("/sponsor/edit_profile/<int:sponsor_id>", methods=["GET", "POST"])
def edit_sponsor_profile(sponsor_id):
    if request.method == "POST":
        name = request.form['editProfileName']
        email = request.form['editProfileEmail']
        username = request.form['editProfileUserName']
        industry = request.form['editProfileIndustry']
        password = request.form['editProfilePassword']
        confirm_password = request.form['editProfileConfirmPassword']


        sponsor = sponsors.query.filter_by(id=sponsor_id).first()
        user_table_data = user_table.query.filter_by(id=sponsor_id).first()
        user_table_data.full_name = name
        user_table_data.email = email
        if user_table.query.filter_by(user_name=username).first() and user_table.query.filter_by(user_name=username).first().id != sponsor_id:
            flash("Username already exists",'danger')
            return redirect(url_for('sponsor_profile',user_id=sponsor_id))
        elif password != confirm_password:
            flash("Passwords do not match",'danger')
            return redirect(url_for('sponsor_profile',user_id=sponsor_id))
        user_table_data.user_name = username
        sponsor.industry = industry
        user_table_data.pwd = password
        
        db.session.commit()
        flash("Profile updated successfully",'success')
        return redirect(url_for('sponsor_profile',user_id=sponsor_id))

@app.route("/sponsor/campaigns/<int:user_id>", methods=["GET", "POST"])
def sponsor_campaigns(user_id):
    
    sponsor_info = get_sponsor_info(user_id)
    campaigns_list = get_sponsor_campaigns(user_id)
    flagged_campaigns_list = flagged_campaigns()
    days_left_list = {}
    for campaign_id in campaigns_list.keys():
        campaign = campaigns.query.filter_by(id=campaign_id).first()
        days_left_list[campaign_id] = days_left(campaign)
    
    return render_template("sponsor_templates/sponsor-campaigns.html",id = user_id,campaigns_list = campaigns_list,sponsor_info = sponsor_info,days_left_list = days_left_list,flagged_campaigns_list = flagged_campaigns_list)

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
        campaign_category = request.form['editCampaignCategory']
        campaign_start_date = request.form['editCampaignStartDate']
        campaign_end_date = request.form['editCampaignEndDate']
        campaign_visibility = request.form['editCampaignVisibility']

        campaign_start_date = datetime.strptime(campaign_start_date, '%Y-%m-%d').date()
        campaign_end_date = datetime.strptime(campaign_end_date, '%Y-%m-%d').date()

        campaign.campaign_name = campaign_name
        campaign.campaign_desc = campaign_description
        campaign.campaign_category = campaign_category
        campaign.campaign_budget = campaign_budget
        campaign.campaign_start_date = campaign_start_date
        campaign.campaign_end_date = campaign_end_date
        if campaign_visibility == 'Public':
            campaign.campaign_visibility = 1
        else:
            campaign.campaign_visibility = 0
        

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
        campaign_category = request.form['campaignCategory']
        campaign_start_date = request.form['campaignStartDate']
        campaign_end_date = request.form['campaignEndDate']
        campaign_visibility = request.form['campaignVisibility']

        campaign_start_date = datetime.strptime(campaign_start_date, '%Y-%m-%d').date()
        campaign_end_date = datetime.strptime(campaign_end_date, '%Y-%m-%d').date()
        sponsor = sponsors.query.filter_by(id=sponsor_id).first()
        if sponsor:
            new_campaign = campaigns(campaign_name=campaign_name,campaign_desc=campaign_description,campaign_status=1,campaign_budget=campaign_budget,campaign_start_date=campaign_start_date,campaign_end_date=campaign_end_date,sponsor_id=sponsor_id,campaign_category = campaign_category)
            db.session.add(new_campaign)
            if campaign_start_date > campaign_end_date:
                flash("Start date cannot be greater than end date",'danger')
                return redirect(url_for('new_campaign',user_id=sponsor_id))
            if campaign_visibility == 'Public':
                new_campaign.campaign_visibility = 1
            else:
                new_campaign.campaign_visibility = 0
            db.session.commit()
            flash("Campaign created successfully",'success')
            flash("Manage Campaigns under Yours Campaigns section",'success')
            return redirect(url_for('sponsor_campaigns',user_id=sponsor_id))

# Deleting campaign
@app.route("/sponsor/delete_campaign/<int:campaign_id>", methods=["GET", "POST"])
def delete_campaign(campaign_id):
    ad_requests = adRequests.query.filter_by(campaign_id=campaign_id).all()
    for ad_request in ad_requests:
        db.session.delete(ad_request)
        db.session.commit()
    
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
            campaigns_dict[campaign.id]=[campaign.campaign_name,campaign.sponsor_id,campaign.campaign_desc,campaign.campaign_status,campaign.campaign_budget,campaign.campaign_start_date,campaign.campaign_end_date,campaign.campaign_category,campaign.campaign_visibility]
            today_date = datetime.now().date()
            if today_date > campaign.campaign_end_date:
                campaign.campaign_status = 2
                db.session.commit()
    return dict(campaigns_dict)

def get_sponsor_info(user_id):
    user = user_table.query.filter_by(id=user_id).first() #user_table data
    sponsor = sponsors.query.filter_by(id=user_id).first() #sponsor table data
    user_info = {}
    user_info[user_id] = [user.email,user.full_name,user.user_name,user.pwd,user.role,user.status]
    user_info[user_id].append(sponsor.industry)
    user_info[user_id].append(sponsor.budget)
    return dict(user_info)

def flagged_campaigns():
    campaigns_list = campaigns.query.filter_by(campaign_status=0).all()
    campaigns_dict={}
    for campaign in campaigns_list:
        if campaign.id not in campaigns_dict.keys():
            campaigns_dict[campaign.id]=[campaign.campaign_name,campaign.sponsor_id,campaign.campaign_desc,campaign.campaign_status,campaign.campaign_budget,campaign.campaign_start_date,campaign.campaign_end_date]
    return dict(campaigns_dict)


def get_influencers():
    influencers_list = influencers.query.all()
    influencers_dict={}
    for influencer in influencers_list:
        if influencer.id not in influencers_dict.keys():
            user_table_data = user_table.query.filter_by(id = influencer.id).first()
            influencers_dict[influencer.id] = []
            influencers_dict[influencer.id].append(user_table_data.full_name)
            influencers_dict[influencer.id].extend([influencer.category,influencer.niche,influencer.followers_count])
            influencers_dict[influencer.id].append(user_table_data.status)
    return dict(influencers_dict)
            
# search functionalities functions

# just for routing to the page
@app.route("/sponsor/search/<int:sponsor_id>" , methods=["GET", "POST"])
def search(sponsor_id):
    sponsor_info = get_sponsor_info(sponsor_id)
    influencers_list = get_influencers()
    return render_template("sponsor_templates/sponsor-search.html",id = sponsor_id,sponsor_info = sponsor_info)

# actual search

from sqlalchemy import text

@app.route("/sponsor/search/influencers/<int:sponsor_id>", methods=["GET", "POST"])
def search_influencers(sponsor_id):
    sponsor_info = get_sponsor_info(sponsor_id)
    campaigns_list = get_sponsor_campaigns(sponsor_id)
    influencers_list = {}

    if request.method == "POST":
        name = request.form.get('influencer_name', '')
        category = request.form.get('category', '')

        query = db.session.query(user_table, influencers).outerjoin(influencers)

        if name:
            query = query.filter(user_table.full_name.ilike(f'%{name}%'))
        
        if category:
            query = query.filter(influencers.category.ilike(f'%{category}%'))

        results = query.all()

        for user, influencer in results:
            influencers_list[influencer.id] = [
                user.full_name,
                influencer.category,
                influencer.niche,
                influencer.followers_count,
            
            ]

    return render_template(
        "sponsor_templates/sponsor-search.html", 
        id=sponsor_id, 
        sponsor_info=sponsor_info, 
        influencers_list=influencers_list,
        campaigns_list=campaigns_list
    )

# stats for the sponsor
def sponsor_total_campaigns(sponsor_id):
    return campaigns.query.filter_by(sponsor_id=sponsor_id).count()
def sponsor_total_expenditure(sponsor_id):
    ad_requests = adRequests.query.filter_by(sponsor_id=sponsor_id).all()
    total = 0
    for ad_request in ad_requests:
        if ad_request.status == 1:
            total = ad_request.payment_amount + total
    return total

def sponsor_total_ad_requests_completed(sponsor_id):
    return adRequests.query.filter_by(sponsor_id=sponsor_id,status=1).count()