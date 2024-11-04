import random
import time
import unittest
from difflib import SequenceMatcher, unified_diff
from crypt import *
from student_code import decrypt  # Remplacer par le nom de la fonction de déchiffrement


def similarity_ratio(str1, str2):
    """
    Calcule le pourcentage de similarité entre deux chaînes de caractères.
    """
    return SequenceMatcher(None, str1, str2).ratio()


def print_diff(original, decrypted):
    """
    Imprime les différences entre le texte original et le texte déchiffré.
    """
    diff = unified_diff(
        original.splitlines(),
        decrypted.splitlines(),
        fromfile='Original',
        tofile='Déchiffré',
        lineterm=''
    )
    for line in diff:
        print(line)


class TestDecryption(unittest.TestCase):

    def test_decryption_accuracy(self):
        # Charger le premier corpus et enlever les 10 000 premiers caractères
        url1 = "https://www.gutenberg.org/ebooks/13846.txt.utf-8"
        corpus1 = load_text_from_web(url1)

        url2 = "https://www.gutenberg.org/ebooks/4650.txt.utf-8"
        corpus2 = load_text_from_web(url2)

        # Combiner les deux corpus
        corpus = corpus1 + corpus2

        caracteres = list(set(list(corpus)))
        nb_caracteres = len(caracteres)
        nb_bicaracteres = 256 - nb_caracteres
        bicaracteres = [item for item, _ in Counter(cut_string_into_pairs(corpus)).most_common(nb_bicaracteres)]
        symboles = ['b', 'j', '\r', 'J', '”', ')', 'Â', 'É', 'ê', '5', 't', '9', 'Y', '%', 'N', 'B', 'V', '\ufeff', 'Ê', '?', '’', 'i', ':', 's', 'C', 'â', 'ï', 'W', 'y', 'p', 'D', '—', '«', 'º', 'A', '3', 'n', '0', 'q', '4', 'e', 'T', 'È', '$', 'U', 'v', '»', 'l', 'P', 'X', 'Z', 'À', 'ç', 'u', '…', 'î', 'L', 'k', 'E', 'R', '2', '_', '8', 'é', 'O', 'Î', '‘', 'a', 'F', 'H', 'c', '[', '(', "'", 'è', 'I', '/', '!', ' ', '°', 'S', '•', '#', 'x', 'à', 'g', '*', 'Q', 'w', '1', 'û', '7', 'G', 'm', '™', 'K', 'z', '\n', 'o', 'ù', ',', 'r', ']', '.', 'M', 'Ç', '“', 'h', '-', 'f', 'ë', '6', ';', 'd', 'ô', 'e ', 's ', 't ', 'es', ' d', '\r\n', 'en', 'qu', ' l', 're', ' p', 'de', 'le', 'nt', 'on', ' c', ', ', ' e', 'ou', ' q', ' s', 'n ', 'ue', 'an', 'te', ' a', 'ai', 'se', 'it', 'me', 'is', 'oi', 'r ', 'er', ' m', 'ce', 'ne', 'et', 'in', 'ns', ' n', 'ur', 'i ', 'a ', 'eu', 'co', 'tr', 'la', 'ar', 'ie', 'ui', 'us', 'ut', 'il', ' t', 'pa', 'au', 'el', 'ti', 'st', 'un', 'em', 'ra', 'e,', 'so', 'or', 'l ', ' f', 'll', 'nd', ' j', 'si', 'ir', 'e\r', 'ss', 'u ', 'po', 'ro', 'ri', 'pr', 's,', 'ma', ' v', ' i', 'di', ' r', 'vo', 'pe', 'to', 'ch', '. ', 've', 'nc', 'om', ' o', 'je', 'no', 'rt', 'à ', 'lu', "'e", 'mo', 'ta', 'as', 'at', 'io', 's\r', 'sa', "u'", 'av', 'os', ' à', ' u', "l'", "'a", 'rs', 'pl', 'é ', '; ', 'ho', 'té', 'ét', 'fa', 'da', 'li', 'su', 't\r', 'ée', 'ré', 'dé', 'ec', 'nn', 'mm', "'i", 'ca', 'uv', '\n\r', 'id', ' b', 'ni', 'bl']
        nb_symboles = len(symboles)
        dictionnaire = gen_key(symboles)

        random.seed(time.time())

        a = random.randint(3400, 7200)
        b = random.randint(36000, 65000)
        l = a+b
        c = random.randint(0, len(corpus)-l)

        M = corpus[c:c+l]

        K = gen_key(symboles)
        C = chiffrer(M, K, dictionnaire)


        # Charger le message original M
        original_message = M  # Remplacer par le texte original utilisé pour le chiffrement

        cryptogram = C  # Remplacer par le cryptogramme chiffré

        # Appeler la fonction de déchiffrement de l'étudiant
        decrypted_message = decrypt(cryptogram)

        # Calculer la similarité
        similarity = similarity_ratio(original_message, decrypted_message)
        print(f"Similarité : {similarity:.2%}")

        # Imprimer les différences si la similarité est inférieure à 98.5 %
        if similarity < 0.985:
            print("Différences entre les messages :")
            print_diff(original_message, decrypted_message)

        # Vérifier que la similarité entre le message original et le message déchiffré est d'au moins 98.5 %
        self.assertGreaterEqual(similarity, 0.985,
                                f"La similarité est seulement de {similarity:.2%}, ce qui est inférieur à 98.5 %.")


if __name__ == '__main__':
    unittest.main()
