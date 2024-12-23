
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

  '''
  # load precalculated data (these data are no longer useful)
  # I originally intend to calculate all n-gram (and words) possibilities, write in csv, then read on need.
  # but... that approach did not bear fruit
  print("Loading CSV")
  stats_ngram_1 = loadStatsNgram('freq_ngram_1.csv')
  stats_ngram_2 = loadStatsNgram('freq_ngram_2.csv')
  stats_ngram_3 = loadStatsNgram('freq_ngram_3.csv')
  stats_ngram_4 = loadStatsNgram('freq_ngram_4.csv')
  stats_ngram_5 = loadStatsNgram('freq_ngram_5.csv')
  stats_ngram_6 = loadStatsNgram('freq_ngram_6.csv')
  '''

  # Cut the raw data into UTF-8 datablock
  C_cutBlock = cutCypherText(C)

  wordCount = []
  wordCount.append(wordCountTest(C_cutBlock, 1, 0))
  wordCount.append(wordCountTest(C_cutBlock, 2, 0))
  wordCount.append(wordCountTest(C_cutBlock, 3, 0))
  wordCount.append(wordCountTest(C_cutBlock, 4, 0))
  wordCount.append(wordCountTest(C_cutBlock, 5, 0))
  wordCount.append(wordCountTest(C_cutBlock, 6, 0))

  # dictionary that store all decrypt symbols
  dictionary_1 = {}

  repeatCount = []
  # find repeating symbols in single alphabet descending order. very recursive. very expensive
  for x in wordCount[0]:
    maxRepeat = 1
    repeat = True
    #print(x[0][0])
    while repeat:
      repeat = False
      matchStr = []
      for i in range(maxRepeat+1):
         matchStr.append(x[0][0])
      #print(matchStr[0])
      for i in wordCount[maxRepeat]:
         if (i[0] == matchStr).all():
            maxRepeat += 1
            repeat = True
            break
      #if (repeat):   print("match in "+str(maxRepeat-1))
      if (maxRepeat > 5): repeat = False
    if (maxRepeat > 3) : 
        maxlen = checkConsecutiveChar(C_cutBlock, x[0][0],1)
        total = countWord(C_cutBlock, x[0][0],1)
        print(str(x[0][0]) + " max repeat "+str(maxRepeat) + " maximumConsecutive "+ str(maxlen) + " total "+str(total))

        if maxlen == 16:  # derived from the fact the corpus has a max repeat of 16 ' '
          print("we might have _")
          addToDict(dictionary_1, str(x[0][0]), ' ')
        elif maxlen == 38:  # derived from the fact the corpus has a max repeat of 38 ' '
          print("we might have *")
          addToDict(dictionary_1, str(x[0][0]), '*')
        else:
          repeatCount.append([str(x[0][0]), total])
    
  #print(repeatCount)

  # Find \r\n in all repeating
  eol = -1
  if (len(repeatCount)>0):
    sortedRepeat = sorted(repeatCount, key=lambda x: x[1], reverse=True)
    #print(sortedRepeat)
    index = 0
    for x in sortedRepeat:
        if str(x[0]) in dictionary_1: continue
        if index == 0 : 
            addToDict(dictionary_1, str(x[0]), '\r\n')
            eol = x[0]
            print("EOL rn FOUND : "+ str(eol))
            break
        # this one is correct guess
        #elif index == 1 : addToDict(dictionary_1, str(x[0]), '\r')
        #elif index == 2 : addToDict(dictionary_1, str(x[0]), '*')
        #else : print("repeatcount exceeding 3 error please check ")

    

  eol_period = -1
  if (eol != -1):

     # find all eol stats
    eol_count = countEOL(C_cutBlock, eol,1,  -1)
    #print(eol_count)
    eol_sorted = sortEOL(eol_count)
    #print(eol_sorted)

    index = 0
    for x in eol_sorted:
      if str(x[0]) in dictionary_1: continue
      if index == 0: 
        eol_period = x[0]
        addToDict(dictionary_1, str(eol_period), '.')
        print("pre-EOL period FOUND : "+ str(eol_period))
      else: break
      index += 1

  # find the thing after EOL
  symbol_qu = -1
  if (eol != -1):
     # find all eol stats
    eol_count = countEOL(C_cutBlock, eol,1, 1)
    eol_sorted = sortEOL(eol_count)
    #print(eol_sorted)
    index = 0
    for x in eol_sorted:
      if str(x[0]) in dictionary_1: continue
      if index == 0: 
        symbol_qu = x[0]
        #addToDict(dictionary_1, str(symbol_qu), 'qu')
        
      else: break
      index += 1
  '''
  the qu finder is not reliable as this finds the -qu on new line.
  but in the corpus provided, this logic can be mistaken with - C
  so here's a divider.

  if we can find quelqu, then we say we found the qu
  if we can't find quelqu, then we assume we have made the mistake, and change it to - C

  ...but really, if we can't find qu, then its a failure.
  '''

  symbol_es = -1

  # find the 'el' in quelque
  if (symbol_qu != -1): 
    returnval = find_quelque(dictionary=dictionary_1, corpus=C_cutBlock, quSymbol=symbol_qu)
    symbol_el = returnval[0]
    symbol__e = returnval[1]
    symbol_es = returnval[2]
    if (symbol_el != -1):
      print("post-EOL qu FOUND : "+ str(symbol_qu))
      addToDict(dictionary_1, str(symbol_qu), 'qu')
      print("quelqu FOUND : "+ str(symbol_el))
      addToDict(dictionary_1, str(symbol_el), 'el')
      print("que_ FOUND : "+ str(symbol__e))
      addToDict(dictionary_1, str(symbol__e), 'e ')
      print("ques FOUND : "+ str(symbol_es))
      addToDict(dictionary_1, str(symbol_es), 'es')
    else:
      # if we cant find quelque
      print("new line '_C' FOUND : "+ str(symbol_qu))
      addToDict(dictionary_1, str(symbol_qu), ' C')
      print("ITS HIGHLY LIKELY THAT THE ALGORITHM FAILED TO FIND THE RN OR QU WEAKNESS, AS SUCH THIS RESULT IS BETTER IGNORED")

  if (symbol_es != -1):
     returnval = find_es_les(dictionary=dictionary_1, corpus=C_cutBlock, esSymbol=symbol_es)
     symbol_les = returnval[0]
     symbol_des = returnval[1]
     if (symbol_les != -1):
      print("esles FOUND : "+ str(symbol_les))
      addToDict(dictionary_1, str(symbol_les), ' l')
      print("esdes FOUND : "+ str(symbol_des))
      addToDict(dictionary_1, str(symbol_des), ' d')

  if (symbol_qu != -1 and symbol_es != -1):
     returnval = find_qui_est(dictionary=dictionary_1, corpus=C_cutBlock, quSymbol=symbol_qu, esSymbol=symbol_es)
     symbol_qui = returnval[0]
     symbol_est = returnval[1]
     symbol_estr = returnval[2]
     if symbol_qui != -1:
        print("qui_est FOUND : "+ str(symbol_qui))
        addToDict(dictionary_1, str(symbol_qui), 'i ')
        if symbol_est != -1:
          print("est FOUND : "+ str(symbol_est))
          addToDict(dictionary_1, str(symbol_est), 't ')
        if symbol_estr != -1:
          print("estr FOUND : "+ str(symbol_estr))
          addToDict(dictionary_1, str(symbol_estr), 't\r') 





  #quit()
  print("PRINTING DICTIONARY ....\n\n\n")     
  print( dictionary_1)

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
    
  #quit()
  M="".join(mfinal)

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

'''
This function cut the corpus into wordlength chunk, and return the descending order of their count
'''
def wordCountTest(corpus, wordLength, ignoreBelow = 0, ignoreAfter = -1):
    arr = []
    for x in range(len(corpus) - wordLength):
      arr.append(corpus[x:x+wordLength])

    strarr = []
    for x in arr:
       s = ""
       for y in x:
          s += str(y)
       strarr.append(s)

    #print(arr)
    #print(strarr)

    nparr = np.unique(strarr, return_counts=True, return_index=True)
    sort = np.flip(nparr[2].argsort())
    sorted = []

    #print(nparr)
    #print(sort)

    index = 0
    for x in sort:
      if (nparr[2][x] < ignoreBelow): break
      if (ignoreAfter > -1 and index >= ignoreAfter): break

      arrayIndex = nparr[1][x]
      arrayValue = nparr[2][x]
      #if hasattr(arr[0], '__len__') and (not isinstance(arr[0], str)) and len(arr[0]) > 0:
      #   arrayIndex = arrayIndex // len(arr[0])
      #   arrayValue = arrayValue // len(arr[0])
      
      #print(arrayIndex)
      
      #if isArrayStorage:
      sorted.append([arr[arrayIndex],arrayValue])
      index += 1
      #else:
      #  sorted.append([[nparr[0][x]],nparr[1][x]])
      #  if (prindConsole): string += "("+str( nparr[0][x])+" "+str(nparr[1][x])+") "

      #else:
      #   string += "("+str( nparr[0][x])+" "+str(nparr[1][x])+") "

    return sorted

'''
This function cut the corpus into wordlength chunk, and return the descending order of their count
'''
def countWord(corpus, word, wordLength):
    count = 0
    for x in range(len(corpus) - wordLength):
      if corpus[x:x+wordLength] == word:
         count += 1

    return count

# this function checks all elements in text and output all entries which has been repeated in specified interval
def checkRepeat(text, symbolSize = 1, interval = 0, ignoreAfter = -1, prindConsole = False, ignoreBelow = 10, isString = True):
    
    arr = []
    for x in range(len(text) - interval - symbolSize):
        if text[x] == text[x+interval+symbolSize]:
            if (symbolSize == 1):
               arr.append(text[x:x+symbolSize])
            else:
              fail = False
              for i in range(1,symbolSize):
                  if x+i+interval+symbolSize < len(text) and text[x+i] != text[x+i+interval+symbolSize]:
                     fail = True
                     break
              if not fail: arr.append(text[x:x+symbolSize])

    nparr = np.unique(arr, return_counts=True, return_index=True)
    sort = np.flip(nparr[2].argsort())

    sorted = []
    arrayLength = 1
    if len(arr) >= 1 and hasattr(arr[0], '__len__') and (not isinstance(arr[0], str)):
       arrayLength = len(arr[0])

    string = "checkRepeat interval "+str(interval)+": arrayLength ["+str(arrayLength)+"]"
    index = 0
    for x in sort:
      if (nparr[2][x] < ignoreBelow): break
      if (ignoreAfter > -1 and index >= ignoreAfter): break

      arrayIndex = nparr[1][x]
      if hasattr(arr[0], '__len__') and (not isinstance(arr[0], str)) and len(arr[0]) > 0:
         arrayIndex = arrayIndex // len(arr[0])
      
      print(str( arr[arrayIndex]))

      sorted.append([arr[arrayIndex],nparr[2][x]])
      index += 1
      if (prindConsole): string += "("+str( arr[arrayIndex])+" "+str(nparr[2][x])+") "
           
    if (prindConsole):
      print(string)

    return sorted

def find_es_les(dictionary, corpus, esSymbol):
  start = -1
  end = -1

  arr = []
  for x in range(len(corpus) - 1):
    symbol = corpus[x]
    if symbol == esSymbol:
      #print("qu match")
      if (end == -1): 
        end = x
      else: 
        start = end
        end = x
        if end - start == 2:

          symbol_es = corpus[end - 1]

          if symbol_es not in dictionary: 
            arr.append(str(symbol_es))


  sorted = []
  nparr = np.unique(arr, return_counts=True, return_index=True)
  sort = np.flip(nparr[2].argsort())
  for x in sort:
    arrayIndex = nparr[1][x]
    sorted.append([arr[arrayIndex],nparr[2][x]])
  #print(sorted)


  # les > des
  finalCandidate = [-1,-1]

  if (len(sorted) > 0):
    finalCandidate[0] = sorted[0][0]
    if (len(sorted) > 1):
      finalCandidate[1] = sorted[1][0]
  else:
     finalCandidate[0] = -1
     finalCandidate[1] = -1
  
  return finalCandidate

