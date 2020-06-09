from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from .forms import EditUserForm
from ..models import db, User, Show, Watched_show
from ..utils.auth_utils import login_required


user = Blueprint('user', __name__, template_folder='templates',
                 static_folder='static')


@user.route('/')
@login_required
def user_dashboard():
    username = session['username']
    cur_user = User.query.get_or_404(username)
    user_shows_list = Watched_show.query.filter(
        Watched_show.user_id == cur_user.username).all()
    # top_shows = db.session.query(Watched_show.show_id, Show.name).join(Show, Watched_show.show_id == Show.id).group_by(Watched_show.show_id).all()
    result = db.engine.execute(
        "SELECT shows.name,  COUNT( show_id), show_id FROM watched_shows JOIN  shows ON watched_shows.show_id = shows.id  GROUP BY show_id, shows.name ORDER BY COUNT(show_id) DESC LIMIT 5;")
    names = [row for row in result]
    print(names)
    return render_template('user_dashboard.html', shows=user_shows_list, top_shows=names)


@user.route('/trackShow', methods=['POST'])
@login_required
def track_show():
    form = request.form
    username = session['username']
    cur_user = User.query.get_or_404(username)

    user_show = Show.query.filter(form['api_id'] == Show.api_id).first()
    if not user_show:
        user_show = Show(name=form['name'], rating=form['rating'],
                         summary=form['summary'], url=form['url'], api_id=form['api_id'], img_url=form['img_url'])
        db.session.add(user_show)
        db.session.commit()
    is_watching = Watched_show.query.filter(
        cur_user.username == Watched_show.user_id, Watched_show.show_id == user_show.id).all()
    if not is_watching:
        user_watched = Watched_show(
            user_id=cur_user.username, show_id=user_show.id)
        db.session.add(user_watched)
        db.session.commit()
        return redirect(url_for('user.user_dashboard'))
    return redirect(url_for('user.user_dashboard'))


@user.route('/<username>/profile')
@login_required
def user_profile(username):
    username = session['username']
    curr_user = User.query.get_or_404(username)

    return render_template('profile.html', user=curr_user)


@user.route('/<username>/edit', methods=["GET", "POST"])
@login_required
def edit_profile(username):
    username = session['username']
    curr_user = User.query.get_or_404(username)
    form = EditUserForm(obj=curr_user)
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
