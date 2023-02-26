import discord
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


def embed_top_albums(number, year, sorted_list):
  counter = 1
  year_text= ' '
  if year != 'alltime':
    year_text += f'de {year}'
  embedVar = discord.Embed(title=f'Lançamentos{year_text} melhor avaliados',
                           color=0x0093FF)
  text = ''
  if number != 0:
      for item in sorted_list:                                
          album = item["artist"] + ' - ' + item["album"]                
          if len(album) > 32:
            album = album[0:32] + '...'                
          if counter == 1:
            counter = '👑'                  
            text += f'**{counter}.** **[{album}]({item["spotify"]})** : **{item["rating"]}**\n'
            counter = 1
            counter += 1                  
          else:            
            try:
              text += f'**{counter}.** **[{album}]({item["spotify"]})** : **{item["rating"]}**\n'
              counter += 1  
            except:                    
              counter += 1                    
          if counter > number:   
              break                
  else:
      text += f'{counter}. {item["artist"]} - {item["album"]} : **{item["rating"]}**\n'
      counter += 1
  embedVar.set_thumbnail(
    url = sorted_list[0]['cover']
  )  
  try:
    embedVar.add_field(
    name='\u200b',
    value= text
      )
  except:
      pass

  embedVar2 = discord.Embed(color=0x0093FF)
  text2 = ''    
  for item in sorted_list[7:14]:                                
      album = item["artist"] + ' - ' + item["album"]                
      if len(album) > 32:
        album = album[0:32] + '...'                
      try:
        text2 += f'**{counter}.** **[{album}]({item["spotify"]})** : **{item["rating"]}**\n'        
        counter += 1  
      except:                            
        counter += 1                                                             
  try:
    embedVar2.add_field(
    name='\u200b',
    value= text2
      )
  except:
    pass
  return embedVar, embedVar2