import random
from collections import Counter
from replit import db

def top_genres():    
    # genres_2022 = [x['genre'].split(',') for x in db['2022']]
    # genres_2023 = [x['genre'].split(',') for x in db['2023']]    	
    genres_2022 = []
    genres_2023 = []    	  
    for item in db['2022']:
      genres = item['genre'].split(',')
      for genre in genres:
        genres_2022.append(genre.lower().strip())
    for item in db['2023']:
      genres = item['genre'].split(',')
      for genre in genres:
        genres_2023.append(genre.lower().strip())
    genres = genres_2022 + genres_2023    
    total = len(set(genres))
    counter = Counter(genres)
    sorted_items = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    top_genre = sorted_items[0][0]
    top_genre_list_2022 = [x['cover'] for x in db['2022'] if top_genre in x['genre']]
    top_genre_list_2023 = [x['cover'] for x in db['2022'] if top_genre in x['genre']]
    top_genre_list = top_genre_list_2022 + top_genre_list_2023
    cover = random.choice(top_genre_list)
    return total, sorted_items, cover


