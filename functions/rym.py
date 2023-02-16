import requests
from urllib.request import Request
from bs4 import BeautifulSoup


def get_rym_page(artist, album):
  text = 'rateyourmusic' + artist + ' ' + album
  results = 10
  page = requests.get(f"https://www.google.com/search?q={text}&num={results}")
  soup = BeautifulSoup(page.content, "html.parser")
  links = soup.findAll('a')
  links_list = []
  
  for link in links:
      link_href = link.get('href')
      if "url?q=" in link_href and not "webcache" in link_href:
          links_list.append(link.get('href').split("?q=")[1].split("&sa=U")[0])
  
  return links_list[0]
 