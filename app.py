from flask import Flask
from flask_cors import CORS

from blueprints.dashboard import dashboard_bp
from blueprints.login import login_bp
from blueprints.manageCamera import manageCamera_bp
from blueprints.manageUsers import manageUsers_bp
from blueprints.userProfile import userProfile_bp
from blueprints.videoFeed import video_feed_bp
from blueprints.historicalRecords import historical_records_bp
import utils.firebase_init  # Import firebase_config to initialize Firebase

utils.firebase_init.initialize_firebase()

app = Flask(__name__)
CORS(app) 

# Additional security headers
@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(login_bp, url_prefix='/login')
app.register_blueprint(manageCamera_bp, url_prefix='/manageCamera')
app.register_blueprint(manageUsers_bp, url_prefix='/manageUsers')
app.register_blueprint(userProfile_bp, url_prefix='/userProfile')
app.register_blueprint(video_feed_bp, url_prefix='/videoFeed')
app.register_blueprint(historical_records_bp, url_prefix='/historicalRecords')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
