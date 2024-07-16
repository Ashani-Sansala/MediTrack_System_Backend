from flask import Flask
from flask_cors import CORS
from blueprints.dashboard import dashboard_bp
from blueprints.login import login_bp
from blueprints.manageCamera import manageCamera_bp
from blueprints.manageUsers import manageUsers_bp
from blueprints.userProfile import userProfile_bp
from blueprints.videoFeed import video_feed_bp
from blueprints.historicalRecords import historical_records_bp
import utils.firebase_init 
from utils.db_init import init_db  

def create_app():
    
    # Create and configure the Flask app.
    app = Flask(__name__)  # Create a Flask application instance
    CORS(app)  # Enable Cross-Origin Resource Sharing (CORS) for the app

    with app.app_context():
        init_db()  # Initialize the database within the Flask application context

    utils.firebase_init.initialize_firebase()  # Initialize Firebase SDK

    # Define additional security headers for all responses
    @app.after_request
    def add_security_headers(response):
        response.headers['Content-Security-Policy'] = "default-src 'self'"  # Set Content Security Policy
        response.headers['X-Content-Type-Options'] = 'nosniff'  # Prevent MIME sniffing
        response.headers['X-Frame-Options'] = 'DENY'  # Avoid clickjacking attacks
        response.headers['X-XSS-Protection'] = '1; mode=block'  # Enable XSS protection
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'  # Use strict Transport Security
        return response

    # Registering Blueprints for different parts of the application
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(login_bp, url_prefix='/login')
    app.register_blueprint(manageCamera_bp, url_prefix='/manageCamera')
    app.register_blueprint(manageUsers_bp, url_prefix='/manageUsers')
    app.register_blueprint(userProfile_bp, url_prefix='/userProfile')
    app.register_blueprint(video_feed_bp, url_prefix='/videoFeed')
    app.register_blueprint(historical_records_bp, url_prefix='/historicalRecords')

    return app  # Return the configured Flask app instance

app = create_app()  # Create the Flask app instance

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Run the Flask app with debug mode enabled
