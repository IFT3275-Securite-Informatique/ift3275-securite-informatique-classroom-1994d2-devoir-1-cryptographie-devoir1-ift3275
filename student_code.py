from crypt import load_text_from_web # type: ignore

Symboles = ['û', 'u', 'b', 'z', 'Î', '™', 'x', '%', 'r', 'h', ':', 'R', '6', '‘', '$', 'î', '5', 'È', '\r', '.', 'ç', 'y', 'ô', 'Â', '_', 'J', '…', 'N', 'T', '3', 'e', 'A', '[', ',', 'H', 'â', 'D', '0', 'M', '\n', 'ë', '4', 'C', 'ù', ']', ')', '—', '!', 'G', '/', 'ê', '«', '\ufeff', '?', 'è', '-', 'c', 'f', "'", 'º', 's', 'E', 'q', 'B', 'P', 'I', 'à', '7', 'À', ' ', 'S', 'W', 'K', '9', 'n', '»', 'k', '“', 'É', 'i', 'm', 'w', '1', '’', 'O', 'v', '•', 'Ç', '#', 'j', '*', 'U', 't', '8', 'Ê', '2', 'X', 'o', 'ï', 'Y', ';', 'a', 'F', 'V', '”', 'L', 'é', '°', 'Z', 'Q', 'g', 'p', '(', 'd', 'l', 'e ', 's ', 't ', 'es', ' d', '\r\n', 'en', 'qu', ' l', 're', ' p', 'de', 'le', 'nt', 'on', ' c', ', ', ' e', 'ou', ' q', ' s', 'n ', 'ue', 'an', 'te', ' a', 'ai', 'se', 'it', 'me', 'is', 'oi', 'r ', 'er', ' m', 'ce', 'ne', 'et', 'in', 'ns', ' n', 'ur', 'i ', 'a ', 'eu', 'co', 'tr', 'la', 'ar', 'ie', 'ui', 'us', 'ut', 'il', ' t', 'pa', 'au', 'el', 'ti', 'st', 'un', 'em', 'ra', 'e,', 'so', 'or', 'l ', ' f', 'll', 'nd', ' j', 'si', 'ir', 'e\r', 'ss', 'u ', 'po', 'ro', 'ri', 'pr', 's,', 'ma', ' v', ' i', 'di', ' r', 'vo', 'pe', 'to', 'ch', '. ', 've', 'nc', 'om', ' o', 'je', 'no', 'rt', 'à ', 'lu', "'e", 'mo', 'ta', 'as', 'at', 'io', 's\r', 'sa', "u'", 'av', 'os', ' à', ' u', "l'", "'a", 'rs', 'pl', 'é ', '; ', 'ho', 'té', 'ét', 'fa', 'da', 'li', 'su', 't\r', 'ée', 'ré', 'dé', 'ec', 'nn', 'mm', "'i", 'ca', 'uv', '\n\r', 'id', ' b', 'ni', 'bl']
occurencesSymboles = [('e ', 62680), ('s ', 51231), ('\r\n', 48488), ('t ', 35802), (' ', 34829), (' d', 32195), (', ', 30024), ('es', 29021), ('g', 26835), ('le', 26546), ('re', 25810), ('a', 25763), (' l', 25758), ('de', 25536), ('on', 24692), ('qu', 23720), ('en', 23120), ('é', 21599), ('ou', 21165), ('nt', 20647), ('c', 20206), (' p', 20024), ('ai', 20001), ('i', 19695), ('d', 19595), ('u', 18935), ('e', 17988), ('f', 17557), ('n', 17453), ('m', 17377), ('r', 17278), ('te', 16889), ('an', 16592), (' c', 16373), (' s', 16322), ('me', 16099), ('. ', 15623), ('t', 15576), (' e', 15313), ('n ', 14892), ('p', 14665), ('r ', 14534), ('ur', 14514), ('b', 14492), ('o', 14296), ('er', 14233), ('in', 14041), ('\n', 13932), ('it', 13741), (' a', 13736), ('l', 13519), ('ie', 13454), ('is', 13397), ('la', 13394), ('v', 13381), ('s', 12870), ('ra', 12724), ('h', 12665), ('il', 12646), ('et', 12577), ('ce', 12244), ('se', 12192), ('us', 12093), ('co', 11914), ('tr', 11622), ('a ', 11555), ('ne', 11540), ('-', 11498), ('x', 11332), ('un', 11005), (' m', 11000), (' q', 10976), ('pa', 10654), ('ns', 10178), ('ar', 9898), ('eu', 9835), ('au', 9813), ('u ', 9700), ("'", 9563), ('oi', 9547), ('ma', 9434), ('ti', 9285), ('y', 9139), (' t', 8996), ('ch', 8951), ('ui', 8903), ('è', 8875), ('pr', 8864), ('i ', 8849), ('ue', 8762), ('ri', 8504), ('.', 8365), ('or', 8327), (' n', 8234), ('ve', 8126), ('po', 8002), ('ut', 7795), ('ro', 7377), (' f', 7318), ('pe', 7078), ('ir', 7074), ('s,', 7028), ("'a", 6927), ('so', 6839), ('di', 6787), ('à ', 6741), ('st', 6660), ('ss', 6629), ('l ', 6628), ('ll', 6528), ('ét', 6433), (' r', 6420), ('el', 6379), ('nd', 6328), ('si', 6283), ('em', 6197), (' v', 6102), ('; ', 6053), ('at', 5888), ('j', 5859), ('e\r', 5844), ('L', 5801), ('é ', 5757), ('vo', 5689), ('ê', 5684), ("'e", 5654), ('e,', 5527), ('sa', 5466), ('mo', 5461), ('as', 5351), ('pl', 5330), ('no', 5246), ('to', 5239), ('bl', 5186), ('’', 5080), ('M', 5061), ("l'", 5039), ('C', 4985), (' à', 4957), ('s\r', 4919), (' u', 4870), ('ta', 4848), ('lu', 4787), ('I', 4774), (' i', 4771), ('li', 4702), ('rt', 4696), ('E', 4678), ('da', 4605), ('rs', 4593), ('om', 4526), (' j', 4483), ('av', 4418), (' o', 4405), ('mm', 4383), ('io', 4374), ('nc', 4367), ('z', 4321), ('je', 4317), ('fa', 4254), ('ée', 4208), (' b', 4192), ('ré', 4072), ('D', 4007), ('A', 3867), ('ca', 3857), ('su', 3720), ('ho', 3566), ('dé', 3430), ('té', 3312), ('P', 3285), ('t\r', 3169), ('ni', 3148), ('S', 3146), ("'i", 2875), ('T', 2724), ('_', 2684), ('uv', 2499), ('os', 2434), (':', 2423), ('ec', 2411), ('!', 2360), ('nn', 2358), ('w', 2352), (',', 2348), ('O', 2305), ('G', 2278), ("u'", 2190), ('R', 2152), ('N', 2116), ('id', 2109), ('J', 2036), ('ç', 1747), ('k', 1711), ('î', 1709), ('B', 1695), ('â', 1629), ('?', 1551), ('V', 1532), ('F', 1462), ('ô', 1453), ('1', 1451), ('U', 1302), ('à', 1156), ('û', 1106), ('ù', 1037), ('H', 988), ('Q', 829), ('«', 827), ('É', 747), ('ï', 679), ('0', 633), ('»', 612), ('8', 502), (';', 488), ('2', 446), ('™', 399), ('X', 391), (')', 364), ('(', 364), ('3', 363), ('6', 331), ('Y', 325), ('W', 297), ('5', 293), ('[', 291), (']', 291), ('4', 283), ('7', 265), ('K', 252), ('q', 224), ('À', 213), ('*', 209), ('9', 187), ('/', 82), ('ë', 80), ('“', 77), ('”', 77), ('Z', 74), ('È', 62), ('\n\r', 52), ('—', 47), ('•', 28), ('Ê', 26), ('Ç', 19), ('°', 17), ('$', 14), ('º', 11), ('…', 8), ('%', 7), ('‘', 7), ('\ufeff', 7), ('#', 7), ('Î', 3), ('Â', 2), ('\r', 0)]
symbolTotal = sum(valeur for _, valeur in occurencesSymboles)
symbolesRatio = [(symbole, valeur / symbolTotal) for symbole, valeur in occurencesSymboles]
#print(symbolesRatio)




