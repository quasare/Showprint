from flask import session, redirect, url_for, request
from ..models import db, User, Show, Watched_show


# Logic to add show to db and to db for user and check if adding
def add_to_user_queue(username, cur_user, form):
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