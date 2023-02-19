import discord
import math
import random
import os
import pytz
import urllib
import time
import random
import requests
import json
import csv
import pandas as pd
import numpy as np
from wordcloud import WordCloud
from collections import OrderedDict
from datetime import datetime
from discord.ext import commands
# from dotenv import load_dotenv
from replit import db
from keep_alive import keep_alive
from os import system
from time import sleep
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from urllib.request import Request
from functions.album_id import *
from functions.discogs import *
from functions.genres import *
from functions.topalbums import *
from functions.status import *
from functions.ratings import *
from functions.reviews import *
from functions.rym import *
from functions.helpers import *
from functions.user import *
from functions.wordcloud import *

# db.db_url = os.environ['DB']
REPLIT_DB_URL = os.getenv("DB")

intents = discord.Intents.all()

client = discord.Client(intents=intents)
#client = discord.Client()


def update_album_genre(user, id, genre):
    if str(user) in db.keys():
        id = id_helper(id)
        lista = list_helper(id)
        db[lista][id]['genre'] = genre.lower()        
    else:
        pass


def unique_roll(lista):
    roll = random.randint(0, len(db[lista]) - 1)
    album = db[lista][roll]    
    return album


def filtered_roll_random(add_filter):
    roll = random.randint(0, len(add_filter) - 1)
    album = add_filter[roll]    
    return album


def remove_points(user):
    db['points'][user] -= 1


def customized_top(number):
    pass


def filtered_roll(user, filter_list, operator, genre):
    add_filter = []
    try:
        if operator == 'only':
            add_filter = [
                x for x in filter_list
                if type(x) is not str and genre in x['genre']
            ]
        elif operator == 'ignore':
            add_filter = [
                x for x in filter_list
                if type(x) is not str and genre not in x['genre']
            ]
        else:
            pass
    except:        
        pass
    album = filtered_roll_random(add_filter)
    return album


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

# DEBUGGER
    if message.content.startswith('!acabou'):
        await message.channel.send(
            "https://thumbs.gfycat.com/AnchoredDesertedEft-size_restricted.gif"
        )

    if message.content.startswith('!run'):
        pass
        

        
    if message.content.startswith('!dburl'):        
        await message.channel.send(os.getenv("REPLIT_DB_URL"))

# ALL TIME
    if message.content.startswith('!roll alltime'):
        roll = random.randint(0, len(db['alltime']) - 1)
        album = db['alltime'][roll]
        filter_list = []
        for item in db[str(message.author)]:
            try:
                if item['tag'] == 'alltime':
                    filter_list.append(item)
            except:
                continue
        filter_list2 = [x['album'] for x in filter_list]
        while album['album'] in filter_list2:
            album = unique_roll('alltime')
        await message.channel.send(
            f'Bem-vindo ao desafio da lista de alltime álbuns do RYM, {message.author}. \nO álbum escolhido para você foi o:\n{divider}**{album["id"]}. {album["artist"]} - {album["album"]}** - *{album["year"]}*{divider}Você tem 24 horas para dar uma audição nesse álbum. Ao final, adicione-o à sua lista, simplesmente digitando !update\n{album["spotify"]}'
        )
        db[str(message.author) + '_temp_list'] = album

    # 2022
    if message.content.startswith('!setgenre'):
        album_id = int(message.content.split(' ', 2)[1])
        album_genre = message.content.split(' ', 2)[-1]
        lista = list_helper(album_id)
        id = id_helper(album_id)
        db[lista][id]["genre"] = album_genre
        try:
            await message.channel.send(
                f'tag(s) **{album_genre}** atualizada(s) com sucesso para o álbum **{db[lista][id]["id"]}. {db[lista][id]["artist"]} - {db[lista][id]["album"]}**'
            )            
        except:
            await message.channel.send(f'Algo deu errado.')

#######################################################

    if message.content.startswith('!genre'):
        genre = message.content.split(' ', 1)[-1].lower()
        if genre.lower() == 'missing':            
            result = [v for v in db['2022'] if not v['genre'].lower()]
            year_2023 = [v for v in db['2023'] if not v['genre'].lower()]
            result.extend(year_2023)            
            if len(result) > 0:
                await message.channel.send(
                    f'Álbuns que precisam ser taggeados:')
                for album in result:
                    await message.channel.send(
                        f'**{album["id"]}**. {album["artist"]} - {album["album"]}\n'
                    )                  
            
                await message.channel.send(
                    f'Todos os álbuns já foram taggeados.')
        else:
            result_2022 = [
                v for v in db['2022'] if genre in v['genre'].lower()
            ]
            result_2023 = [
                v for v in db['2023'] if genre in v['genre'].lower()
            ]
            result = result_2022 + result_2023
            if len(result) < 1:
                await message.channel.send(
                    f'Parece que não há nenhum álbum taggeado com o gênero **{genre}**'
                )
            else:
                await message.channel.send(
                    f'Álbuns taggeados com o(s) gênero(s) **{genre}**:\n{divider}'
                )
                for album in result:
                    await message.channel.send(
                        f'**{album["id"]}**. {album["artist"]} - {album["album"]}'
                    )
                await message.channel.send(f'{divider}')

