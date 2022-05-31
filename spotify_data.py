import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from credentials import client_id, client_secret
from artists import artists
import pandas as pd


client_id = client_id
client_secret = client_secret
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def getTracks(nArtists):
    '''
    Returns a dataframe with the following columns:
    artist_name, track_name, track_id, track_popularity, artist_id, album_name
    '''
    artist_name = []
    track_name = []
    track_popularity = []
    artist_id = []
    track_id = []
    album_name = []
    album_id = []
    for artist in nArtists:
        for i in range(0,1000,50):
            track_results = sp.search(q=f'artist: {artist}', type='track', limit=50, offset=i)
            for i, t in enumerate(track_results['tracks']['items']):
                if artist == t['artists'][0]['name']:
                    artist_name.append(t['artists'][0]['name'])
                    artist_id.append(t['artists'][0]['id'])
                    track_name.append(t['name'])
                    track_id.append(t['id'])
                    track_popularity.append(t['popularity'])
                    album_id.append(t['album']['id'])
                    album_name.append(t['album']['name'])

    results = pd.DataFrame({'track_id' : track_id, 'track_name': track_name,  'track_popularity': track_popularity , 'artist_id': artist_id, 'artist_name': artist_name, 'album_id': album_id, 'album_name': album_name})
    return results

def getAudioFeatures(ids):
  '''
  Returns a dataframe with the following columns:
  track_id, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness,
  liveness, valence, tempo, duration_ms, time_signature.
  '''
  track_id = []
  danceability = []
  energy = []
  key = []
  loudness = []
  mode = []
  speechiness = []
  acousticness = []
  instrumentalness = []
  liveness = []
  valence = []
  tempo = []
  duration_ms = []
  time_signature = []

  for t_id in ids:
    track_features = sp.audio_features(t_id)
    if t_id not in track_id:
      track_id.append(track_features[0]['id'])
      danceability.append(track_features[0]['danceability'])
      energy.append(track_features[0]['energy'])
      key.append(track_features[0]['key'])
      loudness.append(track_features[0]['loudness'])
      mode.append(track_features[0]['mode'])
      speechiness.append(track_features[0]['speechiness'])
      acousticness.append(track_features[0]['acousticness'])
      instrumentalness.append(track_features[0]['instrumentalness'])
      liveness.append(track_features[0]['liveness'])
      valence.append(track_features[0]['valence'])
      tempo.append(track_features[0]['tempo'])
      duration_ms.append(track_features[0]['duration_ms'])
      time_signature.append(track_features[0]['time_signature'])

  results = pd.DataFrame({'track_id': track_id, 'danceability': danceability, 'energy': energy, 'key': key, 'loudness': loudness, 'mode': mode, 'speechiness': speechiness, 'acousticness': acousticness, 'instrumentalness': instrumentalness, 'liveness': liveness, 'valence': valence, 'tempo': tempo, 'duration_ms': duration_ms, 'time_signature': time_signature })
  return results

def getAlbums(ids):
    '''
    Returns a dataframe with the following columns:
    album_id, album_name, album_type, total_tracks, release_date, release_date_precision, artist_id, artist_name.
    '''
    album_id = []
    album_name = []
    album_type = []
    total_tracks = []
    release_date = []
    release_date_precision = []
    artist_id = []
    artist_name = []

    for alb_id in ids:
        lst_alb_id = [alb_id]
        albums = sp.albums(lst_alb_id)
        if alb_id not in album_id:
            album_id.append(albums['albums'][0]['id'])
            album_name.append(albums['albums'][0]['name'])
            album_type.append(albums['albums'][0]['album_type'])
            total_tracks.append(albums['albums'][0]['total_tracks'])
            release_date.append(albums['albums'][0]['release_date'])
            release_date_precision.append(albums['albums'][0]['release_date_precision'])
            artist_id.append(albums['albums'][0]['artists'][0]['id'])
            artist_name.append(albums['albums'][0]['artists'][0]['name'])

    results = pd.DataFrame({'album_id': album_id, 'album_name': album_name, 'album_type': album_type, 'total_tracks': total_tracks, 'release_date': release_date, 'release_date_precision': release_date_precision, 'artist_id': artist_id, 'artist_name': artist_name})
    return results

def getArtistInfo(ids):
    '''
    Returns a dataframe with the following columns for each artist related to the albums in the album_df:
    artist_id, artist_name, popularity, genres, followers.
    '''
    artist_id = []
    artist_name = []
    artist_popularity = []
    artist_genres = []
    artist_followers = []

    for a_id in ids:
        artist = sp.artist(a_id)
        if a_id not in artist_id:
            artist_id.append(a_id)
            artist_name.append(artist['name'])
            artist_popularity.append(artist['popularity'])
            artist_genres.append(artist['genres'])
            artist_followers.append(artist['followers']['total'])

    results = pd.DataFrame({'artist_id': artist_id, 'artist_name': artist_name, 'popularity': artist_popularity, 'genres': artist_genres, 'followers': artist_followers})
    return results
    

def getRelatedArtists(artists):
    related_artist = []

    for ids in artists:
        artist_related = sp.artist_related_artists(ids)
        for j in range(1, len(artist_related['artists'])):
            related_artist.append(artist_related['artists'][j]['name'])
    
    results = pd.DataFrame({'related_artist_name': related_artist})
    return results


# pandas dataframe
track_df = getTracks(artists)
track_features = getAudioFeatures(track_df['track_id'])
album_df = getAlbums(track_df['album_id'])
artist_info_df = getArtistInfo(album_df['artist_id'])
related_artists_df = getRelatedArtists(artist_info_df['artist_id'])

# merge tracks and track features
track_df = pd.merge(track_df, track_features, left_on='track_id', right_on='track_id')




