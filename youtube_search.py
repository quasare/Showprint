import requests


API_KEY = 'AIzaSyAKgp3yYDU8FdNkdCFEs097AVsl4IQAViU'

BASE_URL = 'https://www.googleapis.com/youtube/v3/search'

payload = {'part': 'snippet', 'q': 'pharrell', 'maxResults': 3, 'key': API_KEY}

res = requests.get(f'{BASE_URL}', params=payload)