#######################################################

    if message.content.startswith('!country'):
        c = message.content.split(' ', 1)[1:]        
        country = ' '.join(c).title()        
        if country.lower() == 'missing':
            result_2022 = [v for v in db['2022'] if v['country'] == '#']
            result_2023 = [v for v in db['2023'] if v['country'] == '#']
            result = result_2022 + result_2023
            if len(result) > 0:
                await message.channel.send(
                    f'Álbuns que precisam ser taggeados com o país:')
                for album in result:
                    await message.channel.send(
                        f'**{album["id"]}**. {album["artist"]} - {album["album"]}\n'
                    )
            else:
                await message.channel.send(
                    f'Todos os álbuns já foram taggeados com o país.')
        else:
            result_2022 = [v for v in db['2022'] if country in v['country']]
            result_2023 = [v for v in db['2023'] if country in v['country']]
            result = result_2022 + result_2023
            if len(result) < 1:
                await message.channel.send(
                    f'Parece que não há nenhum álbum do país **{country}**')
            else:
                await message.channel.send(
                    f'Álbuns do país **{country}**:\n{divider}')
                for album in result:
                    await message.channel.send(
                        f'**{album["id"]}**. {album["artist"]} - {album["album"]}'
                    )
                await message.channel.send(f'{divider}')

#######################################################

    if message.content.startswith('!roll 2023'):
        check_user(str(message.author))
        roll = random.randint(0, len(db['2023']) - 1)
        filter1 = message.content.split(' ', 3)
        user_list = [
            x['id'] for x in db[str(message.author)] if type(x) is not str
        ]
        filter_list = [x for x in db['2023'] if x['id'] not in user_list]
        album = db['2023'][roll]
        if len(filter_list) != 0:
            try:
                album = filtered_roll(str(message.author), filter_list,
                                      filter1[2], filter1[-1])
            except:
                roll = random.randint(0, len(filter_list) - 1)
                album = filter_list[roll]
        else:
            await message.channel.send(
                f'{str(message.author)}, parece que não há nenhum álbum disponível para você ouvir com estas configurações'
            )
        album_rating = get_rating_average(album["id"])
        genres = f'*{album["genre"]}*'
        title = album["artist"] + ' - ' + album["album"] + ' (' + album[
            "year"] + ')'
        embedVar = get_album_info(album, album_rating, genres, title)
        embedVar.add_field(
          name = '🎯  **Instruções para o desafio:**  🎯',
          value = '\nBem-vindo ao desafio dos lançamentos de 2023! Você tem 24 horas para dar uma audição nesse álbum. Ao final, adicione-o à sua lista, simplesmente digitando **!update**',
          inline = True
        )
             
        await message.channel.send(embed=embedVar)
        db[str(message.author) + '_temp_list'] = album

         

    if message.content.startswith('!update'):
        try:
            if len(message.content) > 7:
                album_id = int(message.content.split(' ')[-1])
                lista = list_helper(album_id)
                id = id_helper(album_id)                
                db[str(message.author) + '_temp_list'] = db[lista][id]                
                to_update = db[str(message.author) + "_temp_list"]                
            else:                
                to_update = db[str(message.author) + "_temp_list"]                
            update_album(str(message.author), to_update)
            try:                
                del db[str(message.author) + '_temp_list']
            except:
                pass            
            if type(to_update) is not str:                
                try:
                    await message.channel.send(
                        f'**{to_update["id"]}. {to_update["artist"]} - {to_update["album"]}** inserido com sucesso à sua lista!'
                    )
                except:
                    await message.channel.send(
                        f'**{to_update["artist"]} - {to_update["album"]}** inserido com sucesso à sua lista!'
                    )
            else:
                await message.channel.send(
                    f'**{to_update}** inserido com sucesso à sua lista!')
        except:
            await message.channel.send(
                f'**{str(message.author)}**, parece que você não tem nenhum album rollado para atualizar.'
            )

    if message.content.startswith('!review'):
        id = int(message.content.split(' ', 2)[1])
        album_id = id_helper(id)
        lista = list_helper(id)
        album_review = message.content.split(' ', 2)[2:]        
        update_album_review(message.author, id, album_review[0])
        if db[lista][album_id]['reviews'][str(message.author)]:
            await message.channel.send(
                f'Review do álbum **{id}. {db[lista][album_id]["artist"]} - {db[lista][album_id]["album"]}** atualizada com sucesso!'
            )
        else:
            await message.channel.send(f'erro')

    if message.content.startswith('!rating'):
        album_id = int(message.content.split(' ', 2)[1])
        album_rating = message.content.split(' ', 2)[-1]
        album_rating = album_rating.replace(',', '.')
        album_rating = float(album_rating.split('/')[0])
        update_album_rating(message.author, album_id, album_rating)
        lista = list_helper(album_id)
        if album_id > 999:
            album_id -= 1000
        elif album_id < 1000 and album_id > 93:
            album_id -= 95
        try:
            if db[lista][album_id]['rating'][str(message.author)]:
                await message.channel.send(
                    f'Rating de **{album_rating}/10** adicionado ao álbum **{db[lista][album_id]["id"]}. {db[lista][album_id]["artist"]} - {db[lista][album_id]["album"]}** com sucesso!'
                )
        except:
            await message.channel.send(f'Algo deu errado.')

    if message.content.startswith('!getreviews'):
        album_id = int(message.content.split(' ', 1)[-1])
        lista = list_helper(album_id)
        if album_id > 999:
            album_id - 1000
        elif album_id < 1000 and album_id > 93:
            album_id -= 95
        await message.channel.send(
            f'Reviews do **{db[lista][album_id]["artist"]} - {db[lista][album_id]["album"]}:\n**'
        )
        counter = 0
        for review in db[lista][album_id]['reviews'].items():
            await message.channel.send(f'**{review[0]}** - *"{review[1]}"*\n')
            counter += 1
        if counter == 0:
            await message.channel.send(
                f'Nenhuma resenha atribuída para este álbum.')
        await message.channel.send(f'\n{divider}')

