from flask import Flask, escape, request, render_template
from flask import request


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')
 
@app.route('/search', methods=["GET", "POST"])
def search():
	return render_template('search.html', nameDict = response)

if __name__ == '__main__':
	app.run(debug=True)

