import requests
from os import environ
from environs import Env

env = Env()
env.read_env()

# Constants
API_KEY = 'wffwefewfwwefwef'
BASE_URL = 'https://www.googleapis.com/youtube/v3/search'

# Youtube search and format for site
def youtube_search(query):
    vids = []
    payload = {'part': 'snippet', 'q': query, 'maxResults': 4, 'type': 'video',
           'key': API_KEY}
    res = requests.get(f'{BASE_URL}', params=payload).json()
    for n in range(0, 4):
        vid_id =res['items'][n]['id']['videoId']
        vids.append({'vid_url': f"https://www.youtube.com/embed/{vid_id}",
            'thumb': res['items'][n]['snippet']['thumbnails']['medium']['url']
        })

    return vids