########################################################################

    if message.content.startswith('!getratings'):
        id = int(message.content.split(' ', 1)[-1])
        lista = list_helper(id)
        album_id = id_helper(id)
        album = db[lista][album_id]
        album_id = int(message.content.split(' ', 1)[-1])
        embedVar = discord.Embed(title=f'Notas do {album["artist"]} - {album["album"]} ({album["artist"]} - {album["year"]})', color=0x0093FF)
        embedVar.set_thumbnail(
          url = album['cover']
        )
        average = []
        text = ''
        for rating in album['rating'].items():
            user_rating = rating[1]
            average.append(user_rating)
            text += f'✅\u200b \u200b{rating[0]}:\u200b \u200b **{rating[1]}**\n'
        text += '\n\u200b'
        try:
            embedVar.add_field(
            name='\u200b',
            value= text
              ) 
        except:
            pass
              
        if len(average) > 0:
            embedVar.add_field(
            name='**Média do server:**',
            value= f'⭐ **{str(sum(average) / len(average))[:3]}**',
            inline=False
            )
        else:
            embedVar.add_field(
            name='\u200b',
            value= f'Nenhuma nota atribuída para este álbum.',
            inline=False)        
        embedVar.add_field(
          name='Spotify',
          value=f'[link]({album["spotify"]})',
          inline=True
        )
        embedVar.add_field(
          name='RYM',
          value=f'[link]({album["rym"]})',
          inline=True
        )
        await message.channel.send(embed=embedVar)

########################################################################

    if message.content.startswith('!del_album'):
        id = int(message.content.split(' ', 1)[-1])
        user = str(message.author)
        album = del_last_album(id)
        if album:
            await message.channel.send(
                f'Álbum {album["id"]}. {album["artist"]} - {album["album"]} excluído da lista de lançamentos com sucesso!'
            )
            add_points(user)
            await message.channel.send(
                f'\n{divider}**{str(message.author)}**, seu total de pontos atualizado é **{db["points"][str(message.author)]}** ponto(s).'
            )
        else:

            await message.channel.send(
                'ID incorreto. Verifique as informações novamente.')

########################################################################

    if message.content.startswith('!2022status'):        
        total_notas, total_reviews = list_status('2022')
        await message.channel.send(
            f"-A lista de lançamentos de 2022 tem **{len(db['2022'])} álbuns** adicionados.\n-Já foram atribuídas **{total_notas}** notas e **{total_reviews}** reviews.\n{divider}"
        )

