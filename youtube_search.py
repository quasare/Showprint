import requests
from env_variables import API_KEY




BASE_URL = 'https://www.googleapis.com/youtube/v3/search'

payload = {'part': 'snippet', 'q': 'pharrell', 'maxResults': 3, 'key': API_KEY}

res = requests.get(f'{BASE_URL}', params=payload).json()

vid_id = 'tewt'

video_url = f"https://www.youtube.com/watch?v={vid_id}"