from crypt import *

key_now = {}

#Liste des uni et bisymboles fixées par le professeur)
nb_caracteres= 115
caracteres= ['b', 'j', '\r', 'J', '”', ')', 'Â', 'É', 'ê', '5', 't', '9', 'Y', '%', 'N', 'B', 'V', '\ufeff', 'Ê', '?', '’', 'i', ':', 's', 'C', 'â', 'ï', 'W', 'y', 'p', 'D', '—', '«', 'º', 'A', '3', 'n', '0', 'q', '4', 'e', 'T', 'È', '$', 'U', 'v', '»', 'l', 'P', 'X', 'Z', 'À', 'ç', 'u', '…', 'î', 'L', 'k', 'E', 'R', '2', '_', '8', 'é', 'O', 'Î', '‘', 'a', 'F', 'H', 'c', '[', '(', "'", 'è', 'I', '/', '!', ' ', '°', 'S', '•', '#', 'x', 'à', 'g', '*', 'Q', 'w', '1', 'û', '7', 'G', 'm', '™', 'K', 'z', '\n', 'o', 'ù', ',', 'r', ']', '.', 'M', 'Ç', '“', 'h', '-', 'f', 'ë', '6', ';', 'd', 'ô']
nb_bicaracteres= 141
bicaracteres= ['e ', 's ', 't ', 'es', ' d', '\r\n', 'en', 'qu', ' l', 're', ' p', 'de', 'le', 'nt', 'on', ' c', ', ', ' e', 'ou', ' q', ' s', 'n ', 'ue', 'an', 'te', ' a', 'ai', 'se', 'it', 'me', 'is', 'oi', 'r ', 'er', ' m', 'ce', 'ne', 'et', 'in', 'ns', ' n', 'ur', 'i ', 'a ', 'eu', 'co', 'tr', 'la', 'ar', 'ie', 'ui', 'us', 'ut', 'il', ' t', 'pa', 'au', 'el', 'ti', 'st', 'un', 'em', 'ra', 'e,', 'so', 'or', 'l ', ' f', 'll', 'nd', ' j', 'si', 'ir', 'e\r', 'ss', 'u ', 'po', 'ro', 'ri', 'pr', 's,', 'ma', ' v', ' i', 'di', ' r', 'vo', 'pe', 'to', 'ch', '. ', 've', 'nc', 'om', ' o', 'je', 'no', 'rt', 'à ', 'lu', "'e", 'mo', 'ta', 'as', 'at', 'io', 's\r', 'sa', "u'", 'av', 'os', ' à', ' u', "l'", "'a", 'rs', 'pl', 'é ', '; ', 'ho', 'té', 'ét', 'fa', 'da', 'li', 'su', 't\r', 'ée', 'ré', 'dé', 'ec', 'nn', 'mm', "'i", 'ca', 'uv', '\n\r', 'id', ' b', 'ni', 'bl']
symboles = ['b', 'j', '\r', 'J', '”', ')', 'Â', 'É', 'ê', '5', 't', '9', 'Y', '%', 'N', 'B', 'V', '\ufeff', 'Ê', '?', '’', 'i', ':', 's', 'C', 'â', 'ï', 'W', 'y', 'p', 'D', '—', '«', 'º', 'A', '3', 'n', '0', 'q', '4', 'e', 'T', 'È', '$', 'U', 'v', '»', 'l', 'P', 'X', 'Z', 'À', 'ç', 'u', '…', 'î', 'L', 'k', 'E', 'R', '2', '_', '8', 'é', 'O', 'Î', '‘', 'a', 'F', 'H', 'c', '[', '(', "'", 'è', 'I', '/', '!', ' ', '°', 'S', '•', '#', 'x', 'à', 'g', '*', 'Q', 'w', '1', 'û', '7', 'G', 'm', '™', 'K', 'z', '\n', 'o', 'ù', ',', 'r', ']', '.', 'M', 'Ç', '“', 'h', '-', 'f', 'ë', '6', ';', 'd', 'ô', 'e ', 's ', 't ', 'es', ' d', '\r\n', 'en', 'qu', ' l', 're', ' p', 'de', 'le', 'nt', 'on', ' c', ', ', ' e', 'ou', ' q', ' s', 'n ', 'ue', 'an', 'te', ' a', 'ai', 'se', 'it', 'me', 'is', 'oi', 'r ', 'er', ' m', 'ce', 'ne', 'et', 'in', 'ns', ' n', 'ur', 'i ', 'a ', 'eu', 'co', 'tr', 'la', 'ar', 'ie', 'ui', 'us', 'ut', 'il', ' t', 'pa', 'au', 'el', 'ti', 'st', 'un', 'em', 'ra', 'e,', 'so', 'or', 'l ', ' f', 'll', 'nd', ' j', 'si', 'ir', 'e\r', 'ss', 'u ', 'po', 'ro', 'ri', 'pr', 's,', 'ma', ' v', ' i', 'di', ' r', 'vo', 'pe', 'to', 'ch', '. ', 've', 'nc', 'om', ' o', 'je', 'no', 'rt', 'à ', 'lu', "'e", 'mo', 'ta', 'as', 'at', 'io', 's\r', 'sa', "u'", 'av', 'os', ' à', ' u', "l'", "'a", 'rs', 'pl', 'é ', '; ', 'ho', 'té', 'ét', 'fa', 'da', 'li', 'su', 't\r', 'ée', 'ré', 'dé', 'ec', 'nn', 'mm', "'i", 'ca', 'uv', '\n\r', 'id', ' b', 'ni', 'bl']

