from replit import db

def list_status(year):
  total_notas = 0
  total_reviews = 0
  for item in db[year]:
    try:
      if len(item['rating']) > 0:
        for nota in item['rating']:
          if len(nota) > 0:
            total_notas += 1
      if len(item['reviews']) > 0:
        for review in item['reviews']:
          if len(review) > 0:
            total_reviews += 1
    except:
      continue
  return total_notas, total_reviews



def mystatus(list, year, user):
  for album in db[user]:
    if album['year'] == year:      
      list.append(album)        
  percentage = round((len(list) / len(db[year])) * 100, 2)
  return list, percentage
                