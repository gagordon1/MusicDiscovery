import json
from flask import Flask, request, redirect, g, render_template
import requests
from urllib.parse import quote
from playlistDB import PlaylistDB
from accountDB import AccountDB
from SpotifyAuthorization import AppAuthorize, UserAuthorize
from SpotifyApiHandler import SpotifyApiHandler


# Authentication Steps, paramaters, and responses are defined at https://developer.spotify.com/web-api/authorization-guide/
# Visit this url to see all the steps, parameters, and expected response.
#http://127.0.0.1:8080

app = Flask(__name__)

#  Client Keys
CLIENT_ID = "5361fa0e7d3945f3b78faf916d34e7bb"
CLIENT_SECRET = "e08fd9f28c23451f813b56dca6f31384"

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
SPOTIFY_SEARCH_URL = "https://api.spotify.com/v1/search"
SPOTIFY_AUDIO_FEATURES_URL = "https://api.spotify.com/v1/audio-features/"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8080
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "streaming user-read-email user-read-private playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}

keyMap = {
    (0, 0) : "Cm",
    (0, 1) : "C",
    (1, 0) : "C#m",
    (1, 1) : "C#",
    (2, 0) : "Dm",
    (2, 1) : "D",
    (3, 0) : "D#m",
    (3, 1) : "D#",
    (4, 0) : "Em",
    (4, 1) : "E",
    (5, 0) : "Fm",
    (5, 1) : "F",
    (6, 0) : "F#m",
    (6, 1) : "F#",
    (7, 0) : "Gm",
    (7, 1) : "G",
    (8, 0) : "G#m",
    (8, 1) : "G#",
    (9, 0) : "Am",
    (9, 1) : "A",
    (10, 0) : "A#m",
    (10, 1) : "A#",
    (11, 0) : "Bm",
    (11, 1) : "B",


}

keyValues = {
    "Cm" : 0,
    "C" : 1,
    "C#m" : 2,
    "C#" : 3,
    "Dm" : 4,
    "D" :5,
    "D#m" : 6,
    "D#": 7,
    "Em" : 8,
    "E": 9,
    "Fm": 10,
    "F" : 11,
    "F#m" : 12,
    "F#" : 13,
    "Gm" : 14,
    "G" :15,
    "G#m" : 16,
    "G#" :17,
    "Am" :18,
    "A" : 19,
    "A#m" :20,
    "A#" :21,
    "Bm" : 22,
    "B" :23,


}



@app.route("/", methods = ["GET", "POST"])
def home():
    # Auth Step 1: Authorization
    if request.form:
        uri = request.form.get("Play Track")
        return redirect('play/{}'.format(uri))
    return render_template("home.html")

#-------------------------USER DATA AUTHORIZATION-----------------------------------------
@app.route("/authorize_gateway")
def authorize_gateway():
    # Auth Step 1: Authorization
    return render_template("authorize_gate.html")

@app.route("/authorize")
def authorize():
    # Auth Step 1: Authorization
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)

@app.route("/callback/q")
def callback():
    # Auth Step 4: Requests refresh and access tokens

    auth_token = request.args['code']

    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]
    UA = UserAuthorize()
    UA.setTokens(access_token, refresh_token)
    return redirect("/")

#-------------------------------Make and View Playlists---------------------------------------
@app.route("/signIn", methods = ["GET", "POST"])
@app.route("/signIn/<Message>", methods = ["GET", "POST"])
def signIn(Message = ''):
    if request.form:
        un = request.form.get('Username')
        pw = request.form.get('Password')
        aDB = AccountDB()
        if un in aDB.getUsernames():
            if aDB.correctPassword(un, pw):
                return redirect('/Library/{}'.format(un))
            else:
                return render_template("sign_in.html", error = 'Incorrect Password')
        else:
            return render_template("sign_in.html", error = 'Username is not in records')
    return render_template("sign_in.html", error = Message)


@app.route("/createAccount/<Message>", methods = ["GET", "POST"])
@app.route("/createAccount", methods = ["GET", "POST"])
def createAccount(Message = ''):
    if request.form:
        em = request.form.get('E-mail')
        un = request.form.get('Username')
        pw = request.form.get('Password')
        cpw = request.form.get('ConfPassword')
        aDB = AccountDB()
        if cpw == pw:
            un_pw = aDB.getUsernames()
            if un in un_pw:
                message = 'Username already exists. Try something else.'
                return redirect("/createAccount/{}".format(message))
            else:
                aDB.addUser(un, pw, em)
                message = 'Account Created! Please sign in.'
                return redirect("/signIn/{}".format(message))
        else:
            return render_template("create_account.html", error = 'Passwords did not match. Try again')   
    return render_template("create_account.html", error = Message)

