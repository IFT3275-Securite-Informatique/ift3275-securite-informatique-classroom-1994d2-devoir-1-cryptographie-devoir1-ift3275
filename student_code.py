import math
import random
import requests
from collections import Counter
from difflib import SequenceMatcher
import logging
from typing import List, Dict
import spacy
import itertools
from crypt import *

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Chargement du modèle linguistique français
try:
    nlp = spacy.load("fr_core_news_sm")
except OSError:
    logger.error("pas de modèle linguistique français trouvé.")
    raise

def similarity_ratio(str1, str2):
    """Calcule le pourcentage de similarité entre deux chaînes de caractères."""
    return SequenceMatcher(None, str1, str2).ratio()

class FrenchCryptoAnalyzer:
    def __init__(self, reference_url=None, dictionary_url="https://www.freelang.com/dictionnaire/dic-francais.php"):
        self.common_words = self.load_french_words(dictionary_url)
        
        self.symboles = [
                            'b', 'j', '\r', 'J', '”', ')', 'Â', 'É', 'ê', '5', 't', '9', 'Y', '%', 'N', 'B', 'V', '\ufeff', 'Ê', '?', '’', 'i', ':', 's', 'C', 'â', 'ï', 'W', 'y', 'p', 'D', '—', '«', 'º', 'A', '3', 'n', '0', 'q', '4', 'e', 'T', 'È', '$', 'U', 'v', '»', 'l', 'P', 'X', 'Z', 'À', 'ç', 'u', '…', 'î', 'L', 'k', 'E', 'R', '2', '_', '8', 'é', 'O', 'Î', '‘', 'a', 'F', 'H', 'c', '[', '(', "'", 'è', 'I', '/', '!', ' ', '°', 'S', '•', '#', 'x', 'à', 'g', '*', 'Q', 'w', '1', 'û', '7', 'G', 'm', '™', 'K', 'z', '\n', 'o', 'ù', ',', 'r', ']', '.', 'M', 'Ç', '“', 'h', '-', 'f', 'ë', '6', ';', 'd', 'ô',
                            'e ', 's ', 't ', 'es', ' d', '\r\n', 'en', 'qu', ' l', 're', ' p', 'de', 'le', 'nt', 'on', ' c', ', ', ' e', 'ou', ' q', ' s', 'n ', 'ue', 'an', 'te', ' a', 'ai', 'se', 'it', 'me', 'is', 'oi', 'r ', 'er', ' m', 'ce', 'ne', 'et', 'in', 'ns', ' n', 'ur', 'i ', 'a ', 'eu', 'co', 'tr', 'la', 'ar', 'ie', 'ui', 'us', 'ut', 'il', ' t', 'pa', 'au', 'el', 'ti', 'st', 'un', 'em', 'ra', 'e,', 'so', 'or', 'l ', ' f', 'll', 'nd', ' j', 'si', 'ir', 'e\r', 'ss', 'u ', 'po', 'ro', 'ri', 'pr', 's,', 'ma', ' v', ' i', 'di', ' r', 'vo', 'pe', 'to', 'ch', '. ', 've', 'nc', 'om', ' o', 'je', 'no', 'rt', 'à ', 'lu', "'e", 'mo', 'ta', 'as', 'at', 'io', 's\r', 'sa', "u'", 'av', 'os', ' à', ' u', "l'", "'a", 'rs', 'pl', 'é ', '; ', 'ho', 'té', 'ét', 'fa', 'da', 'li', 'su', 't\r', 'ée', 'ré', 'dé', 'ec', 'nn', 'mm', "'i", 'ca', 'uv', '\n\r', 'id', ' b', 'ni', 'bl'
                        ]
        
        self.monogram_freq = {
                                'a': 8.13,
                                'â': 0.03,
                                'à': 0.54,
                                'b': 0.93,
                                'c': 3.15,
                                'ç': 0.01,
                                'd': 3.55,
                                'e': 15.10,
                                'ê': 0.24,
                                'é': 2.13,
                                'è': 0.35,
                                'ë': 0.01,
                                'f': 0.96,
                                'g': 0.97,
                                'h': 1.08,
                                'i': 6.94,
                                'ï': 0.01,
                                'î': 0.03,
                                'j': 0.71,
                                'k': 0.16,
                                'l': 5.68,
                                'm': 3.23,
                                'n': 6.42,
                                'o': 5.27,
                                'ô': 0.07,
                                'œ': 0.01,
                                'p': 3.03,
                                'q': 0.89,
                                'r': 6.43,
                                's': 7.91,
                                't': 7.11,
                                'u': 6.05,
                                'ü': 0.02,
                                'û': 0.05,
                                'ù': 0.02,
                                'v': 1.83,
                                'w': 0.04,
                                'x': 0.42,
                                'y': 0.19,
                                'z': 0.21
                            }
        
        self.bigram_freq = {
                                'es': 3.27,
                                'le': 2.31,
                                'de': 2.15,
                                're': 2.06,
                                'en': 2.03,
                                'er': 1.65,
                                'nt': 1.63,
                                'te': 1.60,
                                'on': 1.56,
                                'et': 1.40,
                                'se': 1.39,
                                'el': 1.34,
                                'la': 1.28,
                                'ou': 1.23,
                                'an': 1.22,
                                'ne': 1.18,
                                'ai': 1.12,
                                'qu': 1.04,
                                'me': 1.04,
                                'ed': 1.03,
                                'ur': 1.00,
                                'is': 0.97,
                                'ec': 0.96,
                                'it': 0.95,
                                'ie': 0.95,
                                'em': 0.90,
                                'ti': 0.88,
                                'in': 0.86,
                                'ue': 0.85,
                                'ra': 0.84,
                                'ce': 0.82,
                                'eu': 0.81,
                                'ar': 0.81,
                                'ns': 0.79,
                                'sa': 0.77,
                                'ta': 0.75,
                                'co': 0.75,
                                'st': 0.73,
                                'un': 0.73,
                                'il': 0.73,
                                'ep': 0.72,
                                'ss': 0.71,
                                'ee': 0.70,
                                'tr': 0.70,
                                'au': 0.67,
                                'al': 0.65,
                                'pa': 0.62,
                                'sd': 0.61,
                                'ri': 0.61,
                                'nd': 0.61,
                                'us': 0.59,
                                'ea': 0.58,
                                'at': 0.58,
                                'so': 0.57,
                                'ui': 0.56,
                                'si': 0.54,
                                'ro': 0.53,
                                'll': 0.51,
                                've': 0.51,
                                'or': 0.51,
                                'li': 0.50,
                                'ma': 0.49,
                                'ut': 0.49,
                                'oi': 0.48,
                                'ir': 0.48,
                                'po': 0.48,
                                'ch': 0.48,
                                'nc': 0.48,
                                'pe': 0.47,
                                'as': 0.46,
                                'sl': 0.45,
                                'ac': 0.44,
                                'io': 0.44,
                                'td': 0.44,
                                'sp': 0.44,
                                'pr': 0.43,
                                'na': 0.43,
                                'du': 0.42,
                                'to': 0.41,
                                'da': 0.41,
                                'rs': 0.40,
                                'sc': 0.39,
                                'om': 0.39,
                                'ap': 0.37,
                                'su': 0.37,
                                'di': 0.37,
                                'ge': 0.37,
                                'ts': 0.36,
                                'tl': 0.35,
                                'rt': 0.35,
                                'lo': 0.35,
                                'rl': 0.34,
                                'no': 0.33,
                                'he': 0.33,
                                'rd': 0.33,
                                'av': 0.33,
                                'ev': 0.33,
                                'ca': 0.32,
                                'ni': 0.31,
                                'tu': 0.29
                            }
        
        self.trigram_freq = {
                                'ent': 0.84,
                                'les': 0.77,
                                'que': 0.62,
                                'ede': 0.61,
                                'des': 0.56,
                                'res': 0.43,
                                'est': 0.42,
                                'ela': 0.41,
                                'eme': 0.41,
                                'ele': 0.41,
                                'sde': 0.40,
                                'ion': 0.39,
                                'lle': 0.38,
                                'ere': 0.37,
                                'tre': 0.37,
                                'ese': 0.37,
                                'ant': 0.37,
                                'men': 0.36,
                                'our': 0.35,
                                'ait': 0.34,
                                'del': 0.33,
                                'une': 0.33,
                                'nte': 0.32,
                                'par': 0.31,
                                'eur': 0.30,
                                'esd': 0.30,
                                'tio': 0.29,
                                'tde': 0.28,
                                'ien': 0.28,
                                'esa': 0.28,
                                'ont': 0.28,
                                'qui': 0.27,
                                'sse': 0.27,
                                'ans': 0.27,
                                'ite': 0.27,
                                'ire': 0.26,
                                'sle': 0.26,
                                'esp': 0.25,
                                'con': 0.25,
                                'son': 0.25,
                                'ess': 0.25,
                                'ons': 0.25,
                                'nde': 0.25,
                                'eco': 0.24,
                                'tes': 0.24,
                                'ati': 0.24,
                                'equ': 0.23,
                                'dan': 0.23,
                                'ais': 0.23,
                                'iqu': 0.22,
                                'ete': 0.22,
                                'ter': 0.22
                            }
        
        # Poids
        self.freq_weights = {
            'mono': 1.0,
            'bi': 1.5,
            'tri': 2.0,
            'word': 2.5,
            'similarity': 5.0,
            'grammar': 10.0
        }
        
        if reference_url:
            self.reference_text = load_text_from_web(reference_url)
            if not self.reference_text:
                logger.warning("impossible de charger le texte de référence.")
                self.reference_text = "par défaut"
        else:
            self.reference_text = "par défaut"
        
        self.best_score = float('-inf')
        self.score_history = []
    
    def load_french_words(self, url):
        """Charge une liste de mots en français depuis un fichier en ligne."""
        common_words = []
        try:
            response = requests.get(url)
            response.raise_for_status()
            for line in response.iter_lines(decode_unicode=True):
                word = line.strip()
                if word:
                    common_words.append(word)
            # Éliminer les doublons tout en préservant l'ordre
            seen = set()
            unique_common_words = []
            for word in common_words:
                if word not in seen:
                    unique_common_words.append(word)
                    seen.add(word)
            logger.info(f"{len(unique_common_words)} mots chargés depuis le dictionnaire en ligne.")
            return unique_common_words
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur lors du chargement du dictionnaire : {e}")
            # Liste de mots courants en français sans doublons
            common_words = [
                "le", "de", "un", "être", "et", "à", "il", "avoir", "ne", "je",
                "son", "que", "se", "qui", "ce", "dans", "en", "du", "elle", "au",
                "par", "pour", "pas", "vous", "avec", "tout", "faire", "sur", "comme",
                "mais", "nous", "dire", "me", "on", "mon", "lui", "ou", "si", "leur",
                "y", "demander", "avant", "même", "bien", "où", "aussi", "après", "voir",
                "aller", "sans", "quel", "donc", "temps", "prendre", "autre", "vouloir",
                "venir", "quand", "grand", "celui", "notre", "mettre", "sous", "trouver", "donner", "peu",
                "parler", "savoir", "falloir", "comprendre", "depuis", "point", "ainsi", "heure", "rester", "toujours",
                "tenir", "penser", "entendre", "rendre", "regarder", "appeler", "partir", "arriver", "connaître", "devoir",
                "femme", "homme", "jour", "moi", "aucun", "chez", "demain", "enfant", "gouvernement"
            ]
            return common_words
    
    def generate_ngrams(self, decrypted_text, n):
        """Génère des n-grammes de taille `n` à partir du texte déchiffré."""
        return [decrypted_text[i:i+n] for i in range(len(decrypted_text) - n + 1)]
    
    def frequency_analysis(self, decrypted_text):
        """Analyse de fréquence pour les monogrammes, bigrammes et trigrammes."""
        mono_freq = Counter(decrypted_text)
        bi_freq = Counter([''.join(bi) for bi in self.generate_ngrams(decrypted_text, 2)])
        tri_freq = Counter([''.join(tri) for tri in self.generate_ngrams(decrypted_text, 3)])
        return mono_freq, bi_freq, tri_freq
    
    def grammar_score(self, decrypted_text):
        """Évalue la validité grammaticale du texte déchiffré."""
        doc = nlp(decrypted_text)
        num_sentences = len(list(doc.sents))
        num_tokens = len(doc)
        if num_sentences == 0 or num_tokens == 0:
            return 0.0
        # Ratio de phrases correctement segmentées
        return num_sentences / num_tokens
    
    def evaluate_text(self, decrypted_text: str) -> float:
        """Évalue la vraisemblance du texte en utilisant l'analyse de fréquence, la similarité et la grammaire."""
        score = 0.0
        text_len = len(decrypted_text)
        
        if text_len == 0:
            return score
        
        # Analyse de fréquence
        mono_freq, bi_freq, tri_freq = self.frequency_analysis(decrypted_text)
        
        # Score pour les monogrammes
        for mono, expected_freq in self.monogram_freq.items():
            actual_freq = (mono_freq.get(mono, 0) / text_len) * 100  # Convertir en pourcentage
            score += (1 - abs(actual_freq - expected_freq) / expected_freq) * self.freq_weights['mono']
        
        # Score pour les bigrammes
        for bi, expected_freq in self.bigram_freq.items():
            actual_freq = (bi_freq.get(bi, 0) / (text_len - 1)) * 100 if text_len > 1 else 0
            score += (1 - abs(actual_freq - expected_freq) / expected_freq) * self.freq_weights['bi']
        
        # Score pour les trigrammes
        for tri, expected_freq in self.trigram_freq.items():
            actual_freq = (tri_freq.get(tri, 0) / (text_len - 2)) * 100 if text_len > 2 else 0
            score += (1 - abs(actual_freq - expected_freq) / expected_freq) * self.freq_weights['tri']
        
        # Score pour les mots courants
        for word in self.common_words:
            occurrences = decrypted_text.count(word)
            score += occurrences * self.freq_weights['word']
        
        # Similarité avec le texte de référence
        similarity_score = similarity_ratio(decrypted_text, self.reference_text)
        score += similarity_score * self.freq_weights['similarity']
        
        # Score de grammaire
        grammar = self.grammar_score(decrypted_text)
        score += grammar * self.freq_weights['grammar']
        
        return score
    
    def create_initial_mapping_enhanced(self, encrypted_symbols: List[str]) -> Dict[str, str]:
        """Crée un mapping initial basé sur la fréquence des symboles."""
        symbol_freq = Counter(encrypted_symbols)
        sorted_encrypted_symbols = [symbol for symbol, freq in symbol_freq.most_common()]
        
        # Sort expected French symbols by frequency
        sorted_french_symbols = sorted(self.monogram_freq.items(), key=lambda x: x[1], reverse=True)
        sorted_french_symbols = [symbol for symbol, freq in sorted_french_symbols]
        
        mapping = {}
        for enc_sym, fr_sym in zip(sorted_encrypted_symbols, sorted_french_symbols):
            mapping[enc_sym] = fr_sym
        
        # Assigner les symboles restants de façon aléatoire à partir des symboles français restants
        remaining_french = sorted_french_symbols[len(sorted_encrypted_symbols):]
        random.shuffle(remaining_french)
        for enc_sym in sorted_encrypted_symbols[len(sorted_french_symbols):]:
            if remaining_french:
                mapping[enc_sym] = remaining_french.pop()
            else:
                mapping[enc_sym] = enc_sym  # Assignation par défaut
        
        logger.debug(f"Mapping initial : {mapping}")
        return mapping
    
    def apply_mapping(self, mapping: Dict[str, str], encrypted_symbols: List[str]) -> str:
        """Applique le mapping pour décrypter le texte."""
        decrypted_symbols = [mapping.get(symbol, '?') for symbol in encrypted_symbols]  # Remplacer par '?' si non trouvé
        return ''.join(decrypted_symbols)
    
    def mutate_mapping(self, mapping):
        """Mutation avancée pour augmenter la précision du mapping."""
        new_mapping = mapping.copy()
        # Choisir deux symboles aléatoires pour échanger leurs mappings
        if len(new_mapping) < 2:
            return new_mapping
        s1, s2 = random.sample(list(new_mapping.keys()), 2)
        new_mapping[s1], new_mapping[s2] = new_mapping[s2], new_mapping[s1]
        return new_mapping
    
    def simulated_annealing_decrypt(self, encrypted_symbols, initial_mapping, initial_temp=1000.0, alpha=0.995, max_iter=50):
        """
        Déchiffre le texte en utilisant l'algorithme de recuit simulé.
        
        :param encrypted_symbols: Liste des symboles chiffrés (chaînes de 8 bits)
        :param initial_mapping: Mapping initial (Dict[str, str])
        :param initial_temp: Température initiale
        :param alpha: Taux de refroidissement
        :param max_iter: Nombre maximal d'itérations
        :return: Mapping optimisé et historique des scores
        """
        current_mapping = initial_mapping.copy()
        decrypted_text = self.apply_mapping(current_mapping, encrypted_symbols)
        best_mapping = current_mapping.copy()
        best_score = self.evaluate_text(decrypted_text)
        
        temperature = initial_temp
        score_history = []
        
        for i in range(max_iter):
            new_mapping = self.mutate_mapping(current_mapping)
            decrypted_text = self.apply_mapping(new_mapping, encrypted_symbols)
            new_score = self.evaluate_text(decrypted_text)
            delta_score = new_score - best_score
            
            if delta_score > 0 or math.exp(delta_score / temperature) > random.random():
                current_mapping = new_mapping
                if new_score > best_score:
                    best_mapping = new_mapping
                    best_score = new_score
                    logger.info(f"Amélioration du score à {best_score:.4f} à l'itération {i}")
                    score_history.append(best_score)
            
            temperature *= alpha
            
            # Arrêt précoce si la température est trop basse
            if temperature < 1e-8:
                break
        
        self.score_history = score_history
        return best_mapping, self.score_history
    
    def optimize_parameters_grid_search(self, encrypted_symbols, initial_mapping, temp_values, alpha_values, max_iter_values):
        """
        Optimise les paramètres en utilisant une recherche par grille.
        
        :param encrypted_symbols: Liste des symboles chiffrés
        :param initial_mapping: Mapping initial
        :param temp_values: Liste de valeurs pour initial_temp
        :param alpha_values: Liste de valeurs pour alpha
        :param max_iter_values: Liste de valeurs pour max_iter
        :return: Mapping optimisé et paramètres utilisés
        """
        best_score = float('-inf')
        best_params = {}
        best_mapping = {}
        
        for temp, alpha, max_it in itertools.product(temp_values, alpha_values, max_iter_values):
            logger.info(f"Testing parameters: initial_temp={temp}, alpha={alpha}, max_iter={max_it}")
            final_mapping, score_history = self.simulated_annealing_decrypt(
                encrypted_symbols, 
                initial_mapping, 
                initial_temp=temp, 
                alpha=alpha, 
                max_iter=max_it
            )
            current_score = score_history[-1] if score_history else 0
            if current_score > best_score:
                best_score = current_score
                best_params = {'initial_temp': temp, 'alpha': alpha, 'max_iter': max_it}
                best_mapping = final_mapping
                
        logger.info(f"Best parameters found: {best_params} with score {best_score}")
        return best_mapping, best_params