########################################################################

    if message.content.startswith('!status '):
        year = str(message.content.split(' ', 1)[-1])
        total_notas, total_reviews = list_status(year)
        total_albums = len(db[year])
        embedVar = discord.Embed(
            title=f'```🔵  Dados da lista de lançamentos de {year}  🔵```',
            color=0x0093FF)
        embedVar.add_field(name='**Álbuns adicionados**',
                           value=total_albums,
                           inline=False)
        embedVar.add_field(
            name='**Notas dadas**',
            value=
            f'**{total_notas}** — {round(total_notas/(total_albums*4)*100), 1}% do total',
            inline=True)

        embedVar.add_field(
            name='**Reviews dados**',
            value=
            f'**{total_reviews}** — {round(total_reviews/(total_albums*4)*100), 1}% do total',
            inline=True)
        embedVar.add_field(name='\u200b', value='\u200b', inline=False)
        embedVar.add_field(
            name='**Primeiro álbum adicionado à lista**',
            value=
            f'{db[year][0]["artist"]} - {db[year][0]["album"]}, em {db[year][0]["added_on_day"]}',
            inline=False)
        embedVar.add_field(
            name='**Último álbum adicionado à lista**',
            value=
            f'{db[year][-1]["artist"]} - {db[year][-1]["album"]}, em {db[year][-1]["added_on_day"]}',
            inline=False)       

        await message.channel.send(embed=embedVar)
      
#######################################################################################
    if message.content.startswith('!mystatus'):
        user = str(message.author).split(' ', 1)[-1]
        total = len(db[(str(message.author))])
        list_2022 = []
        list_2023 = []                 
        embedVar = discord.Embed(
            title=f'🟣  **{user}**  🟣',
            color=0x8000FF)
        embedVar.add_field(name='**Total de álbuns adicionados**',
                           value=total,
                           inline=False)
        embedVar.set_thumbnail(                    
          url=str(message.author.avatar)
        )
      
        if total == 0:
            embedVar.add_field(
            name='**Você ainda não tem nenhum álbum adicionado**',
            value= '#',
            inline=True)
        else:          
            list_2023, percentage_2023 = mystatus(list_2023, '2023',
                                                  str(message.author))
            list_2022, percentage_2022 = mystatus(list_2022, '2022',
                                                  str(message.author))
            try:
                embedVar.add_field(
            name='**Álbuns de 2022**',
            value= f'{len(list_2022)} - ({percentage_2022}%)',
            inline=True)
            except:
              pass
            try:
                embedVar.add_field(
            name='**Álbuns de 2023**',
            value= f'{len(list_2023)} - ({percentage_2023}%)',
            inline=True)
            except:
              pass            

            average = user_average_rating(user)
            embedVar.add_field(
            name='**Nota média**',
            value= average,
            inline=True)

            embedVar.add_field(
            name='**Pontos**',
            value= db['points'][user],
            inline=True)
      
            # try:
            id = db[user][-1]["id"]
            lista = list_helper(id)
            album_id = id_helper(id)
            embedVar.add_field(
              name='** ✅ Último álbum adicionado ✅**',
              value= f'[{db[lista][album_id]["artist"]} - {db[lista][album_id]["album"]}]({db[lista][album_id]["spotify"]}) - id: {db[lista][album_id]["id"]}',
              inline=False)
            # except:
            #   pass
            try:
               embedVar.add_field(
            name='**🎲 Álbum rolado 🎲**',
            value= f'[{db[str(message.author) + "_temp_list"]["id"]}. {db[str(message.author) + "_temp_list"]["artist"]} - {db[str(message.author) + "_temp_list"]["album"]}]({db[str(message.author) + "_temp_list"]["spotify"]}) - id: {db[str(message.author) + "_temp_list"]["id"]}',
            inline=False)
            except:
              embedVar.add_field(
            name='**🎲 Álbum rolado 🎲**',
            value= f'Nenhum álbum rolado para ouvir',
            inline=False)                          
            
            if len(db['obsession'][user]) > 2:
              album = f'[{db["obsession"][user]["artist"]} - {db["obsession"][user]["album"]}]({db["obsession"][user]["spotify"]}) - id: {db["obsession"][user]["id"]}'
            else:
              album = '\u200b'
            embedVar.add_field(
            name='**🔁 No repeat 🔁**',
            value= album,
            inline=False
          )         

            embedVar.set_footer(
              text= 'Para adicionar ou substituir seu "No repeat", digite **!setrepeat ID**'
            )            
              
        await message.channel.send(embed=embedVar)

