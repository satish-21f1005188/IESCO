from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Instance of SQLAlchemy

class user_table(db.Model):
    __tablename__ = "user_table"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    user_name = db.Column(db.String, nullable=False)
    pwd = db.Column(db.String, nullable=False)
    role = db.Column(db.Integer, nullable=False, default=1)
    
    

class influencers(db.Model):
    __tablename__ = "influencers"
    id = db.Column(db.Integer, db.ForeignKey('user_table.id'), primary_key=True)
    category = db.Column(db.String, nullable=False)
    niche = db.Column(db.String, nullable=False)
    followers_count = db.Column(db.Integer, nullable=False)

class sponsors(db.Model):
    __tablename__ = "sponsors"
    id = db.Column(db.Integer, db.ForeignKey('user_table.id'), primary_key=True)
    industry = db.Column(db.String, nullable=False)
    budget = db.Column(db.Integer, nullable=False)

# Relationship to Influencers and Sponsors
user_influencer = db.relationship("Influencers", backref="user")
user_sponsor = db.relationship("Sponsors", backref="user")

