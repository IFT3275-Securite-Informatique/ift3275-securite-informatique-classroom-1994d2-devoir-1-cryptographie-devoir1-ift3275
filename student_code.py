import requests
import numpy as np
import math
from itertools import tee, islice
import re
from collections import Counter
import csv

def decrypt(C):

  #url = "https://www.gutenberg.org/ebooks/13846.txt.utf-8"  # Example URL (replace with your desired URL)
  #corpus = load_text_from_web(url)
  #url = "https://www.gutenberg.org/ebooks/4650.txt.utf-8"  # Example URL (replace with your desired URL)
  #corpus = corpus + load_text_from_web(url)

  # load precalculated data
  print("Loading CSV")
  stats_ngram_1 = loadStatsNgram('freq_ngram_1.csv')
  stats_ngram_2 = loadStatsNgram('freq_ngram_2.csv')
  stats_ngram_3 = loadStatsNgram('freq_ngram_3.csv')
  stats_ngram_4 = loadStatsNgram('freq_ngram_4.csv')
  stats_ngram_5 = loadStatsNgram('freq_ngram_5.csv')
  stats_ngram_6 = loadStatsNgram('freq_ngram_6.csv')
  print("Parsing Cypher")
  C_cutBlock = cutCypherText(C)
  #c_analysis = ngrams_count_plus(C_cutBlock, 2,5)

  print("Counting ngram_2")
  C_mono_Count = ngrams_count(C_cutBlock, 2,5, 50)
  C_mono_Freq = []

  print("Analyzing ngram-2 Frequency Data")
  for x in C_mono_Count:
     C_mono_Freq.append(checkFrequency(C_cutBlock, x[0], x[1], 2, False))

  dictionary_1 = {}
  print("Building ngram-2 Dictionary")
  var = buildNgramDictionary(2, [stats_ngram_4], C_mono_Freq, 20, True)


  dictionary_2 = var[0]

  for x in var[1]:
   dictionary_1.update(x)

  print(dictionary_2)
  print(dictionary_1)
  '''
  print("Comparing ngram-2 ....")
  while (loop):
    loop = False
    reboot = False
    for x in xs:

      for y in ys:
          errMargin_freq = y[2] * 0.05
          errMargin_med = y[3] * 0.1
          if ((abs(x[2] - y[2])) < errMargin_freq and abs(x[3] - y[3])<errMargin_med and x[4] >= y[4]):
            print("we might have a match with ["+str(int(x[0][0]))+"] and ["+str(y[0])+"]!!!!")
            addToDict(dictionary, [int(x[0][0]), y[0]])
            xs.remove(x)
            ys.remove(y)
            loop = True
            reboot = True
          if (reboot): break
      if (reboot): 
        print("Rebooting....")
        break
    
  print("Comparing ngram-1 ....")
  ys = stats_ngram_1.copy()
  loop = True
  while (loop):
    loop = False
    reboot = False
    for x in xs:
      for y in ys:
          errMargin_freq = y[2] * 0.05
          errMargin_med = y[3] * 0.1
          if ((abs(x[2] - y[2])) < errMargin_freq and abs(x[3] - y[3])<errMargin_med and x[4] >= y[4]):
            print("we might have a match with ["+str(int(x[0][0]))+"] and ["+str(y[0])+"]!!!!")
            addToDict(dictionary, [int(x[0][0]), y[0]])
            xs.remove(x)
            ys.remove(y)
            loop = True
            reboot = True
          if (reboot): break
      if (reboot): 
        print("Rebooting....")
        break
  '''
  print("Deciphering ....")     
  #mdec = decipher_with_dict(C_cutBlock, dictionary_3,3)
  mdec = decipher_with_dict(C_cutBlock, dictionary_1,1)

  #print(mdec)
  mfinal = []
  for m in mdec:
    if isinstance(m, int): 
      mfinal.append("?")
    else: 
      mfinal.append(m)
      #print("replaced word: "+m)

  #print(mfinal)

  M="".join(mfinal)
  #print(M)
  #entrez votre code ici.
  #Vous pouvez créer des fonctions auxiliaires et adapter le code à votre façon mais decrypt dois renvoyer le message décrypté

  '''

    # Single check: ' ', 'e' and 's'
  # highest frequency minval 1 : ' ', 'e'. high frequency is either ' ' and 'e', and 
  monofreq = ngrams_count(C_cutBlock, 1,0,50)

  for x in range(50):
    f = checkFrequency(C_cutBlock, monofreq[x][0],1, False)
    if (x < 3 and f[2] == 0 and f[1] > 5.0):
      addToDict(dictionary, [monofreq[x][0], 's'])
      print("S replaced!")
    elif (x < 3 and f[1] > 10.0):
      print("Alert, we have a possible space or e")

      
  checkRepeat_2 = checkRepeat(C_cutBlock, 2,3)
  checkRepeat_2 += checkRepeat(C_cutBlock, 3,3)
  checkRepeat_2 += checkRepeat(C_cutBlock, 4,3)
  checkRepeat_2 += checkRepeat(C_cutBlock, 5,3)
  checkRepeat_2 += checkRepeat(C_cutBlock, 6,3)
  checkRepeat_2 += checkRepeat(C_cutBlock, 7,3)

  print(checkRepeat_2)
  checkRepeat_dict = {}
  for x in checkRepeat_2:

    if x[0] not in checkRepeat_dict:
       checkRepeat_dict[x[0]] = 3
    else:
       checkRepeat_dict[x[0]] += 3

    if x[1] not in checkRepeat_dict:
       checkRepeat_dict[x[1]] = 1
    else:
       checkRepeat_dict[x[1]] += 1

  # Reference https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
  checkRepeat_dict_sort = dict(sorted(checkRepeat_dict.items(), key=lambda item:item[1]))

  print(checkRepeat_dict_sort)
'''
  return M