def decrypt(C: str) -> str:
    """Fonction de déchiffrement."""
    if len(C) % 8 != 0:
        raise ValueError("Le message chiffré doit avoir une longueur multiple de 8")
    
    analyzer = FrenchCryptoAnalyzer(reference_url="https://www.gutenberg.org/files/4650/4650-0.txt")  # Candide comme référence
    encrypted_symbols = [C[i:i+8] for i in range(0, len(C), 8)]
    
    try:
        # Mapping initial basé sur la fréquence
        initial_mapping = analyzer.create_initial_mapping_enhanced(encrypted_symbols)
        
        # Optimiser les paramètres via recherche par grille
        temp_values = [1000.0, 1500.0, 2000.0]
        alpha_values = [0.995, 0.999, 0.9995]
        max_iter_values = [20, 50, 100]
        
        best_mapping, best_params = analyzer.optimize_parameters_grid_search(
            encrypted_symbols, 
            initial_mapping, 
            temp_values, 
            alpha_values, 
            max_iter_values
        )
        
        decrypted = analyzer.apply_mapping(best_mapping, encrypted_symbols)
        final_score = analyzer.evaluate_text(decrypted)
        
        logger.info(f"Score final : {final_score}")
        
        return decrypted
        
    except ValueError as ve:
        logger.error(f"Erreur de valeur : {ve}")
        raise
    except requests.exceptions.RequestException as re:
        logger.error(f"Erreur de requête : {re}")
        raise
    except Exception as e:
        logger.error(f"Erreur inattendue : {e}")
        raise