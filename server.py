from flask import Flask, render_template, request, send_file
from replit import db
import urllib.parse
import os

from datetime import date
import time
from zoneinfo import ZoneInfo

from ytmp3 import downloadMp3
from ytscraper import get_videos

# deleteFile("./templates/downloads/" + filename)

db["searchCount"] = 0
# to reset db["searchCount"] at the start of each day
# keep record of last date in db, then on next server request,
# check current date, if different, reset
# *google api quota resets at midnight Pacific Time (PT)

# in Pacific Time
db["dayOfMonth"] = date.fromtimestamp(time.time(), tz=ZoneInfo("America/Los_Angeles")).day

quit()

def resetSearchCount():
  db["searchCount"] = 0


app = Flask(__name__)

valid_get_paths = ["index.html", "index.js"]

@app.get("/")
@app.get("/<path>")
def getHandler(path="index.html"):

  # urllib.parse.unquote(path)
  print(path)

  try:
    valid_get_paths.index(path)
  except:
    return "invalid url (endpoint)", 405

  searchCount = db["searchCount"]

  template = render_template(path, searchCount=searchCount)

  return template, 200


downloaded_file = ["Me at the zoo.mp3"]
@app.route('/download/<filename>')
def downloadHandle(filename):
  print("download handle")
  try:
    urllib.parse.unquote(filename)
    return send_file("./downloads/"+filename, as_attachment=True)
  except Exception as e:
    print(str(e))
    return str(e), 404

# returns list
def getSearchResults(user_input_str):
  # return []

  db["searchCount"] = db["searchCount"] + 1

  results = get_videos(user_input_str)
  response_arr = []
  for searchResult in results:
    response_arr.append({
      "videoTitle": searchResult["snippet"]["title"],
      "channelTitle": searchResult["snippet"]["channelTitle"],
      "videoId": searchResult["id"]["videoId"],
      "thumbnail": searchResult["snippet"]["thumbnails"]["high"]["url"]
    })
  # print(response_arr[0])
  return response_arr

# returns str, url to resource on server
def downloadOnServer(videoId):
  filename = downloadMp3("https://www.youtube.com/watch?v=" + videoId, "./downloads/")
  filename = filename[filename.rfind("/") + 1:]

  downloaded_file[0] = filename
  
  return filename

def deleteMp3File(x):
  relativeFilepath = "./downloads/" + downloaded_file[0]
  print(relativeFilepath)
  if os.path.isfile(relativeFilepath):
    print(os.remove(relativeFilepath))
  else:
    print("os.path.isfile(filepath) returned False")
  return 0

postFunctions = {
  "getSearchResults": getSearchResults,
  "download": downloadOnServer,
  "delete": deleteMp3File
}

@app.post("/<path>")
def postHandler(path):

  func = postFunctions.get(path, False)
  if func == False:
    return {0: "invalid url (endpoint)"}, 404

  payload = request.get_json()

  response_data = func(payload["payload"])

  return {"payload": response_data}, 200
