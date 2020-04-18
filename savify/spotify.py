import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .track import Track

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


def search(query, query_type='track'):
    results = sp.search(q=query, limit=20, type=query_type)
    if len(results[query_type + 's']['items']) > 0:
        if query_type == 'track':
            return [Track(results[query_type + 's']['items'][0])]
        elif query_type == 'album':
            return pack_album(sp.album(results['album' + 's']['items'][0]['id']))
        elif query_type == 'playlist':
            return pack_playlist(sp.playlist(results['playlist' + 's']['items'][0]['id']))
    else:
        return None


def link(query):
    try:
        if '/track/' in query:
            return [Track(sp.track(query))]
        elif '/album/' in query:
            return pack_album(sp.album(query))
        elif '/playlist/' in query:
            return pack_playlist(sp.playlist(query))
        else:
            return None
    except spotipy.exceptions.SpotifyException:
        return None


def pack_album(album):
    tracks = []
    for track in album['tracks']['items']:
        track_data = track
        track_data['album'] = album
        tracks.append(Track(track_data))
    return tracks


def pack_playlist(playlist):
    tracks = []
    for track in playlist['tracks']['items']:
        tracks.append(Track(track['track']))
    return tracks
