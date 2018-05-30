import pprint
import sys
import json
import sqlite3
import spotipy
import spotipy.util as util
import twitter

from settings_local import SPOTIFY_USERNAME, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, \
  SPOTIFY_REDIRECT_URI, SPOTIFY_PLAYLIST_ID, SPOTIFY_SCOPE, TWITTER_CONSUMER_KEY, \
  TWITTER_CONSUMER_SECRET, TWITTER_USER_TOKEN, TWITTER_USER_SECRET, TWITTER_FOLLOW


con = sqlite3.connect("tracks.db")

api = twitter.Api(consumer_key=TWITTER_CONSUMER_KEY,
                  consumer_secret=TWITTER_CONSUMER_SECRET,
                  access_token_key=TWITTER_USER_TOKEN,
                  access_token_secret=TWITTER_USER_SECRET)

stream = api.GetStreamFilter(follow=[TWITTER_FOLLOW])

for line in stream:
  tweet = twitter.Status.NewFromJsonDict(line)
  if tweet.text is None:
    continue
  (artist, song) = tweet.text.split(' - ', 2)

  track_ids = []

  token = util.prompt_for_user_token(SPOTIFY_USERNAME, SPOTIFY_SCOPE,
    client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI)
  
  if not token:
      print("Can't get token")
      sys.exit()

  spotify = spotipy.Spotify(auth=token)
  results = spotify.search(q='artist:{} {}'.format(artist, song), type='track', limit=1)
  try:
    track_id = results['tracks']['items'][0]['uri']
  except:
    continue

  c = con.cursor()
  t = (track_id,)
  c.execute('SELECT * FROM tracks WHERE tracks=?', t)
  if c.fetchone() is None:
     track_ids.append(results['tracks']['items'][0]['uri'])

  for track_id in track_ids:
     results = spotify.user_playlist_add_tracks(SPOTIFY_USERNAME, SPOTIFY_PLAYLIST_ID, [track_id,])
     c.execute('INSERT INTO tracks(tracks) VALUES (?)', (track_id,))
     con.commit()
     print("Added: {} - {}".format(artist, song))