#TextsForStats
url = "https://www.gutenberg.org/ebooks/13846.txt.utf-8"  # Example URL (replace with your desired URL)
textsForStats = load_text_from_web(url)
url = "https://www.gutenberg.org/ebooks/4650.txt.utf-8"  # Example URL (replace with your desired URL)
textsForStats = textsForStats + load_text_from_web(url)
url = "https://www.gutenberg.org/ebooks/69794.txt.utf-8"
textsForStats = textsForStats + load_text_from_web(url)
url = "https://www.gutenberg.org/ebooks/63267.txt.utf-8"
textsForStats = textsForStats + load_text_from_web(url)
url = "https://www.gutenberg.org/ebooks/18092.txt.utf-8"
textsForStats = textsForStats + load_text_from_web(url)
url = "https://www.gutenberg.org/ebooks/18812.txt.utf-8"
textsForStats = textsForStats + load_text_from_web(url)
url = "https://www.gutenberg.org/ebooks/13704.txt.utf-8"
textsForStats = textsForStats + load_text_from_web(url)


#copier de M_vers_symboles du fichier crypt.py
def encodeSymboles(M, dict):

    encoded_text = []
    i = 0

    while i < len(M):
        # Vérifie les paires de caractères
        if i + 1 < len(M):
            pair = M[i] + M[i + 1]
            if pair in dict:
                encoded_text.append(pair)
                i += 2  # Sauter les deux caractères utilisés
                continue

        # Vérifie le caractère seul
        if M[i] in dict:
            encoded_text.append(M[i])
        i += 1

    return encoded_text

