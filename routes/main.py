from flask import Blueprint, redirect, redirect, render_template, url_for, request
from flask_login import login_required, current_user
from extensions import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # username automatically accessible via current_user
    return render_template('dashboard.html')