#######################################################################################
              

    if message.content.startswith('!top') and str(message.content) != '!topgenres':
        number = 7
        year = ''
        if len(message.content) > 4:
            try:
                year = str(message.content.split(' ')[1])
                print(year)
                number = int(message.content.split(' ')[-1])
                if number > 7:
                  number == 7                
            except:
                pass
        
        sorted_list = top_albums(year)        
        counter = 1
        embedVar = discord.Embed(title=f'Lançamentos de {year} melhor avaliados', color=0x0093FF)
        text = ''
        if number != 0:
            for item in sorted_list:                                
                album = item["artist"] + ' - ' + item["album"]
                if len(album) > 36:
                  album = album[0:36] + '...'                
                if counter == 1:
                  counter = '👑'                  
                  text += f'**{counter}.** **[{album}]({item["spotify"]})** - nota: **{item["rating"]}**\n'
                  counter = 1
                  counter += 1                  
                else:
                  try:
                    text += f'**{counter}.** **[{album}]({item["spotify"]})** - nota: **{item["rating"]}**\n'                    
                  except:
                    print(item["id"])
                  counter += 1                    
                if counter > number:
                    break                
        else:
            text += f'{counter}. {item["artist"]} - {item["album"]} - nota: **{item["rating"]}**\n'
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
        
        embedVar.set_footer(
          text = 'Apenas álbuns com mais de uma nota recebida são contabilizados nessa lista\nAinda não ouviu algum desses álbuns e está curioso? Basta acessá-lo pelo ID e depois atualizar sua lista com **!update ID**, **!review ID** e **!rating ID**'
        )
        await message.channel.send(embed=embedVar)

#######################################################################################

    if message.content.startswith('!bottom'):
        number = 0
        year = 'alltime'
        if len(message.content) > 7:            
            try:
                number = int(message.content.split(' ')[-1])
                year = str(message.content.split(' ')[1])
            except:
                pass
        sorted_list = top_albums(year)
        sorted_list = sorted(sorted_list,
                             key=lambda d: d['rating'],
                             reverse=False)
        await message.channel.send(
            f'Álbuns com as notas mais baixas de {year} rankeados no server:\n{divider}'
        )
        counter = 0
        if number != 0:
            for item in sorted_list:
                await message.channel.send(
                    f'{len(sorted_list) - counter}. {item["artist"]} - {item["album"]}  :  **{item["rating"]}**'
                )
                counter += 1
                if counter > number:
                    break
        else:
            await message.channel.send(
                f'{counter}. {item["artist"]} - {item["album"]}  :  **{item["rating"]}**'
            )
            counter += 1
        await message.channel.send(
            f'{divider}*Apenas álbuns com mais de uma nota recebida são contabilizados nessa lista*'
        )

########################################################################################

    if message.content.startswith('!myreviews'):
        sorted_list = myreviews(str(message.author))
        await message.channel.send(
            f'**{message.author}**, suas reviews foram enviadas no privado.\n{divider}'
        )
        await message.author.send(
            f'**{message.author}**, seguem suas reviews para os lançamentos de 2022:\n{divider}'
        )
        counter = 0
        for item in sorted_list:
            await message.author.send(
                f'**{item["artist"]} - {item["album"]}**  :  *{item["review"]}*\n{divider}'
            )
            time.sleep(1)
            ########################################################################################

    if message.content.startswith('!myratings'):
        user = str(message.author)
        if len(str(message.content)) > 11:
          year = str(message.content.split(' ')[-1])
        else:
          year = 'alltime'
        sorted_list = myratings(str(message.author), year)        
        counter = 1                
        embedVar = discord.Embed(title=f'Melhores avaliados por {user} ({year})', color=0x0093FF)
        text = ''        
        embedVar.set_thumbnail(
              url = sorted_list[0]['cover']
            )
        for item in sorted_list:
            album = item["artist"] + ' - ' + item["album"]
            if len(album) > 36:
              album = album[0:36] + '...'  
            if counter == 1:
              counter = '👑'
              text += f'**{counter}. [{album} ({item["year"]})]({item["spotify"]})** - nota: **{item["rating"]}**\n'                
              counter = 1
              counter += 1              
            else:
              text += f'**{counter}. [{album} ({item["year"]})]({item["spotify"]})** - nota: **{item["rating"]}**\n'
              counter += 1                
            if counter > 7:
                break                                    
        try:
          embedVar.add_field(
          name='\u200b',
          value= text
            )
        except:
            pass        
        
        await message.channel.send(embed=embedVar)

########################################################################################

# HELPER
    if message.content.startswith('!myalbums'):
        lista = myalbums(str(message.author))
        await message.channel.send(lista)

#########################################################################################

