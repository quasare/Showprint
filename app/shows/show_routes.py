from flask import Blueprint, render_template, session,  \
    redirect, url_for, jsonify, request
from .forms import SearchForm, AddShowForm
from ..models import db, Search, Show, Episode
from ..utils.auth_utils import login_required
from ..utils.show_api_utils import shows_search
from ..utils.youtube_utils import youtube_search
from ..utils.show_utils import toggle_ep, get_episodes,\
    watch_show, delete_show, unwatch_show, handle_season


shows = Blueprint('shows', __name__, template_folder='templates',
                  static_folder='static')

# Route to search TV shows
@shows.route('/', methods=['POST', 'GET'])
@login_required
def show_home():
    form = SearchForm()

    # Validate search form
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


@shows.route('/nav_search')
@login_required
def nav_search():
    form = AddShowForm()
    show = request.args.get('q')
    if not show:
        res = shows_search('mash')
    else:
        res = shows_search(show)

    return render_template('search_results.html', res=res, form=form)

# Search results
@shows.route('/results')
@login_required
def search_results():
    form = AddShowForm()
    show = session['search']
    res = shows_search(show)
    return render_template('search_results.html', res=res, form=form)

# Get Episodes for shows
@shows.route('/submit/<id>')
@login_required
def submit(id):
    in_db = Episode.query.filter(Episode.show_id == id).first()
    if not in_db:
        get_episodes(id)
        return redirect(url_for('shows.show_detail', id=id))
    return redirect(url_for('shows.show_detail', id=id))

# Render show detail page
@shows.route('/detail/<id>')
@login_required
def show_detail(id):
    username = session['username']
    show = Show.query.get_or_404(id)

    # Request youtube recap vids
    recap_vids = youtube_search(f'{show.name} preview')
    return render_template('show_detail.html', show=show, vid=recap_vids)

# Route to handle ajax logic to mark Episodes as watched
@shows.route('/watch_ep', methods=['POST'])
@login_required
def watched_ep():
    # Handle ajax post from Frontend
    watched_ep = request.json['userEp'].split(' ')
    ep_id, username = watched_ep

    toggle_ep(ep_id, username)
    return jsonify({"res": 'success'})

# Mark shows a currenlty watching for Current User
@shows.route('/watching/<id>', methods=['POST', 'GET'])
@login_required
def cur_watching_show(id):
    watch_show(id)
    return redirect(url_for('user.user_dashboard'))

# Remove show from currently watching and add back to show of interest
@shows.route('/remove_watching/<id>')
@login_required
def remove_watching(id):
    unwatch_show(id)
    return redirect(url_for('user.user_dashboard'))

#  Delete show from users list of shows
@shows.route('/remove/<id>', methods=['POST', 'GET'])
@login_required
def remove_show(id):
    delete_show(id)
    return redirect(url_for('user.user_dashboard'))

# Mark season as watched for AJAX request
@shows.route('/watch_season', methods=['POST'])
@login_required
def watch_season():
    watched_s = request.json['season'].split(' ')
    season, id, season_id = watched_s
    handle_season(season, id, season_id)
    return redirect(url_for('shows.show_detail', id=id))
