from .requests import requests

BASE_URL = 'http://api.tvmaze.com'

show = 'billons'
payload = {'q': f'{show}'}
r = requests.get(f'{BASE_URL}/singlesearch/shows', params=payload)

def shows_search(show):
    return

def show_search(show):
    return

def episodes_search(show):
    return

def episode_search(show):
    return    


print(r.url)



