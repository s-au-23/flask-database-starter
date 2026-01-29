from flask import Flask, redirect, url_for, render_template
from flask_login import LoginManager, current_user, login_required
from extensions import db
from routes.auth import auth_bp
from routes.main import main_bp
from models import User

# 1️⃣ Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 2️⃣ Initialize extensions
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # where to redirect if not logged in
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# 3️⃣ Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)

# 4️⃣ Default route
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

# 5️⃣ Create database tables
with app.app_context():
    db.create_all()

# 6️⃣ Run the app
if __name__ == "__main__":
    app.run(debug=True)