def buildNgramDictionary(cypherWordLength, stats, cypherFreqArray, statsDelimiter = 50, equivalentCut = False):
  ys = []
  for x in stats:
    length = min(len(x), statsDelimiter)
    ys += x[0:length]
  print(ys)
  dictionary = {}
  dictionary_mono = []
  
  xs = cypherFreqArray.copy()
  loop = True
  while (loop):
    loop = False
    reboot = False
    for x in xs:
      for y in ys:
          errMargin_freq = y[2] * 0.02
          errMargin_med = y[3] * 0.1

          if y[0] in dictionary.values(): continue

          if ((abs(float(x[2]) - float(y[2]))) < errMargin_freq) and (abs(x[3] - y[3])<errMargin_med) and (x[4] - y[4] <= 1):
            word = []
            for i in range(cypherWordLength):
              word.append(int(x[0][i]))
            print(word)
            print("we might have a match with ["+str(word)+"] and ["+str(y[0])+"] check Equivalent cut ["+str(equivalentCut and len(str(y[0]))%2 == 0)+"]!!!!")
            addToDict(dictionary, word, y[0])

            if (equivalentCut and len(str(y[0]))%2 == 0):
              dict_temp = {}
              for i in range(cypherWordLength):
                word_cut = str(int(x[0][i]))
                cy_cut = str(str(y[0])[i*2:i*2+2])
                print("equivalent cut add ["+str(word_cut)+"] and ["+str(cy_cut)+"]!!!!")
                addToDict(dict_temp, word_cut, cy_cut)

              conflict = False
              conflictIndex = -1
              for i in range(len(dictionary_mono)):
                  for key in dict_temp:
                      if key in dictionary_mono[i]:
                        conflict = True
                  if conflict:
                      conflictIndex = i
                      break
              if (conflict and conflictIndex > -1):
                print("Conflict detected, remove keys "+str(dictionary_mono[i].keys))
                dictionary_mono.remove(dictionary_mono[i])

              else:
                dictionary_mono.append(dict_temp)
                print("No conflict, add keys "+str(dict_temp.keys))

            loop = True
            reboot = True
          if (reboot): break
      if (reboot): 
        print("Rebooting....")
        break

  print(dictionary)
  print(dictionary_mono)
  return [dictionary, dictionary_mono]


