import discord
from replit import db


def get_album_info(album, album_rating, genres, title):
    embedVar = discord.Embed(
      title=f'⭐  {title}  ⭐', color=0x00ff00
    )

    embedVar.add_field(
      name='**Genres**',
      value=genres,
      inline=False
    )
    embedVar.add_field(
      name='**ID**',
      value=album["id"],
      inline=True
    )
    embedVar.add_field(
      name='**País**',
      value=album['country'],
      inline=True
    )
  
    embedVar.add_field(
      name='**Adicionado em**',
      value=album["added_on_day"] + ' às ' + album["added_on_time"] + ' por ' + album["added_by"],
      inline=False
    )
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
    embedVar.add_field(
      name='Nota no server',
      value=f'       **{album_rating}**     ',
      inline=True
    )
    embedVar.set_image(url=album['cover'])

    return embedVar