def compter_frequences(texte, symboles):
    compteur = Counter()
    for symbole in symboles:
        compteur[symbole] = texte.count(symbole)
    return compteur


def calculer_frequences_relatives(compteur, total):
    return {symbole: compte / total for symbole, compte in compteur.items()}


def calculer_frequences_moyennes(urls, symboles):
    compteur_global = Counter()
    total_global = 0

    for url in urls:
        texte = load_text_from_web(url)
        if texte:
            compteur = compter_frequences(texte, symboles)
            total = sum(compteur.values())
            compteur_global.update(compteur)
            total_global += total

    frequences_moyennes = calculer_frequences_relatives(compteur_global, total_global)
    return frequences_moyennes

#Analyse les fréquences des séquences de longueur donnée dans le texte chiffré.
def analyser_frequences_chiffrees(C,longueur_sequence=8):
    compteur = Counter()
    for i in range(0, len(C), longueur_sequence):
        segment = C[i:i + longueur_sequence]
        compteur[segment] += 1
    total = sum(compteur.values())
    frequences_chiffrees = {segment: count / total for segment, count in compteur.items()}
    return frequences_chiffrees

#Associe les séquences chiffrées aux symboles français basés sur leurs fréquences.
def construire_dictionnaire_dechiffrement(freq_chiffrees, freq_moyennes):
    # Trier les séquences chiffrées par fréquence décroissante
    sequences_tries = [k for k, v in sorted(freq_chiffrees.items(), key=lambda x: x[1], reverse=True)]

    # Trier les symboles français par fréquence décroissante
    symboles_tries = [k for k, v in sorted(freq_moyennes.items(), key=lambda x: x[1], reverse=True)]

    # Créer le dictionnaire de correspondance
    dictionnaire_dechiffrement = {seq: sym for seq, sym in zip(sequences_tries, symboles_tries)}
    return dictionnaire_dechiffrement

#Calcule la qualité du code déchiffré
def qualite_decrypt_text(M, dictionnaire_dechiffrement):
    score = 0
    for symbol in M:
        score+= dictionnaire_dechiffrement.get(symbol,0)
    return score

#Utilise l'attaque probabilistique pour trouver la meilleure clé(?)
def attack_proba(C, dictionnaire_dechiffrement, max_iteration=3):
    global key_now
    best_key = key_now.copy()
    best_score = qualite_decrypt_text(decrypt(C), dictionnaire_dechiffrement)

    for _ in range(max_iteration):
            nouvelle_key = best_key.copy()
            i,j = rnd.sample(list(best_key.keys()),2)
            nouvelle_key[i],nouvelle_key[j] = nouvelle_key[j],nouvelle_key[i]

            key_now = nouvelle_key
            M = decrypt(C)
            nouveau_score = qualite_decrypt_text(M,dictionnaire_dechiffrement)

            if nouveau_score > best_score:
                best_key, best_score = nouvelle_key, nouveau_score
            else:
                key_now= best_key

    key_now = best_key

def initialise_decrypt_key(C):
    # Listes des URLs pour calculer les fréquences moyennes
    urls = [
        "https://www.gutenberg.org/ebooks/135.txt.utf-8",  # Les Misérables - Victor Hugo
        "https://www.gutenberg.org/ebooks/19942.txt.utf-8",  # Candide - Voltaire
        "https://www.gutenberg.org/cache/epub/5423/pg5423.txt",
        "https://www.gutenberg.org/cache/epub/6318/pg6318.txt",
        "https://www.gutenberg.org/cache/epub/58698/pg58698.txt",
        "https://www.gutenberg.org/cache/epub/63144/pg63144.txt",
        "https://www.gutenberg.org/cache/epub/54873/pg54873.txt",
        "https://www.gutenberg.org/cache/epub/41211/pg41211.txt",
        "https://www.gutenberg.org/cache/epub/70891/pg70891.txt",
        "https://www.gutenberg.org/cache/epub/20262/pg20262.txt"
        #possible d'ajouter d'autres urls pour plus de précision sur la fréquence des symboles
    ]
    frequences_moyennes = calculer_frequences_moyennes(urls, symboles)
    freq_chiffrees = analyser_frequences_chiffrees(C)
    global key_now
    key_now = construire_dictionnaire_dechiffrement(freq_chiffrees, frequences_moyennes)

def decrypt(C):
    # Initialiser la clé de déchiffrement
    initialise_decrypt_key(C)

    dictionnaire_dechiffrement = key_now.copy()

    attack_proba( C, dictionnaire_dechiffrement, 3)

    M = ""
    segment_length = 8
    for i in range(0, len(C), segment_length):
        segment = C[i:i + segment_length]
        M += key_now.get(segment, '?')
    return M

#Inclure le cryptogramme ici
C = "11010101011011000111010011001111000011100110110011001111110011000000110111001010010111010111111011001100011011001100111101101100011000011100111100001110011011001100111111001100000011011100101001011101011111101100110001101100011101001100111100001110011011001100111100111111000100100000011000111101000100100110110011001111011011000110000110010101000011000000111001101100110011110010000011001110011000010110110001110100110011110000111001101100110011110010000011001110011000010110110011001111011011000110000111001111000011100110110011001111001111110001001000000110001111010001001001101100011111001100111101011010001011011100101011001111011011001101010111001111"
C= C[:100]
decrypted_text= decrypt(C)
print(decrypted_text)
