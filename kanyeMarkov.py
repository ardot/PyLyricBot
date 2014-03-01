#!/usr/bin python
from pymarkovchain import MarkovChain
import requests
import json
import re
import human_curl
import csv
from collections import deque
from xml.etree import ElementTree

###############################################################################

# CONSTANTS
# Edit these values to change the results!!

# The file of lyrics used to train the markov chain.
LYRIC_FILE = 'KanyeLyricFiles/kywt.txt'

# The pronunciation dictionary used to create rhymes. This must contain all of
# the words in the lyrics file
RHYMING_DICTIONARY = 'KanyeRhymingDictionary/ky2.dict'

# Number of lyrics produced
NUMBER_LINES = 4

# The number of words per lyric
MAX_WORDS = 8
MIN_WORDS = 5

###############################################################################

# Vowels used to determine whether words rhyme!
vowels = [
  'AA',
  'AE',
  'AH',
  'AO',
  'AW',
  'AY',
  'EH',
  'ER',
  'EY',
  'IH',
  'IY',
  'OW',
  'OY',
  'UH',
  'UW'
]

# Create an instance of the markov chain. By default, it uses MarkovChain.py's location to
# store and load its database files to. You probably want to give it another location, like so:
mc = MarkovChain("./markov")
# To generate the markov chain's language model, in case it's not present
with open (LYRIC_FILE, "r") as myfile:
  data=myfile.read().replace('\n', '\n')
mc.generateDatabase(data, '\n')

rhyming_dictionary = {}
with open(RHYMING_DICTIONARY, 'rb') as csvfile:
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
for i in range(0,NUMBER_LINES):
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
      if (len(stri_split) < MAX_WORDS and len(stri_split) > MIN_WORDS):
        length = 1
    # Determine the last word, syllables, and vowel
    last_word = stri_split[len(stri_split) - 1].upper()
    last_word_syl = rhyming_dictionary[last_word]
    last_vowel = lastVowel(last_word_syl)

    # Check the current line for rhyming against all others generated
    for (strin, word, vowel) in gens:
      if last_vowel == vowel and last_vowel != None and word != last_word:
        print strin
        print stri
        flag = 1
    # Otherwise add to the list of generated lines
    gens.append((stri, last_word, last_vowel))



