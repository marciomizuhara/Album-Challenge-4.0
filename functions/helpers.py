from replit import db

divider = '-----------------------------------------------------------------\n'


def create_db():
  if '2023' in db.keys():
    pass
  else:
    db['2023'] = []
  

def list_helper(id):
  lista = ''
  if id < 94:
    lista = '2022'
  elif id > 94 and id < 1000:
    lista = '2023'
  else:
    lista = 'alltime'
  return lista


def id_helper(id):
  album_id = id
  if id > 999:
    album_id -= 1000
  elif id > 94 and id < 1000:
    album_id -= 95
  else:
    pass
  return album_id  

def myalbums(user):
  lista = []
  for album in db[user]:
    texto = f'{album["artist"]} - {album["album"]}'
    lista.append(texto)
  return lista


def missing(user):
  user_list = [x for x in db[user]]
  review_list = []
  rating_list = []  
  for album in db['2022']:    
    try:
      if user in album['reviews']:
        review_list.append(album['id'])
    except:
      pass
    try:
      if user in album['rating']:
        rating_list.append(album['id'])
    except:
      pass      
  missing_reviews = []
  missing_ratings = []  
  if len(review_list) > 0:
    missing_reviews = [x['id'] for x in user_list if x['id'] not in review_list]
  if len(rating_list) > 0:
    missing_ratings = [x['id'] for x in user_list if x['id'] not in rating_list]
  return missing_reviews, missing_ratings


def del_last_album(id):
  if id == db['2023'][-1]['id']:     
    album = db['2023'][-1]
    del db['2023'][-1]
    return album
  else:
    return None
    