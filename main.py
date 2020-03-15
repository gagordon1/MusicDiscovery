import json
from flask import Flask, request, redirect, g, render_template
import requests
from urllib.parse import quote
import base64
import pickle


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
SCOPE = "playlist-modify-public playlist-modify-private"
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
@app.route("/")
def home():
    # Auth Step 1: Authorization
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

    return redirect("/directory{}".format(access_token))

@app.route("/directory<token>")
def directory(token):
    return render_template("directory.html", token = token)

#-------------------------------Make and View Playlists---------------------------------------
@app.route("/signIn", methods = ["GET", "POST"])
@app.route("/signIn/<Message>", methods = ["GET", "POST"])
def signIn(Message = ''):
    if request.form:
        un = request.form.get('Username')
        pw = request.form.get('Password')
        un_pw = pickle.load( open( "databases/un_pw", "rb" ) )
        if un in un_pw:
            if un_pw[un]['Password'] == pw:
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
        if cpw == pw:
            un_pw = pickle.load( open( "databases/un_pw", "rb" ) )
            if un in un_pw:
                message = 'Username already exists. Try something else.'
                return redirect("/createAccount/{}".format(message))
            else:
                un_pw[un] = {'Password': pw, 'E-mail': em}
                pickle.dump(un_pw, open( "databases/un_pw", "wb" ))
                message = 'Account Created! Please sign in.'
                return redirect("/signIn/{}".format(message))
        else:
            return render_template("create_account.html", error = 'Passwords did not match. Try again')   
    return render_template("create_account.html", error = Message)


@app.route("/viewPlaylist<playlist>")
def viewPlaylist(playlist):
    # A page where given a playlist, users are able to edit and play music\
    pass

@app.route("/Library/<Username>")
def Library(Username):
    # a page where all playlists are shown 
    return "{}'s Library".format(Username)


#-------------------------------USER DATA APPLICATIONS----------------------------------------

@app.route("/myplaylists<token>")
def myplaylists(token):
    # Auth Step 6: Use the access token to access Spotify API
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
    lengths =[i['tracks']['total'] for i in display_arr]

    return render_template("playlists.html", length = len(names), playlist_names=names, playlist_lengths = lengths, 
        display_name = profile_data['display_name'])

#supports searching tracks
#--------------------------------SEARCH MODULE----------------------------------

@app.route("/appAuthorizeSearch")
def appAuthorizeSearch():
    code_payload = {"grant_type": "client_credentials"}
    byte = "{}:{}".format(CLIENT_ID, CLIENT_SECRET).encode('utf-8')
    base64encoded = base64.b64encode(byte).decode('utf-8')
    headers = {"Authorization": "Basic {}".format(base64encoded)}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers = headers)
    post_data = json.loads(post_request.text)
    url = "/search/" + post_data['access_token']
    return redirect(url)

@app.route("/search/<access_token>", methods = ["GET", "POST"])
def search(access_token):
    content = []
    if request.form:
        query = request.form.get('Search Tracks')
        headers = {"Authorization": "Bearer {}".format(access_token)}
        code_payload = {"q":  query, "type": "track"}
        post_request = requests.get(SPOTIFY_SEARCH_URL, params=code_payload, headers = headers)
        response = json.loads(post_request.text)
        
        for track in response['tracks']['items']:
            content.append((track['name'], track['artists'][0]['name'], 
                track['album']['name'], track['popularity'],track['id']))
    return render_template("search.html", access_token = access_token, content = content)


@app.route("/audio-features/<title>/<Id>/<access_token>")
def audio_features(title, Id, access_token):
    headers = {"Authorization": "Bearer {}".format(access_token)}
    url = SPOTIFY_AUDIO_FEATURES_URL + Id
    post_request = requests.get(url, headers = headers)
    response = json.loads(post_request.text)
    return render_template("audio_features.html", track_name = title, resp = response)


if __name__ == "__main__":
    app.run(debug=True, port=PORT)


