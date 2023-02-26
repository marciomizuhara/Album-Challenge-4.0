from replit import db
import discogs_client
import os

discogs_secret = os.environ['DISCOGS_TOKEN']

def get_album_cover(album):
  d = discogs_client.Client(
    user_agent = 'my_user_agent/1.0',
    user_token= discogs_secret
  )
  results = d.search(album)
  try:
    cover = results.page(1)[0].data['cover_image']
  except:
    cover = '#'
  return cover
