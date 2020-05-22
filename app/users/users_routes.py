from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from flask_security import Security, SQLAlchemyUserDatastore, login_required
from .forms import RegisterUserForm
from ..models import db, User, Show, Watched_show
from show_request import seasons_search, seasons_episodes


user = Blueprint('user', __name__, template_folder='templates',
                 static_folder='static')


@user.route('/')
def user_dashboard():
    if 'username' in session:
        username = session['username']
        cur_user = User.query.get_or_404(username)
        user_shows_list = Watched_show.query.filter(
            Watched_show.user_id == cur_user.username).all()
        return render_template('user_dashboard.html', shows=user_shows_list)

    flash('Please login to view this page')
    return redirect(url_for('landing'))


@user.route('/trackShow', methods=['POST'])
def track_show():
    if 'username' in session:
        form = request.form
        username = session['username']
        cur_user = User.query.get_or_404(username)

        user_show = Show.query.filter(form['api_id'] == Show.api_id).first()
        if not user_show:
            user_show = Show(name=form['name'], rating=form['rating'],
                             summary=form['summary'], url=form['url'], api_id=form['api_id'], img_url=form['img_url'])
            db.session.add(user_show)
            db.session.commit()
       

        user_watched = Watched_show(
            user_id=cur_user.username, show_id=user_show.id)
        db.session.add(user_watched)
        db.session.commit()

      
        return redirect(url_for('user.user_dashboard'))
    flash('Please login to view this page')
    return redirect(url_for('landing'))
