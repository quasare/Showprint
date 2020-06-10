from flask import session
from ..models import db, Show, Season, Episode, \
    Watched_episode, Watched_show, Watched_season
from .show_api_utils import seasons_search, seasons_episodes


# **************************** SHOW LOGIC ****************************

# Mark show as currently watching for user
def watch_show(id):
    username = session['username']
    show = Watched_show.query.filter(
        Watched_show.user_id == username, Watched_show.show_id == id).first()
    watching = show.watching = True
    db.session.commit()

# Remove show from currently watching and add back to show of interest
def unwatch_show(id):
    username = session['username']
    show = Watched_show.query.filter(
        Watched_show.user_id == username, Watched_show.show_id == id).first()
    watching = show.watching = False
    db.session.commit()    

# Mark show as not currently watching for user
def delete_show(id):
    username = session['username']
    show = Watched_show.query.filter(
        Watched_show.user_id == username, Watched_show.show_id == id).first()
    db.session.delete(show)
    db.session.commit()


# *************************** SEASON LOGIC ***************************

# Mark season watched in DB
def toggle_season(s_id, username):
    in_db = Watched_season.query.filter(
        Watched_season.season_id == s_id, Watched_season.user_id == username).first()
    if not in_db:
        new_watched_ep = Watched_season(
            user_id=username, season_id=s_id, finished=True)
        db.session.add(new_watched_ep)
        db.session.commit()
    elif in_db:
        db.session.delete(in_db)
        db.session.commit()
    return

# Take data from front-end and toggle season as watched
def handle_season(season, id, season_id):
    username = session['username']
    show = Show.query.get_or_404(id)
    season_idx = (int(season) - 1)
    ep_list = show.seasons[season_idx].episodes
    toggle_season(season_id, username)
    for e in ep_list:
        toggle_ep(e.id, username)


# ************************ EPISODE LOGIC ************************

# Logic to query episodes for show
def get_episodes(id):
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

# Function to mark episode watched in DB
def toggle_ep(ep_id, username):
    in_db = Watched_episode.query.filter(
        Watched_episode.ep_id == ep_id, Watched_episode.user_id == username).first()
    if not in_db:
        new_watched_ep = Watched_episode(
            user_id=username, ep_id=ep_id, finished=True)
        db.session.add(new_watched_ep)
        db.session.commit()
    elif in_db:
        db.session.delete(in_db)
        db.session.commit()
    return









