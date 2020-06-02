import requests
import os
from environs import Env

env = Env()
env.read_env()

API_KEY = env('API_KEY')

BASE_URL = 'https://www.googleapis.com/youtube/v3/search'

def youtube_search(query):
    vids = []
    payload = {'part': 'snippet', 'q': query, 'maxResults': 4,
           'key': API_KEY}
    res = requests.get(f'{BASE_URL}', params=payload).json()
    for n in range(2, 4):
        vid_id =res['items'][n]['id']['videoId']
        vids.append({'vid_url': f"https://www.youtube.com/watch?v={vid_id}",
            'thumb': res['items'][n]['snippet']['thumbnails']['medium']['url']
        })

    return vids




