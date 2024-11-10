from crypt import *
import random as rnd
import math
import requests
from collections import Counter


key_now ={}

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


def analyser_frequences_chiffrees(C, longueur_sequence=8):
    """
    Analyse les fréquences des séquences de longueur donnée dans le texte chiffré.
    """
    compteur = Counter()
    for i in range(0, len(C), longueur_sequence):
        segment = C[i:i + longueur_sequence]
        compteur[segment] += 1
    total = sum(compteur.values())
    frequences_chiffrees = {segment: count / total for segment, count in compteur.items()}
    return frequences_chiffrees


def construire_dictionnaire_dechiffrement(freq_chiffrees, freq_moyennes):
    """
    Associe les séquences chiffrées aux symboles français basés sur leurs fréquences.
    """
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

def attack_proba(C, dictionnaire_dechiffrement, max_iteration=1000):
    global key_now
    best_key = key_now.copy()
    best_score = qualite_decrypt_text(decrypt(C), dictionnaire_dechiffrement)

#Algorithme de annealing pour trouver la meilleure clé (voir le pdf soumis pour les sources)
    t= 1.0
    t_min = 0.00001
    alpha = 0.9

    while t>t_min:
        for _ in range(max_iteration):
            nouvelle_key = best_key.copy()
            i,j = rnd.sample(list(best_key.keys()),2)
            nouvelle_key[i],nouvelle_key[j] = nouvelle_key[j],nouvelle_key[i]

            key_now = nouvelle_key
            M = decrypt(C)
            nouveau_score = qualite_decrypt_text(M,dictionnaire_dechiffrement)

            if nouveau_score > best_score or math.exp((nouveau_score - best_score) / t) > rnd.random():
                best_key, best_score = nouvelle_key, nouveau_score
            else:
                key_now= best_key

        t *= alpha

    key_now = best_key


def initialise_decrypt_key(C,symboles):
    # Générer le dictionnaire dynamiquement
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
    symboles_fixes = symboles
    frequences_moyennes = calculer_frequences_moyennes(urls, symboles_fixes)
    freq_chiffrees = analyser_frequences_chiffrees(C)
    global key_now
    key_now = construire_dictionnaire_dechiffrement(freq_chiffrees, frequences_moyennes)



def decrypt(C):

    #Initialiser la clé de déchiffrement
    initialise_decrypt_key(C)

    dictionnaire_dechiffrement = construire_dictionnaire_dechiffrement(calculer_frequences_moyennes(symboles), analyser_frequences_chiffrees(C))

    attack_proba(C, dictionnaire_dechiffrement,1000)

    M=""
    segment_length = 8
    for i in range(0, len(C), segment_length):
        segment = C[i:i+segment_length]
        M+= key_now.get(segment,'?')
    return M
