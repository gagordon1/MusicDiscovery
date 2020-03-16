import pickle
un_pw = {'test': {'Password': 'test', 'E-mail': 'test@gmail.com'}}
un_pl = {'test': [0]}
pl_info = {0:{'Name': 'Fire', 'Tracks': []}}
IDs = 0
pickle.dump(un_pw, open( "databases/un_pw", "wb" ))
pickle.dump(pl_info, open( "databases/pl_info", "wb" ))
pickle.dump(un_pl, open( "databases/un_pl", "wb" ))
pickle.dump(IDs, open( "databases/Ids", "wb" ))
