from crypt import load_text_from_web # type: ignore

Symboles = ['û', 'u', 'b', 'z', 'Î', '™', 'x', '%', 'r', 'h', ':', 'R', '6', '‘', '$', 'î', '5', 'È', '\r', '.', 'ç', 'y', 'ô', 'Â', '_', 'J', '…', 'N', 'T', '3', 'e', 'A', '[', ',', 'H', 'â', 'D', '0', 'M', '\n', 'ë', '4', 'C', 'ù', ']', ')', '—', '!', 'G', '/', 'ê', '«', '\ufeff', '?', 'è', '-', 'c', 'f', "'", 'º', 's', 'E', 'q', 'B', 'P', 'I', 'à', '7', 'À', ' ', 'S', 'W', 'K', '9', 'n', '»', 'k', '“', 'É', 'i', 'm', 'w', '1', '’', 'O', 'v', '•', 'Ç', '#', 'j', '*', 'U', 't', '8', 'Ê', '2', 'X', 'o', 'ï', 'Y', ';', 'a', 'F', 'V', '”', 'L', 'é', '°', 'Z', 'Q', 'g', 'p', '(', 'd', 'l', 'e ', 's ', 't ', 'es', ' d', '\r\n', 'en', 'qu', ' l', 're', ' p', 'de', 'le', 'nt', 'on', ' c', ', ', ' e', 'ou', ' q', ' s', 'n ', 'ue', 'an', 'te', ' a', 'ai', 'se', 'it', 'me', 'is', 'oi', 'r ', 'er', ' m', 'ce', 'ne', 'et', 'in', 'ns', ' n', 'ur', 'i ', 'a ', 'eu', 'co', 'tr', 'la', 'ar', 'ie', 'ui', 'us', 'ut', 'il', ' t', 'pa', 'au', 'el', 'ti', 'st', 'un', 'em', 'ra', 'e,', 'so', 'or', 'l ', ' f', 'll', 'nd', ' j', 'si', 'ir', 'e\r', 'ss', 'u ', 'po', 'ro', 'ri', 'pr', 's,', 'ma', ' v', ' i', 'di', ' r', 'vo', 'pe', 'to', 'ch', '. ', 've', 'nc', 'om', ' o', 'je', 'no', 'rt', 'à ', 'lu', "'e", 'mo', 'ta', 'as', 'at', 'io', 's\r', 'sa', "u'", 'av', 'os', ' à', ' u', "l'", "'a", 'rs', 'pl', 'é ', '; ', 'ho', 'té', 'ét', 'fa', 'da', 'li', 'su', 't\r', 'ée', 'ré', 'dé', 'ec', 'nn', 'mm', "'i", 'ca', 'uv', '\n\r', 'id', ' b', 'ni', 'bl']
symbolesOccurences = [('e ', 62680), ('s ', 51231), ('\r\n', 48488), ('t ', 35802), (' ', 34829), (' d', 32195), (', ', 30024), ('es', 29021), ('g', 26835), ('le', 26546), ('re', 25810), ('a', 25763), (' l', 25758), ('de', 25536), ('on', 24692), ('qu', 23720), ('en', 23120), ('é', 21599), ('ou', 21165), ('nt', 20647), ('c', 20206), (' p', 20024), ('ai', 20001), ('i', 19695), ('d', 19595), ('u', 18935), ('e', 17988), ('f', 17557), ('n', 17453), ('m', 17377), ('r', 17278), ('te', 16889), ('an', 16592), (' c', 16373), (' s', 16322), ('me', 16099), ('. ', 15623), ('t', 15576), (' e', 15313), ('n ', 14892), ('p', 14665), ('r ', 14534), ('ur', 14514), ('b', 14492), ('o', 14296), ('er', 14233), ('in', 14041), ('\n', 13932), ('it', 13741), (' a', 13736), ('l', 13519), ('ie', 13454), ('is', 13397), ('la', 13394), ('v', 13381), ('s', 12870), ('ra', 12724), ('h', 12665), ('il', 12646), ('et', 12577), ('ce', 12244), ('se', 12192), ('us', 12093), ('co', 11914), ('tr', 11622), ('a ', 11555), ('ne', 11540), ('-', 11498), ('x', 11332), ('un', 11005), (' m', 11000), (' q', 10976), ('pa', 10654), ('ns', 10178), ('ar', 9898), ('eu', 9835), ('au', 9813), ('u ', 9700), ("'", 9563), ('oi', 9547), ('ma', 9434), ('ti', 9285), ('y', 9139), (' t', 8996), ('ch', 8951), ('ui', 8903), ('è', 8875), ('pr', 8864), ('i ', 8849), ('ue', 8762), ('ri', 8504), ('.', 8365), ('or', 8327), (' n', 8234), ('ve', 8126), ('po', 8002), ('ut', 7795), ('ro', 7377), (' f', 7318), ('pe', 7078), ('ir', 7074), ('s,', 7028), ("'a", 6927), ('so', 6839), ('di', 6787), ('à ', 6741), ('st', 6660), ('ss', 6629), ('l ', 6628), ('ll', 6528), ('ét', 6433), (' r', 6420), ('el', 6379), ('nd', 6328), ('si', 6283), ('em', 6197), (' v', 6102), ('; ', 6053), ('at', 5888), ('j', 5859), ('e\r', 5844), ('L', 5801), ('é ', 5757), ('vo', 5689), ('ê', 5684), ("'e", 5654), ('e,', 5527), ('sa', 5466), ('mo', 5461), ('as', 5351), ('pl', 5330), ('no', 5246), ('to', 5239), ('bl', 5186), ('’', 5080), ('M', 5061), ("l'", 5039), ('C', 4985), (' à', 4957), ('s\r', 4919), (' u', 4870), ('ta', 4848), ('lu', 4787), ('I', 4774), (' i', 4771), ('li', 4702), ('rt', 4696), ('E', 4678), ('da', 4605), ('rs', 4593), ('om', 4526), (' j', 4483), ('av', 4418), (' o', 4405), ('mm', 4383), ('io', 4374), ('nc', 4367), ('z', 4321), ('je', 4317), ('fa', 4254), ('ée', 4208), (' b', 4192), ('ré', 4072), ('D', 4007), ('A', 3867), ('ca', 3857), ('su', 3720), ('ho', 3566), ('dé', 3430), ('té', 3312), ('P', 3285), ('t\r', 3169), ('ni', 3148), ('S', 3146), ("'i", 2875), ('T', 2724), ('_', 2684), ('uv', 2499), ('os', 2434), (':', 2423), ('ec', 2411), ('!', 2360), ('nn', 2358), ('w', 2352), (',', 2348), ('O', 2305), ('G', 2278), ("u'", 2190), ('R', 2152), ('N', 2116), ('id', 2109), ('J', 2036), ('ç', 1747), ('k', 1711), ('î', 1709), ('B', 1695), ('â', 1629), ('?', 1551), ('V', 1532), ('F', 1462), ('ô', 1453), ('1', 1451), ('U', 1302), ('à', 1156), ('û', 1106), ('ù', 1037), ('H', 988), ('Q', 829), ('«', 827), ('É', 747), ('ï', 679), ('0', 633), ('»', 612), ('8', 502), (';', 488), ('2', 446), ('™', 399), ('X', 391), (')', 364), ('(', 364), ('3', 363), ('6', 331), ('Y', 325), ('W', 297), ('5', 293), ('[', 291), (']', 291), ('4', 283), ('7', 265), ('K', 252), ('q', 224), ('À', 213), ('*', 209), ('9', 187), ('/', 82), ('ë', 80), ('“', 77), ('”', 77), ('Z', 74), ('È', 62), ('\n\r', 52), ('—', 47), ('•', 28), ('Ê', 26), ('Ç', 19), ('°', 17), ('$', 14), ('º', 11), ('…', 8), ('%', 7), ('‘', 7), ('\ufeff', 7), ('#', 7), ('Î', 3), ('Â', 2), ('\r', 0)]
occurAvant_e_space = [(' d', 11594), ('qu', 7295), ('tr', 4306), (' l', 4213), ('un', 3610), (' n', 2017), ('ll', 2009), ('mm', 1850), ('g', 1692), (' j', 1538), ('L', 1411), ('ir', 1380), ('bl', 1355), ('h', 1312), (' s', 1288), (' c', 1142), ('J', 1065), ('nc', 1037), ('ur', 954), ('in', 938), (' m', 812), ('ss', 635), ('ch', 575), ('nd', 534), ('it', 491), ('us', 440), ('nt', 411), ('os', 398), ('ut', 395), ('C', 393), ('or', 304), ('rt', 286), ('pl', 280), ('il', 250), ('st', 232), ('is', 214), ('dé', 214), ('b', 208), ('ni', 199), ('z', 193), ('D', 190), ('id', 188), ('nn', 184), ('ri', 182), ('ns', 162), ('ré', 141), ('uv', 132), ('li', 122), ('pr', 119), ('oi', 109), ('ar', 106), ('ti', 94), ('at', 92), (' t', 86), ('té', 83), ('di', 78), ('si', 77), ('e', 70), ('re', 70), ('ï', 67), ('an', 67), ('N', 66), ('er', 63), (' b', 56), ('as', 52), ('om', 51), ('w', 49), ('ou', 48), ('av', 46), ('on', 38), ('rs', 37), ('y', 33), ('f', 33), ('x', 30), ('k', 25), ('es', 21), ('ai', 21), ('eu', 21), ('lu', 17), ('ui', 14), ('M', 10), ('4', 7), ('W', 7), ('I', 6), ('2', 6), ('su', 5), ('5', 4), ('T', 4), ('3', 4), ('0', 3), ('8', 3), ('X', 2), ('V', 2), ('en', 2), ('6', 1), ('7', 1), ('S', 1), (', ', 1), ('a ', 1), ('û', 0), ('u', 0), ('Î', 0), ('™', 0), ('%', 0), ('r', 0), (':', 0), ('R', 0), ('‘', 0), ('$', 0), ('î', 0), ('È', 0), ('\r', 0), ('.', 0), ('ç', 0), ('ô', 0), ('Â', 0), ('_', 0), ('…', 0), ('A', 0), ('[', 0), (',', 0), ('H', 0), ('â', 0), ('\n', 0), ('ë', 0), ('ù', 0), (']', 0), (')', 0), ('—', 0), ('!', 0), ('G', 0), ('/', 0), ('ê', 0), ('«', 0), ('\ufeff', 0), ('?', 0), ('è', 0), ('-', 0), ('c', 0), ("'", 0), ('º', 0), ('s', 0), ('E', 0), ('q', 0), ('B', 0), ('P', 0), ('à', 0), ('À', 0), (' ', 0), ('K', 0), ('9', 0), ('n', 0), ('»', 0), ('“', 0), ('É', 0), ('i', 0), ('m', 0), ('1', 0), ('’', 0), ('O', 0), ('v', 0), ('•', 0), ('Ç', 0), ('#', 0), ('j', 0), ('*', 0), ('U', 0), ('t', 0), ('Ê', 0), ('o', 0), ('Y', 0), (';', 0), ('a', 0), ('F', 0), ('”', 0), ('é', 0), ('°', 0), ('Z', 0), ('Q', 0), ('p', 0), ('(', 0), ('d', 0), ('l', 0), ('e ', 0), ('s ', 0), ('t ', 0), ('\r\n', 0), (' p', 0), ('de', 0), ('le', 0), (' e', 0), (' q', 0), ('n ', 0), ('ue', 0), ('te', 0), (' a', 0), ('se', 0), ('me', 0), ('r ', 0), ('ce', 0), ('ne', 0), ('et', 0), ('i ', 0), ('co', 0), ('la', 0), ('ie', 0), ('pa', 0), ('au', 0), ('el', 0), ('em', 0), ('ra', 0), ('e,', 0), ('so', 0), ('l ', 0), (' f', 0), ('e\r', 0), ('u ', 0), ('po', 0), ('ro', 0), ('s,', 0), ('ma', 0), (' v', 0), (' i', 0), (' r', 0), ('vo', 0), ('pe', 0), ('to', 0), ('. ', 0), ('ve', 0), (' o', 0), ('je', 0), ('no', 0), ('à ', 0), ("'e", 0), ('mo', 0), ('ta', 0), ('io', 0), ('s\r', 0), ('sa', 0), ("u'", 0), (' à', 0), (' u', 0), ("l'", 0), ("'a", 0), ('é ', 0), ('; ', 0), ('ho', 0), ('ét', 0), ('fa', 0), ('da', 0), ('t\r', 0), ('ée', 0), ('ec', 0), ("'i", 0), ('ca', 0), ('\n\r', 0)]
occurApres_e_space = [('de', 3923), ('qu', 2652), ('la', 2315), ('le', 2303), ('d', 1867), ('co', 1784), ('f', 1481), ('ce', 1353), ('se', 1306), ('pa', 1302), ('et', 1278), ("l'", 1274), ('so', 1233), ('b', 1025), ('no', 1025), ('re', 990), ('po', 936), ('à ', 936), ('pr', 932), ('vo', 927), ('mo', 912), ('to', 899), ('ch', 874), ('je', 872), ('m', 865), ('j', 841), ('ne', 839), ('pe', 823), ('sa', 816), ('n', 797), ('en', 790), ('ma', 788), ('g', 734), ('v', 732), ('au', 729), ('su', 701), ('me', 668), ('fa', 636), ('c', 631), ('tr', 620), ('un', 619), ('pl', 618), ('te', 560), ('di', 553), ('dé', 526), ('s', 477), ('P', 475), ('es', 474), ('D', 465), ('p', 465), ('l', 454), ('a', 443), ('ca', 425), ('M', 413), ('da', 406), ('lu', 374), ('av', 337), ('ré', 336), ('in', 301), ('si', 290), ('o', 278), ('h', 273), ('ét', 268), ('ou', 246), ('é', 229), ('ra', 227), ('ve', 214), ('B', 209), ('e', 208), ('t', 205), ('w', 201), ('C', 198), ('F', 186), ('a ', 186), ('_', 183), ('L', 179), ('li', 170), ('an', 168), ('G', 153), ('ta', 149), ('S', 148), ('i', 138), ('il', 136), ('R', 134), ('ar', 134), ('ro', 133), ('ri', 125), ('U', 98), ('V', 97), ('or', 90), ('à', 85), ('on', 85), ('T', 84), ('ti', 84), ('1', 83), ('ho', 83), ('id', 78), ('us', 75), ('as', 74), ('bl', 74), ('r', 71), ('st', 68), ('y', 63), ('ai', 63), ('at', 60), ('ni', 57), ('eu', 55), ('N', 48), ('â', 42), ('J', 37), ('ê', 37), ('A', 35), ('el', 30), ('H', 29), ('it', 29), ('2', 27), ('em', 23), ('I', 22), ('K', 20), ('X', 20), ('(', 20), ('4', 18), ('k', 17), ('is', 17), ('té', 13), ('z', 12), ('O', 12), ('Z', 10), ('ut', 10), ('3', 9), ('«', 9), ('E', 9), ('W', 9), ('er', 9), ('8', 8), ('om', 8), ('6', 7), ('“', 7), ('É', 6), ('os', 6), ('uv', 6), ('7', 5), ('ir', 5), ('5', 4), ('ç', 4), ('Q', 4), ('î', 2), ('[', 2), ('Y', 2), ('ô', 1), ('è', 1), ('9', 1), ('oi', 1), ('io', 1), ('ec', 1), ('û', 0), ('u', 0), ('Î', 0), ('™', 0), ('x', 0), ('%', 0), (':', 0), ('‘', 0), ('$', 0), ('È', 0), ('\r', 0), ('.', 0), ('Â', 0), ('…', 0), (',', 0), ('0', 0), ('\n', 0), ('ë', 0), ('ù', 0), (']', 0), (')', 0), ('—', 0), ('!', 0), ('/', 0), ('\ufeff', 0), ('?', 0), ('-', 0), ("'", 0), ('º', 0), ('q', 0), ('À', 0), (' ', 0), ('»', 0), ('’', 0), ('•', 0), ('Ç', 0), ('#', 0), ('*', 0), ('Ê', 0), ('ï', 0), (';', 0), ('”', 0), ('°', 0), ('e ', 0), ('s ', 0), ('t ', 0), (' d', 0), ('\r\n', 0), (' l', 0), (' p', 0), ('nt', 0), (' c', 0), (', ', 0), (' e', 0), (' q', 0), (' s', 0), ('n ', 0), ('ue', 0), (' a', 0), ('r ', 0), (' m', 0), ('ns', 0), (' n', 0), ('ur', 0), ('i ', 0), ('ie', 0), ('ui', 0), (' t', 0), ('e,', 0), ('l ', 0), (' f', 0), ('ll', 0), ('nd', 0), (' j', 0), ('e\r', 0), ('ss', 0), ('u ', 0), ('s,', 0), (' v', 0), (' i', 0), (' r', 0), ('. ', 0), ('nc', 0), (' o', 0), ('rt', 0), ("'e", 0), ('s\r', 0), ("u'", 0), (' à', 0), (' u', 0), ("'a", 0), ('rs', 0), ('é ', 0), ('; ', 0), ('t\r', 0), ('ée', 0), ('nn', 0), ('mm', 0), ("'i", 0), ('\n\r', 0), (' b', 0)]
occurAvant_s_space = [('le', 6694), ('ou', 3285), ('de', 3248), ('an', 2537), ('ai', 2263), ('t', 1831), ('pa', 1732), ('re', 1666), ('on', 1660), ('oi', 1585), ('te', 1563), ('è', 1479), ('lu', 1399), ('se', 1355), ('ur', 1304), ('me', 1270), ('ce', 1206), ('é', 1154), ('il', 1039), ('l', 1007), ('p', 902), ('in', 874), ('nt', 807), ('ui', 758), ('ée', 750), ('er', 702), ('ne', 576), ('en', 474), ('d', 346), ('y', 303), ('té', 301), ('ue', 298), ('no', 296), ('ie', 291), ('it', 288), ('nd', 280), ('f', 222), ('or', 212), ('ri', 202), ('k', 187), ('ra', 185), ('m', 167), ('ve', 164), ('nc', 160), ('pe', 157), ('el', 134), ('di', 134), ('un', 115), ('ré', 107), (' i', 106), ('c', 102), ('et', 100), ('rt', 99), ('ro', 94), ('vo', 79), ('at', 66), ('g', 62), ('ir', 62), ('po', 59), ('w', 58), ('ti', 44), ('si', 44), ('dé', 44), ('ma', 42), (' a', 41), ('os', 38), ('li', 37), ('ut', 36), ("'a", 36), ('ca', 36), ('la', 35), ('’', 28), ('h', 23), ('ch', 20), ('ni', 20), ('id', 19), ('su', 18), ('ar', 15), ('om', 15), ('st', 14), ('es', 11), (' u', 11), ('eu', 10), ("'e", 7), ('ho', 6), ('ta', 4), ('ï', 3), ('ec', 3), ('ù', 2), ("'", 2), ('j', 2), ('co', 2), ('b', 1), ('I', 1), (' e', 1), ('au', 1), ('ll', 1), (' o', 1), ('sa', 1), ('û', 0), ('u', 0), ('z', 0), ('Î', 0), ('™', 0), ('x', 0), ('%', 0), ('r', 0), (':', 0), ('R', 0), ('6', 0), ('‘', 0), ('$', 0), ('î', 0), ('5', 0), ('È', 0), ('\r', 0), ('.', 0), ('ç', 0), ('ô', 0), ('Â', 0), ('_', 0), ('J', 0), ('…', 0), ('N', 0), ('T', 0), ('3', 0), ('e', 0), ('A', 0), ('[', 0), (',', 0), ('H', 0), ('â', 0), ('D', 0), ('0', 0), ('M', 0), ('\n', 0), ('ë', 0), ('4', 0), ('C', 0), (']', 0), (')', 0), ('—', 0), ('!', 0), ('G', 0), ('/', 0), ('ê', 0), ('«', 0), ('\ufeff', 0), ('?', 0), ('-', 0), ('º', 0), ('s', 0), ('E', 0), ('q', 0), ('B', 0), ('P', 0), ('à', 0), ('7', 0), ('À', 0), (' ', 0), ('S', 0), ('W', 0), ('K', 0), ('9', 0), ('n', 0), ('»', 0), ('“', 0), ('É', 0), ('i', 0), ('1', 0), ('O', 0), ('v', 0), ('•', 0), ('Ç', 0), ('#', 0), ('*', 0), ('U', 0), ('8', 0), ('Ê', 0), ('2', 0), ('X', 0), ('o', 0), ('Y', 0), (';', 0), ('a', 0), ('F', 0), ('V', 0), ('”', 0), ('L', 0), ('°', 0), ('Z', 0), ('Q', 0), ('(', 0), ('e ', 0), ('s ', 0), ('t ', 0), (' d', 0), ('\r\n', 0), ('qu', 0), (' l', 0), (' p', 0), (' c', 0), (', ', 0), (' q', 0), (' s', 0), ('n ', 0), ('is', 0), ('r ', 0), (' m', 0), ('ns', 0), (' n', 0), ('i ', 0), ('a ', 0), ('tr', 0), ('us', 0), (' t', 0), ('em', 0), ('e,', 0), ('so', 0), ('l ', 0), (' f', 0), (' j', 0), ('e\r', 0), ('ss', 0), ('u ', 0), ('pr', 0), ('s,', 0), (' v', 0), (' r', 0), ('to', 0), ('. ', 0), ('je', 0), ('à ', 0), ('mo', 0), ('as', 0), ('io', 0), ('s\r', 0), ("u'", 0), ('av', 0), (' à', 0), ("l'", 0), ('rs', 0), ('pl', 0), ('é ', 0), ('; ', 0), ('ét', 0), ('fa', 0), ('da', 0), ('t\r', 0), ('nn', 0), ('mm', 0), ("'i", 0), ('uv', 0), ('\n\r', 0), (' b', 0), ('bl', 0)]
occurApres_s_space = [('de', 4843), ('qu', 2606), ('le', 2310), ('d', 2105), ('et', 1581), ('pa', 1382), ('en', 1252), ('co', 1216), ('f', 1048), ('so', 1028), ('à ', 1010), ('se', 921), ('au', 901), ('la', 882), ('a', 842), ('un', 841), ('b', 827), ('po', 817), ('av', 749), ('pr', 734), ('g', 699), ('ch', 664), ('o', 624), ('m', 611), ('re', 598), ('ce', 588), ('pl', 553), ('ma', 540), ('ne', 526), ('n', 502), ('no', 498), ('in', 489), ('da', 486), ('mo', 473), ('su', 463), ('c', 453), ('tr', 449), ("l'", 441), ('ét', 432), ('v', 431), ('s', 407), ('j', 406), ('é', 400), ('pe', 398), ('to', 397), ('di', 391), ('dé', 376), ('vo', 372), ('l', 367), ('sa', 367), ('an', 340), ('ou', 339), ('h', 325), ('me', 320), ('on', 318), ('il', 305), ('fa', 305), ('ca', 305), ('ho', 289), ('ar', 277), ('p', 276), ('y', 263), ('e', 261), ('si', 226), ('ve', 203), ('ra', 197), ('es', 193), ('te', 191), ('ré', 191), ('i', 183), ('je', 179), ('t', 162), ('ai', 154), ('ri', 154), ('ê', 149), ('or', 143), ('as', 139), ('li', 130), ('lu', 122), ('ta', 117), ('ro', 113), ('at', 103), ('à', 93), ('id', 93), ('a ', 92), ('G', 88), ('w', 85), ('_', 83), ('M', 83), ('A', 76), ('el', 72), ('r', 71), ('eu', 71), ('ti', 71), ('em', 69), ('ni', 57), ('É', 56), ('P', 46), ('B', 44), ('1', 44), ('T', 39), ('E', 39), ('I', 39), ('D', 33), ('S', 31), ('us', 29), ('bl', 29), ('C', 28), ('k', 28), ('R', 27), ('F', 26), ('L', 26), ('st', 26), ('té', 26), ('V', 21), ('er', 19), ('â', 18), ('u', 17), ('ir', 17), ('J', 13), ('(', 12), ('H', 11), ('oi', 11), ('ut', 10), ('os', 9), ('W', 8), ('is', 8), ('6', 7), ('3', 7), ('O', 6), ('om', 6), ('N', 5), ('K', 5), ('X', 4), ('ec', 4), ('z', 3), ('î', 3), (' ', 3), ('io', 3), ('ç', 2), ('ô', 2), ('[', 2), ('x', 1), ('4', 1), ('«', 1), ('»', 1), ('2', 1), ('Y', 1), ('ur', 1), ('û', 0), ('Î', 0), ('™', 0), ('%', 0), (':', 0), ('‘', 0), ('$', 0), ('5', 0), ('È', 0), ('\r', 0), ('.', 0), ('Â', 0), ('…', 0), (',', 0), ('0', 0), ('\n', 0), ('ë', 0), ('ù', 0), (']', 0), (')', 0), ('—', 0), ('!', 0), ('/', 0), ('\ufeff', 0), ('?', 0), ('è', 0), ('-', 0), ("'", 0), ('º', 0), ('q', 0), ('7', 0), ('À', 0), ('9', 0), ('“', 0), ('’', 0), ('•', 0), ('Ç', 0), ('#', 0), ('*', 0), ('U', 0), ('8', 0), ('Ê', 0), ('ï', 0), (';', 0), ('”', 0), ('°', 0), ('Z', 0), ('Q', 0), ('e ', 0), ('s ', 0), ('t ', 0), (' d', 0), ('\r\n', 0), (' l', 0), (' p', 0), ('nt', 0), (' c', 0), (', ', 0), (' e', 0), (' q', 0), (' s', 0), ('n ', 0), ('ue', 0), (' a', 0), ('it', 0), ('r ', 0), (' m', 0), ('ns', 0), (' n', 0), ('i ', 0), ('ie', 0), ('ui', 0), (' t', 0), ('e,', 0), ('l ', 0), (' f', 0), ('ll', 0), ('nd', 0), (' j', 0), ('e\r', 0), ('ss', 0), ('u ', 0), ('s,', 0), (' v', 0), (' i', 0), (' r', 0), ('. ', 0), ('nc', 0), (' o', 0), ('rt', 0), ("'e", 0), ('s\r', 0), ("u'", 0), (' à', 0), (' u', 0), ("'a", 0), ('rs', 0), ('é ', 0), ('; ', 0), ('t\r', 0), ('ée', 0), ('nn', 0), ('mm', 0), ("'i", 0), ('uv', 0), ('\n\r', 0), (' b', 0)]

