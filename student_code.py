from crypt import *

key_now = {}
#Générer la liste de symboles (assumant qu'on doit utiliser les uni et bisymboles fixées par le professeur)
def list_fixed_symboles():
    urls= ["https://www.gutenberg.org/ebooks/13846.txt.utf-8",
        "https://www.gutenberg.org/ebooks/4650.txt.utf-8"]
    text = ""
    for url in urls:
        text_loader = load_text_from_web(url)
        if text_loader:
            text += text_loader

    caracteres = list(set(list(text)))
    nb_caracteres = len(caracteres)
    nb_bicaracteres = 256 - nb_caracteres
    bicaracteres = [item for item, _ in Counter(cut_string_into_pairs(text)).most_common(nb_bicaracteres)]
    symboles = caracteres + bicaracteres
    return symboles
symboles= list_fixed_symboles()

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
def analyser_frequences_chiffrees(C, longueur_sequence=8):
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
    for i in range(len(M)-1):
        symbol = M[i]
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
    frequences_moyennes = calculer_frequences_moyennes(urls, list_fixed_symboles())
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
C = "Cryptogramme quel conque donné"
decrypted_text= decrypt(C)
print(decrypted_text)
