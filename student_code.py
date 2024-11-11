from collections import Counter
import math
import random
from crypt_1 import chiffrer, chiffrer2, cut_string_into_pairs, gen_key, load_text_from_web

import string

# Inclure les lettres minuscules, les lettres majuscules et l'espace
symboles = list(string.ascii_lowercase + string.ascii_uppercase + ' ')

import math
import random
from collections import Counter
import requests
import time

def load_text_from_web(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du chargement du texte : {e}")
        return ""

def cut_string_into_pairs(text):
    pairs = []
    for i in range(0, len(text) - 1, 2):
        pairs.append(text[i:i + 2])
    if len(text) % 2 != 0:
        pairs.append(text[-1] + '_')
    return pairs

def gen_key(symboles):
    l = len(symboles)
    if l > 256:
        return False
    random.seed(1337)
    int_keys = random.sample(list(range(256)), l)
    dictionary = dict({})
    for s, k in zip(symboles, int_keys):
        dictionary[s] = "{:08b}".format(k)
    return dictionary

def chiffrer(M, K):
    encoded_text = []
    i = 0
    while i < len(M):
        # Vérifier les bigrammes
        if i + 1 < len(M):
            pair = M[i] + M[i + 1]
            if pair in K:
                encoded_text.append(K[pair])
                i += 2
                continue
        # Vérifier les monogrammes
        if M[i] in K:
            encoded_text.append(K[M[i]])
        else:
            # Ignorer les symboles inconnus
            pass
        i += 1
    return ''.join(encoded_text)

def decrypt(C):
    import math
    import random
    from collections import Counter

    # Votre ensemble de symboles spécifique
    symboles = ['b', 'j', '\r', 'J', '”', ')', 'Â', 'É', 'ê', '5', 't', '9', 'Y', '%', 'N', 'B', 'V', '\ufeff', 'Ê', '?', '’', 'i', ':', 's', 'C', 'â', 'ï', 'W', 'y', 'p', 'D', '—', '«', 'º', 'A', '3', 'n', '0', 'q', '4', 'e', 'T', 'È', '$', 'U', 'v', '»', 'l', 'P', 'X', 'Z', 'À', 'ç', 'u', '…', 'î', 'L', 'k', 'E', 'R', '2', '_', '8', 'é', 'O', 'Î', '‘', 'a', 'F', 'H', 'c', '[', '(', "'", 'è', 'I', '/', '!', ' ', '°', 'S', '•', '#', 'x', 'à', 'g', '*', 'Q', 'w', '1', 'û', '7', 'G', 'm', '™', 'K', 'z', '\n', 'o', 'ù', ',', 'r', ']', '.', 'M', 'Ç', '“', 'h', '-', 'f', 'ë', '6', ';', 'd', 'ô', 'e ', 's ', 't ', 'es', ' d', '\r\n', 'en', 'qu', ' l', 're', ' p', 'de', 'le', 'nt', 'on', ' c', ', ', ' e', 'ou', ' q', ' s', 'n ', 'ue', 'an', 'te', ' a', 'ai', 'se', 'it', 'me', 'is', 'oi', 'r ', 'er', ' m', 'ce', 'ne', 'et', 'in', 'ns', ' n', 'ur', 'i ', 'a ', 'eu', 'co', 'tr', 'la', 'ar', 'ie', 'ui', 'us', 'ut', 'il', ' t', 'pa', 'au', 'el', 'ti', 'st', 'un', 'em', 'ra', 'e,', 'so', 'or', 'l ', ' f', 'll', 'nd', ' j', 'si', 'ir', 'e\r', 'ss', 'u ', 'po', 'ro', 'ri', 'pr', 's,', 'ma', ' v', ' i', 'di', ' r', 'vo', 'pe', 'to', 'ch', '. ', 've', 'nc', 'om', ' o', 'je', 'no', 'rt', 'à ', 'lu', "'e", 'mo', 'ta', 'as', 'at', 'io', 's\r', 'sa', "u'", 'av', 'os', ' à', ' u', "l'", "'a", 'rs', 'pl', 'é ', '; ', 'ho', 'té', 'ét', 'fa', 'da', 'li', 'su', 't\r', 'ée', 'ré', 'dé', 'ec', 'nn', 'mm', "'i", 'ca', 'uv', '\n\r', 'id', ' b', 'ni', 'bl']

    # Charger le corpus
    urls = [
        "https://www.gutenberg.org/ebooks/13846.txt.utf-8",
        "https://www.gutenberg.org/ebooks/4650.txt.utf-8",
    ]
    corpus = ""
    for url in urls:
        corpus += load_text_from_web(url)

    # Calculer les fréquences des symboles dans le corpus
    symbol_counts = Counter()
    i = 0
    while i < len(corpus):
        # Vérifier les bigrammes
        if i + 1 < len(corpus):
            pair = corpus[i] + corpus[i + 1]
            if pair in symboles:
                symbol_counts[pair] += 1
                i += 2
                continue
        # Vérifier les monogrammes
        if corpus[i] in symboles:
            symbol_counts[corpus[i]] += 1
        i += 1

    total_symbols = sum(symbol_counts.values())
    symbol_freqs = {symbol: count / total_symbols for symbol, count in symbol_counts.items()}

    # Diviser le cryptogramme en codes de 8 bits
    codes = [C[i:i + 8] for i in range(0, len(C), 8)]

    # Calculer les fréquences des codes
    code_counts = Counter(codes)
    total_codes = len(codes)
    code_freqs = {code: count / total_codes for code, count in code_counts.items()}

    # Établir un mapping initial basé sur les fréquences
    sorted_symbols = [symbol for symbol, _ in symbol_counts.most_common()]
    sorted_codes = [code for code, _ in code_counts.most_common()]

    # Fixer les mappings pour les symboles les plus fréquents
    fixed_mappings = {}
    num_fixed = int(len(symboles) * 0.1)  # Fixer 10% des symboles les plus fréquents
    for i in range(num_fixed):
        fixed_mappings[sorted_codes[i]] = sorted_symbols[i]

    # Créer le mapping initial en respectant les mappings fixes
    remaining_codes = sorted_codes[num_fixed:]
    remaining_symbols = sorted_symbols[num_fixed:]
    initial_mapping = fixed_mappings.copy()
    initial_mapping.update(dict(zip(remaining_codes, remaining_symbols)))

    # Fonction pour déchiffrer avec un mapping donné
    def decrypt_with_mapping(codes, mapping):
        decrypted_symbols = [mapping.get(code, '') for code in codes]
        plaintext = ''.join(decrypted_symbols)
        return plaintext

    # Construire un modèle de langue basé sur les 5-grammes
    def build_ngram_model(corpus_text, n=5):
        ngram_counts = Counter()
        total_ngrams = 0
        for i in range(len(corpus_text) - n + 1):
            ngram = corpus_text[i:i + n]
            if all(char in symboles for char in ngram):
                ngram_counts[ngram] += 1
                total_ngrams += 1
        return ngram_counts, total_ngrams

    ngram_counts, total_ngrams = build_ngram_model(corpus, n=5)

    # Fonction pour évaluer le texte déchiffré
    def score_text(text, ngram_counts, total_ngrams):
        score = 0
        n = 5
        for i in range(len(text) - n + 1):
            ngram = text[i:i + n]
            if ngram in ngram_counts:
                score += math.log(ngram_counts[ngram] / total_ngrams)
            else:
                score += math.log(1e-9)  # Pénalité pour les n-grammes inconnus
        return score

    # Algorithme génétique combiné avec recuit simulé
    def genetic_algorithm(codes, initial_mapping, ngram_counts, total_ngrams, population_size=100, generations=1000, mutation_rate=0.1):
        # Initialiser la population
        population = []
        for _ in range(population_size):
            mapping = initial_mapping.copy()
            codes_to_shuffle = [code for code in mapping if code not in fixed_mappings]
            random.shuffle(codes_to_shuffle)
            symbols_to_assign = [symbol for symbol in symboles if symbol not in fixed_mappings.values()]
            mapping.update(dict(zip(codes_to_shuffle, symbols_to_assign)))
            population.append(mapping)

        best_mapping = None
        best_score = float('-inf')

        for generation in range(generations):
            scored_population = []
            for mapping in population:
                decrypted_text = decrypt_with_mapping(codes, mapping)
                score = score_text(decrypted_text, ngram_counts, total_ngrams)
                scored_population.append((score, mapping))

            # Trier la population par score décroissant
            scored_population.sort(reverse=True, key=lambda x: x[0])

            # Garder les meilleurs mappings
            population = [mapping for _, mapping in scored_population[:population_size // 2]]

            # Mettre à jour le meilleur score
            if scored_population[0][0] > best_score:
                best_score = scored_population[0][0]
                best_mapping = scored_population[0][1]
                # Optionnel : afficher les améliorations
                print(f"Génération {generation}: Meilleur score = {best_score}")

            # Croisement et mutation
            new_population = population.copy()
            while len(new_population) < population_size:
                parent1 = random.choice(population)
                parent2 = random.choice(population)
                child = crossover(parent1, parent2)
                child = mutate(child, mutation_rate)
                new_population.append(child)
            population = new_population

        return decrypt_with_mapping(codes, best_mapping)

    def crossover(parent1, parent2):
        child = fixed_mappings.copy()
        codes_to_assign = [code for code in parent1 if code not in fixed_mappings]
        split = random.randint(0, len(codes_to_assign))
        for code in codes_to_assign[:split]:
            child[code] = parent1[code]
        for code in codes_to_assign[split:]:
            child[code] = parent2[code]
        return child

    def mutate(mapping, rate):
        mapping = mapping.copy()
        codes_to_mutate = [code for code in mapping if code not in fixed_mappings]
        for code in codes_to_mutate:
            if random.random() < rate:
                other_code = random.choice(codes_to_mutate)
                mapping[code], mapping[other_code] = mapping[other_code], mapping[code]
        return mapping

    # Appliquer l'algorithme génétique
    M = genetic_algorithm(codes, initial_mapping, ngram_counts, total_ngrams)

    return M

# --- Code principal ---

# Votre ensemble de symboles spécifique
symboles = ['b', 'j', '\r', 'J', '”', ')', 'Â', 'É', 'ê', '5', 't', '9', 'Y', '%', 'N', 'B', 'V', '\ufeff', 'Ê', '?', '’', 'i', ':', 's', 'C', 'â', 'ï', 'W', 'y', 'p', 'D', '—', '«', 'º', 'A', '3', 'n', '0', 'q', '4', 'e', 'T', 'È', '$', 'U', 'v', '»', 'l', 'P', 'X', 'Z', 'À', 'ç', 'u', '…', 'î', 'L', 'k', 'E', 'R', '2', '_', '8', 'é', 'O', 'Î', '‘', 'a', 'F', 'H', 'c', '[', '(', "'", 'è', 'I', '/', '!', ' ', '°', 'S', '•', '#', 'x', 'à', 'g', '*', 'Q', 'w', '1', 'û', '7', 'G', 'm', '™', 'K', 'z', '\n', 'o', 'ù', ',', 'r', ']', '.', 'M', 'Ç', '“', 'h', '-', 'f', 'ë', '6', ';', 'd', 'ô', 'e ', 's ', 't ', 'es', ' d', '\r\n', 'en', 'qu', ' l', 're', ' p', 'de', 'le', 'nt', 'on', ' c', ', ', ' e', 'ou', ' q', ' s', 'n ', 'ue', 'an', 'te', ' a', 'ai', 'se', 'it', 'me', 'is', 'oi', 'r ', 'er', ' m', 'ce', 'ne', 'et', 'in', 'ns', ' n', 'ur', 'i ', 'a ', 'eu', 'co', 'tr', 'la', 'ar', 'ie', 'ui', 'us', 'ut', 'il', ' t', 'pa', 'au', 'el', 'ti', 'st', 'un', 'em', 'ra', 'e,', 'so', 'or', 'l ', ' f', 'll', 'nd', ' j', 'si', 'ir', 'e\r', 'ss', 'u ', 'po', 'ro', 'ri', 'pr', 's,', 'ma', ' v', ' i', 'di', ' r', 'vo', 'pe', 'to', 'ch', '. ', 've', 'nc', 'om', ' o', 'je', 'no', 'rt', 'à ', 'lu', "'e", 'mo', 'ta', 'as', 'at', 'io', 's\r', 'sa', "u'", 'av', 'os', ' à', ' u', "l'", "'a", 'rs', 'pl', 'é ', '; ', 'ho', 'té', 'ét', 'fa', 'da', 'li', 'su', 't\r', 'ée', 'ré', 'dé', 'ec', 'nn', 'mm', "'i", 'ca', 'uv', '\n\r', 'id', ' b', 'ni', 'bl']

# Génération de la clé
K = gen_key(symboles)

# Charger le corpus pour sélectionner le message à chiffrer
urls = [
    "https://www.gutenberg.org/ebooks/13846.txt.utf-8",
    "https://www.gutenberg.org/ebooks/4650.txt.utf-8",
]
corpus = ""
for url in urls:
    corpus += load_text_from_web(url)

# Sélection du message à chiffrer
random.seed(time.time())
c = random.randint(0, len(corpus) - 1000)
l = 1000  # Vous pouvez ajuster la longueur pour des tests plus rapides
M = corpus[c:c+l]

# Chiffrement du message
C = chiffrer(M, K)

# Déchiffrement du message
message_dechiffre = decrypt(C)

# Calcul de la similarité
from difflib import SequenceMatcher

similarity = SequenceMatcher(None, M, message_dechiffre).ratio()
print(f"Similarité : {similarity:.2%}")

# Affichage du résultat si la similarité est supérieure à 50%
if similarity >= 0.5:
    print("Message déchiffré :")
    print(message_dechiffre)
else:
    print("Le déchiffrement n'a pas atteint une similarité de 50%.")

# Affichage du message original pour comparaison
print("\nMessage original :")
print(M)