symbolTotal = sum(valeur for _, valeur in symbolesOccurences)
symbolesRatio = [(symbole, valeur / symbolTotal) for symbole, valeur in symbolesOccurences]
#print(symbolesRatio)

"""

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
  if(textEnSymboles[i] == 's '):

    if(i>0):
      occurencesPrevious[Symboles.index(textEnSymboles[i-1])] += 1 #increment occurencePrevious à l'index du symbole
    if(i< (len(textEnSymboles)-2)):
      occurencesNext[Symboles.index(textEnSymboles[i+1])] += 1 #increment occurenceNext à l'index du symbole

avant_a_space = list(zip(Symboles, occurencesPrevious))
apres_a_space = list(zip(Symboles, occurencesNext))

sortedAvant = sorted(avant_a_space, key=lambda x: x[1], reverse=True)
sortedApres = sorted(apres_a_space, key=lambda x: x[1], reverse=True)
print("Avant 's ': ", sortedAvant, "\n\nApres 's ': ", sortedApres)
"""
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
def cutInOctets(C):
   return [C[i:i+8] for i in range (0, len(C), 8)]

#for testing purposes
def decrypt(C):
    
    #calculer les stats du chiffrage 
    cypherOctets = cutInOctets(C)            #découpage de cypher en tableau d'octet

    #Tuple d'octets et la somme de chaque octet dans le message crypté
    octetsOccurences = sorted(octetsByOccurences(cypherOctets), key=lambda item: item[1], reverse=True)

    occurencesPrevious = [0] * 256 # array de 256 zeros
    occurencesNext = [0] * 256

    for i in range(len(cypherOctets)): #compte les occureces des octets avant et apres 'e '
        if(cypherOctets[i] == octetsOccurences[0][0]): #si on a un 'e '

            if(i>0):
                occurencesPrevious[int(cypherOctets[i-1], 2)] += 1 #increment occurencePrevious à l'index octet convertit en int
                if(i< (len(cypherOctets)-2)):
                    occurencesNext[int(cypherOctets[i+1], 2)] += 1 #increment occurenceNext à l'index octet converti en int

    octets = [i for i in range(256)] # fait une liste de nombre de 0 a 255
    for i in range (len(octets)): octets[i] = (bin(octets[i])[2:]).zfill(8) # convertit les nombres en octets
    avant_e_space = list(zip(octets, occurencesPrevious))
    apres_e_space = list(zip(octets, occurencesNext))

    sortedAvant_e_space = sorted(avant_e_space, key=lambda x: x[1], reverse=True)
    sortedApres_e_space = sorted(apres_e_space, key=lambda x: x[1], reverse=True)

    occurencesPrevious_s_space = [0] * 256 # array de 256 zeros
    occurencesNext_s_space = [0] * 256

    for i in range(len(cypherOctets)): #compte les occureces des octets avant et apres 's '
        if(cypherOctets[i] == octetsOccurences[1][0]): #si on a un 's '

            if(i>0):
                occurencesPrevious_s_space[int(cypherOctets[i-1], 2)] += 1 #increment occurencePrevious à l'index octet convertit en int
                if(i< (len(cypherOctets)-2)):
                    occurencesNext_s_space[int(cypherOctets[i+1], 2)] += 1 #increment occurenceNext à l'index octet converti en int

    avant_s_space = list(zip(octets, occurencesPrevious_s_space))
    apres_s_space = list(zip(octets, occurencesNext_s_space))

    sortedAvant_s_space = sorted(avant_s_space, key=lambda x: x[1], reverse=True)
    sortedApres_s_space = sorted(apres_s_space, key=lambda x: x[1], reverse=True)
    

    dictToutSymbol= dict(symbolesOccurences)
    dictToutBits= dict(octetsOccurences)
    dictChiffreVersLettre = dict(list(zip(dictToutBits, dictToutSymbol)))

    for i in range(0,4):
      if (sortedAvant_e_space[1][0] == sortedApres_e_space[i][0]):
        swap(dictChiffreVersLettre, sortedAvant_e_space[1][0], 'qu')
    swap(dictChiffreVersLettre, sortedAvant_s_space[0][0], 'le')
    swap(dictChiffreVersLettre, sortedAvant_e_space[0][0], ' d')
    swap(dictChiffreVersLettre, sortedApres_e_space[0][0], 'de')

    sortedAvant_e_space = sorted(avant_e_space, key=lambda x: x[1], reverse=True)
    sortedApres_e_space = sorted(apres_e_space, key=lambda x: x[1], reverse=True)

    if(sortedAvant_e_space[0][0] == sortedApres_e_space[0][0]):
        dictChiffreVersLettre[sortedAvant_e_space[0][0]] = 'qu'
    else:
        swap(dictChiffreVersLettre, sortedAvant_e_space[0][0], ' d')
        swap(dictChiffreVersLettre, sortedApres_e_space[0][0], 'de')

   #déduire 'de'
    candidat1 = sortedApres_e_space[0]
    candidat2 = sortedApres_s_space[0]
    candidat3 = sortedAvant_s_space[2]

    if(candidat1 == candidat2):
        swap(dictChiffreVersLettre, candidat1, ' de')
    elif(candidat2 == candidat3):
        swap(dictChiffreVersLettre, candidat2, ' de')
    elif(candidat3 == candidat1):
        swap(dictChiffreVersLettre, candidat3, ' de')      

    dictionnaire_cryptogramme = dictChiffreVersLettre
    
    M = ""
    for cypher in cypherOctets:
      char = dictChiffreVersLettre.get(cypher)
      M = M + char

    return M


def octetsByOccurences(cypherOctets):
    occurences = [0]*256
    for octet in cypherOctets:
        occurences[int((octet),2)] += 1 #incremente à l'indice == l'octet

    octets = [i for i in range(256)] # fait une liste de nombre de 0 a 255
    for i in range (len(octets)): octets[i] = (bin(octets[i])[2:]).zfill(8)# convertit les nombres en octet
    octetsOccurences = list(zip(octets, occurences))
    return octetsOccurences


def swap(dictChiffreVersLettre, cypher, symbol):
    oldVal = dictChiffreVersLettre[cypher]
    oldKey = None
    for key, val in dictChiffreVersLettre.items():
      if val == symbol:
          oldKey = key
          break

    dictChiffreVersLettre[oldKey] = oldVal
    dictChiffreVersLettre[cypher] = symbol
    