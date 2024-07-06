from flask import Flask
from flask_cors import CORS
from datetime import timedelta

from blueprints.dashboard import dashboard_bp
from blueprints.login import login_bp
from blueprints.manageCamera import manageCamera_bp
from blueprints.manageUsers import manageUsers_bp
from blueprints.userProfile import userProfile_bp
from blueprints.historicalRecords import historical_records_bp

app = Flask(__name__)
CORS(app) 

app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(login_bp, url_prefix='/login')
app.register_blueprint(manageCamera_bp, url_prefix='/manageCamera')
app.register_blueprint(manageUsers_bp, url_prefix='/manageUsers')
app.register_blueprint(userProfile_bp, url_prefix='/userProfile')
app.register_blueprint(historical_records_bp, url_prefix='/historicalRecords')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
