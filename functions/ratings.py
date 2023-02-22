from replit import db
from functions.helpers import *


def myratings(user, year):
  unsorted_list = []  
  list1 = [x for x in db['2022']]
  list2 = [x for x in db['2023']]
  iterable_list = list1 + list2  
  for item in iterable_list:
    for nota in item['rating']:                        
        if nota == user:                            
                     
            new_entry = {
                'id': item['id'],
                'artist': item['artist'],
                'album': item['album'],
                'rating': item['rating'][nota],
                'year': item['year'],
                'cover': item['cover'],
                'spotify': item['spotify'],
            }
            unsorted_list.append(new_entry)            
  if year == 'alltime':
    sorted_list = sorted(unsorted_list, key=lambda d: d['rating'], reverse=True)    
    return sorted_list[0:10]
  else:
    year_list = [x for x in unsorted_list if x['year'] == year]
    sorted_list = sorted(year_list, key=lambda d: d['rating'], reverse=True)    
    return sorted_list


def getratings(lista, album_id):
  pass


def update_album_rating(user, id, rating):    
    lista = list_helper(id)
    id = id_helper(id)    
    if str(user) in db.keys():
        if str(user) not in db[lista][id]['rating'].keys():
          db[lista][id]['rating'][str(user)] = {}
        db[lista][id]['rating'][str(user)] = rating
    else:
        pass

def get_rating_average(id):
    album_id = id_helper(id)
    average = []
    lista = list_helper(id)        
    try:
      for rating in db[lista][album_id]['rating'].items():
        user_rating = rating[1]
        average.append(user_rating)
      album_rating = str(sum(average) / len(average))[:3]
      return album_rating
    except:
      return 'Ainda sem notas'
