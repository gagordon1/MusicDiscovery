import base64
import requests
import json
import pickle

class AppAuthorize:
	def __init__(self):
		#  Client Keys
		self.CLIENT_ID = "5361fa0e7d3945f3b78faf916d34e7bb"
		self.CLIENT_SECRET = "e08fd9f28c23451f813b56dca6f31384"

		# Spotify URLS
		self.SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
		self.SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
		self.SPOTIFY_API_BASE_URL = "https://api.spotify.com"
		self.SPOTIFY_SEARCH_URL = "https://api.spotify.com/v1/search"
		self.SPOTIFY_AUDIO_FEATURES_URL = "https://api.spotify.com/v1/audio-features/"
		self.API_VERSION = "v1"
		self.SPOTIFY_API_URL = "{}/{}".format(self.SPOTIFY_API_BASE_URL, self.API_VERSION)

	def getAppToken(self):
		'''
		Authorizes an app use of the API by getting a token.
		'''
		code_payload = {"grant_type": "client_credentials"}
		byte = "{}:{}".format(self.CLIENT_ID, self.CLIENT_SECRET).encode('utf-8')
		base64encoded = base64.b64encode(byte).decode('utf-8')
		headers = {"Authorization": "Basic {}".format(base64encoded)}
		post_request = requests.post(self.SPOTIFY_TOKEN_URL, data=code_payload, headers = headers)
		post_data = json.loads(post_request.text)
		return post_data['access_token']

class UserAuthorize:
	'''
	Useful for setting and updating global access keys
	'''
	def __init__(self):
		self.CLIENT_ID = "5361fa0e7d3945f3b78faf916d34e7bb"
		self.CLIENT_SECRET = "e08fd9f28c23451f813b56dca6f31384"
		self.SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

	def setTokens(self, access, refresh):
		'''
		given an access and refresh token, saves them to a pickle file
		'''
		info = {'refresh token': refresh, 'access token': access}
		token_file = open('databases/tokens', 'wb')
		pickle.dump(info, token_file)

	def getTokens(self):
		'''
		returns the current refresh and access token as a two element tuple.
		'''
		token_file = open('databases/tokens', 'rb')
		info = pickle.load(token_file)
		return info['refresh token'], info['access token']

	def refreshTokens(self):
		'''
		uses current refresh token to get and save new tokens (returns new access token)
		'''
		refresh, access = self.getTokens()
		code_payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh
		}
		toEncode = "{}:{}".format(self.CLIENT_ID, self.CLIENT_SECRET).encode('ascii')
		encoded = base64.b64encode(toEncode)
		decoded = encoded.decode('ascii')
		header = {"Authorization": "Basic {}".format(decoded)}
		post_request = requests.post(self.SPOTIFY_TOKEN_URL, headers = header , data=code_payload)

		# Auth Step 5: Tokens are Returned to Application
		response_data = json.loads(post_request.text)
		access_token = response_data["access_token"]
		self.setTokens(access_token, refresh)
		return access_token




