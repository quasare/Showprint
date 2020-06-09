import requests

BASE_URL = 'http://api.tvmaze.com'


def shows_search(show):
    payload = {'q': f'{show}'}
    r = requests.get(f'{BASE_URL}/search/shows', params=payload)
    first_nine = r.json()[:9]
    showList = [serialize_show(s) for s in first_nine]
    return showList


def seasons_search(show_id):
    r = requests.get(f'{BASE_URL}/shows/{show_id}/seasons').json()
    season_list = [serialize_season(s) for s in r]
    return season_list


def seasons_episodes(season_id):
    r = requests.get(f'{BASE_URL}/seasons/{season_id}/episodes').json()
    ep_list = [serialize_ep(e, season_id) for e in r]
    return ep_list


def serialize_show(show):
    if show['show']['image']:
        api_url = show['show']['image']['medium']
    else:
        api_url = 'app/static/imgs/show_placholder.jpg'

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


def serialize_season(season):
    season_obj = {
        'season_num': season['number'],
        'api_id': season['id'],
    }
    return season_obj


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


# def single_show_search(show):
#     payload = {'q': f'{show}'}
#     r = requests.get(f'{BASE_URL}/singlesearch/shows', params=payload)
#     return r.json()

# def episodes_search(show_id):
#     r = requests.get(f'{BASE_URL}/shows/{show_id}/episodes')
#     return r.json()

# def episode_search(ep_id):
#     r = requests.get(f'{BASE_URL}/episodes/{ep_id}')
#     return r.json()
