import time
import discord
import pytz
from replit import db
from datetime import datetime
from functions.rym import *
from functions.discogs import *
from functions.helpers import *
from functions.user import *

def add_new_album(user, message):
  create_db()
  album_novo = message.split(' - ')
  artist = album_novo[1]
  album = album_novo[2]
  spotify = album_novo[3]
  rym = get_rym_page(artist, album)
  id = 0
  try:
      id = db['2023'][-1]['id'] + 1
  except:
      pass
  # Make sure id increments through years
  if len(db['2023']) < 1:
      id = len(db['2022']) + 1
  reviews = {}
  rating = {}
  genre = '#'
  year = '2023'
  country = ''
  cover = get_album_cover(artist + ' ' + album)              
  added_on_day = datetime.now(
      pytz.timezone('America/Sao_Paulo')).strftime("%d/%m/%Y")
  added_on_time = datetime.now(
      pytz.timezone('America/Sao_Paulo')).strftime("%H:%M:%S")
  added_by = user
  new = {
      'artist': artist,
      'album': album,
      'spotify': spotify,
      'id': id,
      'reviews': reviews,
      'rating': rating,
      'genre': genre,
      'year': year,
      'country': country,
      'rym': rym,
      'added_on_day': added_on_day,
      'added_on_time': added_on_time,
      'added_by': added_by,
      'cover': cover
  }
  album_list = [x['album'].lower() for x in db['2023']]
  embedVar = discord.Embed(
    title=f'Mensagem de confirmação do bot', color=0xFF0000
  )
  text = ''
  if db['points'][user] > 0:
      if '2023' in db.keys():
          if new['album'].lower() in album_list:                    
              text += f'Não foi possível adicionar esse álbum pois ele já está na lista.'
              
          else:                    
              db['2023'].append(new)
              text += f'✅\u200b\u200b **{new["artist"]} - {new["album"]} ({new["year"]})** inserido à lista de lançamentos de 2023 com sucesso em **{new["added_on_day"]}** às **{new["added_on_time"]}** por **{new["added_by"]}**' 
              remove_points(user)
          embedVar.add_field(
                    name='\u200b',
                    value= text,
                    inline=False
            )
          embedVar.add_field(
                    name='\u200b',
                    value= f'id: **{new["id"]}**',
                    inline=False
            ) 
          embedVar.add_field(
                    name='\u200b',
                    value= f'**{user}**, seu total de pontos atualizado é **{db["points"][user]}** ponto(s).',
            inline=False
                      )
          embedVar.set_thumbnail(url=new["cover"])
      else:
          db['2023'] = [new]
  else:
      embedVar.add_field(
                    name='\u200b',
                    value= f'❌\u200b\u200b **{user}**, você não tem pontos suficientes para esta operação. Total de pontos: **{db["points"][user]}**'
      )
      embedVar.add_field(
                    name='\u200b',
                    value= f'Para ganhar pontos, participe do desafio do #album-challenge ', inline=False
      )
      

  return embedVar
  