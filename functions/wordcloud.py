from wordcloud import WordCloud
from PIL import Image
import io
import matplotlib.pyplot as plt


def word_cloud(text):
  common_words = ['a','o','as', 'os', 'um','uma','é','e','são','uns','umas',
                  'ele','ela','eles','elas','dos','das','do','da','com','como'
                'esse','essa','que','mais','mas','de','em','por','para']

  filtered_text = [x for x in text.split(' ') if x.lower() not in common_words]
  new_text = ' '.join(filtered_text)
  wc = WordCloud().generate(new_text)
  plt.axis('off')
  plt.imshow(wc)
  img_buff = io.BytesIO()
  plt.savefig(img_buff, format='png')
  
  im = Image.open((img_buff))  
  # word_cloud_chart = plt.show()
  # print(word_cloud_chart)
  return im