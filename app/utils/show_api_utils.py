import requests

BASE_URL = 'http://api.tvmaze.com'

# Search api for show


def shows_search(show):
    payload = {'q': f'{show}'}
    r = requests.get(f'{BASE_URL}/search/shows', params=payload)
    first_nine = r.json()[:9]
    showList = [serialize_show(s) for s in first_nine]
    return showList

# Search api for seasons


def seasons_search(show_id):
    r = requests.get(f'{BASE_URL}/shows/{show_id}/seasons').json()
    season_list = [serialize_season(s) for s in r]
    return season_list

# Search api for Episodes


def seasons_episodes(season_id):
    r = requests.get(f'{BASE_URL}/seasons/{season_id}/episodes').json()
    ep_list = [serialize_ep(e, season_id) for e in r]
    return ep_list


# **********************************Format API Data**************************

# Format and extract show response data
def serialize_show(show):
    if show['show']['image']:
        api_url = show['show']['image']['medium']
    else:
        api_url = 'static/imgs/show_placeholder.jpg'

    if show['show']['rating']['average']:
        show_rating = show['show']['rating']['average']
    else:
        show_rating = 0

    show_obj = {
        'name': show['show']['name'],
        'rating': show_rating,
        'summary': show['show']['summary'],
        'api_id': show['show']['id'],
        'url': show['show']['officialSite'],
        'img_url': api_url
    }
    return show_obj

# Format and extract Season data


def serialize_season(season):
    season_obj = {
        'season_num': season['number'],
        'api_id': season['id'],
    }
    return season_obj

# Format and extract episode data


def serialize_ep(ep, id):
    ep_object = {
        'name': ep['name'],
        'summary': ep['summary'],
        'api_id': ep['id'],
        'ep_num': ep['number'],
        'season_num': ep['season'],
        'season_id': id
    }
    return ep_object
