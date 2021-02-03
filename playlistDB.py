import pickle
from SpotifyApiHandler import SpotifyApiHandler

class PlaylistDB:
	def create_playlist(self, username, title):
		'''
		Given a username and title of playlist, adds a playlist to their list of records
		'''
		pl_info = pickle.load(open( "databases/pl_info", "rb" ))
		un_pl = pickle.load(open( "databases/un_pl", "rb" ))
		lastId = self.lastID()
		newId = lastId + 1
		un_pl[username].append(newId)
		pl_info[newId] = {'Name': title, 'Tracks':[]}
		pickle.dump(newId, open( "databases/Ids", "wb" ))
		pickle.dump(pl_info, open( "databases/pl_info", "wb" ))
		pickle.dump(un_pl, open( "databases/un_pl", "wb" ))

	def get_tracks(self, playlist):
		'''
		given a unique playlist ID, return associated tracks as a list of 
		tuples of the form (title, artists (list), album, uri)
		'''
		pl_info = pickle.load(open( "databases/pl_info", "rb" ))
		final = pl_info[int(playlist)]['Tracks']
		new = []
		SAH = SpotifyApiHandler()
		for URI in final:
			track = SAH.get_track(URI, uri = True)
			artists = ''
			for i in range(len(track['artists'])):
				artists += track['artists'][i]['name'] + ', ' 
			new.append((track['name'], artists[:-2], track['album']['name'], track['uri']))
		return new

	def get_name(self, playlist):
		'''
		given a unique playlist ID, return its name.
		'''
		pl_info = pickle.load(open( "databases/pl_info", "rb" ))
		return pl_info[int(playlist)]['Name']

	def delete_playlist(self, username, title):
		'''
		given a username and title to be deleted, deletes a playlist
		'''
		pass

	def add_track(self, playlist, track):
		'''
		given a playlist and track, adds track to the playlist as a tuple of the form
		(title, artist, album, uri)
		'''
		pl_info = pickle.load(open( "databases/pl_info", "rb" ))
		pl_info[int(playlist)]['Tracks'].append(track)
		pickle.dump(pl_info, open( "databases/pl_info", "wb" ))

	def delete_track(self, playlist, track):
		'''
		given a playlist and track, deletes the track
		'''
		pass
	def lastID(self):
		'''
		returns most recently added ID as an integer
		'''
		return pickle.load(open( "databases/Ids", "rb" ))
	def getHtmlPlaylists(self, username):
		'''
		given a username, returns html parsable list of tuples where the 0 
		index is the unique id and 1 index is the name for each playlist
		'''
		pl_info = pickle.load(open( "databases/pl_info", "rb" ))
		un_pl = pickle.load(open( "databases/un_pl", "rb" ))
		return [(i, pl_info[i]['Name']) for i in un_pl[username]]
	def getPlaylists(self, username):
		'''
		given a username, return associated playlists as a list
		'''
		pl_info = pickle.load(open( "databases/pl_info", "rb" ))
		un_pl = pickle.load(open( "databases/un_pl", "rb" ))
		return [pl_info[i]['Name'] for i in un_pl[username]]



