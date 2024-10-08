from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Instance of SQLAlchemy

class user_table(db.Model):
    __tablename__ = "user_table"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    user_name = db.Column(db.String, nullable=False)
    pwd = db.Column(db.String, nullable=False)
    role = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer,nullable = False,default = 1)
    # Relationship to Influencers and Sponsors
    user_influencer = db.relationship("influencers", backref="user")
    user_sponsor = db.relationship("sponsors", backref="user")
    
    

class influencers(db.Model):
    __tablename__ = "influencers"
    id = db.Column(db.Integer, db.ForeignKey('user_table.id'), primary_key=True)
    category = db.Column(db.String, nullable=False)
    niche = db.Column(db.String, nullable=False)
    followers_count = db.Column(db.Integer, nullable=False)
    earnings = db.Column(db.Integer,nullable = False,default = 0)

class sponsors(db.Model):
    __tablename__ = "sponsors"
    id = db.Column(db.Integer, db.ForeignKey('user_table.id'), primary_key=True)
    industry = db.Column(db.String, nullable=False)
    budget = db.Column(db.Integer, nullable=False)


class campaigns(db.Model):
    __tablename__ = "campaigns"
    id = db.Column(db.Integer, primary_key=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsors.id'))
   
    campaign_name = db.Column(db.String, nullable=False)
    campaign_desc = db.Column(db.String, nullable=False)
    campaign_status = db.Column(db.Integer, nullable=False, default=0)
    campaign_budget = db.Column(db.Integer, nullable=False)
    campaign_start_date = db.Column(db.Date, nullable=False)
    campaign_end_date = db.Column(db.Date, nullable=False)
    campaign_category = db.Column(db.String)
    # 1 for public, 0 for private
    campaign_visibility = db.Column(db.Integer, nullable=False, default=1)
    
    
    # Relationship to Influencers and Sponsors
    
    campaign_sponsor = db.relationship("sponsors", backref="campaign")

class adRequests(db.Model):
    __tablename__ = "adRequests"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'))
    influencer_id = db.Column(db.Integer,db.ForeignKey('influencers.id'))
    sponsor_id = db.Column(db.Integer,db.ForeignKey('sponsors.id'))
    # 2 for pending, 1 for accepted, 0 for rejected
    status = db.Column(db.Integer, nullable=False, default=2)
    payment_amount = db.Column(db.Integer,nullable = False,default = 0)
    payment_status = db.Column(db.Integer,nullable = False,default = 2 )
    message = db.Column(db.String,nullable = False)
    # 1 is requested by the sponsor, 2 is requested by the influencer
    requested_by = db.Column(db.Integer,nullable = False,default = 1)


    # Relationship to Influencers and Sponsors
    adRequests_campaign = db.relationship("campaigns", backref="adRequests")
    adRequests_influencer = db.relationship("influencers", backref="adRequests")
    adRequests_sponsor = db.relationship("sponsors", backref="adRequests")

