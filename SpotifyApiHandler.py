from SpotifyAuthorization import AppAuthorize
import requests
import json

class SpotifyApiHandler:
	def __init__(self):
		self.Authorizer = AppAuthorize()
		self.token = self.Authorizer.getAppToken()
	def get_track(self, Id, uri = False):
		'''
		gets a track given a spotify ID. If the id is a uri, then
		it is appropriately sliced to get the id. Returns the track object
		'''
		url = self.Authorizer.SPOTIFY_API_BASE_URL + '/' + self.Authorizer.API_VERSION + '/tracks'
		if uri:
			Id = Id[14:]
		headers = {"Authorization": "Bearer {}".format(self.token)}
		post_request = requests.get(url + '/{}'.format(Id), headers = headers)
		return json.loads(post_request.text)

	def query(self, q, types):
		'''
		given a query string and a list of item types to search across where
		valid types are: album , artist, playlist, and track, returns a dictionary response
		'''
		AA = AppAuthorize()
		t = ''
		for typ in types:
			t += (typ + ',')
		t = t[:-1] 
		access_token = AA.getAppToken()
		headers = {"Authorization": "Bearer {}".format(access_token)}
		code_payload = {"q":  q, "type": t}
		post_request = requests.get(AA.SPOTIFY_SEARCH_URL, params=code_payload, headers = headers)
		return json.loads(post_request.text)

