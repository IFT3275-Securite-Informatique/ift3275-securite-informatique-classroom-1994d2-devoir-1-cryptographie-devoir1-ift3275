import math
import random as rnd
import numpy as np
import requests
from collections import Counter

# exponentiation modulaire
def modular_pow(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if (exponent % 2 == 1):
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

# inverse multiplicatif de a modulo m
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception("Pas d'inverse multiplicatif")
    else:
        return x % m








class Main:
    def __init__(self):
        # Initialisation des attributs, si nécessaire
        self.message = "Devoir1 IFT3275"

    def run(self):
        # Méthode principale pour exécuter la logique de votre programme
        print(self.message)


        # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # Question 1.1


        # Clé publique Question 1.1
        N = 143516336909281815529104150147210248002789712761086900059705342103220782674046289232082435789563283739805745579873432846680889870107881916428241419520831648173912486431640350000860973935300056089286158737579357805977019329557985454934146282550582942463631245697702998511180787007029139561933433550242693047924440388550983498690080764882934101834908025314861468726253425554334760146923530403924523372477686668752567287060201407464630943218236132423772636675182977585707596016011556917504759131444160240252733282969534092869685338931241204785750519748505439039801119762049796085719106591562217115679236583
        e = 3

        # Cryptogramme 1.1
        C = 1101510739796100601351050380607502904616643795400781908795311659278941419415375

        # fonction calcule la racine n-ième entière de k
        def integer_nth_root(k, n):
            u, s = k, k + 1
            while u < s:
                s = u
                t = (n - 1) * s + k // pow(s, n - 1)
                u = t // n
            if s ** n == k:
                return s
            else:
                return None

        # fonction tente de décrypter un message chiffré en utilisant une opération de racine n-ième
        def decrypt_msg(C, e):
            # Trouver la racine n-ième de C avec l'exposant e
            M = integer_nth_root(C, e)

            if M is not None:
                print("M:", M)
                if pow(M, e) == C:
                    message = int_to_str(M)
                    print("message：", message)
                else:
                    print("M^e != C")
            else:
                print("Le décryptage a échoué")

        # fonction convertit un entier x en une chaîne de caractères
        def int_to_str(x):

            binary_str = bin(x)[2:]
            while len(binary_str) % 8 != 0:
                binary_str = '0' + binary_str
            chars = []
            for i in range(0, len(binary_str), 8):
                byte = binary_str[i:i + 8]
                chars.append(chr(int(byte, 2)))
            return ''.join(chars)

        print("---Question1.1---")
        decrypt_msg(C, e)





        # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # Question 1.2


        # Clé publique Question 1.2
        N = 172219604291138178634924980176652297603347655313304280071646410523864939208855547078498922947475940487766894695848119416017067844129458299713889703424997977808694983717968420001033168722360067307143390485095229367172423195469582545920975539060699530956357494837243598213416944408434967474317474605697904676813343577310719430442085422937057220239881971046349315235043163226355302567726074269720408051461805113819456513196492192727498270702594217800502904761235711809203123842506621973488494670663483187137290546241477681096402483981619592515049062514180404818608764516997842633077157249806627735448350463
        e = 173

        # Cryptogramme 1.2
        C = 25782248377669919648522417068734999301629843637773352461224686415010617355125387994732992745416621651531340476546870510355165303752005023118034265203513423674356501046415839977013701924329378846764632894673783199644549307465659236628983151796254371046814548224159604302737470578495440769408253954186605567492864292071545926487199114612586510433943420051864924177673243381681206265372333749354089535394870714730204499162577825526329944896454450322256563485123081116679246715959621569603725379746870623049834475932535184196208270713675357873579469122917915887954980541308199688932248258654715380981800909

        p = 10715086071862673209484250490600018105614048117055336074437503883703510511249361224931983788156958581275946729175531468251871452856923140435984577574698574803934567774824230985421074605062371141877954182153046474983581941267398767559165543946077062914571196477686542167660429831652624386837205668069673

        q = 16072629107794009814226375735900027158421072175583004111656255825555265766874041837397975682235437871913920093763297202377807179285384710653976866362047862205901851662236346478131611907593556712816931273229569712475372911901098151338748315919115594371856794716529813251490644747478936580257043048672231

        # Fonction de déchiffrement RSA
        def rsa_decrypt(C, e, p, q):
            # Calcul de l'indice d'Euler phi(N)
            if p * q == N:
                phi_N = (p - 1) * (q - 1)
            else:
                raise ValueError("Les valeurs de p et q sont incorrectes.")

            # Calcul de l'exposant privé d
            d = modinv(e, phi_N)

            # Déchiffrement : calculer M = C^d mod N
            M = modular_pow(C, d, N)

            # Convertir M en bytes et interpréter en tant que chaîne de caractères
            byte_length = (M.bit_length() + 7) // 8  # Nombre de bytes nécessaires
            message_bytes = M.to_bytes(byte_length, byteorder='big')  # Convertir en bytes
            try:
                message = message_bytes.decode('utf-8')  # Décoder en UTF-8
            except UnicodeDecodeError:
                message = message_bytes.decode('utf-8', errors='ignore')  # Ignorer les erreurs de décodage

            return message

        print("---Question1.2---")
        # Appel de la fonction
        try:
            message = rsa_decrypt(C, e, p, q)
            print("Message converti en texte:", message)
        except Exception as ex:
            print("Erreur lors du déchiffrement:", ex)


if __name__ == "__main__":
    # Création d'une instance de la classe Main et exécution de la méthode run
    main_instance = Main()
    main_instance.run()