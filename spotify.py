
import spotipy
import sys
import spotipy.util as util

scope = 'user-library-read'
# if len(sys.argv) >1:
#     username = sys.argv[1]
# else:
# 	print(sys.argv)
# 	print("Usage: %s username" %(sys.argv[0],))
# 	sys.exit()
username = 'garrettg45'

token = util.prompt_for_user_token(username,scope,client_id = '5361fa0e7d3945f3b78faf916d34e7bb', 
                                   client_secret = 'e08fd9f28c23451f813b56dca6f31384', 
                                   redirect_uri = 'http://localhost/')

# spotipy = spotipy.Spotify(auth=token)
# user = spotipy.user('garrettg45')
# x = spotipy.current_user_playlists(limit=50)
