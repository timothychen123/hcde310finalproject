from flask import Flask, render_template, request
import urllib.parse, urllib.request, urllib.error, json

app = Flask(__name__)

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

def safeGet(url):
    try:
        response = urllib.request.urlopen(url)
        return response.read()
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print("The server couldn't fulfill the request.")
            print("Error code: ", e.code)
        elif hasattr(e,'reason'):
            print("We failed to reach a server")
            print("Reason: ", e.reason)

def average_album(name, limit=30):
  term = name
  data = {"term": term, "limit": limit, "attribute": "allArtistTerm"}
  datastr = urllib.parse.urlencode(data)
  base_url = "https://itunes.apple.com/"
  request_artist = base_url +"search?" + datastr
  request_artiststr = urllib.request.urlopen(request_artist).read()
  request_artiststr = json.loads(request_artiststr)
  if request_artiststr["results"] == []:
      print("Not an existing artist in the database, please enter a different artist.")
      quit()
  result = safeGet(request_artist)
  if result is not None:
    uniqueAlbum = {}
    for album in request_artiststr["results"]:
      albumName = album["collectionName"]
      if albumName not in uniqueAlbum:
        uniqueAlbum[albumName] = album["collectionPrice"]
  total = 0
  for value in uniqueAlbum.values():
    total = total + value
  total = total / len(uniqueAlbum)
  total = float(format(total, ".2f"))
  artist_album = {}
  artist_album[term] = total
  return artist_album

def more_album_info(name, limit=30):
  term = name
  data = {"term": term, "limit": limit, "attribute": "allArtistTerm"}
  datastr = urllib.parse.urlencode(data)
  base_url = "https://itunes.apple.com/"
  request_artist = base_url +"search?" + datastr
  request_artiststr = urllib.request.urlopen(request_artist).read()
  request_artiststr = json.loads(request_artiststr)
  if request_artiststr["results"] == []:
      print("Not an existing artist in the database, please enter a different artist.")
      quit()
  result = safeGet(request_artist)
  if result is not None:
    uniqueAlbums = {}
    for album in request_artiststr["results"]:
      albumName = album["collectionName"]
      if albumName not in uniqueAlbums:
        uniqueAlbums[albumName] = {}
        uniqueAlbums[albumName]["Album Name"] = album["collectionCensoredName"]
        uniqueAlbums[albumName]["Album URL"] = album["collectionViewUrl"]
        uniqueAlbums[albumName]["Artwork URL"] = album["artworkUrl100"]
        uniqueAlbums[albumName]["Release Date"] = album["releaseDate"].split("T")[0]
#        uniqueAlbum[albumName + " Album Name"] = album["collectionCensoredName"]
#        uniqueAlbum[albumName + " Album URL"] = album["collectionViewUrl"]
#        uniqueAlbum[albumName + " Artwork URL"] = album["artworkUrl100"]
#        uniqueAlbum[albumName + " Release Date"] = album["releaseDate"].split("T")[0]
  return uniqueAlbums

@app.route("/")
def main_handler():
    app.logger.info("In MainHandler")
    return render_template('greetresponse.html',page_title="Greeting Form")

@app.route("/gresponse", methods = ["POST"])
def artist_response_handler():
  app.logger.info(request.form.get('artist'))
  name = request.form.get('artist')
  try:
    if name:
      return render_template("template.html",
        artist_album = average_album(name),
        more_info = more_album_info(name)
      )
    else:
      return render_template("greetresponse.html", page_title="Greeting Page")
  except:
    return render_template('error.html', page_title="Error Page")


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)