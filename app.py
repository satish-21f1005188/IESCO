from flask import Flask,render_template,session
from backend.models import *


def init_app():
    app = Flask(__name__)
    app.debug = True
    app.app_context().push()
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///iesco.sqlite3"
    db.init_app(app)
    print("App started")
    return app
    

app = init_app()
app.secret_key = '5#y2L"F4Q8z\n\xec]/'

from backend.controllers import *
from backend.sponsor_controllers import *
from backend.manage_ad_requests import *
from backend.influencer_controllers import *

if __name__ == '__main__':
    app.run(debug=True)