# HELPER
    if message.content.startswith('!missing'):
        missing_reviews, missing_ratings = missing(str(message.author))
        await message.channel.send(
            f'**{str(message.author)}**, seguem suas resenhas faltantes:\n{divider}'
        )
        try:
            for id in missing_reviews:
                await message.channel.send(
                    f'**{db["2022"][id]["id"]}.** {db["2022"][id]["artist"]} - {db["2022"][id]["album"]}'
                )
        except:
            pass
        await message.channel.send(f'{divider}')
        await message.channel.send(
            f'**{str(message.author)}**, seguem suas notas faltantes:\n{divider}'
        )
        try:
            for id in missing_ratings:
                await message.channel.send(
                    f'**{db["2022"][id]["id"]}.** {db["2022"][id]["artist"]} - {db["2022"][id]["album"]}'
                )
        except:
            pass
        await message.channel.send(f'{divider}')

        ########################################################################################

    if message.content.startswith('!lastadded'):
        counter = 1
        year = '2023'
        index = len(db[year]) - counter
        title = f'```🔵  Últimos 10 álbuns adicionados à lista de {year}  ```🔵'
        embedVar = discord.Embed(title=f'{title}', color=0x0093FF)
        text = ''
        for album in range(10):
            text += f'{db[year][index]["id"]}. **{db[year][index]["artist"]} - {db[year][index]["album"]}**, em {db[year][index]["added_on_day"]}\n'
            index -= 1
          
          
        try:
            embedVar.add_field(
                name='\u200b',
                value= text
            )
        except:
            pass

        await message.channel.send(embed=embedVar)