def find_qui_est(dictionary, corpus, quSymbol, esSymbol):
  start = -1
  end = -1

  arr = []
  arr2 = []
  for x in range(len(corpus) - 1):
    symbol = corpus[x]
    if symbol == quSymbol:
      start = x
    elif symbol == esSymbol:
      #print("qu match")
      end = x
      if end > start and end - start == 2:
          symbol_qui = corpus[end - 1]
          symbol_est = corpus[end + 1]
          if symbol_qui not in dictionary: 
            arr.append(str(symbol_qui))
            arr2.append(str(symbol_est))


  sorted = []
  nparr = np.unique(arr, return_counts=True, return_index=True)
  sort = np.flip(nparr[2].argsort())
  for x in sort:
    arrayIndex = nparr[1][x]
    sorted.append([arr[arrayIndex],nparr[2][x]])
  #print(sorted)

  sorted2 = []
  nparr2 = np.unique(arr2, return_counts=True, return_index=True)
  sort2 = np.flip(nparr2[2].argsort())
  for x in sort2:
    arrayIndex = nparr2[1][x]
    sorted2.append([arr2[arrayIndex],nparr2[2][x]])

  # qui est, est_, est\r
  finalCandidate = [-1,-1,-1]

  if (len(sorted) > 0):
    finalCandidate[0] = sorted[0][0]
    if (len(sorted2) > 0):
       finalCandidate[1] = sorted2[0][0]
       if (len(sorted2) > 1):
          finalCandidate[2] = sorted2[1][0]

  return finalCandidate

def find_quelque(dictionary, corpus, quSymbol):
  start = -1
  end = -1
  el_arr = []
  e__arr = []
  for x in range(len(corpus) - 1):
    symbol = corpus[x]
    if symbol == quSymbol:
      #print("qu match")
      if (end == -1): 
        end = x
      else: 
        start = end
        end = x
        if end - start == 2:
          symbol_pre = corpus[start - 1]
          symbol_el = corpus[end - 1]
          symbol_que = corpus[end + 1]
          if symbol_el != symbol_que and symbol_el != symbol_pre and symbol_el not in dictionary: 
            el_arr.append(str(symbol_el))
          e__arr.append(symbol_que)

  el_sorted = []
  el_nparr = np.unique(el_arr, return_counts=True, return_index=True)
  el_sort = np.flip(el_nparr[2].argsort())
  for x in el_sort:
    arrayIndex = el_nparr[1][x]
    el_sorted.append([el_arr[arrayIndex],el_nparr[2][x]])

  print(el_sorted)

  e__sorted = []
  e__nparr = np.unique(e__arr, return_counts=True, return_index=True)
  e__sort = np.flip(e__nparr[2].argsort())
  for x in e__sort:
    arrayIndex = e__nparr[1][x]
    e__sorted.append([e__arr[arrayIndex],e__nparr[2][x]])
  print(e__sorted)
  
  finalCandidate = [-1,-1,-1]


  if (len(el_sorted) > 0):
    finalCandidate[0] = el_sorted[0][0]
  else:
     finalCandidate[0] = -1

  if (len(e__sorted) > 0):
    finalCandidate[1] = e__sorted[0][0]
    if (len(e__sorted) > 1):
      finalCandidate[2] = e__sorted[1][0]
  else:
     finalCandidate[1] = -1
     finalCandidate[2] = -1
  
  return finalCandidate

def countEOL(corpus, eolSymbol = '\r\n', eolSymbolLen = 2, countSymbol = -1):
# count symbol < 0 count before. count symbol > 0 count after
    word = eolSymbol
    array = []
    wordlen = eolSymbolLen

    start = -countSymbol
    if start < 0 : start = 0

    for x in range(start, len(corpus) - wordlen):
      string = corpus[x:x+wordlen][0]
      if int(string) == int(word):
         
         #targetWord = corpus[x-countSymbol:x][0]
        # array.append(corpus[x-countSymbol:x][0])
        if countSymbol < 0: array.append(corpus[x+countSymbol:x][0])
        else: array.append(corpus[x+wordlen:x+wordlen+countSymbol][0])
    return array

def sortEOL(arr):

  sorted = []
  nparr = np.unique(arr, return_counts=True, return_index=True)
  sort = np.flip(nparr[2].argsort())
  for x in sort:
    arrayIndex = nparr[1][x]
    sorted.append([arr[arrayIndex],nparr[2][x]])
  return sorted[1:] 
  # 1: exclude the other \r\n

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


def checkConsecutiveChar(text, acceptChar, charLen, printConsole = False):
  accept_len = charLen
  results = []
  results_maxlength = []
  i = 0
  j = 0
  while i < len(text)-accept_len:
      if text[i:i+accept_len] == acceptChar:
          j += 1
          results.append("1")
          results_maxlength.append(j)
          i += accept_len
      else:
          results.append("0")
          i += 1
          j = 0
          results_maxlength.append(j)

  #concat = ''.join(results)
  #print(results_maxlength)
  maxlen = 0
  if (len(results_maxlength) > 0): 
    maxlen = np.max(results_maxlength)
    if printConsole: print("max consecutive appearance for ["+str(acceptChar)+"] is "+str(maxlen))
  return maxlen


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
=======
import bisect
import os
import random as rnd
import re
from difflib import get_close_matches

import requests
from collections import Counter, defaultdict
import time

global allow_rand
allow_rand = True

global possible_chars_in_word
possible_chars_in_word = ['b', 'j', 'J', 'Â', 'É', 'ê', 't', 'Y', 'N', 'B', 'V', 'Ê',
                          '’', 'i', 's', 'C', 'â', 'ï', 'W', 'y', 'p', 'D', 'A', 'n', 'q',
                          'e', 'T', 'È', 'U', 'v', 'l', 'P', 'X', 'Z', 'À', 'ç', 'u', 'î', 'L', 'k', 'E', 'R',
                          'é', 'O', 'Î', 'a', 'F', 'H', 'c', "'", 'è', 'I', 'S', 'x', 'à', 'g', 'Q', 'w', 'û', 'G', 'm',
                          'K', 'z', 'o', 'ù', 'r',
                          'M', 'Ç', 'h', 'f', 'ë', 'd', 'ô', 'es',
                          'en', 'qu', 're', 'de', 'le', 'nt', 'on', 'ou', 'ue',
                          'an', 'te', 'ai', 'se', 'it', 'me', 'is', 'oi', 'er', 'ce', 'ne', 'et', 'in', 'ns',
                          'ur', 'eu', 'co', 'tr', 'la', 'ar', 'ie', 'ui', 'us', 'ut', 'il', 'pa', 'au',
                          'el', 'ti', 'st', 'un', 'em', 'ra', 'e,', 'so', 'or', 'll', 'nd', 'si', 'ir',
                          'ss', 'po', 'ro', 'ri', 'pr', 's,', 'ma', 'di', 'vo', 'pe', 'to', 'ch',
                          've', 'nc', 'om', 'je', 'no', 'rt', 'lu', "'e", 'mo', 'ta', 'as', 'at', 'io', 'sa',
                          "u'", 'av', 'os', "l'", "'a", 'rs', 'pl', 'ho', 'té', 'ét', 'fa', 'da', 'li',
                          'su', 'ée', 'ré', 'dé', 'ec', 'nn', 'mm', "'i", 'ca', 'uv', 'id', 'ni', 'bl']

global fr_dict
fr_dict = set()


def capture_groups(start_str, n_bytes_min, n_bytes_max, end_str, encoded_bytes, key, decrypt_when_possible=False,
                   bytes_with_starting_spaces=[False] * 256, bytes_with_ending_spaces=[False] * 256,
                   include_start_and_end=False, debug=False):
    '''
  Arguments
      - start_str: Une regex qui délimite le début des mots à capturer (ex.: '[^ ]? ' pour indiquer que la chaîne commence par n'importe quel caractère suivi d'un espace)
          start_str doit toujours comporter un espace
      - n_bytes_min: longueur minimale de la chaîne du milieu en bytes
      - n_bytes_max: longueur maximale de la chaîne du milieu en bytes
      - end_str: Une regex qui délimite la fin des mots à capturer (ex.: ' [^ ]?' pour indiquer que la chaîne se termine par un espace suivi de n'importe quel caractère)
          end_str doit toujours comporter un espace
      - decrypt_when_possible: Si vrai, les bytes déjà substitués sont transformés en leur représentation en string dans les groupes. Faux par défaut
      - bytes_with_starting_spaces: Optionnel. Liste de Booléens qui indique si le byte i commence par un espace.
          Si le byte i commence par un espace, on segmente le groupe en conséquence
          Note: ' ' ne doit pas être True
      - bytes_with_ending_spaces: Optionnel. Liste de Booléens qui indique si le byte i se termine par un espace.
          Si le byte i se termine par un espace, on segmente le groupe en conséquence
          Note: ' ' ne doit pas être True

  Retourne
      - Une liste des mots du texte qui correspondent aux bytes à l'intérieur de start_str et end_str
  '''

    # Note: On utilise le symbole '~' pour indiquer un caractère inconnu
    groups = []
    group = []
    capturing = False
    start_str_matched = ""
    for i in range(2, len(encoded_bytes) - 2):
        debug = False
        byte = encoded_bytes[i]
        next_byte = encoded_bytes[i + 1]
        char = key[byte]
        if not capturing:
            start_str_matched = ""

        # Si char est None, vérifier bytes_with_starting_spaces ou bytes_with_ending_spaces et ajuster char
        if char is None:
            if bytes_with_starting_spaces[byte]:
                char = ' ~'
            elif bytes_with_ending_spaces[byte]:
                char = '~ '
        char2 = key[next_byte]
        # Si char2 est None, vérifier bytes_with_starting_spaces ou bytes_with_ending_spaces et ajuster char2
        if char2 is None:
            if bytes_with_starting_spaces[next_byte]:
                char2 = ' ~'
            elif bytes_with_ending_spaces[next_byte]:
                char2 = '~ '

        if char is not None:
            # On capture présentement le mot
            if capturing:
                if debug: print("char1 != None and capturing")
                # On trouve la fin du mot sur 1 byte
                if re.fullmatch(string=char, pattern=end_str):
                    if debug: print("char == end_str")
                    capturing = False
                    if len(group) >= n_bytes_min and len(group) <= n_bytes_max:
                        if include_start_and_end:
                            group.append(char)
                            group = [start_str_matched] + group
                        groups.append(group)
                    group = []
                # On trouve la fin du mot sur 2 bytes
                elif char2 is not None and re.fullmatch(string=char + char2, pattern=end_str):
                    if debug: print("char + char2 == end_str")
                    capturing = False
                    if len(group) >= n_bytes_min and len(group) <= n_bytes_max:
                        if include_start_and_end:
                            group.append(char + char2)
                            group = [start_str_matched] + group
                        groups.append(group)
                    group = []
                # On n'a pas matché de fin de mot mais on doit s'arrêter (mot trop long ou espace)
                elif len(group) > n_bytes_max or (char2 is not None and ' ' in char2):
                    if debug: print("len(group) > n_bytes_max or ' ' in char2")
                    capturing = False
                    group = []
                # On continue de capturer le mot
                elif decrypt_when_possible:
                    if debug: print("decrypt_when_possible")
                    group.append(char)
                # On laisse un caractère bidon si on ne veut pas décrypter
                else:
                    if debug: print("not decrypt_when_possible")
                    group.append(byte)
            # On ne capture pas présentement le mot
            else:
                if debug: print("char1 != None and not capturing")
                # On commence à capturer le mot sur 1 byte
                if re.fullmatch(string=char, pattern=start_str):
                    if debug: print("char == start_str")
                    capturing = True
                    start_str_matched = char
                    group = []
                # On commence à capturer le mot sur 2 bytes
                elif char2 is not None and re.fullmatch(string=char + char2, pattern=start_str):
                    if debug: print("char + char2 == start_str")
                    capturing = True
                    start_str_matched = char + char2
                    i += 1
                    group = []
        # char est None
        else:
            if char2 is not None:
                # On capture présentement le mot
                if capturing:
                    if debug: print("char2 != None and capturing")
                    group.append(byte)
                    # On trouve la fin du mot sur le prochain byte
                    if re.fullmatch(string=char2, pattern=end_str):
                        if debug: print("char2 == end_str")
                        capturing = False
                        if len(group) >= n_bytes_min and len(group) <= n_bytes_max:
                            if include_start_and_end:
                                group.append(char2)
                                group = [start_str_matched] + group
                            groups.append(group)
                        group = []
                    # On n'a pas matché de fin de mot mais on doit s'arrêter (mot trop long ou espace)
                    elif len(group) > n_bytes_max or ' ' in char2:
                        if debug: print("len(group) > n_bytes_max or ' ' in char2")
                        capturing = False
                        group = []
            # char1 et char2 est None
            else:
                if capturing:
                    if debug: print("chars == None and capturing")
                    if len(group) <= n_bytes_max:
                        group.append(byte)
                    else:
                        capturing = False
                        group = []
                else:
                    if debug: print("chars == None and not capturing")
        # Print i, len(group), byte, next_byte, char, char2 pour déboggage
        if debug: print("i:", i, "group:", (group), "byte:", byte, "next_byte:", next_byte, "char1", char, "char2",
                        char2)
    return groups


