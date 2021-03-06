import spotipy
import spotipy.util as util
from settings_local import SPOTIFY_USERNAME, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, \
  SPOTIFY_REDIRECT_URI, SPOTIFY_PLAYLIST_ID, SPOTIFY_SCOPE

token = util.prompt_for_user_token(SPOTIFY_USERNAME, SPOTIFY_SCOPE,
    client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI)