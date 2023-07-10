from flask import Flask, request
from flask_cors import CORS
from YoutubeManager import getVideoDetails, getPlaylist

app = Flask(__name__)

# adding cors policy
CORS(app, resources={r"/api/*": {"origins": "*"}})


# routing
@app.route("/")
def index():
    return 'Server is Working!'


@app.route('/api/video')
def getVideoRoute():
    url = request.args.get('url')
    return getVideoDetails(url)

@app.route('/api/playlist')
def getPlaylistRoute():
    url = request.args.get('url')
    return getPlaylist(url)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
