import pickle

class AccountDB:
	def getUsernames(self):
		'''
		returns user -> password dictionary keys (all users)
		'''
		return pickle.load(open( "databases/un_pw", "rb" ) ).keys()

	def addUser(self, username, password, email):
		'''
		given a username, password and email, adds user to the system
		'''
		un_pw = pickle.load(open( "databases/un_pw", "rb" ) )
		un_pl = pickle.load(open( "databases/un_pl", "rb" ) )
		un_pw[username] = {'Password': password, 'E-mail': email}
		un_pl[username] = []
		pickle.dump(un_pl, open( "databases/un_pl", "wb" ))
		pickle.dump(un_pw, open( "databases/un_pw", "wb" ))

	def correctPassword(self, username, password):
		'''
		given username and password, checks if correct records
		'''
		un_pw = pickle.load(open( "databases/un_pw", "rb" ) )
		if username in un_pw:
			return un_pw[username]['Password'] == password
		return False

