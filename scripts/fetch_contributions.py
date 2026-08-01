"""
fetch_contributions.py
Scrape the public contributions fragment for a username and write data/contributions.json
Usage: python scripts/fetch_contributions.py <username>
"""
import requests
from bs4 import BeautifulSoup
import json
import sys
import os

URL = 'https://github.com/users/{}/contributions'

def fetch(username):
    r = requests.get(URL.format(username), timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    rects = soup.select('rect[data-date]')
    days = []
    for rect in rects:
        days.append({
            'date': rect.get('data-date'),
            'count': int(rect.get('data-count', '0'))
        })
    out = {'username': username, 'days': days}
    os.makedirs('data', exist_ok=True)
    with open(os.path.join('data','contributions.json'),'w',encoding='utf-8') as f:
        json.dump(out,f,indent=2)
    print('Wrote data/contributions.json')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python scripts/fetch_contributions.py <username>')
        sys.exit(1)
    fetch(sys.argv[1])
