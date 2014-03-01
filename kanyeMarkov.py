#!/usr/bin python
from pymarkovchain import MarkovChain
import requests
import json
import re
import human_curl
import csv
from collections import deque
from xml.etree import ElementTree


#r = requests.get('http://developer.echonest.com/api/v4/song/search?api_key=EYIQEWOOIAQIWILVH&artist=kanye+west&results=100')
#json_response = r.json()
#songs = json_response['response']['songs']
#for song in songs:
#  title = song['title']
#  stripped = re.sub(r'\([^)]*\)', '', title)
#  stripped = re.sub(r'\)', '', stripped)
#  stripped = re.sub(r'\'', '', stripped)
#  split = stripped.split()
#  first = 1
#  conca = ""
#  for word in split:
#    if first == 1:
#      conca = conca + word
#      first = 0
#    else:
#      conca = conca + "+" + word
#  url = "http://api.chartlyrics.com/apiv1.asmx/SearchLyric?artist=kanye%20west&song=" + conca
#  print url
#  r = requests.get(url)
#  tree = ElementTree.fromstring(r.content)
#  print tree.findall('SearchLyricResult')
#  for result in tree.findall('SearchLyricResult'):
#    print result

vowels = ['AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'EH', 'ER', 'EY', 'IH', 'IY', 'OW', 'OY', 'UH', 'UW']

# Create an instance of the markov chain. By default, it uses MarkovChain.py's location to
# store and load its database files to. You probably want to give it another location, like so:
mc = MarkovChain("./markov")
# To generate the markov chain's language model, in case it's not present
with open ("kywt.txt", "r") as myfile:
  data=myfile.read().replace('\n', '\n')
mc.generateDatabase(data, '\n')

rhyming_dictionary = {}
with open('ky2.dict', 'rb') as csvfile:
  spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
  for row in spamreader:
    rhyming_dictionary[row[0]] = row[1:]

# Finds the last vowel in a group of words
def lastVowel(syllables):
  counter = len(syllables) - 1
  while counter > 0:
    if syllables[counter] in vowels:
      return syllables[counter:]
    counter = counter - 1


d = deque()
# generate 4 lines
for i in range(0,4):
  flag = 0
  length = 0
  stri = ""
  stri_split = []
  while length == 0:
    stri = mc.generateString()
    stri_split = stri.split(' ')
    if (len(stri_split) < 8 and len(stri_split) > 5):
      length = 1
  last_word = stri_split[len(stri_split) - 1].upper()
  last_word_syl = rhyming_dictionary[last_word]
  last_vowel = lastVowel(last_word_syl)
  #last_syl = last_word_syl[len(last_word_syl) - 1]

  gens = []
  gens.append((stri, last_word, last_vowel))


  while flag == 0:
    length = 0
    while length == 0:
      stri = mc.generateString()
      stri_split = stri.split(' ')
      if (len(stri_split) < 8 and len(stri_split) > 5):
        length = 1
    last_word = stri_split[len(stri_split) - 1].upper()
    last_word_syl = rhyming_dictionary[last_word]
    last_vowel = lastVowel(last_word_syl)
    #last_syl_2 = last_word_syl[len(last_word_syl) - 1]
    #if last_syl_2 == last_syl:
    for (strin, word, vowel) in gens:
      if last_vowel == vowel and last_vowel != None and word != last_word:
        print strin
        print stri
        flag = 1
    gens.append((stri, last_word, last_vowel))