########################################################################################

    if message.content.startswith('!sc'):
        id = int(message.content.split(' ', 2)[1])
        album_id = id_helper(id)
        lista = list_helper(id)
        c = message.content.split(' ', 2)[2:]
        country = ' '.join(c).title()
        db[lista][album_id]['country'] = country
        await message.channel.send(
            f'{country} atribuído para o id {db[lista][album_id]["id"]}')

    if message.content.startswith('!users'):        
        nivel = len(db[(str(message.author))])
        await message.channel.send('Usuários participando do desafio:\n')
        for user in db.keys():
            if '_temp_list' not in str(user) and '#' in str(user):
                sender = len(db[(str(user))])
                await message.channel.send(f'{user}, Challenger +{sender}')

    if message.content.startswith('!leaderboard'):        
        nivel = len(db[(str(message.author))])
        await message.channel.send(f'Leaderboard:\n')
        leaderboard = []
        for user in db.keys():
            if '#' in user and '_temp_list' not in user:
                badges = len(db[(str(user))])
                sender1 = {'name': user, 'nbadges': badges}
                leaderboard.append(sender1)
        for user in sorted(leaderboard,
                           key=lambda i: i['nbadges'],
                           reverse=True):
            await message.channel.send(
                f"{user.get('nbadges')} - {user.get('name')}\n")

    if message.content.startswith('!del_users'):
        for n in db.keys():
            del db[n]

    if message.content.startswith('!commands'):
        await message.channel.send(
            f'Comandos do bot:\n\n**!newalbum - ARTISTA - ALBUM - SPOTIFY**   Adiciona um álbum à lista de lançamentos de 2022.\n**!roll alltime**   Seleciona um álbum aleatório da lista de melhores álbuns rankeados de todos os tempos.\n**!roll 2022**   Seleciona um álbum aleatório da nossa lista de lançamentos de 2022.\n**!roll 2022 only GENRE**   Rola apenas álbuns taggeados com o gênero específico da lista de lançamentos de 2022.\n**!roll 2022 ignore GENRE**   Ignora o gênero específico ao rolar álbuns da lista de lançamentos de 2022.\n**!update**   Atualiza sua lista de álbuns ouvidos com o último álbum rollado.\n**!mystatus**   Exibe seus status no desafio.\n**!myratings**    Exibe seus álbuns ouvidos melhores avaliados.**\n**!myreviews**    Exibe, por mensagem direta (DM), todas as resenhas que você já realizou no desafio.\n!2022status**   Exibe a quantidade de álbuns da lista de lançamentos de 2022.\n**!list2022**   Exibe todos os álbuns já adicionados à lista de lançamentos de 2022.\n**!list LETRA**   Exibe todos os artistas adicionados na lista de lançamentos de 2022 que comecem com a LETRA escolhida.\n**!id NUMERO**    Exibe o álbum com o respectivo ID\n**!review ID TEXTO**    Salva o texto como a resenha para o álbum do respectivo ID\n**!rating ID NOTA**    Salva a nota para o álbum do respectivo ID\n**!getreviews ID**    Exibe todas as resenhas para o álbum do respectivo ID\n**!getratings ID**    Exibe todas as notas para o álbum do respectivo ID\n**!topalbums**    Exibe os álbuns mais bem avaliados do server\n**!users**   Exibe todos os usuários participantes do desafio.\n**!leaderboard**   Exibe a leaderboard do desafio.'
        )
    if message.content.startswith('!newalltime'):
        album_novo = message.content.split(' - ')
        artist = album_novo[1]
        album = album_novo[2]
        year = str(album_novo[3])
        spotify = album_novo[4]
        id = db['alltime'][-1]['id'] + 1
        reviews = {}
        rating = {}
        genre = '#'
        tag = 'alltime'
        new = {
            'artist': artist,
            'album': album,
            'spotify': spotify,
            'id': id,
            'reviews': reviews,
            'rating': rating,
            'genre': genre,
            'year': year,
            'tag': tag
        }
        if 'alltime' in db.keys():
            if new in db['alltime']:
                await message.channel.send(
                    f'Não foi possível adicionar esse álbum pois ele já está na lista.'
                )
            else:
                db['alltime'].append(new)
                await message.channel.send(
                    f'**{new["artist"]} - {new["album"]}** inserido à lista de alltime do RYM com sucesso! (id: **{new["id"]}**)'
                )
        else:
            db['alltime'] = [new]

    if message.content.startswith('!newalbum') or message.content.startswith(
            '!new'):
        create_db()
        album_novo = message.content.split(' - ')
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
        added_by = str(message.author)
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
        if db['points'][str(message.author)] > 0:
            if '2023' in db.keys():
                if new['album'].lower() in album_list:                    
                    await message.channel.send(
                        f'Não foi possível adicionar esse álbum pois ele já está na lista.'
                    )
                else:                    
                    db['2023'].append(new)
                    await message.channel.send(
                        f'**{new["artist"]} - {new["album"]}** inserido à lista de lançamentos de 2023 com sucesso! (id: **{new["id"]})**\n{divider}adicionado em **{new["added_on_day"]}** às **{new["added_on_time"]}** por **{new["added_by"]}**'
                    )
                    remove_points(str(message.author))
                    await message.channel.send(
                        f'\n{divider}**{str(message.author)}**, seu total de pontos atualizado é **{db["points"][str(message.author)]}** ponto(s).'
                    )
            else:
                db['2023'] = [new]
        else:
            await message.channel.send(
                f'**{str(message.author)}**, você não tem pontos suficientes para esta operação. Total de pontos: **{db["points"][str(message.author)]}**\nPara ganhar pontos, participe do desafio do #album-challenge '
            )

    if message.content.startswith('!teste'):                
        user_id = str(message.author.id)        
        user = 'discordapp.com/users/' + user_id
        await message.channel.send(f'bot funcionando normalmente.\n{user}')

    if message.content.startswith('!listgenres'):
        genres = list(
            set([x['genre'] for x in db['2022'] if type(x) is not str]))
        print(genres)        

    if message.content.startswith('!list2022'):
        new_entries = [[v for v in d.values()][:-1] for d in db['2022']]
        new_entries2 = []
        counter = 0
        number = 0
        for item in new_entries:
            new_entries2.append(f'**{number}**. {item[0]} - {item[1]}')
            counter += 1
            number += 1
        await message.channel.send(
            'Álbuns já adicionados à lista de lançamentos de 2022:\n')
        for album in new_entries2:
            await message.channel.send(album)
        await message.channel.send(divider)

    if message.content.startswith('!listalltime'):

        await message.channel.send(
            f'Álbuns da lista de alltime álbuns do RYM:\n{divider}')
        for album in db['alltime']:
            await message.channel.send(
                f'**{album["id"]}**. {album["artist"]} - {album["album"]} - *{album["year"]}*'
            )
        await message.channel.send(divider)

    if message.content.startswith('!list '):
        if len(message.content.split(' ')) < 3:
            year = '2023'
            letter = message.content.split(' ')[-1][0]
        else:
            year = message.content.split(' ')[1]
            letter = message.content.split(' ')[2][0]
        new_entries = [[v for v in d.values()] for d in db[year]]
        new_entries2 = []
        for item in new_entries:
            new_entries2.append(f'{item[0]} - {item[1]} (id: **{item[3]}**)')
        await message.channel.send(
            f'Álbuns de artistas que começam com a letra **{letter.upper()}** já adicionados à lista de lançamentos de {year}:\n'
        )
        number = 0
        for album in new_entries2:
            if album[0].lower() == letter.lower():
                await message.channel.send(album)
                number += 1
        await message.channel.send(f'{divider}')
        if number == 0:
            await message.channel.send(
                f'Nenhum artista com a letra **{letter.upper()}**')
        elif number == 1:
            await message.channel.send(
                f'- **{number}** artista com a letra **{letter.upper()}**')
        else:
            await message.channel.send(
                f'- **{number}** artistas com a letra **{letter.upper()}**')

        #############################################################################

    if message.content.startswith('!id '):
        id = int(message.content.split(' ')[-1])
        lista = list_helper(id)
        album_id = id_helper(id)        
        album = db[lista][album_id]
        album_rating = get_rating_average(id)
        genres = f'*{album["genre"]}*'
        title = album["artist"] + ' - ' + album["album"] + ' (' + album[
            "year"] + ')'
        embedVar = get_album_info(album, album_rating, genres, title)

        await message.channel.send(embed=embedVar)        

