from flask import Flask,render_template,request,flash,redirect,url_for
from datetime import datetime
from flask import current_app as app # current running app
from .models import *


@app.route("/sponsor/manage_ad_requests/<int:campaign_id>", methods=["GET", "POST"])
def manage_requests(campaign_id):
    return render_template("sponsor_templates/campaign-ad-requests.html",campaign_id = campaign_id)