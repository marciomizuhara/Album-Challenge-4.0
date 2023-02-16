from replit import db

def top_albums(year):
  unsorted_list = []  
  if year == 'alltime':
    for item in db['2022']:
      try:
        if len(item['rating']) > 0:
           try:
              if len(item['rating'].values()) > 1:
                score = sum(item['rating'].values())
                final_score = round(score/len(item['rating'].values()), 2)
                new_entry = {
                    'id': item['id'],
                    'artist': item['artist'],
                    'album': item['album'],
                    'rating': final_score,
                    'cover': item['cover'],
                    'spotify': item['spotify']
                  
                }
                unsorted_list.append(new_entry)
           except:
              continue
      except:
        continue
    for item in db['2023']:
      try:
        if len(item['rating']) > 0:
           try:
              if len(item['rating'].values()) > 1:
                score = sum(item['rating'].values())
                final_score = round(score/len(item['rating'].values()), 2)
                new_entry = {
                    'id': item['id'],
                    'artist': item['artist'],
                    'album': item['album'],
                    'rating': final_score,
                    'cover': item['cover'],
                    'spotify': item['spotify']
                }
                unsorted_list.append(new_entry)
           except:
             continue
      except:
        continue
    sorted_list = sorted(unsorted_list, key=lambda d: d['rating'], reverse=True)
    return sorted_list
  else:    
    for item in db[year]:      
      try:
        if len(item['rating']) > 0:
           try:
              if len(item['rating'].values()) > 1:
                score = sum(item['rating'].values())
                final_score = round(score/len(item['rating'].values()), 2)
                new_entry = {
                    'id': item['id'],
                    'artist': item['artist'],
                    'album': item['album'],
                    'rating': final_score,
                    'cover': item['cover'],
                    'spotify': item['spotify'],
                }
                unsorted_list.append(new_entry)
           except:
              continue
      except:
        continue
    sorted_list = sorted(unsorted_list, key=lambda d: d['rating'], reverse=True)
    return sorted_list


def bottom_albums():
  pass
  