def loadStatsNgram(filename):
  array = []

  with open(filename, encoding='utf8') as csvfile:
    data = list(csv.reader(csvfile))

    for index in range(len(data)):
        if (index == 0): continue
        if (len(data[index]) < 1) :continue
        temp = [data[index][0],int(float(data[index][1])),float(data[index][2]),float(data[index][3]),int(float(data[index][4]))]
        #print(temp)
        array.append(temp)
  return array


def load_text_from_web(url):
  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.text
  except requests.exceptions.RequestException as e:
    print(f"An error occurred while loading the text: {e}")
    return None
  
def cut_string_into_pairs(text):
    txt = str(text)
    pairs = []
    for i in range(0, len(txt) - 1, 2):
        pairs.append(txt[i:i+2])
    return pairs
    
# This function takes an array of elements and analyse the frequency of each single element
# sorted in descending order
def frequencyAnalysis(array):
    # https://stackoverflow.com/questions/15637336/numpy-unique-with-order-preserved
    arr = np.array(array)
    freq = np.unique(arr, return_counts=True)
    #print(freq[0].size)
    sum = np.sum(freq[1])
    
    sort = np.flip(np.argsort(freq[1]))

    arrSorted = []
    for i in range(sort.size):
      index = sort[i]
      arrSorted.append([freq[0][index], freq[1][index]/sum])

    return np.array(arrSorted)

def mergeFreq(monoArr, biArr, maxKeys = 256):

    if maxKeys < monoArr.shape[0] : 
      maxKeys = monoArr.shape[0]
    bi_keysCount = maxKeys - monoArr.shape[0]
    bi_cut = biArr[0:bi_keysCount, :]
    #print(bi_cut.shape)

    arr = np.concatenate((monoArr, bi_cut))
    print(arr.shape)
    print(arr[0])

    weights = np.array(arr[:,1], dtype=float)
    print(weights[0])
    sort = np.flip(weights.argsort())
    print(sort[0])

    arr = arr[sort]
    print(arr[0:50])
    return arr


# https://stackoverflow.com/questions/57049685/convert-string-of-0-and-1-to-its-binary-equivalent-python
# This function receive a encrypted binary message and cut it into an array of utf8 chunks
def cutCypherText(string):
    arr = []
    cypherText = int(string, base=2)
    charCount = math.ceil(cypherText.bit_length() / 8)
    print("charcount "+str(charCount))
    c = cypherText.to_bytes(charCount, byteorder='big')

    for x in range(charCount):
      arr.append(c[x])

    return np.array(arr, dtype=int)

# This function takes in a list of elements (raw text) and a specified element 
# (target string, could target multiple strings if correct symbol size is entered)
# and it will return the frequency of that single element 
def checkFrequency(text, sy, count = 0, symbol_size = 1, printConsole = False):
    occurence = []
    counter = 0

    first = True

    symbol = sy

    if (symbol_size > 1):
       symbol = np.array(sy)
    else:
       symbol = sy

    for x in range(len(text) - symbol_size + 1):

        if (symbol_size > 1):
          targ = np.array(text[x:x+symbol_size])
        else:
          targ = text[x:x+symbol_size]
        
        #print(targ)
        if ((symbol_size < 2 and symbol == targ) or (symbol_size > 1 and (symbol == targ).all())) and not first:
            occurence.append(counter)
            counter = 0
        else:
            counter += 1

        first = False
    
    if (printConsole and len(occurence) > 0):
        print("symbol ["+str(sy)+"] frequency ["+"{:.3f}".format(len(occurence) / len(text) * 100)+"%] mean interval ["+str(np.mean(occurence))+"] minVal ["+str(np.min(occurence))+"] maxVal ["+str(np.max(occurence))+"] median ["+str(np.median(occurence))+"]")
    elif (printConsole):
        print("symbol ["+str(sy)+"] no occurence")
    
    if (len(occurence) < 1): 
       return [sy, count,0,0,0]
    else: return [sy, count, len(occurence) / len(text) * 100, float(np.median(occurence)), float(np.min(occurence))]

