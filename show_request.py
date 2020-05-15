import requests

BASE_URL = 'http://api.tvmaze.com'


def shows_search(show):
    payload = {'q': f'{show}'}
    r = requests.get(f'{BASE_URL}/search/shows', params=payload)
    first_nine = r.json()[:9]
    return first_nine

def single_show_search(show):
    payload = {'q': f'{show}'}
    r = requests.get(f'{BASE_URL}/singlesearch/shows', params=payload)
    return r.json()

def episodes_search(show_id):
    r = requests.get(f'{BASE_URL}/shows/{show_id}/episodes')
    return r.json()

def seasons_search(show_id):
    r = requests.get(f'{BASE_URL}/shows/{show_id}/seasons')
    return r.json()    

def seasons_episodes(season_id):
    r = requests.get(f'{BASE_URL}/seasons/{season_id}/episodes')
    return r.json()       

def episode_search(ep_id):
    r = requests.get(f'{BASE_URL}/episodes/{ep_id}')
    return r.json()   







