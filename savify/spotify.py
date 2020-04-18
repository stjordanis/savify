import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .track import Track

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


def search(query, query_type='track'):
    results = sp.search(q=query, limit=20, type=query_type)
    if len(results[query_type + 's']['items']) > 0:
        if query_type == 'track':
            return Track(results[query_type + 's']['items'][0])
        elif query_type == 'album':
            tracks = []
            album = sp.album(results['album' + 's']['items'][0]['id'])
            for track in album['tracks']['items']:
                track_data = track
                track_data['album'] = album
                tracks.append(track(track_data))
            return tracks
        elif query_type == 'playlist':
            tracks = []
            playlist = sp.playlist(results['playlist' + 's']['items'][0]['id'])
            for track in playlist['tracks']['items']:
                tracks.append(track(track['track']))
            return tracks
    else:
        return None
