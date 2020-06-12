from flask import Blueprint, render_template, session, redirect,\
     url_for, flash, request
from .forms import EditUserForm
from ..models import db, User, Show, Watched_show
from ..utils.auth_utils import login_required
from ..utils.user_utils import add_to_user_queue


user = Blueprint('user', __name__, template_folder='templates',
                 static_folder='static')


# Render user dashboard
@user.route('/')
@login_required
def user_dashboard():
    username = session['username']
    cur_user = User.query.get_or_404(username)
    user_shows_list = Watched_show.query.filter(
        Watched_show.user_id == cur_user.username).all()
    result = db.engine.execute(
        "SELECT shows.name,  COUNT( show_id), show_id FROM watched_shows JOIN  shows ON watched_shows.show_id = shows.id  GROUP BY show_id, shows.name ORDER BY COUNT(show_id) DESC LIMIT 5;")
    names = [row for row in result]
    return render_template('user_dashboard.html', shows=user_shows_list, top_shows=names)

# Allow user to track show and add to DB if not there
@user.route('/trackShow', methods=['POST'])
@login_required
def track_show():
    form = request.form
    username = session['username']
    cur_user = User.query.get_or_404(username)
    add_to_user_queue(username, cur_user, form)
    return redirect(url_for('user.user_dashboard'))

# Render user profile
@user.route('/<username>/profile')
@login_required
def user_profile(username):
    username = session['username']
    curr_user = User.query.get_or_404(username)
    return render_template('profile.html', user=curr_user)

# Edit user profile
@user.route('/<username>/edit', methods=["GET", "POST"])
@login_required
def edit_profile(username):
    username = session['username']
    curr_user = User.query.get_or_404(username)
    form = EditUserForm(obj=curr_user)

    # Validate user form
    if form.validate_on_submit():
        if User.authenticate(username, form.password.data):
            curr_user.first_name = form.first_name.data
            curr_user.last_name = form.last_name.data
            curr_user.email = form.email.data
            db.session.commit()
            return redirect(url_for('user.user_profile', username=username))
        else:
            flash("Failed password", "danger")
            return redirect(url_for('user.user_profile', username=username))
    return render_template('edit_user.html', form=form)


# Delete user profile
@user.route('/<username>/delete', methods=["GET", "POST"])
@login_required
def delete_profile(username):
    username = session['username']
    curr_user = User.query.get_or_404(username)
    db.session.delete(curr_user)
    db.session.commit()
    flash("Profile Deleted", "succes")
    return redirect(url_for('logout'))


