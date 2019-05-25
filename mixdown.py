# Script of getting mixes off of Mixcloud

import subprocess
import requests
import re
from subprocess import call

# genres are literal url paths after /discover you can add or remove them to your liking
# dump file full of links only.

for genre in ["beats", "deep-house", "drum-bass", "dub", "dubstep", "edm", "electronica", "house", "tech-house", "techno", "trance", "trap"] :
   command = "lynx -dump -listonly www.mixcloud.com/discover/"
   command += genre
   command += " > urls.txt"
   call(command, shell=True)

# for every line in file see if is a good url and strip out ones we don't want

   with open("urls.txt") as file:
      for line in file :
         url = re.findall(r'(https?://www.mixc[^\s]+)', line)
         url = str(url)
         if url :
            slashes = url.count("/") # ensure correct path depth
            select = url.count("select") # thise are just links to more lists
            discover = url.count("discover")

            if slashes == 5 and select == 0 and discover == 0 :
               # string cleaning
               url = url.replace("[","")
               url = url.replace("]","")
               url = url[1:]
               url = url[:-1]
           
               print(url)

               # using a 3rd party download site to generate the direct link as i've not figured that out !

               sess = requests.Session()
               r = sess.get("http://99downloader.com/mixcloud-downloader")
               token = r.cookies['csrftoken']
               print(token)

               # create post data for link form

               data = {'csrfmiddlewaretoken':token, 
                    'mvideo-url':url} 
               print(data)
            
            #break

               r = sess.post(url = "http://99downloader.com/download-mixcloud", data = data) # send link in form
            #print(r.text)
               linky = re.findall(r'(href="https://stream[^\s]+)', r.text) # pull direct download link from retuned webpage
               linky = str(linky) # string conversion
               linky = linky[7:]  # string cleanup
               linky = linky[:-2]
               linky += "\"" 
               print(linky)

               # filename generation

               filename = url[25:]
               filename = filename[:-1]
               filename = filename.replace("/","-")

               if "m4a" in linky :
                  filename += ".m4a"
               if "mp3" in linky :
                  filename += ".mp3"
               print(filename)
               print(len(filename))
               if len(filename) > 250 :
                  filename = filename[:250]

               # command string generation
               command = "wget -nc -b -O ./downloads/" # yes this does generate about 120 wget instances but that's fine.
               command += filename
               command += " "
               command += linky
            
               call(command, shell=True) # actually call the wget shell comand.
#              break


            
