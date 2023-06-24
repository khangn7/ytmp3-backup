import requests, os

# api documentation at
# https://developers.google.com/youtube/v3/docs/search/list

api_key = os.environ["API_KEY"]

url = "https://youtube.googleapis.com/youtube/v3/search"

MAX_RESULTS = 15

# gets youtube search results of unformattedQueryStr
# if fails, try again until fifth fail, then return False
# if succeeds, returns list[] of youtube#searchResult" objects
def get_videos(unformattedQueryStr, try_no=5):

  if try_no == 0:
    return False
  
  queryParams = {
    "part": "snippet",
    "maxResults": MAX_RESULTS,
    "q": unformattedQueryStr,
    "key": api_key
  }
  
  response = requests.get(url, params=queryParams)

  if response.status_code != 200:
    return get_videos(unformattedQueryStr, try_no-1)
  
  json = response.json()

  if json.get("error", False):
    return []
  
  videos = []
  
  for searchResult in json["items"]:
    if searchResult["id"]["kind"] == "youtube#video":
      videos.append(searchResult)

  return videos


# example get request url
# url = "https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=25&q=the%20weeknd&key=" + api_key
# example response.json()
# {
#   "kind": "youtube#searchListResponse",
#   "etag": "3yLW4SK2P4zXmcF2rMtk4CefhWE",
#   "nextPageToken": "CBkQAA",
#   "regionCode": "CA",
#   "pageInfo": {
#     "totalResults": 1000000,
#     "resultsPerPage": 25
#   },
#   "items": [
#     {
#       "kind": "youtube#searchResult",
#       "etag": "mnsfi7GpF7eViBgsZYcGmkGtUg8",
#       "id": {
#         "kind": "youtube#video",
#         "videoId": "XXYlFuWEuKI"
#       },
#       "snippet": {
#         "publishedAt": "2021-01-05T17:00:12Z",
#         "channelId": "UCF_fDSgPpBQuh1MsUTgIARQ",
#         "title": "The Weeknd - Save Your Tears (Official Music Video)",
#         "description": "Official music video by The Weeknd performing \"Save Your Tears\"– 'After Hours' available everywhere now: ...",
#         "thumbnails": {
#           "default": {
#             "url": "https://i.ytimg.com/vi/XXYlFuWEuKI/default.jpg",
#             "width": 120,
#             "height": 90
#           },
#           "medium": {
#             "url": "https://i.ytimg.com/vi/XXYlFuWEuKI/mqdefault.jpg",
#             "width": 320,
#             "height": 180
#           },
#           "high": {
#             "url": "https://i.ytimg.com/vi/XXYlFuWEuKI/hqdefault.jpg",
#             "width": 480,
#             "height": 360
#           }
#         },
#         "channelTitle": "TheWeekndVEVO",
#         "liveBroadcastContent": "none",
#         "publishTime": "2021-01-05T17:00:12Z"
#       }
#     }, {...}
#    ]... }


