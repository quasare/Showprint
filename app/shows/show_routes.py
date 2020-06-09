from flask import Blueprint, render_template, session,  \
    redirect, url_for, flash, jsonify, request
from .forms import SearchForm, AddShowForm
from ..models import db, Search, Show, Season, Episode, \
    Watched_episode, Watched_show, Watched_season
from ..utils.auth_utils import login_required
from ..utils.show_api_utils import seasons_search, seasons_episodes, shows_search
from ..utils.youtube_utils import youtube_search
from ..utils.show_utils import toggle_ep, toggle_season


shows = Blueprint('shows', __name__, template_folder='templates',
                  static_folder='static')


# 
@shows.route('/', methods=['POST', 'GET'])
@login_required
def show_home():
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


@shows.route('/results')
@login_required
def search_results():
    form = AddShowForm()
    show = session['search']
    res = shows_search(show)
    return render_template('search_results.html', res=res, form=form)


@shows.route('/submit/<id>')
@login_required
def submit(id):
    in_db = Episode.query.filter(Episode.show_id == id).first()
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


@shows.route('/detail/<id>')
@login_required
def show_detail(id):
    username = session['username']
    show = Show.query.get_or_404(id)
    user_season = Watched_season.query.filter()
    user_ep = Watched_episode.query.filter(Watched_episode.user_id == username).all()
    recap_vids = youtube_search(f'{show.name} preview') 

    return render_template('show_detail.html', show=show,vid=recap_vids )


@shows.route('/watch_ep', methods=['POST'])
@login_required
def watched_ep():
    watched_ep = request.json['userEp'].split(' ')
    ep_id, username = watched_ep
    in_db = Watched_episode.query.filter(
        Watched_episode.ep_id == ep_id, Watched_episode.user_id == username).first()
    toggle_ep(ep_id, username)
    return jsonify(res='success')


@shows.route('/watching/<id>', methods=['POST', 'GET'])
@login_required
def cur_watching_show(id):
    username = session['username']
    show = Watched_show.query.filter(
        Watched_show.user_id == username, Watched_show.show_id == id).first()
    watching = show.watching = True
    db.session.commit()
    return redirect(url_for('user.user_dashboard'))


@shows.route('/remove/<id>', methods=['POST', 'GET'])
@login_required
def remove_show(id):
    username = session['username']
    show = Watched_show.query.filter(
        Watched_show.user_id == username, Watched_show.show_id == id).first()
    db.session.delete(show)
    db.session.commit()
    return redirect(url_for('user.user_dashboard'))


@shows.route('/remove_watching/<id>')
@login_required
def remove_watching(id):
    username = session['username']
    show = Watched_show.query.filter(
        Watched_show.user_id == username, Watched_show.show_id == id).first()
    watching = show.watching = False
    db.session.commit()
    return redirect(url_for('user.user_dashboard'))


@shows.route('/watch_season', methods=['POST'])
@login_required
def watch_season():
    username = session['username']
    watched_s = request.json['season'].split(' ')

    season, id, season_id = watched_s
    show = Show.query.get_or_404(id)
    s = (int(season) - 1)
    ep_list = show.seasons[s].episodes
    Season_bool = show.seasons[s].watched
    toggle_season(season_id, username)
    for e in ep_list:
        toggle_ep(e.id, username)
    return redirect(url_for('shows.show_detail', id=id))
