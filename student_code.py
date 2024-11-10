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
  #print("Loading CSV")
  stats_ngram_1 = loadStatsNgram('freq_ngram_1.csv')
  stats_ngram_2 = loadStatsNgram('freq_ngram_2.csv')
  stats_ngram_3 = loadStatsNgram('freq_ngram_3.csv')
  stats_ngram_4 = loadStatsNgram('freq_ngram_4.csv')
  stats_ngram_5 = loadStatsNgram('freq_ngram_5.csv')
  stats_ngram_6 = loadStatsNgram('freq_ngram_6.csv')
  #print("Parsing Cypher")
  C_cutBlock = cutCypherText(C)
  #c_analysis = ngrams_count_plus(C_cutBlock, 2,5)

  '''
  print("Counting ngram_1")
  C_mono_Count = ngrams_count(C_cutBlock, 1,5, 256)
  C_mono_Freq = []

  print("Analyzing ngram-1 Frequency Data")
  for x in C_mono_Count:
     C_mono_Freq.append(checkFrequency(C_cutBlock, x[0], x[1], 1, False))

  print("Counting complete")
  for x in C_mono_Freq:
     print(x)

  print("\n\n\n")
  print("Counting ngram_2")
  C_bi_Count = ngrams_count(C_cutBlock, 2,5, 300)
  C_bi_Freq = []

  print("Analyzing ngram-2 Frequency Data")
  for x in C_bi_Count:
     C_bi_Freq.append(checkFrequency(C_cutBlock, x[0], x[1], 2, False))

  print("Counting complete")
  for x in C_bi_Freq:
     print(x)

  print("\n\n\n")
  '''
  '''
  cypher_repeat_1_mostFrequent = []


  print("-- Mono-Bi 1 repeat")
  mono_b1 = []
  mono_b1.append(checkRepeat(C_cutBlock,1,0,-1, True,0, False))
  mono_b1.append(checkRepeat(C_cutBlock,1,1,-1, True,0, False))
  mono_b1.append(checkRepeat(C_cutBlock,1,2,-1, True,0, False))
  mono_b1.append(checkRepeat(C_cutBlock,1,3,-1, True,0, False))
  mono_b1.append(checkRepeat(C_cutBlock,1,4,-1, True,0, False))
  mono_b1.append(checkRepeat(C_cutBlock,1,5,-1, True,0, False))
  mono_b1.append(checkRepeat(C_cutBlock,1,6,-1, True,0, False))
  mono_b1.append(checkRepeat(C_cutBlock,1,7,-1, True,0, False))

  print("-- Mono-Bi 2 repeat")
  mono_b2 = []
  mono_b2.append(checkRepeat(C_cutBlock,2,0,-1, True,0, False))
  mono_b2.append(checkRepeat(C_cutBlock,2,1,-1, True,0, False))
  mono_b2.append(checkRepeat(C_cutBlock,2,2,-1, True,0, False))
  mono_b2.append(checkRepeat(C_cutBlock,2,3,-1, True,0, False))
  mono_b2.append(checkRepeat(C_cutBlock,2,4,-1, True,0, False))
  mono_b2.append(checkRepeat(C_cutBlock,2,5,-1, True,0, False))
  mono_b2.append(checkRepeat(C_cutBlock,2,6,-1, True,0, False))
  mono_b2.append(checkRepeat(C_cutBlock,2,7,-1, True,0, False))

  print("-- Mono-Bi 3 repeat")
  checkRepeat(C_cutBlock,3,0,-1, True,0, False)
  checkRepeat(C_cutBlock,3,1,-1, True,0, False)
  checkRepeat(C_cutBlock,3,2,-1, True,0, False)
  checkRepeat(C_cutBlock,3,3,-1, True,0, False)
  checkRepeat(C_cutBlock,3,4,-1, True,0, False)
  checkRepeat(C_cutBlock,3,5,-1, True,0, False)
  checkRepeat(C_cutBlock,3,6,-1, True,0, False)
  checkRepeat(C_cutBlock,3,7,-1, True,0, False)

  print("-- Mono-Bi 4 repeat")
  checkRepeat(C_cutBlock,4,0,-1, True,0, False)
  checkRepeat(C_cutBlock,4,1,-1, True,0, False)
  checkRepeat(C_cutBlock,4,2,-1, True,0, False)
  checkRepeat(C_cutBlock,4,3,-1, True,0, False)
  checkRepeat(C_cutBlock,4,4,-1, True,0, False)
  checkRepeat(C_cutBlock,4,5,-1, True,0, False)
  checkRepeat(C_cutBlock,4,6,-1, True,0, False)
  checkRepeat(C_cutBlock,4,7,-1, True,0, False)


  print("-- Mono-Bi 5 repeat")
  checkRepeat(C_cutBlock,5,0,-1, True,0, False)
  checkRepeat(C_cutBlock,5,1,-1, True,0, False)
  checkRepeat(C_cutBlock,5,2,-1, True,0, False)
  checkRepeat(C_cutBlock,5,3,-1, True,0, False)
  checkRepeat(C_cutBlock,5,4,-1, True,0, False)
  checkRepeat(C_cutBlock,5,5,-1, True,0, False)
  checkRepeat(C_cutBlock,5,6,-1, True,0, False)
  checkRepeat(C_cutBlock,5,7,-1, True,0, False)

  '''
  #print(wordCountTest(C_cutBlock, 2, 0, 30))

  #corp = [[1],[2],[3],[2],[3],[4],[3],[4],[5]]
  #w = wordCountTest(corp, 2, 0, 30)
  #print(w)

 # quit()
  
  #print("WordCount Test")
  wordCount = []
  wordCount.append(wordCountTest(C_cutBlock, 1, 0))
  wordCount.append(wordCountTest(C_cutBlock, 2, 0))
  wordCount.append(wordCountTest(C_cutBlock, 3, 0))
  wordCount.append(wordCountTest(C_cutBlock, 4, 0))
  wordCount.append(wordCountTest(C_cutBlock, 5, 0))
  wordCount.append(wordCountTest(C_cutBlock, 6, 0))
  #wordCount.append(wordCountTest(C_cutBlock, 7, 0, 100))
  #wordCount.append(wordCountTest(C_cutBlock, 8, 0, 100))
  #wordCount.append(wordCountTest(C_cutBlock, 9, 0, 100))
  #wordCount.append(wordCountTest(C_cutBlock, 10, 0, 100))
  #wordCount.append(wordCountTest(C_cutBlock, 11, 0, 100))
  #wordCount.append(wordCountTest(C_cutBlock, 12, 0, 100))
  #for x in wordCount:
  #   print(x[:30])

  dictionary_1 = {}

  repeatCount = []

  # find ** in single alphabet descending order. very recursive. very expensive
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

        if maxlen == 16:
          print("we might have _")
          addToDict(dictionary_1, str(x[0][0]), ' ')
        elif maxlen == 38:
          print("we might have *")
          addToDict(dictionary_1, str(x[0][0]), '*')
        else:
           repeatCount.append([str(x[0][0]), total])
    
  #print(repeatCount)

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
        # this one is correct guess
        #elif index == 1 : addToDict(dictionary_1, str(x[0]), '\r')
        #elif index == 2 : addToDict(dictionary_1, str(x[0]), '*')
        #else : print("repeatcount exceeding 3 error please check ")
        break
    

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

  '''
  # we didnt catch all eol tho. we missing the in-paragraph '. '
  if (eol_period != -1):

    # ?. using only EOL period is hard to find this.    
    eol_count = countEOL(C_cutBlock, eol_period, 1,  1)
    #print(eol_count)
    eol_sorted = sortEOL(eol_count)
    print(eol_sorted)

    index = 0
    for x in eol_sorted:
      if str(x[0]) in dictionary_1: continue
      if index == 0: addToDict(dictionary_1, str(x[0]), '')
      #elif index == 1: addToDict(dictionary_1, str(x[0]), 'nt')
      #elif index == 2: addToDict(dictionary_1, str(x[0]), 'le')
      else: break
      index += 1

    # ?. using only EOL period is hard to find this.    
    eol_count = countEOL(C_cutBlock, eol_period, 1,  -1)
    #print(eol_count)
    eol_sorted = sortEOL(eol_count)
    print(eol_sorted)

    index = 0
    for x in eol_sorted:
      if str(x[0]) in dictionary_1: continue
      if index == 0: addToDict(dictionary_1, str(x[0]), '')
      #elif index == 1: addToDict(dictionary_1, str(x[0]), 'nt')
      #elif index == 2: addToDict(dictionary_1, str(x[0]), 'le')
      else: break
      index += 1
  '''
  '''
  ,
  ,_
  e,
  s,


  CheckRepeat strat
  use the difference between checkRepeat x and checkRepeat x+1 to find some stuff.
  for ngram_1 the most popular recurring word is '_',
  for ngram_2 the most popular is 'e_'
  but from previous experiences, this combination is very likely to get masked. There is probably a dozen combination of '?_'.

  So, let's target the ngram_3 and beyond, where the most popular word is 'que'.
  From the list of most frequent ngram_2, we know that '_q', 'qu', 'ue', 'e_' are all very popular (all 4 are among the first 25 most commons).
  Considering the logic of encoding algorithm, where it prioritize encoding 2 word with 1 symbol, we can reasonably assume that:
  ' que' will always be encoded in 2 symbol.
  'que ' will always be encoded in 2 symbol.

  que does not repeat at 0 interval

  S check
  this might works 1/10 time. but result is not accurate. FAIL

  arr = np.unique(cypher_repeat_1_mostFrequent, return_counts=True)
  sort = np.flip(arr[1].argsort())
  # if the most recurring symbol has at least 5/8 appearance
  # and if it lost the 2nd position
  # and if it lost 0th position
  #print(cypher_repeat_1_mostFrequent)
  #print(arr)
  #print(sort)
  #if (arr[1][sort[0]] >= 5 and cypher_repeat_1_mostFrequent[0] != arr[0][sort[0]] and cypher_repeat_1_mostFrequent[2] != arr[0][sort[0]]):
  if (arr[1][sort[0]] >= 5):
     #print("WE HAVE A S CANDIDATE "+ str(arr[0][sort[0]]) )
     addToDict(dictionary_1, str(arr[0][sort[0]]), 'qu')


  UPDATE: MY ALGORITHM WASNT WORKING AS INTENDED. AFTER FIX, ALL PREV CONCLUSIONS ARE USELESS
  '''

  '''
  NEW CHECKREPEAT STRAT






  firstIndex = -1

  if len(mono_b2[0]) > 0 and mono_b2[0][0][0][0] == mono_b2[0][0][0][1]:
    firstIndex = 0

    if len(mono_b2[2]) > 0 and mono_b2[0][0][0][0] == mono_b2[2][0][0][0]:
      # we have a star
      #addToDict(dictionary_1, str(mono_b2[0][0][0][0]), '*')
      # this works reliably.
      # but, in case the text has no *, this algo might mistake \r\n with *. need finetuning

      # now we check for double space
      firstIndex += 1

    if len(mono_b2[0]) >= firstIndex + 1 and mono_b2[0][firstIndex][0][0] == mono_b2[0][firstIndex][0][1]:
        #if len(mono_b2[1]) > 0 and mono_b2[0][0][0][0] == mono_b2[2][0][0][0]:
          # we have a double space
          #addToDict(dictionary_1, str(mono_b2[0][firstIndex][0][0]), ' ')
          addToDict(dictionary_1, str(mono_b2[0][firstIndex][0][0]), ' ')
          print("addtodict "+str(mono_b2[0][firstIndex][0][0]))
       

  '''
  '''
  we know that ll and ss are certainly to get shadowed.
  In fact, we know there are 115 mono and 141 bi
  bi chara selection might vary at small scale
  but the top ones are certainly not influenced so long as we have a large enough sample
    
  We know! that some alphabet that have chances of repeating (ngram_1 minOccurence == 0)
  see '  ' 'ee' 'ss' 'nn' 'tt' 'ii' 'aa' 'rr' 'oo' 'll' 'dd' etc
  but when transformed into bigram, their repeat chance decreased drastically
  we only have a '    ' at rank 264, and 'IIII' at order 482... and they are way beyond the bigram 141 range so its rare to see them
  So, we can conclude that, if we have a word that immediately repeats, then its very likely to be a monogram.
  '''


  '''
  naiveRange = math.factorial(256)

  possibilityRange = math.factorial(141)*math.factorial(115)
  print("Possibility Range: "+str(possibilityRange))
  print("Possibility Range reduction to  ["+str(possibilityRange / naiveRange)+"]")
  print("Counting possible monogram...")
  counter = 0

  list_repeat_cipher = []
  for x in C_mono_Freq:
     if x[4] == 0:
        counter += 1
        list_repeat_cipher.append(x)
        #print("possible monogram : "+str(x))
  print("Counting Complete. possible monogram count ["+str(counter)+"]")


  list_repeat_ref = []
  for x in stats_ngram_1:
     if x[4] == 0:
        list_repeat_ref.append(x)
  '''

  '''
  what can this counter tells us ?
  it can tells us that, among the 47 monograms that can repeat, how many did not appear or, hidden.

  lets take all repeat bigram that are most likely to appear (in frequency order, frequency decrease by around half at each rank gap)
  1st rank : ll(r70) ss(r78)
  2nd rank : mm(r133) nn(r137)
  3rd rank : tt(r180)
  4th rank : rr(r213) pp(r238) ff(r249) '  ' (we will not consider these)

  these above, especially from rank 1 to rank 3, are very likely to be hidden. 
  But since the algorithm is made to hide in order of appearance frequency, and since it must include monogram,
  then it cannot hide the very low-frequency repeat monograms.

  anyway. if we get at least A repeat-monogram count, that means 
  possibilityRange = (141)! * (115-A)! * (47*46*45....47-A)!
  
  ...still too much for brute force

  repeatRange = 1
  for x in range(counter):
     repeatRange *= (47-x)
    
  possibilityRange_reduce1 = math.factorial(141)*math.factorial(115-counter)*repeatRange
  print("Possibility Range reduced by repeat factor : "+str(possibilityRange_reduce1))
  print("Possibility Range reduction to ["+str( possibilityRange_reduce1 / possibilityRange)+"]")


  lets first bruteforce replace the first 50 ngrams
  '''
  





  #print("Building ngram-2 Dictionary")
  #var = buildNgramDictionary(2, [stats_ngram_4], C_mono_Freq, 20, True)
  #var = buildNgramDictionary(1, [stats_ngram_2], C_mono_Freq, 141, False)

  #dictionary_1 = var[0]

  #for x in var[1]:
  # dictionary_1.update(x)

  #print(dictionary_2)
  #print(dictionary_1)

  #addToDict(dictionary_1, str(C_mono_Freq[0][0][0]), 'e ')
  '''  
  next = False
  for x in list_repeat_cipher:
    next = False
    for y in list_repeat_ref:
        det = y[3]*0.05
        if (x[4] == y[4] and abs(x[3] - y[3]) < det):
            print("Adding to dictionary : ["+str(x[0][0])+"] -> ["+str(y[0][0])+"]")     
            addToDict(dictionary_1, str(x[0][0]), str(y[0][0]))
            next = True
        if next: continue
    if next: continue
  '''

  '''
  Trying to match bigram to 4gram. failed
  print("Adding to dictionary : ["+str(C_bi_Freq[0][0][0])+"] -> ["+str(stats_ngram_4[0][0][:2])+"]")    
  print("Adding to dictionary : ["+str(C_bi_Freq[0][0][1])+"] -> ["+str(stats_ngram_4[0][0][2:])+"]")    
  addToDict(dictionary_1, str(C_bi_Freq[0][0][0]), str(stats_ngram_4[0][0][:2]))
  addToDict(dictionary_1, str(C_bi_Freq[0][0][1]), str(stats_ngram_4[0][0][2:]))
  '''

  '''
  Trying to match monogram to 2gram, also failed
  print("Adding to dictionary : ["+str(C_mono_Freq[0][0][0])+"] -> ["+str(stats_ngram_2[0][0])+"]")    
  addToDict(dictionary_1, str(C_mono_Freq[0][0][0]), str(stats_ngram_2[0][0]))
  '''

  '''
  hasHit = False
  mono_index = 0
  bi_index = 0
  for x in C_mono_Freq:
    hasHit = False
    for i in range(bi_index, len(stats_ngram_2)):
      if x[4] < stats_ngram_2[i][4]: continue
      elif x[3]*1.2 < stats_ngram_2[i][3]:
          bi_index = i
          break
      elif (abs(x[3] - stats_ngram_2[i][3]) < stats_ngram_2[i][3]*0.1):
        word1 = str(x[0][0])
        word2 = stats_ngram_2[i][0]
        print("Adding to dictionary : ["+word1+"] -> ["+word2+"]")  
        addToDict(dictionary_1, word1, word2)
        bi_index = i+1
        hasHit = True
        break
    if hasHit: continue
    for i in range(mono_index, len(stats_ngram_1)):
      if x[4] < stats_ngram_1[i][4]: continue
      elif x[3]*1.2 < stats_ngram_1[i][3]:
          mono_index = i
          break
      elif (abs(x[3] - stats_ngram_1[i][3]) < stats_ngram_1[i][3]*0.1):
        word1 = str(x[0][0])
        word2 = stats_ngram_1[i][0]
        print("Adding to dictionary : ["+word1+"] -> ["+word2+"]")  
        addToDict(dictionary_1, word1, word2)
        mono_index =i+1
        hasHit = True
        break
    if hasHit: continue
  '''
    
      

  

  '''
  lets narrow it even further.
  bigram repeat chance ? this might happen.
  '  ' bigram minfreq 0 rank 528
  'II' bigram minfreq 0 rank 965/2. Lets assume first option

  bi_freq_hack = 0
  for x in C_bi_Freq:
     if int(x[4]) == 0 and x[3] > 0.1:
        bi_freq_hack += 1
        word1 = str(x[0][0])
        word2 = " "
        print("Adding to dictionary : ["+word1+"] -> ["+word2+"]")   
        addToDict(dictionary_1, word1, word2)
        break

  print("bigram hack test ["+str(bi_freq_hack)+"]")
  
  '''






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