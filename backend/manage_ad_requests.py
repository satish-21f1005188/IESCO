from flask import Flask,render_template,request,flash,redirect,url_for
from datetime import datetime
from flask import current_app as app # current running app
from .models import *
from .sponsor_controllers import *
from .influencer_controllers import *
from .controllers import *

# sponsor ad request

@app.route("/sponsor/send_request/<int:sponsor_id>/<int:influencer_id>", methods=["GET", "POST"])
def send_request(sponsor_id,influencer_id):
    if request.method == "POST":
        campaign_id = request.form['campaign_id']
        adRequestMessage = request.form['adRequestMessage']
        adRequestPayment = request.form['adRequestPayment']
        ad_request = adRequests.query.filter_by(campaign_id=campaign_id,influencer_id=influencer_id).first()
        campaign = campaigns.query.filter_by(id=campaign_id).first()
        if not ad_request :
            if int(adRequestPayment) > campaign.campaign_budget:
                flash("Budget is not enough for this ad request",'danger')
                flash(f"Enter amount less than or equal to {campaign.campaign_budget}", 'danger')
                return redirect(url_for('search_influencers',sponsor_id=sponsor_id))
            new_ad_request = adRequests(campaign_id=campaign_id,influencer_id= influencer_id,sponsor_id=sponsor_id,message=adRequestMessage,payment_amount=adRequestPayment)
            campaign.campaign_budget = campaign.campaign_budget - int(adRequestPayment)
            db.session.add(new_ad_request)
            db.session.commit()
            flash("Ad request sent successfully",'success')
        else:
            flash("Ad request already exists",'danger')

    return redirect(url_for('search_influencers',sponsor_id=sponsor_id)) 


# influencer ad request
@app.route("/influencer/send_request/<int:sponsor_id>/<int:influencer_id>", methods=["GET", "POST"])
def influencer_send_request(sponsor_id,influencer_id):
    if request.method == "POST":
        campaign_id = request.form['adRequestId']
        adRequestMessage = request.form['adRequestMessage']
        adRequestPayment = request.form['adRequestPayment']
        ad_request = adRequests.query.filter_by(campaign_id=campaign_id,influencer_id=influencer_id).first()
        campaign = campaigns.query.filter_by(id=campaign_id).first()
        if not ad_request :
            if int(adRequestPayment) > campaign.campaign_budget:
                flash("Budget is not enough for this ad request",'danger')
                flash(f"Enter amount less than or equal to {campaign.campaign_budget}", 'danger')
                return redirect(url_for('search_influencers',sponsor_id=sponsor_id))
            new_ad_request = adRequests(campaign_id=campaign_id,influencer_id= influencer_id,sponsor_id=sponsor_id,message=adRequestMessage,payment_amount=adRequestPayment,requested_by = 2)
            campaign.campaign_budget = campaign.campaign_budget - int(adRequestPayment)
            db.session.add(new_ad_request)
            db.session.commit()
            flash("Ad request sent successfully",'success')
        else:
            flash("Ad request already exists",'danger')
    return redirect(url_for('influencer_search_campaigns',influencer_id=influencer_id))

# sponsor manage_requests
@app.route("/sponsor/manage_requests/<int:campaign_id>",methods = ["GET","POST"])
def manage_requests(campaign_id):
    ad_requests = get_ad_requests(campaign_id)
    campaign = campaigns.query.filter_by(id=campaign_id).first()
    id = campaign.sponsor_id
    campaign_info = [campaign.campaign_name,campaign.campaign_desc,campaign.campaign_start_date,campaign.campaign_end_date,campaign.campaign_budget]
    

    return render_template("sponsor_templates/manage-requests.html",ad_requests = ad_requests,campaign_info = campaign_info,id = id)   

# influencer manage_requests
@app.route("/influencer/manage_requests/<int:influencer_id>",methods = ["GET","POST"])
def influencer_manage_requests(influencer_id):
    ad_requests = get_ad_requests_by_influencer(influencer_id)
    influencer_info = get_influencer_info(influencer_id)
    return render_template("influencers_templates/influencer-manage-requests.html",ad_requests = ad_requests,id = influencer_id,influencer_info = influencer_info)


# get ad requests by campaign id
def get_ad_requests(campaign_id):
    ad_requests = adRequests.query.filter_by(campaign_id = campaign_id).all()
    ad_requests_list = {}
    for ad_request in ad_requests:
        sponsor = user_table.query.filter_by(id=ad_request.sponsor_id).first()
        ad_requests_list[ad_request.id] = [sponsor.full_name,ad_request.message,ad_request.payment_amount,ad_request.status,ad_request.requested_by]
    return dict(ad_requests_list)
    
# get ad requests by influencer id
def get_ad_requests_by_influencer(influencer_id):
    ad_requests = adRequests.query.filter_by(influencer_id = influencer_id).all()
    ad_requests_list = {}
    for ad_request in ad_requests:
        influencer = user_table.query.filter_by(id=ad_request.influencer_id).first()
        ad_requests_list[ad_request.id] = [influencer.full_name,ad_request.message,ad_request.payment_amount,ad_request.status,ad_request.requested_by]
    return dict(ad_requests_list)
    
# accepting ad request
@app.route("/sponsor/accept_request/<int:ad_request_id>",methods = ["GET","POST"])
def accept_request(ad_request_id):
    ad_request = adRequests.query.filter_by(id=ad_request_id).first()
    campaign_id = ad_request.campaign_id
    ad_request.status = 1
    db.session.commit()
    flash("Ad request accepted successfully",'success')
    return redirect(url_for('manage_requests',campaign_id = campaign_id))

# rejecting ad request
@app.route("/sponsor/reject_request/<int:ad_request_id>",methods = ["GET","POST"])
def reject_request(ad_request_id):
    ad_request = adRequests.query.filter_by(id=ad_request_id).first()
    campaign_id = ad_request.campaign_id
    ad_request.status = 0
    db.session.commit()
    flash("Ad request rejected successfully",'danger')
    return redirect(url_for('manage_requests',campaign_id = campaign_id))