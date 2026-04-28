import requests
import re
import json
from html import unescape

headers = {"User-Agent": "Mozilla/5.0"}

def fetch_tracks(url):
    response = requests.get(url, headers=headers)
    html = response.text
    match = re.search(r'new BookPlayer\(\s*\d+,\s*(\[\{.*?\}\])', html, re.DOTALL)
    if not match:
        print("Не удалось найти список треков.")
        return []
    tracks_json = match.group(1)
    tracks_json = unescape(tracks_json)
    try:
        tracks = json.loads(tracks_json)
    except json.JSONDecodeError as e:
        print("Ошибка парсинга JSON:", e)
        return []
    return tracks


def track_links(url):
    tracks = fetch_tracks(url)
    for i, track in enumerate(tracks, 1):
        title = track.get("title", f"track{i}")
        audio_url = track.get("url")
        yield i, title, audio_url