def encode_with_sequential_bytes(sequenced_text):
    '''
  Encodage du texte séquencé en bytes.
  Transforme chacun des caractères en bytes séquentiels.
  Retourne l'encodage en bytes et le dictionnaire de correspondance.
  '''
    byte_encode = 0
    chars_encoded = {}
    sequenced_bytes_text = []
    all_possible_chars = text_to_symbols(sequenced_text)
    for i in range(len(sequenced_text)):
        char = sequenced_text[i]
        if not char in all_possible_chars:
            continue
        char = char.replace('\r', '&').replace('\n', '@').replace('\ufeff', '<')

        if char not in chars_encoded:
            chars_encoded[char] = byte_encode
            byte_encode += 1
        sequenced_bytes_text.append(chars_encoded[char])

    # Inverser le dictionnaire chars_encoded pour obtenir byte -> char
    byte_to_char = {v: k for k, v in chars_encoded.items()}

    return sequenced_bytes_text, byte_to_char, chars_encoded


def sequence_fr_text(*urls):
    """Télécharge et traite les textes des URLs données."""
    corpus = ""

    # Charger et traiter chaque URL
    for url in urls:
        text = load_text_from_web(url)

        # Enlever les 5000 premiers et derniers caractères
        if len(text) > 10000:
            text = text[5000:-5000]

        # Enlever les premiers caractères jusqu'au premier mot complet, puis les derniers caractères jusqu'au dernier
        # mot complet, en gardant cette fois-ci l'espace
        text = text[text.index(' ') + 1:text.rindex(' ') + 1]

        # Ajouter le texte traité au corpus
        corpus += text

    # Chiffrer le corpus combiné
    symbols = text_to_symbols(corpus)
    key = gen_key(symbols)
    sequenced_text = M_vers_symboles(corpus, key)

    sequenced_text, bytes_to_char, char_to_byte = encode_with_sequential_bytes(sequenced_text)

    return sequenced_text, bytes_to_char, char_to_byte


# Fonction pour obtenir le max et le 2e max d'une liste ainsi que leurs valeurs
def max_2_ignore(lst, ignore_set=None):
    max1, max2 = -1, -1
    max1_index, max2_index = -1, -1
    if ignore_set is None:
        for i, value in enumerate(lst):

            if value > max1:
                max2 = max1
                max2_index = max1_index
                max1 = value
                max1_index = i
            elif value > max2:
                max2 = value
                max2_index = i
    else:
        for i, value in enumerate(lst):
            if i in ignore_set:
                continue

            if value > max1:
                max2 = max1
                max2_index = max1_index
                max1 = value
                max1_index = i
            elif value > max2:
                max2 = value
                max2_index = i

    return max1, max2, max1_index, max2_index


def max_2_dict(dictionnary):
    max1, max2 = -1, -1
    max1_key, max2_key = None, None

    for key, value in dictionnary.items():
        if value > max1:
            max2 = max1
            max2_key = max1_key
            max1 = value
            max1_key = key
        elif value > max2:
            max2 = value
            max2_key = key

    return max1, max2, max1_key, max2_key


def frequence_matrixes_combinations(dimension, encoded_bytes, add_indexes=False):
    """
  Crée une matrice de fréquences de bytes de dimension donnée.
  Problème:
      Étant donné N bytes fixes, déterminer la fréquence d'apparition de chaque byte formant un N+1-uplet avec ces N bytes dans le texte.
      Stocker les fréquences dans une matrice où chaque ligne représente un N-uplet et chaque colonne représente un byte.
          Modif: La colonne qui représente un byte est modifiée pour être un tuple.
              À l'indexe 0 on a le byte, et à l'indexe 1 on a un tableau des indexes de toutes les occurences du groupe de bytes dans le texte

  Arguments:
      dimension: La dimension de la matrice voulue (nombre de bytes fixes dans les tuples)
      encoded_bytes: Le texte encodé sous forme de tableau de bytes
      byte_probabilities: Dictionnaire des probabilités pour chaque byte.
          Utilisé pour conserver l'ordre décroissant de probabilités des bytes pour l'insertion dans la matrice


  Retourne:
      La matrice de fréquences des bytes
  """
    if add_indexes:
        matrice = {}
        for i in range(len(encoded_bytes) - dimension):
            if dimension == 1:
                if encoded_bytes[i + 1] in matrice:
                    liste_freq_bytes, indexes = matrice[encoded_bytes[i + 1]]
                    liste_freq_bytes[encoded_bytes[i]] += 1
                    indexes.append(i)
                else:
                    liste_freq_bytes = [0 for _ in range(256)]
                    liste_freq_bytes[encoded_bytes[i]] += 1
                    indexes = [i]
                    matrice[encoded_bytes[i + 1]] = (liste_freq_bytes, indexes)
                if encoded_bytes[i] in matrice:
                    liste_freq_bytes, indexes = matrice[encoded_bytes[i]]
                    liste_freq_bytes[encoded_bytes[i + 1]] += 1
                    indexes.append(i)
                else:
                    liste_freq_bytes = [0 for _ in range(256)]
                    liste_freq_bytes[encoded_bytes[i + 1]] += 1
                    indexes = [i]
                    matrice[encoded_bytes[i + 1]] = (liste_freq_bytes, indexes)
            else:
                window = encoded_bytes[i:i + dimension + 1]

                for j in range(len(window)):
                    current_byte = window[j]
                    other_bytes = window[:j] + window[j + 1:]
                    other_bytes = sorted(other_bytes)
                    other_bytes = tuple(other_bytes)

                    if other_bytes in matrice:
                        liste_freq_bytes, indexes = matrice[other_bytes]
                        liste_freq_bytes[current_byte] += 1
                        indexes.append(i)
                    else:
                        liste_freq_bytes = [0 for _ in range(256)]
                        liste_freq_bytes[current_byte] += 1
                        indexes = [i]
                        matrice[other_bytes] = (liste_freq_bytes, indexes)
    else:
        matrice = {}
        for i in range(len(encoded_bytes) - dimension):
            if dimension == 1:
                if encoded_bytes[i + 1] in matrice:
                    matrice[encoded_bytes[i + 1]][encoded_bytes[i]] += 1
                else:
                    matrice[encoded_bytes[i + 1]] = [0 for _ in range(256)]
                    matrice[encoded_bytes[i + 1]][encoded_bytes[i]] += 1
                if encoded_bytes[i] in matrice:
                    matrice[encoded_bytes[i]][encoded_bytes[i + 1]] += 1
                else:
                    matrice[encoded_bytes[i]] = [0 for _ in range(256)]
                    matrice[encoded_bytes[i]][encoded_bytes[i + 1]] += 1
            else:
                window = encoded_bytes[i:i + dimension + 1]

                for j in range(len(window)):
                    current_byte = window[j]
                    other_bytes = window[:j] + window[j + 1:]
                    other_bytes = sorted(other_bytes)
                    other_bytes = tuple(other_bytes)

                    if other_bytes in matrice:
                        matrice[other_bytes][current_byte] += 1
                    else:
                        matrice[other_bytes] = [0 for _ in range(256)]
                        matrice[other_bytes][current_byte] += 1
    return matrice


def frequence_matrixes(dimension, fr_text, encoded_bytes):
    """
  Crée deux matrices de fréquences (bytes et langue française) de dimension donnée.
  Pour dimension = 1: les matrices sont des dictionnaires simples.
      Ex.: Pour obtenir la liste des bytes qui forment une paire avec le byte 1 on fait matrice[1]
  Pour dimension >1, les matrices sont en réalité des dictionnaires de tuples.
      Ex.: Pour obtenir la liste des bytes qui forment un trio avec le byte 1 et 3 on fait matrice_bytes[(1,3)]

  Arguments:
      dimension: La dimension de la matrice voulue
      texte_fr: Un tableau d'un texte en français dont les caractères sont séquencés selon l'encodage en bytes
      encoded_bytes: Les bytes encodés
  """
    matrice_bytes = {}
    matrice_fr = {}
    for texte, matrice in ((encoded_bytes, matrice_bytes), (fr_text, matrice_fr)):
        for i in range(len(texte) - dimension):
            window = texte[i:i + dimension]
            next_char_or_byte = texte[i + dimension]
            if dimension == 1:
                char_or_byte = window[0]
                if char_or_byte in matrice:
                    matrice[char_or_byte][next_char_or_byte] += 1
                else:
                    matrice[char_or_byte] = [0 for _ in range(256)]
                    matrice[char_or_byte][next_char_or_byte] += 1
            else:
                chars_or_bytes = tuple(window)
                if chars_or_bytes in matrice:
                    matrice[chars_or_bytes][next_char_or_byte] += 1
                else:
                    matrice[chars_or_bytes] = [0 for _ in range(256)]
                    matrice[chars_or_bytes][next_char_or_byte] += 1

    return matrice_bytes, matrice_fr


def cut_string_into_pairs(text):
    pairs = []
    for i in range(0, len(text) - 1, 2):
        pairs.append(text[i:i + 2])
    if len(text) % 2 != 0:
        pairs.append(text[-1] + '_')  # Add a placeholder if the string has an odd number of characters
    return pairs


