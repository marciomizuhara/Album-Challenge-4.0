from replit import db
from functions.helpers import *


def myreviews(user):
  unsorted_list = []      
  for item in db['2023']:
    for review in item['reviews']:
      if review == user:            
        try:
          new_entry = {
                'artist': item['artist'],
                'album': item['album'],
                'review': item['reviews'][review]
            }
          unsorted_list.append(new_entry)              
        except:              
          continue
  sorted_list = sorted(unsorted_list, key=lambda d: d['artist'])
  return sorted_list


def update_album_review(user, id, review):    
    album_id = id_helper(id)
    lista = list_helper(id)    
    if str(user) in db.keys():
        if str(user) not in db[lista][album_id]['reviews'].keys():
          db[lista][album_id]['reviews'][str(user)] = {}
        db[lista][album_id]['reviews'][str(user)] = review
    else:
        pass