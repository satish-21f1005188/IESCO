from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() #Instance of SQLAlchemy

class table_1(db.Model):
    __tablename__ = "table_1"
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String,nullable=False)
    full_name=db.Column(db.String,nullable=False)
    user_name=db.Column(db.String,nullable=False)
    pwd=db.Column(db.String,nullable=False)
    role=db.Column(db.Integer,nullable=False,default=1)