def load_text_from_web(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while loading the text: {e}")
        return None


def M_vers_symboles(M, K):
    encoded_text = []
    i = 0

    while i < len(M):
        # Vérifie les paires de caractères
        if i + 1 < len(M):
            pair = M[i] + M[i + 1]
            if pair in K:
                encoded_text.append(pair)
                i += 2  # Sauter les deux caractères utilisés
                continue

        # Vérifie le caractère seul
        if M[i] in K:
            encoded_text.append(M[i])
        else:
            # Conserve le caractère tel quel si non trouvé
            encoded_text.append(M[i])
        i += 1

    return encoded_text


def chiffrer(M, K):
    l = M_vers_symboles(M, K)
    l = [K[x] for x in l]
    return ''.join(l)


def chiffrer2(M, K) -> str:
    """
  Encode le texte en utilisant un dictionnaire personnalisé.

  :param text: Le texte à encoder
  :param custom_dict: Le dictionnaire de correspondances
  :return: Le texte encodé
  """
    encoded_text = []
    i = 0

    while i < len(M):
        # Vérifie les paires de caractères
        if i + 1 < len(M):
            pair = M[i] + M[i + 1]
            if pair in K:
                encoded_text.append(K[pair])
                i += 2  # Sauter les deux caractères utilisés
                continue

        # Vérifie le caractère seul
        if M[i] in K:
            encoded_text.append(K[M[i]])
        else:
            # Conserve le caractère tel quel si non trouvé
            encoded_text.append(M[i])
        i += 1

    return ''.join(encoded_text)


def gen_key(symboles):
    l = len(symboles)
    if l > 256:
        return False

    rnd.seed(1337)
    int_keys = rnd.sample(list(range(l)), l)
    dictionary = dict({})
    for s, k in zip(symboles, int_keys):
        dictionary[s] = "{:08b}".format(k)
    return dictionary


def text_to_symbols(text):
    symboles = ['b', 'j', '\r', 'J', '”', ')', 'Â', 'É', 'ê', '5', 't', '9', 'Y', '%', 'N', 'B', 'V', '\ufeff', 'Ê',
                '?', '’', 'i', ':', 's', 'C', 'â', 'ï', 'W', 'y', 'p', 'D', '—', '«', 'º', 'A', '3', 'n', '0', 'q', '4',
                'e', 'T', 'È', '$', 'U', 'v', '»', 'l', 'P', 'X', 'Z', 'À', 'ç', 'u', '…', 'î', 'L', 'k', 'E', 'R', '2',
                '_', '8', 'é', 'O', 'Î', '‘', 'a', 'F', 'H', 'c', '[', '(', "'", 'è', 'I', '/', '!', ' ', '°', 'S', '•',
                '#', 'x', 'à', 'g', '*', 'Q', 'w', '1', 'û', '7', 'G', 'm', '™', 'K', 'z', '\n', 'o', 'ù', ',', 'r',
                ']', '.', 'M', 'Ç', '“', 'h', '-', 'f', 'ë', '6', ';', 'd', 'ô', 'e ', 's ', 't ', 'es', ' d', '\r\n',
                'en', 'qu', ' l', 're', ' p', 'de', 'le', 'nt', 'on', ' c', ', ', ' e', 'ou', ' q', ' s', 'n ', 'ue',
                'an', 'te', ' a', 'ai', 'se', 'it', 'me', 'is', 'oi', 'r ', 'er', ' m', 'ce', 'ne', 'et', 'in', 'ns',
                ' n', 'ur', 'i ', 'a ', 'eu', 'co', 'tr', 'la', 'ar', 'ie', 'ui', 'us', 'ut', 'il', ' t', 'pa', 'au',
                'el', 'ti', 'st', 'un', 'em', 'ra', 'e,', 'so', 'or', 'l ', ' f', 'll', 'nd', ' j', 'si', 'ir', 'e\r',
                'ss', 'u ', 'po', 'ro', 'ri', 'pr', 's,', 'ma', ' v', ' i', 'di', ' r', 'vo', 'pe', 'to', 'ch', '. ',
                've', 'nc', 'om', ' o', 'je', 'no', 'rt', 'à ', 'lu', "'e", 'mo', 'ta', 'as', 'at', 'io', 's\r', 'sa',
                "u'", 'av', 'os', ' à', ' u', "l'", "'a", 'rs', 'pl', 'é ', '; ', 'ho', 'té', 'ét', 'fa', 'da', 'li',
                'su', 't\r', 'ée', 'ré', 'dé', 'ec', 'nn', 'mm', "'i", 'ca', 'uv', '\n\r', 'id', ' b', 'ni', 'bl']
    return symboles


def decode(encoded_bytes, key):
    decoded_text = ""
    for i in range(0, len(encoded_bytes)):
        byte = encoded_bytes[i]
        char = key[byte]
        if char is None:
            char = ' '
        else:
            char = char.replace('&', '\r').replace('@', '\n').replace('<', '\ufeff')
        decoded_text += char
    return decoded_text


def clean_repr(char_or_pair):
    rep = repr(char_or_pair)
    # Enlever les guillemets si c'est une chaîne de caractères
    if rep.startswith("'") and rep.endswith("'"):
        return rep[1:-1]
    elif rep.startswith('"') and rep.endswith('"'):
        return rep[1:-1]
    return rep


def main(test_number):
    # Stocker les probabilités des 256 caractères possibles dans un fichier
    if not os.path.exists("probabilities.txt"):
        urls = ["https://www.gutenberg.org/ebooks/13846.txt.utf-8",
                "https://www.gutenberg.org/ebooks/4650.txt.utf-8",
                "https://www.gutenberg.org/cache/epub/35064/pg35064.txt",
                "https://www.gutenberg.org/cache/epub/14793/pg14793.txt",
                "https://www.gutenberg.org/cache/epub/73384/pg73384.txt",
                "https://www.gutenberg.org/cache/epub/74455/pg74455.txt",
                "https://www.gutenberg.org/cache/epub/13951/pg13951.txt",
                "https://www.gutenberg.org/cache/epub/55501/pg55501.txt"]
        combined_text = ""
        for url in urls:
            text = load_text_from_web(url)
            if len(text) > 10000:
                text = text[5000:-5000]  # Enlever les 5000 premiers et derniers caractères
            else:
                continue
            text = text[text.index(' ') + 1:text.rindex(
                ' ') + 1]  # Enlever les premiers et derniers caractères jusqu'au premier et dernier mot
            combined_text += text

        cle_secrete = gen_key(text_to_symbols(combined_text))
        C = chiffrer2(combined_text, cle_secrete)
        # Enlever tous les caractères non-binaires dans C
        C = re.sub(r"[^01]", "", C)

        # Sachant que le texte encodé est des 1 et des 0 où chaque tranche de 8 bits est un caractère

        # Déterminer le nombre de 0 à ajouter au début du texte pour obtenir un nombre de bits multiple de 8
        num_padding_bits = (8 - (len(C) % 8)) % 8

        # Ajouter les bits de padding au début du texte
        C = "0" * num_padding_bits + C

        # Séparer le texte encodé en tranches de 8 caractères
        encoded_bytes = [C[i:i + 8] for i in range(0, len(C), 8)]

        # Obtenir les probabilités de chaque séquence de 8 bits
        byte_probabilities = {byte: 0 for byte in set(encoded_bytes)}
        for byte in encoded_bytes:
            byte_probabilities[byte] += 1
        total_bytes = sum(byte_probabilities.values())
        byte_probabilities = {byte: count / total_bytes for byte, count in byte_probabilities.items()}

        char_to_probability = {}
        for char in cle_secrete:
            if cle_secrete[char] in byte_probabilities:
                char_to_probability[char] = byte_probabilities[cle_secrete[char]]
            else:
                char_to_probability[char] = 0

        # Trier les caractères en ordre décroissant de probabilité
        sorted_chars = sorted(char_to_probability, key=char_to_probability.get, reverse=True)

        with open("probabilities.txt", "w", encoding="utf-8") as f:
            for char in sorted_chars:
                # Remplacer les caractères spéciaux par d'autres représentations qui ne sont pas des symboles de la clé pour éviter des maux de tête
                clean_char = clean_repr(char.replace('\r', '&').replace('\n', '@').replace('\ufeff', '<'))
                f.write(f"{clean_char}: {char_to_probability[char]}\n")

    if not os.path.exists("word_probabilities.txt"):
        urls = ["https://www.gutenberg.org/ebooks/13846.txt.utf-8",
                "https://www.gutenberg.org/ebooks/4650.txt.utf-8",
                "https://www.gutenberg.org/cache/epub/35064/pg35064.txt",
                "https://www.gutenberg.org/cache/epub/14793/pg14793.txt",
                "https://www.gutenberg.org/cache/epub/73384/pg73384.txt",
                "https://www.gutenberg.org/cache/epub/74455/pg74455.txt",
                "https://www.gutenberg.org/cache/epub/13951/pg13951.txt",
                "https://www.gutenberg.org/cache/epub/55501/pg55501.txt"]
        combined_text = ""
        for url in urls:
            text = load_text_from_web(url)
            if len(text) > 10000:
                text = text[5000:-5000]  # Enlever les 5000 premiers et derniers caractères
            else:
                continue
            text = text[text.index(' ') + 1:text.rindex(
                ' ') + 1]  # Enlever les premiers et derniers caractères jusqu'au premier et dernier mot
            combined_text += text

        # Séparer le texte en mots
        words = combined_text.split()

        # Compter le nombre d'occurrences de chaque mot
        word_counts = Counter(words)

        # Calculer les probabilités de chaque mot
        total_words = sum(word_counts.values())
        word_probabilities = {word: count / total_words for word, count in word_counts.items()}
        sorted_words = sorted(word_probabilities, key=word_probabilities.get, reverse=True)

        with open("word_probabilities.txt", "w", encoding="utf-8") as f:
            for word in sorted_words:
                f.write(f"{word}: {word_probabilities[word]}\n")

    # Chiffrer le texte du test.py fourni:
    # Charger le premier corpus et enlever les 10 000 premiers caractères
    # "https://www.gutenberg.org/cache/epub/18812/pg18812.txt"#"https://www.gutenberg.org/ebooks/13846.txt.utf-8"
    urls_1 = ["https://www.gutenberg.org/cache/epub/58290/pg58290.txt",
              "https://www.gutenberg.org/cache/epub/19248/pg19248.txt",
              "https://www.gutenberg.org/cache/epub/62196/pg62196.txt",
              "https://www.gutenberg.org/cache/epub/14286/pg14286.txt",
              "https://www.gutenberg.org/cache/epub/64086/pg64086.txt",
              "https://www.gutenberg.org/cache/epub/23582/pg23582.txt",
              "https://www.gutenberg.org/cache/epub/12338/pg12338.txt",
              "https://www.gutenberg.org/cache/epub/16023/pg16023.txt",
              "https://www.gutenberg.org/cache/epub/28827/pg28827.txt",
              "https://www.gutenberg.org/cache/epub/16824/pg16824.txt"]

    # Charger le deuxième corpus et enlever les 10 000 premiers caractères
    # "https://www.gutenberg.org/cache/epub/51632/pg51632.txt"#"https://www.gutenberg.org/ebooks/4650.txt.utf-8"
    urls_2 = ["https://www.gutenberg.org/cache/epub/18494/pg18494.txt",
              "https://www.gutenberg.org/cache/epub/29900/pg29900.txt",
              "https://www.gutenberg.org/cache/epub/73653/pg73653.txt",
              "https://www.gutenberg.org/cache/epub/72954/pg72954.txt",
              "https://www.gutenberg.org/cache/epub/58698/pg58698.txt",
              "https://www.gutenberg.org/cache/epub/61697/pg61697.txt",
              "https://www.gutenberg.org/cache/epub/49712/pg49712.txt",
              "https://www.gutenberg.org/cache/epub/72982/pg72982.txt",
              "https://www.gutenberg.org/cache/epub/14059/pg14059.txt",
              "https://www.gutenberg.org/cache/epub/17747/pg17747.txt"]

    corpus1 = load_text_from_web(urls_1[test_number - 1])
    corpus2 = load_text_from_web(urls_2[test_number - 1])

    # Combiner les deux corpus
    corpus = corpus1 + corpus2
    rnd.seed(time.time())
    global allow_rand
    a, b, l, c = 0, 0, 0, 0
    M = ""
    if allow_rand:
        a = rnd.randint(3400, 7200)
        b = rnd.randint(96000, 125000)
        l = (a + b)
        c = rnd.randint(0, len(corpus) - l)
        M = corpus[c:c + l]
    else:
        M = corpus[10000:270000]

    # print("Longueur du message à décoder: ", len(M))

    cle_secrete = gen_key(text_to_symbols(M))

    C = chiffrer2(M, cle_secrete)
    # Enlever tous les caractères non-binaires dans C
    C = re.sub(r"[^01]", "", C)

    # Décoder le texte chiffré
    decrypt(C, cle_secrete, test_number)

    return


def decrypt(encoded_text):
    # ---------------------- Préparation des données ----------------------

    # Stocker les probabilités des mots de la langue française du fichier "word_probabilities.txt"
    word_probabilities = {}
    with open("word_probabilities.txt", "r", encoding="utf-8") as f:
        for line in f:
            word, prob = line.rsplit(": ", 1)
            word_probabilities[word] = float(prob)

    # Créer un dictionnaire des probabilités par caractère basé sur une clé secrète générée sur un long texte avec la méthode donnée
    char_probabilities = {}
    with open("probabilities.txt", "r", encoding="utf-8") as f:
        for line in f:
            char, prob = line.rsplit(": ", 1)
            char_probabilities[char] = float(prob)

    # Trier char_probabilities en ordre décroissant de probabilité
    sorted_chars = sorted(char_probabilities, key=char_probabilities.get, reverse=True)

    # Déterminer le nombre de 0 à ajouter au début du texte pour obtenir un nombre de bits multiple de 8
    num_padding_bits = (8 - (len(encoded_text) % 8)) % 8

    # Ajouter les bits de padding au début du texte
    encoded_text = "0" * num_padding_bits + encoded_text

    # Séparer le texte encodé en bytes (convertis en entiers)
    encoded_bytes = [int(encoded_text[i:i + 8], 2) for i in range(0, len(encoded_text), 8)]

    # Obtenir les probabilités de chaque byte
    byte_probabilities = {byte: 0 for byte in set(encoded_bytes)}
    for byte in encoded_bytes:
        byte_probabilities[byte] += 1
    total_bytes = sum(byte_probabilities.values())
    byte_probabilities = {byte: count / total_bytes for byte, count in byte_probabilities.items()}

    # Trier les séquences de 8 bits en ordre décroissant de probabilité
    sorted_bytes = sorted(byte_probabilities, key=byte_probabilities.get, reverse=True)

    # ------------------------------ DÉCODAGE--------------------------------------------------
    global key
    key = [None] * 256
    # ______________ 1. Trouver la substitution "e " et "s " ___________

    # Parmi toutes les paires de substitution du top 10 plus fréquents bytes, on doit trouver quel est le "e " et quel est le "s "
    best_pair = (None, None)
    max_groups_pair = 0
    # On suppose que
    for indice_e in range(0, 8):
        for indice_s in range(indice_e, 8):
            if indice_e == indice_s:
                continue

            # Supposons qu'on a trouvé la bonne paire de "e " et "s "
            key[sorted_bytes[indice_e]] = 'e '

            # On veut faire ça:
            key[sorted_bytes[indice_s]] = 's '

            # On vérifie si la substitution est valide
            if validate_space_substitution(sorted_bytes[indice_e], 'e ', key,
                                           encoded_bytes) > 0.001 or validate_space_substitution(sorted_bytes[indice_s],
                                                                                                 's ', key,
                                                                                                 encoded_bytes) > 0.001:
                # La substitution n'est pas valide
                # print("Substitution invalide pour 'e ' et 's '", secret_key_byte_to_char[sorted_bytes[indice_e]], secret_key_byte_to_char[sorted_bytes[indice_s]])
                key[sorted_bytes[indice_e]] = None
                key[sorted_bytes[indice_s]] = None
                continue

            # On forme des groupes de mots de forme "e " + BYTE + "e " et des groupes de "s " + BYTE + "s "
            # L'objectif est que les groupes de forme "e " + BYTE + "e " ont moins de BYTE possibles
            # et que les groupes de forme "s " + BYTE + "s " ont beaucoup de BYTE possibles
            groups_e = capture_groups(start_str=r'e ', n_bytes_min=1, n_bytes_max=1, end_str=r'e ',
                                      encoded_bytes=encoded_bytes, key=key)
            groups_s = capture_groups(start_str=r's ', n_bytes_min=1, n_bytes_max=1, end_str=r's ',
                                      encoded_bytes=encoded_bytes, key=key)

            # On vérifie que la taille des groupes est >= 5:
            # Si non, ça veut dire que le groupe associé est en réalité "\r\n",
            #   car il ne devrait pas (ou très peu) y avoir 2 sauts de ligne consécutifs séparés d'un seul byte dans le texte.
            # print("Nombre de groupes de 'e ' trouvés: ", len(groups_e))
            # print("Nombre de groupes de 's ' trouvés: ", len(groups_s))

            # On semble avoir trouvé une bonne paire candidate pour "e " et "s "
            # print("Paire candidate pour 'e ' et 's ' trouvée: '" + secret_key_byte_to_char[sorted_bytes[indice_e]] + "' et '" + secret_key_byte_to_char[sorted_bytes[indice_s]] + "'")
            # On calcule les fréquences de chaque byte dans les groupes de "e "

            # print("Groups_e:")
            # Créer un set avec tous les bytes dans groups_e:
            all_bytes_e = []
            for group in groups_e:
                for byte in group:
                    if byte not in all_bytes_e:
                        # print(secret_key_byte_to_char[byte], end=" ")
                        all_bytes_e.append(byte)

            # print("\nGroups_s:")
            # Créer un set avec tous les bytes dans groups_s:
            all_bytes_s = []
            for group in groups_s:
                for byte in group:
                    if byte not in all_bytes_s:
                        # print(secret_key_byte_to_char[byte], end=" ")
                        all_bytes_s.append(byte)

            # On sait qu'il y a au moins 1 byte différents dans les groupes de "e ", car "que" est un mot commun.
            if len(all_bytes_e) < 1 or len(all_bytes_s) < 1:
                key[sorted_bytes[indice_e]] = None
                key[sorted_bytes[indice_s]] = None
                continue
            # On sait qu'il y a au moins 3 bytes différents dans les groupes de "s "
            # Ex.: "les", "des", "ses", "tes", "mes", "nos", "vos"...
            if len(all_bytes_e) < 4 and len(all_bytes_s) < 4:
                key[sorted_bytes[indice_e]] = None
                key[sorted_bytes[indice_s]] = None
                continue

            # On a trouvé une bonne paire de "e " et "s "
            """ print("Nombre de bytes différents dans les groupes de 'e ': ", len(all_bytes_e))
      print("Nombre de bytes différents dans les groupes de 's ': ", len(all_bytes_s))
      print() """

            # Le groupe avec le plus de bytes différents est "s "
            # Appliquer l'échange si on s'est trompé dans l'assignation
            if len(all_bytes_e) > len(all_bytes_s):
                indice_e, indice_s = indice_s, indice_e

            # Dernier critère pour ne pas effectuer une fausse substitution: On remarque que la somme des longueurs des groupes de "e " et "s " est maximale
            if (len(groups_e) + len(groups_s)) > max_groups_pair:
                # print("Nouvelle meilleure paire (e, s) trouvée: '" + secret_key_byte_to_char[sorted_bytes[indice_e]] + "' et '" + secret_key_byte_to_char[sorted_bytes[indice_s]] + "'")
                # print(len(groups_e), len(groups_s))
                max_groups_pair = len(groups_e) + len(groups_s)
                best_pair = (indice_e, indice_s)

            key[sorted_bytes[indice_s]] = None
            key[sorted_bytes[indice_e]] = None

    indice_e, indice_s = best_pair
    try:
        key[sorted_bytes[indice_e]] = 'e '
        key[sorted_bytes[indice_s]] = 's '
    except:
        # Notre algorithme a échoué à trouver une bonne paire de "e " et "s "
        # On assume que les 1er et 2e byte les plus probables sont "e " et "s "
        indice_e = 0
        indice_s = 1
        key[sorted_bytes[indice_e]] = 'e '
        key[sorted_bytes[indice_s]] = 's '
        print("FAILED TO LOCATE E AND S")

    # On va ensuite créer un set avec tous les bytes qui se répètent plus de 3 fois d'affilée dans le texte.
    # Cela va capturer les bytes du genre "..." ou "   " qui sont des espaces répétées pour formattage.
    # On va pouvoir utiliser cette information plus tard pour ne pas confondre les bytes alphanumériques avec des espaces ou points ou \r\n
    consecutive_3_bytes = set()
    for i in range(len(encoded_bytes)):
        group = [encoded_bytes[i]]
        while i < len(encoded_bytes) - 1 and encoded_bytes[i] == encoded_bytes[i + 1]:
            i += 1
            group.append(encoded_bytes[i])
        if len(group) >= 3:
            consecutive_3_bytes.add(group[0])

    # Même chose pour 2 bytes consécutifs
    consecutive_2_bytes = set()
    for i in range(len(encoded_bytes)):
        group = [encoded_bytes[i]]
        while i < len(encoded_bytes) - 1 and encoded_bytes[i] == encoded_bytes[i + 1]:
            i += 1
            group.append(encoded_bytes[i])
        if len(group) >= 2:
            consecutive_2_bytes.add(group[0])

    # Supposer "t "
    # Trouver les groupes 'e/s ' + BYTE + 't '
    # Déduire une heuristique pour trouver "t " en faisant plusieurs tests
    max_freq = len(encoded_bytes) / 12000
    best_sub = None
    for indice_t in range(0, 8):
        if key[sorted_bytes[indice_t]] is not None:
            continue
        # Supposons qu'on a trouvé la bonne substitution de "t "
        key[sorted_bytes[indice_t]] = 't '
        # print("On suppose '" + secret_key_byte_to_char[sorted_bytes[indice_t]] + "' = 't '")

        # On vérifie si la substitution est valide
        if validate_space_substitution(sorted_bytes[indice_t], 't ', key, encoded_bytes) > 0.001:
            # La substitution n'est pas valide
            key[sorted_bytes[indice_t]] = None
            continue

        # On forme des groupes de mots de forme "(e|s) " + BYTE + "t "
        groups_t = capture_groups(start_str=r'(e|s) ', n_bytes_min=1, n_bytes_max=1, end_str=r't ',
                                  encoded_bytes=encoded_bytes, key=key)
        # print("Length de groups_t: " + str(len(groups_t)))
        # On calcule les fréquences de chaque byte dans les groupes

        # print("Groups_t:")
        # Créer un set avec tous les bytes dans groups_t:
        all_bytes_t = []
        byte_frequencies_t = {}
        for group in groups_t:
            for byte in group:
                if byte not in all_bytes_t:
                    # print(secret_key_byte_to_char[byte], end=" ")
                    all_bytes_t.append(byte)
                    byte_frequencies_t[byte] = 1
                else:
                    byte_frequencies_t[byte] += 1

        # On sait qu'il y a au moins 3 bytes différent dans les groupes de "s/e ", car "est", "cet", "dit"... sont des mots communs
        # Cependant il y en a aussi moins de 10
        if len(all_bytes_t) < 3 or len(all_bytes_t) > 10:
            key[sorted_bytes[indice_t]] = None
            continue

        if sorted_bytes[indice_t] in consecutive_2_bytes:  # C'est le caractère espace.
            key[sorted_bytes[indice_t]] = ' '
            continue

        # Dernier critère pour ne pas effectuer une fausse substitution: Le groupe "e/s " + BYTE + "t " est très fréquent, et les BYTE possibles ont une haute fréquence
        # print("Nombre de groupes t: " + str(len(groups_t)))
        if (len(groups_t) > max_freq and (
                best_sub is None or byte_probabilities[sorted_bytes[best_sub]] < byte_probabilities[
            sorted_bytes[indice_t]])):
            # print("Nouvelle substitution 't ' trouvée: '" + secret_key_byte_to_char[sorted_bytes[indice_t]] + "'")
            max_freq = len(groups_t)
            best_sub = indice_t

        key[sorted_bytes[indice_t]] = None
    indice_t = best_sub

    if indice_t is not None:
        key[sorted_bytes[indice_t]] = 't '
        """ print("Étape 1: Substitution de '" + str(sorted_bytes[indice_t]) + "' par 't ', Obs = " + str(byte_probabilities[sorted_bytes[indice_t]]) + " | Théorique = " + str(char_probabilities['t ']))
    print("Validation avec la clé secrète: '" + secret_key_byte_to_char[sorted_bytes[indice_t]] + "'") """

        # Puisqu'on connaît le "t " on peut aussi aller chercher le "es"
        groups = capture_groups(start_str=r'(e|t) ', n_bytes_min=1, n_bytes_max=1, end_str=r't ',
                                encoded_bytes=encoded_bytes, key=key)

        # Créer un set avec tous les bytes dans groups_t:
        # print("Groups_t V2:")
        all_bytes_t = []
        byte_frequencies_t = {}
        for group in groups:
            for byte in group:
                if byte not in all_bytes_t:
                    # print(secret_key_byte_to_char[byte], end=" ")
                    all_bytes_t.append(byte)
                    byte_frequencies_t[byte] = 1
                else:
                    byte_frequencies_t[byte] += 1
        # print()
        max1_freq = 0
        max1_byte = None
        max1_prob = 0
        max2_freq = 0
        max2_byte = None
        max2_prob = 0

        es_byte = None
        for byte in byte_frequencies_t:
            freq = byte_frequencies_t[byte]
            if freq > max1_freq:
                max1_freq = max2_freq
                max1_byte = max2_byte
                max1_prob = max2_prob
                max1_freq = freq
                max1_byte = byte
                max1_prob = byte_probabilities[byte]
            elif freq > max2_freq:
                max2_freq = freq
                max2_byte = byte
                max2_prob = byte_probabilities[byte]
        # Le byte "es" est soit le plus fréquent par un facteur 2, soit le plus probable par un facteur 1.5, sinon on ne peut pas conclure
        if max1_freq > 2 * max2_freq:
            es_byte = max1_byte
        else:
            if max1_prob > 2 * max2_prob:
                es_byte = max1_byte
            elif max2_prob > 2 * max1_prob:
                es_byte = max2_byte
        if es_byte is not None:
            key[es_byte] = "es"
        else:
            print("FAILED TO LOCATE ES")


    else:
        # Notre algorithme a échoué à trouver "t "
        print("FAILED TO LOCATE T AND ES")

    # ________________ 3. Capturer les groupes 'e ' + BYTE + 'e ' _________________

    """ # Test de la fonction capture_groups OK
  # B2 = 'e ', B4 = 't '
  # C = B1 B2 B3 B4
  # M = e ,~, ,e ,~, ,~,~,e ,~,e 
  # On s'attend aux groupes [B3]
  encoded_bytes = [1, 2, 3, 4]
  key = [None] * 256
  key[2] = 'e '
  key[4] = 't '
  groups = capture_groups(start_str=r'e ', n_bytes_min=1, n_bytes_max=1, end_str=r't ')
  """

    # b) Obtenir les bytes qui sont de forme (' '|'e ') + BYTE + 'e ' et leur fréquence
    groups = capture_groups(start_str=r'e ', n_bytes_min=1, n_bytes_max=1, end_str=r'e ', encoded_bytes=encoded_bytes,
                            key=key)

    """ print("Nombre de groupes capturés: ", len(groups))
  for group in groups:
      for byte in group:
          print("Byte : '" + str(byte) + "' =  char '" + secret_key_byte_to_char[byte] +"'") """

    # Trouver le nombre d'occurences de chaque byte dans les groupes
    occurences_group = {}
    for group in groups:
        for byte in group:
            if byte in occurences_group:
                occurences_group[byte] += 1
            else:
                occurences_group[byte] = 1

    # Trier les bytes en ordre décroissant d'occurences
    sorted_occurences_group = sorted(occurences_group, key=occurences_group.get, reverse=True)

    # Le premier byte est "qu". On ignore le reste qui est trop rare
    # On peut donc les substituer directement
    key[sorted_occurences_group[0]] = 'qu'

    # On cherche maintenant tous les bytes qui suivent "e " + "qu" sauf ceux déjà décodés
    bytes_after_e_qu = {}
    for i in range(2, len(encoded_bytes)):
        byte = encoded_bytes[i]
        prev_prev_char = key[encoded_bytes[i - 2]]
        prev_char = key[encoded_bytes[i - 1]]
        if prev_prev_char == 'e ' and prev_char == 'qu' and key[byte] == None:
            if byte in bytes_after_e_qu:
                bytes_after_e_qu[byte] += 1
            else:
                bytes_after_e_qu[byte] = 1

    # ---------------------- 4. Substitution automatique des bytes ----------------------
    # 1- Encoder un texte en français qui servira de données théoriques pour les fréquences des caractères.
    # fr_text: Texte en français encodé en bytes
    fr_text, fr_byte_to_char, fr_char_to_byte = sequence_fr_text("https://www.gutenberg.org/ebooks/13846.txt.utf-8",
                                                                 "https://www.gutenberg.org/ebooks/4650.txt.utf-8",
                                                                 "https://www.gutenberg.org/cache/epub/35064/pg35064.txt",
                                                                 "https://www.gutenberg.org/cache/epub/14793/pg14793.txt",
                                                                 "https://www.gutenberg.org/cache/epub/73384/pg73384.txt",
                                                                 "https://www.gutenberg.org/cache/epub/74455/pg74455.txt",
                                                                 "https://www.gutenberg.org/cache/epub/13951/pg13951.txt",
                                                                 "https://www.gutenberg.org/cache/epub/55501/pg55501.txt")

    # Initialiser les bytes connus
    bytes_connus = [byte for byte in range(256) if key[byte] is not None]
    bytes_connus = sorted(bytes_connus)
    bytes_connus_autre_encodage = [fr_char_to_byte[key[byte]] for byte in bytes_connus]
    bytes_connus_autre_encodage = sorted(bytes_connus_autre_encodage)

    # Fonction pour performer les substitutions
    def perform_substitution(matrice_bytes, matrice_fr, dimension, min_freq, ratio_threshold_bytes, ratio_threshold_fr,
                             char_probabilities, byte_probabilities, excluded_substitutions, exclude_substitutions,
                             exclude_rare_chars, consecutive_3_bytes, encoded_bytes):

        for (context, freqs_bytes) in matrice_bytes.items():
            # Vérifie si le contexte consiste en des bytes connus
            if dimension == 1:
                byte = context
                if byte not in bytes_connus:
                    continue
                char = key[byte]
                # Obtenir le contexte correspondant dans le texte français
                fr_context = fr_char_to_byte.get(char)
                if fr_context is None or fr_context not in matrice_fr:
                    continue
                freqs_fr = matrice_fr[fr_context]
            else:
                if not all(b in bytes_connus for b in context):
                    continue
                # Pour dimension > 1, 'contexte' est un tuple de bytes
                # Obtenir le contexte de caractères
                char_context = tuple(key[b] for b in context)
                # Convertir le contexte de caractères en bytes dans l'encodage français
                byte_context_fr = tuple(sorted(fr_char_to_byte[ch] for ch in char_context))
                # Obtenir les fréquences des bytes suivant le contexte dans le texte français
                freqs_fr = matrice_fr.get(byte_context_fr)
                if freqs_fr is None:
                    continue

            # Ignorer les bytes déjà connus
            freqs_bytes_ignore = freqs_bytes
            freqs_fr_ignore = freqs_fr

            # Trouver les bytes les plus fréquents dans les deux fréquences
            max1, max2, max1_index, max2_index = max_2_ignore(freqs_bytes_ignore, bytes_connus)
            max1_fr, max2_fr, max1_fr_index, max2_fr_index = max_2_ignore(freqs_fr_ignore, bytes_connus_autre_encodage)

            # On a déjà exclu cette substitution
            if excluded_substitutions[max1_index][max1_fr_index]:
                continue

            # Au début de l'algorithme, on ne veut pas s'aventurer dans des substitutions trop risquées (majuscules, apostrophes, caractères étranges, etc.)
            if exclude_rare_chars:
                if not re.match(r'[^\\*yéwàâô’jkzA-Zx!?»\\(\\);\\—-]+', fr_byte_to_char[max1_fr_index]):
                    continue

            # Obtenir les probabilités des 2 bytes les plus fréquents
            max1_prob = byte_probabilities.get(max1_index)
            max2_prob = byte_probabilities.get(max2_index)
            if max1_prob is None or max2_prob is None:
                continue

            # Obtenir la probabilité théorique des 2 char les plus fréquents
            max1_fr_prob = char_probabilities[fr_byte_to_char[max1_fr_index]]
            max2_fr_prob = char_probabilities[fr_byte_to_char[max2_fr_index]]

            # On veut s'assurer que la substitution max1 -> max1_fr est fiable
            # Pour ce faire, on évalue l'ordre relatif des probabilités de (max1, max2), et (max1_fr, max2_fr)
            #   Si (max1_prob > max_prob) & (max1_fr_prob > max2_fr_prob), on permet la substitution
            #   Si (max1_prob < max2_prob) & (max1_fr_prob < max2_fr_prob), on permet la substitution.
            # La substitution est bloquée uniquement dans le cas où l'ordre relatif entre les probabilités observées et théoriques sont inversées
            respects_order = (max1_prob > max2_prob) == (max1_fr_prob > max2_fr_prob)

            # Appliquer les seuils pour assurer des substitutions fiables
            if (
                    max1 >= min_freq
                    and max1 > ratio_threshold_bytes * max2
                    and max1_fr >= min_freq
                    and max1_fr > ratio_threshold_fr * max2_fr
            ):
                # Vérifier si la substitution est plausible
                if key[max1_index] is None and fr_byte_to_char[max1_fr_index] not in key:
                    # Bloquer la substitution si c'est le cas
                    if not respects_order:
                        # print("Substitution bloquée: " + secret_key_byte_to_char[max1_index] + " ou " + secret_key_byte_to_char[max2_index] + " -> " + fr_byte_to_char[max1_fr_index] + " ou " + fr_byte_to_char[max2_fr_index])
                        continue

                    # Si le byte qu'on remplace apparaît 3 fois de suite dans notre texte, on sait que la bonne substitution doit être du formattage (espace, point, etc.)
                    if max1_index in consecutive_3_bytes:
                        if fr_byte_to_char[max1_fr_index] not in [" ", "&@", "."]:
                            excluded_substitutions[max1_index][max1_fr_index] = True
                            continue

                    # On fait une dernière vérification (très coûteuse) pour savoir si cette substitution est fiable.
                    if exclude_substitutions:
                        # substitution_accepted si une substitution acceptée a été trouvée. replacement est un char autre que celui proposé si une meilleure substitution a été trouvée
                        substitution_accepted, replacement = verify_substitution_in_text(max1_index,
                                                                                         fr_byte_to_char[max1_fr_index],
                                                                                         key, encoded_bytes)

                        # On pense avoir trouvé une meilleure substitution.
                        if replacement is not None:
                            # Avant ça, on vérifie si elle est bonne.
                            if not excluded_substitutions[max1_index][fr_char_to_byte[replacement]]:
                                if verify_substitution_in_text(max1_index, replacement, key, encoded_bytes)[0]:
                                    key[max1_index] = replacement
                                    bisect.insort(bytes_connus, max1_index)
                                    bisect.insort(bytes_connus_autre_encodage, fr_char_to_byte[replacement])
                                    return
                            # La substitution est moins bonne que prévue. On ne la prend pas.
                            else:
                                excluded_substitutions[max1_index][fr_char_to_byte[replacement]] = True
                                continue

                        if not substitution_accepted:
                            excluded_substitutions[max1_index][max1_fr_index] = True
                            continue

                        # Les substitutions avec des espaces sont PARTICULIÈREMENT importantes.
                        # On ne veut absolument pas se tromper là-dessus, parce que les espaces délimitent les mots.
                        if ' ' in fr_byte_to_char[max1_fr_index]:
                            error_frequency = validate_space_substitution(max1_index, fr_byte_to_char[max1_fr_index],
                                                                          key, encoded_bytes)
                            if error_frequency > 0.06:
                                excluded_substitutions[max1_index][max1_fr_index] = True
                                continue

                    key[max1_index] = fr_byte_to_char[max1_fr_index]
                    bisect.insort(bytes_connus, max1_index)
                    bisect.insort(bytes_connus_autre_encodage, max1_fr_index)
                    return
        return

    # --------------- PARAMÈTRES POUR LES COMBINAISONS ------------------------
    initial_min_freq_comb = 20
    initial_ratio_threshold_bytes_comb = 1.9
    initial_ratio_threshold_fr_comb = 1.9

    min_min_freq_comb = 10
    min_ratio_threshold_bytes_comb = 1.3
    min_ratio_threshold_fr_comb = 1.3

    # Décrémenter les seuils
    min_freq_decrement_comb = 1
    ratio_threshold_decrement_comb = 0.1

    freq_decrement_per_dimension_comb = 1
    ratio_decrement_per_dimension_comb = 0.05

    # Dimensions des n-grammes à considérer
    dimensions_comb = [1, 2]

    matrices_fr_comb = [None for _ in range(len(dimensions_comb))]
    matrices_bytes_comb = [None for _ in range(len(dimensions_comb))]
    for dimension in dimensions_comb:
        matrices_bytes_comb[dimension - 1] = frequence_matrixes_combinations(dimension=dimension,
                                                                             encoded_bytes=encoded_bytes)
        matrices_fr_comb[dimension - 1] = frequence_matrixes_combinations(dimension=dimension, encoded_bytes=fr_text)

    # --------------------- PARAMÈTRES GÉNÉRAUX -------------------------------
    # Nombre minimum de bytes connus désirés
    desired_minimum_known_bytes = len(byte_probabilities)

    # Après combien de substitutions de combinaisons on passe aux fréquences, et vice-versa
    # On veut diminuer le nombre de substitutions consécutives par la même approche pour éviter le plus possible les erreurs
    no_of_substitutions_comb = [desired_minimum_known_bytes]
    no_of_substitutions_seq = [5]
    swap_thresholds = []
    cumul = 0
    for i in range(len(no_of_substitutions_comb)):
        cumul += no_of_substitutions_comb[i]
        swap_thresholds.append(cumul)
        cumul += no_of_substitutions_seq[i]
        swap_thresholds.append(cumul)
    while cumul < desired_minimum_known_bytes + 1:
        cumul += no_of_substitutions_comb[-1]
        swap_thresholds.append(cumul)
        cumul += no_of_substitutions_seq[-1]
        swap_thresholds.append(cumul)

    swap_threshold_current_index = 0

    # --------------------- PRÉPARATION DE LA PREMIÈRE ITÉRATION --------------------------
    initial_min_freq = initial_min_freq_comb
    initial_ratio_threshold_bytes = initial_ratio_threshold_bytes_comb
    initial_ratio_threshold_fr = initial_ratio_threshold_fr_comb

    current_min_freq = initial_min_freq_comb
    current_ratio_threshold_bytes = initial_ratio_threshold_bytes_comb
    current_ratio_threshold_fr = initial_ratio_threshold_fr_comb

    min_min_freq = min_min_freq_comb
    min_ratio_threshold_bytes = min_ratio_threshold_bytes_comb
    min_ratio_threshold_fr = min_ratio_threshold_fr_comb

    min_freq_decrement = min_freq_decrement_comb
    ratio_threshold_decrement = ratio_threshold_decrement_comb

    freq_decrement_per_dimension = freq_decrement_per_dimension_comb
    ratio_decrement_per_dimension = ratio_decrement_per_dimension_comb

    dimensions = dimensions_comb

    matrices_bytes = matrices_bytes_comb
    matrices_fr = matrices_fr_comb

    nombre_bytes_connus_initial = len(bytes_connus)

    excluded_substitutions = [[False for _ in range(256)] for _ in range(256)]

    # Ce paramètre permet de réinitialiser un certain nombre de fois fois les substitutions bloquées avant de terminer l'algorithme si jamais on n'a pas trouvé assez de symboles.
    reset_excluded_substitutions = 0

    # À partir de combien de substitutions on fait la longue vérification de si la substitution est fiable
    exclude_substitutions_at = 1
    exclude_substitutions = False

    # À partir de combien de substitutions on accepte de substituter des caractères "rares" (=risqués) comme les majuscules, apostrophes, etc.
    # On ne peut pas trop monter cette limite sinon notre algorithme commence à faire des erreurs!
    exclude_rare_chars_until = 90
    exclude_rare_chars = True

    global possible_chars_in_word
    possible_chars_in_word = set(possible_chars_in_word)

    # Ouvrir le dictionnaire de la langue française "word_probabilities_cleansed.txt".
    global fr_dict
    fr_dict = set()
    with open("word_probabilities_cleansed.txt", "r", encoding="utf-8") as f:
        for word in f:
            word = word.strip()
            fr_dict.add(word)
            if word[-1].isalpha():
                # On considère qu'un mot peut se terminer par un point ou une virgule
                fr_dict.add(word + ",")
                fr_dict.add(word + ".")

    """ # Ouvrir un second dictionnaire de la langue française "liste.de.mots.francais.frgut.txt"
  with open("liste.de.mots.francais.frgut.txt", "r", encoding="utf-8") as f:
      for word in f:
          word = word.strip()
          fr_dict.add(word)
          fr_dict.add(word + ",")
          fr_dict.add(word + ".") """

    # -------------------- ITÉRATION DES SUBSTITUTIONS --------------------------
    while (
            current_min_freq >= min_min_freq
            and current_ratio_threshold_bytes >= min_ratio_threshold_bytes
            and current_ratio_threshold_fr >= min_ratio_threshold_fr
    ):
        substitutions_made = True
        while substitutions_made:
            substitutions_made = False
            for dimension in dimensions:
                # print(f"Début des substitutions avec n-grammes de dimension {dimension}")
                matrice_bytes = matrices_bytes[dimension - 1]

                matrice_fr = matrices_fr[dimension - 1]

                # Adjust thresholds based on dimension
                adjusted_min_freq = max(
                    current_min_freq - (dimension - 1) * freq_decrement_per_dimension,
                    min_min_freq
                )
                adjusted_ratio_threshold_bytes = max(
                    current_ratio_threshold_bytes - (dimension - 1) * ratio_decrement_per_dimension,
                    min_ratio_threshold_bytes
                )
                adjusted_ratio_threshold_fr = max(
                    current_ratio_threshold_fr - (dimension - 1) * ratio_decrement_per_dimension,
                    min_ratio_threshold_fr
                )

                # Perform substitutions
                substitutions_before = len(bytes_connus)
                perform_substitution(
                    matrice_bytes,
                    matrice_fr,
                    dimension,
                    adjusted_min_freq,
                    adjusted_ratio_threshold_bytes,
                    adjusted_ratio_threshold_fr,
                    char_probabilities,
                    byte_probabilities,
                    excluded_substitutions,
                    exclude_substitutions,
                    exclude_rare_chars,
                    consecutive_3_bytes,
                    encoded_bytes
                )
                substitutions_after = len(bytes_connus)
                if len(bytes_connus) - nombre_bytes_connus_initial >= exclude_rare_chars_until:
                    exclude_rare_chars = False
                if len(bytes_connus) - nombre_bytes_connus_initial >= exclude_substitutions_at:
                    exclude_substitutions = True
                if substitutions_after - nombre_bytes_connus_initial >= swap_thresholds[swap_threshold_current_index]:
                    break

                if substitutions_after > substitutions_before:
                    substitutions_made = True
                    # Recommencer depuis la première dimension pour prendre en compte les nouvelles substitutions
                    # Tout en remontant les seuils
                    current_min_freq = initial_min_freq
                    current_ratio_threshold_bytes = initial_ratio_threshold_bytes
                    current_ratio_threshold_fr = initial_ratio_threshold_fr
                    break
        # Vérifier si le nombre de bytes connus est suffisant
        if len(bytes_connus) >= desired_minimum_known_bytes:
            print(f"Nombre de symboles connus suffisant atteint: {len(bytes_connus)} symboles.")
            break
        else:
            if current_min_freq == min_min_freq and current_ratio_threshold_bytes == min_ratio_threshold_bytes and current_ratio_threshold_fr == min_ratio_threshold_fr:
                print("Seuils minimaux atteints, mais nombre de symboles connus insuffisant.")
                if exclude_substitutions and len(bytes_connus) - nombre_bytes_connus_initial < 20:
                    exclude_substitutions = False
                    exclude_substitutions_at = len(bytes_connus) - nombre_bytes_connus_initial + 2
                    excluded_substitutions = [[False for _ in range(256)] for _ in range(256)]
                    print(
                        "On a repoussé la limite d'exclusion de substitutions car on n'avait pas atteint 20 substitutions")
                    continue
                elif exclude_rare_chars:
                    print(
                        "On a exclu les caractères rares, mais on n'a pas trouvé assez de substitutions. On recommence sans les exclure.")
                    exclude_rare_chars = False
                    continue
                elif reset_excluded_substitutions > 0:
                    print("On réinitialise les substitutions bloquées pour trouver de nouvelles substitutions.")
                    reset_excluded_substitutions -= 1
                    excluded_substitutions = [[False for _ in range(256)] for _ in range(256)]
                    continue
                else:
                    break

            # Ajuster les seuils globaux
            current_min_freq = max(current_min_freq - min_freq_decrement, min_min_freq)
            current_ratio_threshold_bytes = max(
                current_ratio_threshold_bytes - ratio_threshold_decrement, min_ratio_threshold_bytes
            )
            current_ratio_threshold_fr = max(
                current_ratio_threshold_fr - ratio_threshold_decrement, min_ratio_threshold_fr
            )

    known_chars = set()
    for curr_char in key:
        if curr_char is not None:
            known_chars.add(curr_char)

    unknown_chars = set()
    all_chars = text_to_symbols(encoded_bytes)
    for curr_char in all_chars:
        if not curr_char in known_chars:
            unknown_chars.add(curr_char)
    all_groups = capture_groups(start_str=r'[^ ]? [^ ]?', n_bytes_min=2, n_bytes_max=6, end_str=r'[^ ]? [^ ]?',
                                encoded_bytes=encoded_bytes, key=key, include_start_and_end=True)

    unknown_chars = set(curr_char for curr_char in unknown_chars if curr_char in possible_chars_in_word)

    # Les indices des mots dans all_groups pour chaque byte si le byte est le seul qui est inconnu dans le mot
    groups_per_unknown_byte = [[] for _ in range(256)]
    for i in range(len(all_groups)):
        curr_group = all_groups[i]
        # Un groupe qui commence par une string et finit par une string. On veut ajouter i dans groups_per_byte si le seul byte inconnu du groupe est dans unknown_bytes.
        unknown_bytes_in_group = [curr_byte for curr_byte in curr_group if
                                  (isinstance(curr_byte, int) and key[curr_byte] is None)]
        if len(unknown_bytes_in_group) == 1:
            groups_per_unknown_byte[unknown_bytes_in_group[0]].append(i)

    # On itère sur chaque byte qui a des groupes dont il est le seul sans substitution
    for byte in range(len(groups_per_unknown_byte)):
        groups = groups_per_unknown_byte[byte]
        chars_possible_and_frequencies = {}
        if len(groups) != 0:
            # Il y a des mots de longueur 2 à 6 bytes dont byte est le seul inconnu.
            # On essaie de trouver un remplacement pour ce byte qui forme un mot
            for group_index in groups:
                chars_possible = verifier_substitutions_possibles(all_groups[group_index][1:-1], byte, unknown_chars,
                                                                  all_groups[group_index][0],
                                                                  all_groups[group_index][-1])
                if chars_possible is not None:
                    for char_possible in chars_possible:
                        if char_possible in chars_possible_and_frequencies:
                            chars_possible_and_frequencies[char_possible] += 1
                        else:
                            chars_possible_and_frequencies[char_possible] = 1
            # On choisit la plus haute fréquence
            max_char = None
            max_frequency = -1
            for char, frequency in chars_possible_and_frequencies.items():
                if frequency > max_frequency:
                    max_char = char
                    max_frequency = frequency
            if max_char is not None:
                key[byte] = max_char
                # print("FOUND WORD COMPLETION WITH CHAR " + max_char)

                known_chars.add(max_char)
                unknown_chars.remove(max_char)
                # On doit recapturer les groupes parce qu'on va peut-être en trouver plus maintenant qu'on a une nouvelle substitution
                all_groups = capture_groups(start_str=r'[^ ]? [^ ]?', n_bytes_min=2, n_bytes_max=6,
                                            end_str=r'[^ ]? [^ ]?', encoded_bytes=encoded_bytes, key=key,
                                            include_start_and_end=True)
                # Les indices des mots dans all_groups pour chaque byte si le byte est le seul qui est inconnu dans le mot
                groups_per_unknown_byte = [[] for _ in range(256)]
                for i in range(len(all_groups)):
                    curr_group = all_groups[i]
                    # Un groupe qui commence par une string et finit par une string. On veut ajouter i dans groups_per_byte si le seul byte inconnu du groupe est dans unknown_bytes.
                    unknown_bytes_in_group = [curr_byte for curr_byte in curr_group if
                                              (isinstance(curr_byte, int) and key[curr_byte] is None)]
                    if len(unknown_bytes_in_group) == 1:
                        groups_per_unknown_byte[unknown_bytes_in_group[0]].append(i)

    # Écrire decoded_text dans un fichier, en n'oubliant pas de remettre les caractères spéciaux \n, \r, \ufeff.
    decoded_text = ""
    for byte in encoded_bytes:
        if key[byte] is not None:
            decoded_text += key[byte].replace('&', '\n').replace('@', '\r').replace('<', '\ufeff')
        else:
            decoded_text += '~'

    # Complète les mots inconnus avec des substitutions possibles
    M = complete_unknown_words(decoded_text, fr_dict)

    return M


def verify_substitution_in_text(byte, char, key, text):
    '''
  Cette fonction trouve des mots de 1 à 8 bytes qui contiennent le byte donné et
  vérifie si substituer le byte par le char bénificie au texte.

  Retourne un tuple (Bool, String). Bool = True si la substitution est bonne, False sinon.
      Si on trouve une meilleure substitution, on la retourne comme 2e élément du tuple.
  '''
    known_chars = set()
    for curr_char in key:
        if curr_char is not None:
            known_chars.add(curr_char)

    unknown_chars = set()
    all_chars = text_to_symbols(text)
    for curr_char in all_chars:
        if not curr_char in known_chars:
            unknown_chars.add(curr_char)

    # On enlève de unknown_chars tous les caractères qui ne sont pas possibles dans les mots français
    global possible_chars_in_word
    unknown_chars = set(curr_char for curr_char in unknown_chars if curr_char in possible_chars_in_word)

    substitution_score = 0

    other_substitutions_possible = unknown_chars.copy()

    # Trouver tous les groupes de mots de 1 à 8 bytes qui contiennent le byte donné et dont seulement le byte donné est inconnu.
    groups = capture_groups(start_str='[^ ]? [^ ]?', n_bytes_min=1, n_bytes_max=8, end_str='[^ ]? [^ ]?',
                            encoded_bytes=text, key=key, include_start_and_end=True)
    no_of_words_found = 0
    no_of_occurences = 0
    for group in groups:
        # Vérifier si le byte donné est dans le groupe
        if byte in group:
            no_of_occurences += 1
            start = None
            end = None
            if isinstance(group[0], str):
                start = group[0]
            if isinstance(group[-1], str):
                end = group[-1]
            group = [b for b in group if isinstance(b, int)]
            # Tous les autres bytes du groupe devraient avoir une substitution connue dans la clé
            if not all(key[b] is not None for b in group if b != byte):
                continue

            # Si le groupe est un mot français, aucun problème
            if verifier_substitution(group, byte, char, start, end):
                no_of_words_found += 1
                substitution_score += 1
                continue
            # Si le groupe n'est pas un mot français, on doit vérifier s'il y avait un mot français possible avant la substitution.
            # On doit donc vérifier si le groupe est un mot français si on remplace le byte par n'importe quel char de unknown_chars
            char_substitutions = verifier_substitutions_possibles(group, byte, unknown_chars, start, end)
            if char_substitutions is not None:
                no_of_words_found += 1
                # Il y avait une substitution possible qui formait un mot français, et maintenant il n'y en a plus.
                # La substitution n'est donc pas fiable.
                key[byte] = "~"
                print("Substitution non fiable de '" + char + "' dans '" + start + "|" + ''.join(
                    key[byte] for byte in group) + "|" + end + "' car substitution par '" + next(
                    iter(char_substitutions)) + "' était possible.")
                key[byte] = None
                substitution_score -= 1
                # Enlever les substitutions qui ne sont plus possibles si le groupe a une longueur de 2 bytes et plus
                if len(group) >= 2:
                    other_substitutions_possible.intersection_update(char_substitutions)

    # On a trouvé d'autres substitutions qui semblent meilleures
    if (substitution_score < 0 and no_of_words_found > 2):
        # S'il y a seulement une substitution possible, on la prend
        if len(other_substitutions_possible) == 1:
            char = other_substitutions_possible.pop()
            return (True, char)
        # Si on ne peut pas remplacer la substitution par autre chose, on la bloque
        return (False, None)

    # Aucun problème trouvé, la substitution semble fiable.
    return (True, None)


def verifier_substitution(mot_bytes, byte_a_substituer, caractere_remplacement, start, end):
    """
  Vérifie si la substitution du byte spécifié par un caractère donné
  donne un mot valide selon le dictionnaire.
  """
    if ' ' in start:
        if start[-1] == ' ':
            start = ""
        else:
            start = start[-1]
    if ' ' in end:
        if end[0] == ' ':
            end = ""
        else:
            end = end[0]
    if ' ' in caractere_remplacement:
        # On doit séparer le mot en plusieurs parce qu'on ajoute un espace.
        # La substitution est valide seulement si tous les mots formés sont valides.
        curr_mot = start
        # Le char à substituer est le caractère espace " "
        if len(caractere_remplacement) == 1:
            for byte in mot_bytes:
                if byte == byte_a_substituer:
                    if not curr_mot in fr_dict:
                        return False
                    curr_mot = ""
                else:
                    curr_mot += key[byte]
            if not (curr_mot + end) in fr_dict:
                return False
        # Le char à substituer est de forme " x"
        elif caractere_remplacement[0] == ' ':
            for byte in mot_bytes:
                if byte == byte_a_substituer:
                    if not curr_mot in fr_dict:
                        return False
                    curr_mot = caractere_remplacement[1]
                else:
                    curr_mot += key[byte]
            if not (curr_mot + end) in fr_dict:
                return False
        # Le char à substituer est de forme "x "
        else:
            for byte in mot_bytes:
                if byte == byte_a_substituer:
                    if not (curr_mot + caractere_remplacement[0]) in fr_dict:
                        return False
                    curr_mot = ""
                else:
                    curr_mot += key[byte]
            if not (curr_mot + end) in fr_dict:
                return False
        return True

    # Le char à substituer ne contient pas d'espace.
    else:
        # Construire le mot en remplaçant le byte
        mot = "".join(
            key[current_byte] if current_byte != byte_a_substituer else caractere_remplacement
            for current_byte in mot_bytes
        )
        mot = start + mot + end
        # Vérifie si le mot construit est dans le dictionnaire
        if mot in fr_dict:
            # print("Mot trouvé: " + mot)
            return True
        return False


def verifier_substitutions_possibles(mot_bytes, byte_a_substituer, caracteres_possibles, start, end):
    """
  Vérifie si la substitution du byte spécifié par un des caractères
  possibles donne un mot du dictionnaire.
  """
    chars_found = set()
    for caractere in caracteres_possibles:
        if verifier_substitution(mot_bytes, byte_a_substituer, caractere, start, end):
            chars_found.add(caractere)

    # Si chars_found est vide, il n'y a pas de substitution possible
    if len(chars_found) == 0:
        return None

    # Retourner chars_found
    return chars_found


# On veut vérifier si la substitution de byte par space_substitution est fiable
# On parcourt tout le texte à la recherche de 2 bytes de suite qui comportent des espaces, 
# ce qui indiquerait une erreur sauf dans le cas où une seule lettre peut être considérée comme un mot (ex.: " a " ou " à ")
def validate_space_substitution(byte, space_substitution, key, encoded_bytes):
    global fr_dict
    space_bytes = set()

    key = key[:]
    for i in range(len(key)):
        if key[i] is not None and ' ' in key[i]:
            space_bytes.add(i)
    key[byte] = space_substitution
    space_bytes.add(byte)

    no_of_errors = 0
    # Trouver les bytes adjacents à byte qui contiennent un espace
    no_of_occurences = 0
    for i in range(1, len(encoded_bytes) - 1):
        if encoded_bytes[i] == byte:
            no_of_occurences += 1
            prev_byte = encoded_bytes[i - 1]
            next_byte = encoded_bytes[i + 1]
            # Vérifier si prev_byte et next_byte sont des espaces
            if prev_byte in space_bytes:
                group = key[prev_byte] + space_substitution
                if '  ' in group:
                    # On a trouvé un groupe de 2 espaces, ce n'est pas normal
                    no_of_errors += 1
                    continue
                words = group.split()
                if len(words) == 2:
                    # ' x' ' y' -> ['x', 'y']
                    if group[0] == ' ':
                        # Le mot à vérifier est words[0]
                        if not (words[0] == 'à' or words[0] == 'a'):
                            no_of_errors += 1
                    # 'x ' 'y ' -> ['x', 'y']
                    else:
                        # Le mot à vérifier est words[1]
                        if not (words[1] == 'à' or words[1] == 'a'):
                            no_of_errors += 1
                    continue
                else:
                    # ' x' 'y ' -> ['xy']
                    # On vérifie si le mot de 2 lettres formé est dans le dictionnaire
                    if words[0] not in fr_dict:
                        no_of_errors += 1

            if next_byte in space_bytes:
                group = space_substitution + key[next_byte]
                if '  ' in group:
                    # On a trouvé un groupe de 2 espaces, ce n'est pas normal
                    no_of_errors += 1
                    continue
                words = group.split()
                if len(words) == 2:
                    # ' x' ' y' -> ['x', 'y']
                    if group[0] == ' ':
                        # Le mot à vérifier est words[0]
                        if not (words[0] == 'à' or words[0] == 'a'):
                            no_of_errors += 1
                    # 'x ' 'y ' -> ['x', 'y']
                    else:
                        # Le mot à vérifier est words[1]
                        if not (words[1] == 'à' or words[1] == 'a'):
                            no_of_errors += 1
                    continue
                else:
                    # ' x' 'y ' -> ['xy']
                    # On vérifie si le mot de 2 lettres formé est dans le dictionnaire
                    if words[0] not in fr_dict:
                        no_of_errors += 1
    return no_of_errors / no_of_occurences


def complete_unknown_words(decoded_text, fr_dict):
    print("Complétion des mots inconnus...")

    length_to_words = defaultdict(list)
    for word in fr_dict:
        length_to_words[len(word)].append(word.lower())

    new_text = decoded_text

    # Trouver des mots contenant au moins un tilde '~' et gérer les caractères français et les apostrophes
    word_pattern = re.compile(r"\b[a-zA-ZÀ-ÿ']*~[a-zA-ZÀ-ÿ']*\b")

    # Suivre les remplacements pour la cohérence
    replacements = {}

    # Itérer sur chaque mot contenant au moins un tilde
    for word_match in word_pattern.finditer(decoded_text):
        word = word_match.group().lower()  # Convertir en minuscules pour la correspondance
        start, end = word_match.start(), word_match.end()
        word_length = len(word)

        # Vérifier si nous avons déjà vu ce motif
        if word in replacements:
            new_text = new_text[:start] + replacements[word] + new_text[end:]
            print(f"Réutilisation de la substitution précédente : '{word}' → '{replacements[word]}'")
            continue

        # Construire un motif regex pour correspondre aux candidats
        # Le rendre plus flexible en permettant des variations d'accents
        pattern = '^' + re.escape(word).replace('\\~', '[a-zA-ZÀ-ÿ]') + '$'

        if word_length not in length_to_words:
            print(f"Aucun candidat de longueur {word_length} pour le mot '{word}'.")
            continue

        # Trouver les mots candidats qui correspondent au motif
        candidates = [
            candidate for candidate in length_to_words[word_length]
            if re.match(pattern, candidate, re.IGNORECASE)
        ]

        if not candidates:
            print(f"Aucun candidat trouvé pour le mot '{word}'.")
            continue

        # Utiliser difflib pour trouver la correspondance la plus proche parmi les candidats
        base_word = word.replace('~', '')

        # Ajuster le seuil en fonction du ratio de caractères connus
        known_char_ratio = len(base_word) / len(word)
        cutoff = max(0.6, known_char_ratio * 0.8)  # Seuil dynamique basé sur les caractères connus

        best_match = get_close_matches(base_word, candidates, n=1, cutoff=cutoff)

        if best_match:
            best_candidate = best_match[0]
            print(f"Remplacement de '{word}' par '{best_candidate}'")
            replacements[word] = best_candidate
            # Remplacer le mot dans le texte tout en préservant la casse d'origine
            if word.isupper():
                best_candidate = best_candidate.upper()
            elif word[0].isupper():
                best_candidate = best_candidate.capitalize()
            new_text = new_text[:start] + best_candidate + new_text[end:]
        else:
            print(f"Aucun match approprié trouvé pour le mot '{word}'.")

    return new_text