@app.route("/viewPlaylist/<playlist>/<playlistId>/<token>/<sortBy>", methods = ["GET", "POST"])
@app.route("/viewPlaylist/<playlist>/<playlistId>/<token>", methods = ["GET", "POST"])
def viewPlaylist(playlist, playlistId, token, sortBy = None):

    # A page where given a playlist, users are able to edit and play music
    authorization_header = {"Authorization": "Bearer {}".format(token)}
    
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = json.loads(profile_response.text)

    # Get user playlist data
    playlist_api_endpoint = "{}/playlists/{}/tracks".format(profile_data["href"], playlistId)
    item_length = 1
    track_index = 0
    limit = 100
    
    items = []

    
    while (item_length != 0):
        code_payload = {"offset": track_index, "limit": limit}
        playlists_response = requests.get(playlist_api_endpoint, params = code_payload, headers=authorization_header)

        playlist_data = json.loads(playlists_response.text)
        it = playlist_data["items"]
        items.extend(it)
        item_length = len(it)
        track_index += 100


    tr = []

    AA = AppAuthorize()
    access_token = AA.getAppToken()

    for i in items:
        name = i["track"]["name"]
        print(name)
        if len(i["track"]["album"]["artists"]) >0 :
            artist = i["track"]["album"]["artists"][0]["name"]
        else:
            continue
        album = i["track"]["album"]["name"]
        track_id = i["track"]["id"]
        popularity = i["track"]["popularity"]
        
        headers = {"Authorization": "Bearer {}".format(access_token)}
        url = SPOTIFY_AUDIO_FEATURES_URL + track_id
        post_request = requests.get(url, headers = headers)
        if post_request.status_code == 200:
            response = json.loads(post_request.text)


            key = response["key"]
            mode = response["mode"]

            stringKey = keyMap[(key,mode)]
            BPM = response["tempo"]
            danceability = response["danceability"]

            tri = (name, artist, album, stringKey, BPM, danceability, popularity)
            tr.append(tri)

    keyIndex = 3
    bpmIndex = 4
    danceabilityIndex = 5
    popularityIndex = 6


    if sortBy == "Key":
        #SORT tr
        tr = parameterSort(tr, keyIndex, isKey = True)
    elif sortBy == "BPM":
        tr = parameterSort(tr, bpmIndex)
    elif sortBy == "Danceability":
        tr = parameterSort(tr, danceabilityIndex)
    elif sortBy == "Popularity":
        tr = parameterSort(tr, popularityIndex)
    else:
        tr = parameterSort(tr, keyIndex, isKey = True)

    return render_template("playlistView.html", tracks = tr, playlist = playlist, playlistId = playlistId, token = token)

    
@app.route("/Library/<Username>/<Message>", methods = ["POST", "GET"])
@app.route("/Library/<Username>", methods = ["POST", "GET"])
def Library(Username, Message = ''):
    # a page where all playlists are shown. If user clicks create playlist, a new playlist is added as a unique integer.

    pDB = PlaylistDB()
    if request.form:
        name = request.form.get('Name')
        Playlists = pDB.getPlaylists(Username)
        if name in Playlists:
            Message = 'Name already used! Try something else.'
        else:
            pDB.create_playlist(Username, name)
    return render_template("Library.html", playlists = pDB.getHtmlPlaylists(Username), username = Username, error = Message)

#-------------------------------USER DATA APPLICATIONS----------------------------------------
@app.route("/myplaylists")
def myplaylists():
    # Auth Step 6: Use the access token to access Spotify API
    UA = UserAuthorize()
    token = UA.getTokens()[1]
    authorization_header = {"Authorization": "Bearer {}".format(token)}
    
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = json.loads(profile_response.text)

    # Get user playlist data
    playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
    code_payload = {"limit": 50}
    playlists_response = requests.get(playlist_api_endpoint, params = code_payload, headers=authorization_header)
    playlist_data = json.loads(playlists_response.text)

    # Combine profile and playlist data to display
    display_arr = playlist_data["items"]
    names = [i['name'] for i in display_arr]
    IDs = [i['uri'][17:] for i in display_arr]
    lengths =[i['tracks']['total'] for i in display_arr]
    return render_template("playlists.html", length = len(names), playlist_names=names, playlist_lengths = lengths, 
        display_name = profile_data['display_name'], playlist_ids = IDs, token = token)

@app.route("/play/<uri>")
def play(uri):
    UA = UserAuthorize()
    access_token = UA.refreshTokens()
    return render_template('fire.html', access_token = access_token, URI = uri)

#supports searching tracks
#--------------------------------SEARCH MODULE----------------------------------

@app.route("/search", methods = ["GET", "POST"])
def search():
    content = []
    access_token = None
    if request.form: 
        quer = request.form.get('Search Tracks')
        SAH = SpotifyApiHandler()
        response = SAH.query(quer, ['track'])
        for track in response['tracks']['items']:
            content.append((track['name'], track['artists'][0]['name'], 
                track['album']['name'], track['popularity'],track['id']))
    return render_template("search.html", content = content)

@app.route("/audio-features/<title>/<Id>")
def audio_features(title, Id):
    AA = AppAuthorize()
    access_token = AA.getAppToken()
    headers = {"Authorization": "Bearer {}".format(access_token)}
    url = SPOTIFY_AUDIO_FEATURES_URL + Id
    post_request = requests.get(url, headers = headers)
    response = json.loads(post_request.text)
    return render_template("audio_features.html", track_name = title, resp = response)


#returns the tracks sorted on the specified index
#tracks is a list of tuples
#index is an integer 0-len(tracks[0]) that shows which variable to sort on
def parameterSort(tracks, index, isKey = False):
    final = []
    while tracks != []:
        highest = 0
        highest_track = None
        for track in tracks:

            if isKey:
                if keyValues[track[index]] >= highest:
                    highest = keyValues[track[index]]
                    highest_track = track


            elif track[index] >= highest:
                highest = track[index]
                highest_track = track
        tracks.remove(highest_track)
        final.append(highest_track)
    return final



if __name__ == "__main__":
    app.run(debug=True, port=PORT)