#############################################################################

# Bring latest 4 albums
    if message.content.startswith('!getnew'):
        for number in range(4):
            await message.channel.send(
                f'\n{album_artist_title[number].getText()[40::].strip()} - {album_title[number].getText()}\n'
                f'Release date: {release_date[number].findChild("span").getText()} —— '
                f'Rating: {album_rating[number].contents[1].getText().strip()}'
            )
            time.sleep(0.5)
            await message.channel.send('...\n')
        await message.channel.send(
            f'\nsource: https://www.metacritic.com/browse/albums/release-date/new-releases/date'
        )

#############################################################################
# Get RYM album page

    if message.content.startswith('!sr'):
        rym = message.content.split(' ', 2)[-1]
        id = int(message.content.split(' ', 2)[1])
        album_id = id_helper(id)
        lista = str(list_helper(id))        
        db[lista][album_id]['rym'] = rym
        await message.channel.send(
            f'link {rym} atribuído para o álbum id {db[lista][album_id]["id"]}'
        )


#############################################################################
    if message.content.startswith('!addpoints'):
        user = message.content.split(' ', 2)[1]
        if str(message.author) == 'Mizuhara#8189':
            points = int(message.content.split(' ', 2)[-1])
            add_points(user)
            await message.channel.send(
                f'Total de pontos do usuário {user}: {db["points"][user]}')
        else:
            await message.channel.send(f'Operação permitida apenas para Mods')

    if message.content.startswith('!removepoints'):
        user = message.content.split(' ', 2)[1]
        if str(message.author) == 'Mizuhara#8189':
            points = int(message.content.split(' ', 2)[-1])
            remove_points(user)
            await message.channel.send(
                f'Total de pontos do usuário {user}: {db["points"][user]}')
        else:
            await message.channel.send(f'Operação permitida apenas para Mods')

#############################################################################
    if message.content.startswith('!setstatus'):
        msg = str(message.content.split(' ', 1)[-1])
        user = str(message.author)        
        db['status'][user] = msg
        await message.channel.send('Mensagem de status atualizada!')

#############################################################################
    if message.content.startswith('!setcover'):
        cover = message.content.split(' ', 2)[-1]
        id = int(message.content.split(' ', 2)[1])
        album_id = id_helper(id)
        lista = str(list_helper(id))
        db[lista][album_id]['cover'] = cover
        await message.channel.send('album cover atualizado!')

#############################################################################
    if message.content.startswith('!serverstatus'):
        for msg in db['status']:
            await message.channel.send(f'**{msg}:** *{db["status"][msg]}*')


#############################################################################
          
    if message.content.startswith('!setrepeat'):
        id = int(message.content.split(' ', 1)[-1])
        lista = str(list_helper(id))
        album_id = id_helper(id)
        db['obsession'][str(message.author)] = db[lista][album_id]
        await message.channel.send(f'No repeat atualizado!')

#############################################################################
          
    if message.content.startswith('!topgenres'):        
        total, genres, cover = top_genres()
        embedVar = discord.Embed(title=f'Gêneros mais adicionados', color=0x0093FF)  
        embedVar.set_thumbnail(
          url = cover
        )
        text = ''
        counter = 0        
        for item in genres:            
            text += f'🎵\u200b \u200b{item[0]}:\u200b \u200b **{item[1]}**\n'
            counter += 1
            if counter == 20:
              break          
        # text += '\n\u200b'        
        embedVar.add_field(
        name='\u200b',
        value= text
          )
        embedVar.add_field(
        name='Quantidade de tipos de gêneros adicionados',
        value= f'{total} gêneros diferentes',
        inline= False
          )
        
        await message.channel.send(embed=embedVar)

#############################################################################
    if message.content.startswith('!wordcloud'):
        id = int(message.content.split(' ', 2)[-1])
        lista = str(list_helper(id))
        album_id = id_helper(id)
        text = []
        for review in db[lista][album_id]['reviews']:
            user_review = db[lista][album_id]['reviews'][review].replace(
                '"', "'")
            text.append(user_review)
        text = ' '.join(text)
        new_text = text.replace('"', "'")
        wordcloud = word_cloud(new_text)
        url = wordcloud.show()
        await message.channel.send(url)

my_secret = os.environ['TOKEN']

keep_alive()
try:
    client.run(my_secret)
except discord.errors.HTTPException:
    print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
    system("python restarter.py")
    system('kill 1')
    # time.sleep(50)
