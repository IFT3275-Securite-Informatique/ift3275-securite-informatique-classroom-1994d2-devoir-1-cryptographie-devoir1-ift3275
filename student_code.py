# Devoir1 IFT3275

#Auteur: Yongkang He  20220607
#Auteur: Wanting Teng 20179470

import random
import time
from collections import Counter
import requests
from langdetect import detect, DetectorFactory, LangDetectException
import random as rnd
import re

# Set seed for langdetect to make its results deterministic
DetectorFactory.seed = 0

# Define helper functions
def load_text_from_web(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.text
    except requests.exceptions.RequestException as e:
        return None

def cut_string_into_pairs(text):
    pairs = []
    for i in range(0, len(text) - 1, 2):
        pairs.append(text[i:i + 2])
    if len(text) % 2 != 0:
        pairs.append(text[-1] + '_')  # Add a placeholder if the string has an odd number of characters
    return pairs


# Fonction pour vérifier que seuls certains peuvent être d'un espace
# seuil de 5
def has_valid_single_char_words(text):
    words = text.split()
    single_char_words = set()

    for word in words:
        # Vérifie si le mot de longueur 1 n'est pas dans les caractères autorisés
        if len(word) == 1 and word not in {'à', 'y', 'À', 'ô'} and \
                word.lower() not in 'abcdefghijklmnopqrstuvwxyz' and \
                word not in '0123456789':  # Ajout des chiffres 0-9
            single_char_words.add(word)

            if len(single_char_words) > 5:
                return False
    return True

# Fonction pour vérifier que les mots ne dépassent pas 25 lettres
# seuil de 5
def has_no_long_words(text):
    words = text.split()
    long_words = set()

    for word in words:
        if len(word) > 25:
            long_words.add(word)
            if len(long_words) > 5:
                return False

    return True


# Fonction pour vérifier la présence de majuscules au milieu d'une phrase
# mais accepter les mots entièrement en majuscules
# seuil de 20
def has_mid_sentence_capitals(text):
    words = text.split()
    count_invalid_capitals = 0

    for word in words:
        # Vérifie les mots qui ne sont pas entièrement en majuscules
        if not word.isupper():
            for i in range(1, len(word)):
                # Si une majuscule est trouvée après le premier caractère
                if word[i].isupper():
                    # Ignore la majuscule si elle se trouve juste après une apostrophe ou un soulignement
                    if word[i - 1] in {'’', '_', '-', '—', '(', '«'}:
                        continue
                    count_invalid_capitals += 1
                    print(f"Invalid capital found: '{word}'")

                    if count_invalid_capitals > 20:
                        return True
    return False


# Fonction pour vérifier s'il y a un espace après la ponctuation (virgule, point, point-virgule, etc ...)
# seuil de 20
def has_proper_spacing_after_punctuation(text):
    punctuation_marks = {',', '.', ';', '!', '?'}
    error_count = 0  # Compteur d'erreurs d'espacement

    for i in range(len(text) - 1):
        # Vérifie les signes de ponctuation simples
        if text[i] in punctuation_marks and text[i + 1].isprintable() and text[i + 1] not in {' ', '—', '_', ',', '.',
                                                                                              '-', '»', ')', '\n'}:
            print(f"Improper spacing after punctuation: '{text[i]}' followed by '{text[i + 1]}' at position {i}")
            error_count += 1
            if error_count >= 20:
                return False

        # Vérifie les points de suspension (...)
        if text[i:i + 3] == '...' and (i + 3 < len(text)) and text[i + 3].isprintable() and text[i + 3] not in {' ',
                                                                                                                '-',
                                                                                                                '\n'}:
            print(f"Improper spacing after ellipsis: '...' followed by '{text[i + 3]}' at position {i}")
            error_count += 1
            if error_count >= 20:
                return False
    return True


# Fonction pour vérifier les séquences de ponctuation incorrectes
# seuil de 3
def has_invalid_punctuation_sequences(text):
    count = 0
    matches = re.finditer(r'[^\w\s]{4,}', text)  # Trouve toutes les occurrences de 4+ ponctuations consécutives

    for match in matches:
        count += 1
        if count > 3:
            return True
        print(f"Invalid punctuation sequence found: {match.group(0)}")

    return False


# Fonction pour vérifier s'il y a plusieurs espaces consécutifs
# seuil de 5
def has_multiple_spaces(text):
    count = 0
    index = 0

    # Parcourt le texte pour trouver des occurrences de doubles espaces
    while index < len(text) - 1:
        # Vérifie s'il y a deux espaces consécutifs
        if text[index] == ' ' and text[index + 1] == ' ':
            count += 1

            if count >= 5:
                print("plusieurs multiples spaces")
                return True

            # Avance l'index pour éviter de compter les espaces superposés plusieurs fois
            index += 2
        else:
            index += 1

    return False

# Fonction pour tester les deux cas si necessaire
def meilleurOption(val):
    temps = time.time()
    temps_int = int(temps)
    result1 = methode2(val, 0, 20000)

    if result1 is None:
        result1 = methode2(val, temps_int - 3000, temps_int + 3000)
    return result1


# Fonction pour decrypter C si la methode frequence prend trop de temps
def methode2(encrypted_text,initial,final):
    symboles = ['b', 'j', '\r', 'J', '”', ')', 'Â', 'É', 'ê', '5', 't', '9', 'Y', '%', 'N', 'B', 'V', '\ufeff', 'Ê',
                '!', '’', 'i', ':', 's', 'C', 'â', 'ï', 'W', 'y', 'p', 'D', '—', '«', 'º', 'A', '3', 'n', '0', 'q', '4',
                'e', 'T', 'È', '$', 'U', 'v', '»', 'l', 'P', 'X', 'Z', 'À', 'ç', 'u', '…', 'î', 'L', 'k', 'E', 'R', '2',
                '_', '8', 'é', 'O', 'Î', '‘', 'a', 'F', 'H', 'c', '[', '(', "'", 'è', 'I', '/', '?', ' ', '°', 'S', '•',
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

    # Fonction pour générer la clé de dictionnaire
    def gen_key2(symbols, seed):
        rnd.seed(seed)
        l = len(symbols)
        int_keys = rnd.sample(list(range(l)), l)
        dictionary = {s: "{:08b}".format(k) for s, k in zip(symbols, int_keys)}
        return dictionary

    for seed in range(initial, final, 1):
        # Génère la clé avec la graine actuelle
        dictionary = gen_key2(symboles, seed)
        reverse_dict = {v: k for k, v in dictionary.items()}

        try:
            decrypted_text = ''.join([reverse_dict[encrypted_text[i:i + 8]] for i in range(0, len(encrypted_text), 8)])

            # Vérifie la langue et les conditions de validation
            try:
                language = detect(decrypted_text)
                if (language == 'fr' and
                        has_no_long_words(decrypted_text) and  # moins de 25 de long
                        has_valid_single_char_words(decrypted_text)   # mots valide dun espace
                        # not has_mid_sentence_capitals(decrypted_text) and  # pas de majuscule au milieu sauf si tout majuscule
                        # has_proper_spacing_after_punctuation(decrypted_text) and  # space apres ponctuation
                        # not has_multiple_spaces(decrypted_text) and  # pas plusieurs espaces
                        # not has_invalid_punctuation_sequences(decrypted_text)
                ):
                    return decrypted_text
            except LangDetectException:
                continue

        except KeyError:
            continue

    return None




def decrypt(cryptogram):
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

    # Nombre total de symboles et codes possibles
    num_symbols = len(symboles)
    code_length = 8

    # Extraire les codes du cryptogramme
    cryptogram_codes = [cryptogram[i:i+code_length] for i in range(0, len(cryptogram), code_length)]
    codes_list = list(set(cryptogram_codes))

    # Construire la fréquence des codes dans le cryptogramme
    code_freq = Counter(cryptogram_codes)
    codes_by_freq = [code for code, _ in code_freq.most_common()]

    # Construire les distributions de fréquence à partir d'un texte français
    # Pour l'estimation initiale de la fréquence des symboles
    url1 = "https://www.gutenberg.org/ebooks/13846.txt.utf-8"
    url2 = "https://www.gutenberg.org/ebooks/4650.txt.utf-8"

    # Charger les textes depuis les URL fournies
    corpus1 = load_text_from_web(url1) or ""
    corpus2 = load_text_from_web(url2) or ""
    corpus = corpus1 + corpus2

    # Construire le dictionnaire de paires (identique à celui de l'encryption)
    nb_caracteres = len(set(corpus))
    nb_bicaracteres = 256 - nb_caracteres
    bicaracteres = [item for item, _ in Counter(cut_string_into_pairs(corpus)).most_common(nb_bicaracteres)]
    dictionaire = {pair: True for pair in bicaracteres}

    # Fonction de prétraitement du corpus
    def preprocess_corpus(corpus, symboles, dictionaire):
        symbols = []
        i = 0
        while i < len(corpus):
            if i + 1 < len(corpus):
                pair = corpus[i] + corpus[i + 1]
                if pair in dictionaire:
                    symbols.append(pair)
                    i += 2
                    continue
            if corpus[i] in symboles:
                symbols.append(corpus[i])
            else:
                symbols.append(corpus[i])
            i += 1
        return symbols

    # Appliquer le prétraitement du corpus
    corpus_symbols = preprocess_corpus(corpus, symboles, dictionaire)

    # Construire la fréquence des symboles dans le corpus
    symbol_freq = Counter(corpus_symbols)
    symbols_by_freq = [symbol for symbol, _ in symbol_freq.most_common()]

    # Mapping initial basé sur l'analyse de fréquence
    initial_mapping = dict(zip(codes_by_freq, symbols_by_freq[:len(codes_by_freq)]))

    # Fonction d'aide pour décoder le cryptogramme en utilisant un mapping
    def decode_cryptogram(mapping):
        decoded_symbols = []
        for code in cryptogram_codes:
            symbol = mapping.get(code, '')
            decoded_symbols.append(symbol)
        return decoded_symbols

    # Fonction de validation pour vérifier si le texte décrypté respecte les critères
    def is_valid_text(text):
        try:
            detected_language = detect(text)
            if detected_language != 'fr':
                return False
        except:
            return False

        # extra validation
        if not has_valid_single_char_words(text):
            return False
        if not has_no_long_words(text):
            return False

        return True



    # Début du processus de décryptage
    time_limit = 1200  # Limite de temps en secondes
    start_time = time.time()

    best_mapping = initial_mapping.copy()
    best_decoded = decode_cryptogram(best_mapping)
    decrypted_message = ''.join(best_decoded)

    # Vérifier si le message décrypté est valide
    if is_valid_text(decrypted_message):
        return decrypted_message



    # Initialisation de l'ensemble pour stocker les mappings déjà tentés
    attempted_mappings = set()

    # Fonction pour séparer les symboles en trois groupes : low, medium, high
    # aide a augmenter la vitesse de solution mais diminue la similarity
    def split_symbols_by_count(symbols_by_freq, high_count=226, medium_count=10):
        # Séparer les symboles en trois groupes : low, medium et high
        high_group = symbols_by_freq[:high_count]
        medium_group = symbols_by_freq[high_count:high_count + medium_count]
        low_group = symbols_by_freq[high_count + medium_count:]

        return low_group, medium_group, high_group

    # Séparer les symboles en trois groupes
    low_group, medium_group, high_group = split_symbols_by_count(symbols_by_freq)

    # Si le mapping initial ne donne pas un texte valide, essayer de trouver un mapping valide
    max_attempts = 30000  # Nombre maximum de tentatives
    attempts = 0

    while time.time() - start_time < time_limit and attempts < max_attempts:
        attempts += 1

        # Mélanger les trois groupes séparément
        random.shuffle(high_group)
        random.shuffle(medium_group)
        random.shuffle(low_group)

        # Créer un nouveau mapping en combinant les groupes mélangés
        shuffled_symbols = high_group + medium_group + low_group
        new_mapping = tuple(
            zip(codes_by_freq, shuffled_symbols[:len(codes_by_freq)]))  # Utiliser un tuple pour être hashable

        # Vérifier si ce mapping a déjà été essayé
        if new_mapping in attempted_mappings:
            continue  # Si ce mapping a déjà été essayé, passer à la tentative suivante

        # Ajouter le mapping à l'ensemble des tentatives
        attempted_mappings.add(new_mapping)

        # Décoder avec le nouveau mapping
        decoded_symbols = decode_cryptogram(dict(new_mapping))
        decrypted_message = ''.join(decoded_symbols)
        #print(decrypted_message)
        #print("-----------------")
        #print(attempts)

        if is_valid_text(decrypted_message):
            print("-----------------")
            return decrypted_message

    print("---------------")
    # si ca depasse le temps, on essaye un autre methode
    return meilleurOption(cryptogram)