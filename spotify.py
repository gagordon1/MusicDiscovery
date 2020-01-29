
import spotipy
import sys
import spotipy.util as util
util.prompt_for_user_token(username,scope,
	client_id='5361fa0e7d3945f3b78faf916d34e7bb',client_secret='e08fd9f28c23451f813b56dca6f31384',
	redirect_uri= 'http://localhost/')

sp = spotipy.Spotify()

sp.trace = True # turn on tracing
sp.trace_out = True # turn on trace out



user = sp.user('garrettg45')
print(user)