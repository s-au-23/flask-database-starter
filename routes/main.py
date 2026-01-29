from flask import Blueprint, redirect, redirect, render_template, url_for, request
from flask_login import login_required, current_user
from extensions import db
from models import Product
main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # username automatically accessible via current_user
    return render_template('dashboard.html')

@main_bp.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']

        product = Product(
            name=name,
            price=price,
            user_id=current_user.id
        )
        db.session.add(product)
        db.session.commit()

        return redirect(url_for('main.dashboard'))

    return render_template('add_product.html')




@main_bp.route('/edit-product/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = request.form['price']
        db.session.commit()
        return redirect(url_for('main.dashboard'))
    return render_template('edit_product.html', product=product)


@main_bp.route('/delete-product/<int:id>')
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('main.dashboard'))  