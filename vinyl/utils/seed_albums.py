import requests

def get_cover(artist, album):
    query = f"{artist} {album}"

    url = "https://musicbrainz.org/ws/2/release-group/"
    params = {"query": query, "fmt": "json"}

    r = requests.get(url, params=params, headers={"User-Agent": "Mozilla/5.0"})
    data = r.json()

    try:
        mbid = data["release-groups"][0]["id"]
        return f"https://coverartarchive.org/release-group/{mbid}/front-500"
    except:
        return None