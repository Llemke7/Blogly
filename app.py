"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'supersecret'

toolbar = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.create_all()

@app.route('/')
def list_users():
    """homepage with users"""
    users = User.query.all()
    return render_template('list.html', users = users)

@app.route('/', methods=["POST"])
def new_user():
    """Create new User"""
    
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/user/{new_user.id}")

@app.route('/user/<int:user_id>') 
def show_user (user_id):
    """Show User"""
    user = User.query.get(user_id)
    return render_template ("details.html", user= user)



@app.route('/user/<int:user_id>/edit', methods=["GET", "POST"])
def edit_user(user_id):
    """Edit User"""
    user = User.query.get(user_id)

    if request.method == "POST":
        user.first_name = request.form["first_name"]
        user.last_name = request.form["last_name"]
        user.image_url = request.form["image_url"]

        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(f"/user/{user.id}")

    return render_template("edit.html", user=user)

@app.route('/user/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete User"""
    user = User.query.get_or_404(user_id)
    user_name = f"{user.first_name} {user.last_name}" 
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user_name} deleted.")
    return redirect(url_for('list_users'))