# this function checks all elements in text and output all entries which has been repeated in specified interval
def checkRepeat(text, interval = 0, ignoreAfter = -1, prindConsole = False):
    arr = []
    for x in range(len(text) - interval - 1):
        if text[x] == text[x+interval+1]:
            arr.append(text[x])

    nparr = np.unique(arr, return_counts=True)

    sort = np.flip(nparr[1].argsort())

    if (prindConsole):
      string = "checkRepeat interval "+str(interval)+": "
      for x in sort:
        string += "("+str(nparr[0][x])+" "+str(nparr[1][x])+") "
      print(string)

    sorted = []
    index = 0
    for x in sort:
      sorted.append([nparr[0][x], nparr[1][x]])
      index += 1

    if (ignoreAfter > 0): return sorted[0:min(index, ignoreAfter)]
    else: return sorted


# require a dict object.
# add a decrypt entry to dictionary
def addToDict(dict, cypher, word):
    cypher_concat = ""
    for x in cypher:
       cypher_concat += str(x)
    dict[cypher_concat] = word

# use the dictionary to replace all matching entries in cypherArray
def decipher_with_dict(cypherArray, dict, cypherLength):
    string = []

    for x in range(len(cypherArray)-cypherLength+1):
      word = ""
      for i in range(cypherLength):
        word += str(int(cypherArray[x+i]))

      if (word in dict): 
        string.append(dict[word])
        x += cypherLength

      else : string.append(int(cypherArray[x]))

    return string

# This checks the maximum consecutive occurence of a given string
def checkConsecutiveStringFormat(text, acceptString, denyString = ""):
    accept_len = len(acceptString)
    deny_len = min(len(denyString),1)
    results = []
    results_maxlength = []
    i = 0
    j = 0
    while i < len(text):
        if i + accept_len < len(text) and text[i:i+accept_len] == acceptString:
            j += 1
            results.append("1")
            results_maxlength.append(j)
            i += accept_len
        elif i + deny_len < len(text) and len(denyString) > 0 and text[i:i+deny_len] == denyString:
            results.append("0")
            i += deny_len
            j = 0
            results_maxlength.append(j)
        elif i + deny_len < len(text) and len(denyString) == 0 and text[i:i+deny_len] != acceptString:
            results.append("0")
            i += deny_len
            j = 0
            results_maxlength.append(j)
        else:
            i += 1

    concat = ''.join(results)
    print(results_maxlength)
    if (len(results_maxlength) > 0): print("max consecutive appearance is "+str(np.max(results_maxlength)))
    return concat.count("11")



# Reference : https://stackoverflow.com/questions/12488722/counting-bigrams-pair-of-two-words-in-a-file-using-python

def ngrams(lst, n):
  tlst = lst
  while True:
    a, b = tee(tlst)
    l = tuple(islice(a, n))
    if len(l) == n:
      yield l
      next(b)
      tlst = b
    else:
      break

def ngrams_count(lst, n, ignoreFreqSmallerThan = 0, countFirst = 100):
  aaa = Counter(ngrams(lst, n))

  mostCommon = aaa.most_common()
  index = 0
  loop = True

  newList = []

  while (loop):
     if mostCommon[index][1] < ignoreFreqSmallerThan:
        loop = False
     else: 
        newList.append(mostCommon[index])
        index += 1

     if (index+1 >= len(mostCommon)): loop = False
     if (index + 1 >= countFirst): loop = False

  return newList

def ngrams_count_plus(lst, n, nplus, ignoreFreqSmallerThan = 0, countFirst = 100):
  list = Counter(ngrams(lst, n))
  for i in range( n+1, nplus+1):
    list += Counter(ngrams(lst, i))

  mostCommon = list.most_common()

  newList = []

  index = 0
  loop = True
  while (loop):
     if mostCommon[index][1] < ignoreFreqSmallerThan:
        loop = False
     else: 
        newList.append(mostCommon[index])
        index += 1

     if (index+1 >= len(mostCommon)): loop = False
     if (index + 1 >= countFirst): loop = False

  return newList