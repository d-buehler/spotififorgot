import requests
from base64 import b64encode
from urllib.parse import urlencode
from utils import getConfig


class InvalidTrackName(Exception):
    def __init__(self):
        self.message = ""


def spotify_login(conf):
    """
    Authenticates to the Spotify API; returns an auth token
    :param conf: the config to use
    """
    api_base = conf.get("API", "api_base")
    auth_endpoint = "/".join([api_base, "token"])

    creds = ":".join([conf.get("API", "client_id"), conf.get("API", "client_secret")])
    creds_encoded = str(b64encode(bytes(creds, encoding="utf-8")), encoding="utf-8")
    headers = {"Authorization": "Basic " + creds_encoded}

    grantType = "client_credentials"
    data = {"grant_type": grantType}

    r = requests.post(auth_endpoint, headers=headers, data=data)

    return r.json()


def getTracksFromResponse(resp):
    """
    Returns the tracks from an API response
    :param resp: Spotify search API response
    """
    return resp.json().get("tracks", {}).get("items", [])


def searchTracks(conf, trackName, limit=50, removeSingles=True, debug=False):
    """
    Queries the Spotify search API for the provided track
    :param conf: the config to use
    :param trackName: the track to search for
    :param limit: the max number of items to return in a page of results (Spotify's max is 50)
    :param removeSingles: flag for whether or not to include singles (vs albums or compilations) in results
    :param debug: true = more stuff is printed
    """
    if len(trackName) == 0:
        raise InvalidTrackName()

    creds = spotify_login(conf)
    headers = {"Authorization": " ".join([creds["token_type"], creds["access_token"]])}
    if debug:
        print("Headers: {}".format(str(headers)))

    searchEndpoint = conf.get("API", "search_endpoint")
    query = {"q": trackName, "type": "track", "market": "US", "limit": limit}
    queryEncoded = urlencode(query)
    if debug:
        print("First query: {}".format(queryEncoded))

    resp = requests.get(searchEndpoint, headers=headers, params=queryEncoded)
    searchResults = getTracksFromResponse(resp)

    nextSearchUrl = resp.json().get("tracks", {}).get("next", None)
    while nextSearchUrl is not None:
        if debug:
            print("Querying {}".format(nextSearchUrl))

        resp = requests.get(nextSearchUrl, headers=headers)
        searchResults += getTracksFromResponse(resp)
        nextSearchUrl = resp.json().get("tracks", {}).get("next", None)

    if removeSingles:
        searchResults = [
            track for track in searchResults if track["album"]["album_type"] != "single"
        ]

    return searchResults
