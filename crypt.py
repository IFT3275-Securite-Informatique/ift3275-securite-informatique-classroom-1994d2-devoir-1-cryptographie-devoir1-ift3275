import math
import random as rnd
import numpy as np
import requests
from collections import Counter

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

def gen_key(symboles):

  l=len(symboles)
  if l > 256:
    return False

  rnd.seed(1337)
  int_keys = rnd.sample(list(range(l)),l)
  dictionary = dict({})
  for s,k in zip(symboles,int_keys):
    dictionary[s]="{:08b}".format(k )
  return dictionary

def M_vers_symboles(M, K, dictionaire):
    encoded_text = []
    i = 0

    while i < len(M):
        # Vérifie les paires de caractères
        if i + 1 < len(M):
            pair = M[i] + M[i + 1]
            if pair in dictionaire:
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

def chiffrer(M,K, dictionnaire):
  l = M_vers_symboles(M, K, dictionnaire)
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


def meme_cles(d1, d2):
    return set(d1.keys()) == set(d2.keys())
