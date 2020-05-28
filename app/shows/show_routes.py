from flask import Blueprint, render_template, session, redirect, url_for, flash, jsonify, request
from .forms import SearchForm, AddShowForm
from show_request import shows_search
from ..models import db, Search, Show, Season, Episode, Watched_episode
from show_request import seasons_search, seasons_episodes

shows = Blueprint('shows', __name__, template_folder='templates',
                  static_folder='static')


@shows.route('/', methods=['POST', 'GET'])
def show_home():
    if 'username' in session:
        form = SearchForm()
        if form.validate_on_submit():

            show = form.search.data
            existing_search = Search.query.filter(
                show == Search.search_value).first()
            if not existing_search:
                new_search = Search(search_value=show)
                db.session.add(new_search)
                db.session.commit()

            session['search'] = show
            return redirect(url_for('shows.search_results'))
        return render_template('show_home.html', form=form)
    flash('Please login to view this page')
    return redirect(url_for('landing'))


@shows.route('/results')
def search_results():
    if 'username' in session:
        form = AddShowForm()
        show = session['search']
        res = shows_search(show)
        return render_template('search_results.html', res=res, form=form)
    flash('Please login to view this page')
    return redirect(url_for('landing'))


@shows.route('/submit/<id>')
def submit(id):
    if 'username' in session:
        in_db = Episode.query.filter(Episode.show_id == id).first()
        print(in_db)
        if not in_db:
            ep_list = []
            show = Show.query.get_or_404(id)
            season = seasons_search(show.api_id)
            season_list = [Season(season_num=s['season_num'],
                                  api_id=s['api_id'], show_id=show.id) for s in season]
            db.session.add_all(season_list)
            db.session.commit()
            eps = [seasons_episodes(s.api_id) for s in season_list]
            for s_e in eps:
                for e in s_e:
                    new_ep = Episode(name=e['name'], season_id=e['season_id'], summary=e['summary'],
                                     number=e['ep_num'], api_id=e['api_id'], show_id=show.id)

                    ep_list.append(new_ep)
            db.session.add_all(ep_list)
            db.session.commit()

            return redirect(url_for('shows.show_detail', id=id))
        return redirect(url_for('shows.show_detail', id=id))
    flash('Please login to view this page')
    return redirect(url_for('landing'))


@shows.route('/detail/<id>')
def show_detail(id):
    if 'username' in session:
        show = Show.query.get_or_404(id)
        return render_template('show_detail.html', show=show)
    flash('Please login to view this page')
    return redirect(url_for('landing'))


@shows.route('/watched', methods=['POST'])
def watched_show():
    if 'username' in session:
        watched_ep = request.json['userEp'].split(' ')
        ep_id, username = watched_ep
        in_db = Watched_episode.query.filter(
            Watched_episode.ep_id == ep_id, Watched_episode.user_id == username).first()
        if not in_db:
            new_watched_ep = Watched_episode(
                user_id=username, ep_id=ep_id, finished=True)
            db.session.add(new_watched_ep)
            db.session.commit()
            return jsonify(res='success')
        elif in_db:
            db.session.delete(in_db)
            db.session.commit()
            return jsonify(res='success')
    flash('Please login to view this page')
    return redirect(url_for('landing'))

# ep_list = []
#         show = Show.query.get_or_404(id)
#         season = seasons_search(show.api_id)
#         season_list = [Season(season_num=s['season_num'],
#                               api_id=s['api_id'], show_id=show.id) for s in season]
#         db.session.add_all(season_list)
#         db.session.commit()
#         eps = [seasons_episodes(s.api_id) for s in season_list]
#         for s_e in eps:
#             for e in s_e:
#                 new_ep = Episode(name=e['name'], season_id=e['season_id'], summary=e['summary'],
#                                  number=e['ep_num'], api_id=e['api_id'], show_id=show.id)

#                 ep_list.append(new_ep)
#         db.session.add_all(ep_list)
#         db.session.commit()