textEnSymboles = encodeSymboles(textsForStats, Symboles)
occurencesPrevious = [0] * 256 # array de 256 zeros
occurencesNext = [0] * 256

for i in range(len(textEnSymboles)):
  if(textEnSymboles[i] == 'e '):

    if(i>0):
      occurencesPrevious[Symboles.index(textEnSymboles[i-1])] += 1 #increment occurence à l'index du symbole
    if(i< (len(textEnSymboles)-2)):
      occurencesNext[Symboles.index(textEnSymboles[i+1])] += 1 #increment occurence à l'index du symbole

avant_e_space = list(zip(Symboles, occurencesPrevious))
apres_e_space = list(zip(Symboles, occurencesNext))

sortedAvant = sorted(avant_e_space, key=lambda x: x[1], reverse=True)
sortedApres = sorted(apres_e_space, key=lambda x: x[1], reverse=True)
print("Avant 'e ': ", sortedAvant, "\n\nApres 'e ': ", sortedApres)

"""
# pour calculer occurencesSymboles ---------------------------------------------

# fortement inspirer de la fonction M_vers_symboles du prof dans crypt.py
i = 0

while i < len(textsForStats):
  if i + 1 < len(textsForStats):
    # Vérifie les paires de caractères
    pair = textsForStats[i] + textsForStats[i + 1]
    if pair in Symboles:
      occurences[Symboles.index(pair)] += 1 #trouve l'index de la pair et incremente occurence au meme index
      i += 2  # Sauter les deux caractères utilisés
      continue
    if textsForStats[i] in Symboles:
      occurences[Symboles.index(textsForStats[i])] += 1 #increment occurence à l'index du symbole
    i += 1


stats = list(zip(Symboles, occurences))
sortedStats = sorted(stats, key=lambda x: x[1], reverse=True)

#print(sortedStats)
#-------------------------------------------------------------------------------
"""
def bitToTab(C):
   return [C[i:i+8] for i in range (0, len(C), 8)]

#for testing purposes
dictionnaire_cryptogramme = {}

def decrypt(C):
    
    global dictionnaire_cryptogramme    #for testing

    #calculer les stats du chiffrage 
    bitTab = bitToTab(C)
    tupleBits = sorted(bitCharByOccurence(bitTab).items(), key=lambda item: item[1], reverse=True)
    #print(tupleBits)
    #print(occurencesSymboles)
    #print("student_code stats tupleBits", tupleBits)

    #mapper chaque chiffre avec la lettre
    dictToutSymbol= dict(occurencesSymboles)
    dictToutBits= dict(tupleBits)

    #modifier ça pour aller vers des proba
    dictChiffreVersLettre = dict(list(zip(dictToutBits, dictToutSymbol)))
    
    #print("student_code dictionnaire", dictChiffreVersLettre)
    dictionnaire_cryptogramme = dictChiffreVersLettre

    #dechiffrer le message chiffré avec les occurences

    M = ""
    for cypher in bitTab:
      char = dictChiffreVersLettre.get(cypher)
      M = M + char

    #print("**************MESSAGE***************:\n", M)
    #print("**************MESSAGE DÉCRYPTÉ***************\n", decrypt(c))

  
    return M

def dict_cryptogramme():
   return dictionnaire_cryptogramme


def bitCharByOccurence(bitTab):
    dictBitChar = {}
    for bitchar in bitTab:
    #mettre dans un dictionnaire qui incrémente à ch fois
    #si clé exite, créer clé
       if(dictBitChar.get(bitchar)==None):
            dictBitChar[bitchar] = 1
       else:
          dictBitChar.update({bitchar : dictBitChar.get(bitchar)+1})

    return dictBitChar
