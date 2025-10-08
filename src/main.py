import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db, User
from src.models.link import Link
from src.models.tracking_event import TrackingEvent
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.links import links_bp
from src.routes.track import track_bp
from src.routes.events import events_bp
from src.routes.analytics import analytics_bp
from src.routes.campaigns import campaigns_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), '..', 'src', 'static'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ej5B3Amppi4gjpbC65te6rJuvJzgVCWW_xfB-ZLR1TE')

# Enable CORS for all routes
CORS(app, supports_credentials=True)

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(links_bp, url_prefix='/api')
app.register_blueprint(analytics_bp, url_prefix='/api')
app.register_blueprint(campaigns_bp, url_prefix='/api')
app.register_blueprint(track_bp)
app.register_blueprint(events_bp)

# Database configuration - use SQLite for testing
database_url = os.environ.get('DATABASE_URL')
if database_url and 'postgresql' in database_url:
    # Production - PostgreSQL (Neon)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Development/Testing - SQLite fallback
    os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'src', 'database'), exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), '..', 'src', 'database', 'app.db')}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()
    # Create default admin user if not exists
    if not User.query.filter_by(username="Brain").first():
        admin_user = User(username="Brain", email="admin@brainlinktracker.com")
        admin_user.set_password("Mayflower1!!")
        db.session.add(admin_user)
        db.session.commit()
        print("Default admin user \"Brain\" created.")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    # Skip API routes - let them be handled by blueprints
    if path.startswith('api/'):
        return "API route not found", 404
    
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

