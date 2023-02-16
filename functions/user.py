from replit import db
from functions.helpers import *


def check_user(user):
  if not db[user]:    
    db[user] = []
    db['points'][user] = 1    
  else:
    pass


def add_points(user):    
    db['points'][user] += 1 


def update_album(user, album):
  del album['spotify']
  del album['reviews']
  del album['rating']
  del album['genre']
  del album['added_by']
  del album['added_on_time']
  del album['added_on_day']
  del album['country']
  del album['cover']  
  if str(user) in db.keys():
      lista1 = db[str(user)]
      lista1.append(album)
      db[str(user)] = lista1
  else:
      db[str(user)] = [album]        
  add_points(user)


def user_average_rating(user):
  notas = []
  for album in db['2022']:
    try:
      notas.append(album['rating'][user])
    except:
      continue
  for album in db['2023']:
    try:
      notas.append(album['rating'][user])
    except:
      continue
  return round(sum(notas)/len(notas), 2)


