import numpy as np
from crypt import load_text_from_web

Symboles = ['û', 'u', 'b', 'z', 'Î', '™', 'x', '%', 'r', 'h', ':', 'R', '6', '‘', '$', 'î', '5', 'È', '\r', '.', 'ç', 'y', 'ô', 'Â', '_', 'J', '…', 'N', 'T', '3', 'e', 'A', '[', ',', 'H', 'â', 'D', '0', 'M', '\n', 'ë', '4', 'C', 'ù', ']', ')', '—', '!', 'G', '/', 'ê', '«', '\ufeff', '?', 'è', '-', 'c', 'f', "'", 'º', 's', 'E', 'q', 'B', 'P', 'I', 'à', '7', 'À', ' ', 'S', 'W', 'K', '9', 'n', '»', 'k', '“', 'É', 'i', 'm', 'w', '1', '’', 'O', 'v', '•', 'Ç', '#', 'j', '*', 'U', 't', '8', 'Ê', '2', 'X', 'o', 'ï', 'Y', ';', 'a', 'F', 'V', '”', 'L', 'é', '°', 'Z', 'Q', 'g', 'p', '(', 'd', 'l', 'e ', 's ', 't ', 'es', ' d', '\r\n', 'en', 'qu', ' l', 're', ' p', 'de', 'le', 'nt', 'on', ' c', ', ', ' e', 'ou', ' q', ' s', 'n ', 'ue', 'an', 'te', ' a', 'ai', 'se', 'it', 'me', 'is', 'oi', 'r ', 'er', ' m', 'ce', 'ne', 'et', 'in', 'ns', ' n', 'ur', 'i ', 'a ', 'eu', 'co', 'tr', 'la', 'ar', 'ie', 'ui', 'us', 'ut', 'il', ' t', 'pa', 'au', 'el', 'ti', 'st', 'un', 'em', 'ra', 'e,', 'so', 'or', 'l ', ' f', 'll', 'nd', ' j', 'si', 'ir', 'e\r', 'ss', 'u ', 'po', 'ro', 'ri', 'pr', 's,', 'ma', ' v', ' i', 'di', ' r', 'vo', 'pe', 'to', 'ch', '. ', 've', 'nc', 'om', ' o', 'je', 'no', 'rt', 'à ', 'lu', "'e", 'mo', 'ta', 'as', 'at', 'io', 's\r', 'sa', "u'", 'av', 'os', ' à', ' u', "l'", "'a", 'rs', 'pl', 'é ', '; ', 'ho', 'té', 'ét', 'fa', 'da', 'li', 'su', 't\r', 'ée', 'ré', 'dé', 'ec', 'nn', 'mm', "'i", 'ca', 'uv', '\n\r', 'id', ' b', 'ni', 'bl']
occurences = [0] * 256 # array de 256 zeros

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

i = 0

while i < len(textsForStats):
  if i + 1 < len(textsForStats):
    # Vérifie les paires de caractères
    pair = textsForStats[i] + textsForStats[i + 1]
    if pair in Symboles:
      occurences[Symboles.index(pair)] += 1
      i += 2  # Sauter les deux caractères utilisés
      continue
    if textsForStats[i] in Symboles:
      occurences[Symboles.index(textsForStats[i])] += 1
    i += 1


stats = list(zip(Symboles, occurences))
sortedStats = sorted(stats, key=lambda x: x[1], reverse=True)

print(sortedStats)
def decrypt(C):
  M=""
  #entrez votre code ici.
  #Vous pouvez créer des fonctions auxiliaires et adapter le code à votre façon mais decrypt dois renvoyer le message décrypté
  return M
