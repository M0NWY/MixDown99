# Script of getting mixes off of Mixcloud

import time
import subprocess
import requests
import re
from subprocess import call

	
import psutil 
def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

# genres are literal url paths after /discover you can add or remove them to your liking
# dump file full of links only.

for genre in ["beats", "deep-house", "drum-bass", "dubstep", "edm", "electronica", "house", "tech-house", "techno", "trance", "trap"] :
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
               print("URL:")
               print(url)

               # using a 3rd party download site to generate the direct link as i've not figured that out !

               sess = requests.Session()
               r = sess.get("http://99downloader.com/mixcloud-downloader")
               token = r.cookies['csrftoken']
               print("Token:")
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
               linky = linky[8:]  # string cleanup
               linky = linky[:-2]
               linky += "\"" 
               print("linky:")
               print(linky)

               # filename generation

               filename = url[25:]
               filename = filename[:-1]
               filename = filename.replace("/","-")
               noext = filename

               if "m4a" in linky :
                  filename += ".m4a"
               if "mp3" in linky :
                  filename += ".mp3"
               print(filename)
               print(len(filename))
               if len(filename) > 250 :
                  filename = filename[:250]

               # command string generation
               command = "wget -nc -b -O ./downloads/" 
               command += filename
               command += " "
               command += linky
#               command += " && ffmpeg -i ./downloads/"
#               command += filename
#               command += " -acodec libmp3lame ./downloads/"
#               command += noext
#               command += ".mp3"
#               command += " && rm ./downloads/"
#               command += filename
               
               print("command :")
               print(command)
          
               call(command, shell=True) # actually call the wget shell comand.

while checkIfProcessRunning('wget'):
   print(" Yawn... waiting for wget(s) to finish " )
   time.sleep(300) # check every 5 mins

print(" Woooot.. converting to mp3 ")
call("./convert.sh", shell=True)

print("Phew... done")

# for i in *.m4a ; ffmpeg -i "$i" -acodec libmp3lame "$(basename "${i/.m4a}")".mp3 ; done
