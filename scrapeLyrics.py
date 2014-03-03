#!/usr/bin/python
import json
import urllib2

#################################################################################

# CONSTANTS
# Edit these values to change the results!!

ARTIST = 'Cake'

###############################################################################

# Lyric wikia urls for scraping data
lyric_wikia = 'http://lyrics.wikia.com/api.php?artist='
fmt = '&fmt=json'

def sanitize_url(url):
  bads = ['/', '&', '?']
  goods = ['%2F', '%26', '%3F']

  for i in range(0, len(bads)):
    url= url.replace(bads[i], goods[i])
  return url

test = "lkasjdf/alkjasdf/;lkjsdf"
print sanitize_url(test)
# Splice the artist and create the url to get artist data
artist = ARTIST.replace(' ', '+')
artist = sanitize_url(artist)
url = lyric_wikia + artist
data = json.load(urllib2.urlopen(url + fmt))

# Run through each song, and get lyric data
for album in data['albums']:
  for song in album['songs']:

    # Make an API call for the individual song
    song_plus = song.replace(' ', '+')
    song_plus = sanitize_url(song_plus)
    song_url = url + '&song=' + song_plus

    try:
      data = urllib2.urlopen(song_url + fmt)
      data_string = data.read()

      # Parse the response and get the URL for the song lyrics
      index = data_string.index('\'url\':')
      lyrics_url = data_string[(index+7):]
      lyrics_url = lyrics_url[:-4]

      # Get the Lyrics site HTML
      data = urllib2.urlopen(lyrics_url)
      data_string = data.read()

      # print '#######################################################'
      # Parse the HTML to get only the lyrics
      index = data_string.index('\'lyricbox\'')
      lyrics = data_string[(index):]
      index = lyrics.index('</div')
      lyrics = lyrics[(index+6):]
      div = lyrics.index('<p>')

      # Dumb parsing because of how the lyrics site formats their text
      lyrics = lyrics[:-(len(lyrics)-div+6)]
      lyrics = lyrics.replace("<br />", "12;")
      lyrics = lyrics.replace("&#", "")

      # Split into array
      lyrics_split = lyrics.split(";")
      replaced_split = []
      for x in lyrics_split:
        try:
          if x != '' and ((int(x) < 123 and int(x) > 64) or (int(x) == 32 or int(x) == 12)):
            replaced_split.append(x)
        except ValueError, e:
          print "Exception at " + x

      #lyrics_split[:] = [x for x in lyrics_split if x != '' and ((int(x) < 123 and int(x) > 64) or (int(x) == 32 or int(x) == 12))]

      lyrics_string = ''
      for i in replaced_split:
        if int(i) == 12:
          lyrics_string = lyrics_string + "\n"
        else:
          lyrics_string = lyrics_string + str(chr(int(i)))

      #print lyrics_string
      #lyrics_string = ''.join(chr(int(i)) for i in replaced_split)
      lyrics_words = lyrics_string.split(' ')


      filename = 'LyricFiles/' + ARTIST
      wordname = 'LyricFiles/' + ARTIST + '_words'
      f_words = open(wordname, 'a')
      f = open(filename, 'a')
      f.write(lyrics_string)
      for word in lyrics_words:
        f_words.write(word + '\n')

    except urllib2.HTTPError, e:
      print "Exception at URL: " + song_url
