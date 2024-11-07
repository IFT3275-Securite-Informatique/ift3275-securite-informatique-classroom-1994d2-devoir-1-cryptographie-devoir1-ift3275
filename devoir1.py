import math
import random as rnd
import numpy as np
import decimal
import time
from datetime import datetime

class codeBreaker_RSA:
    def __init__(self):
        pass

    def __ethRoot(self, C, E, N = None):
        # Reference: https://stackoverflow.com/questions/15424123/calculating-n-th-roots-using-python-3s-decimal-module

        targetRange = round( decimal.Decimal(C) ** (decimal.Decimal(1.0) / decimal.Decimal(E)))
        return targetRange

    def __meet_in_middle(self, N,E,C):

        n = decimal.Decimal(N)
        e = decimal.Decimal(E)
        c = decimal.Decimal(C)

        value = -1

        end = int(n.sqrt())+1
        #end = 10
        results_x = np.empty(0, dtype='uint64')
        results_y = np.empty(0, dtype='uint64')

        data_delimiter = min(1000000, end)

        now = datetime.now()
        start = now

        sx = np.zeros((data_delimiter), dtype='uint64')
        sy = np.zeros((data_delimiter), dtype='uint64')

        for x in range(1, end):
            xx = decimal.Decimal(x)
            yy = decimal.Decimal(end - x)

            # yi reverse sequence
            xi = int(divmod(c / (xx**e), n)[1])
            yi = int((end - x) ** E % N)

            index = (x - 1) % data_delimiter

            sx[index] = xi
            sy[index] = yi

            if (index == 0 and x > 1):
                now = datetime.now()
                elapsed = now - start

                print("1m mark, elapsed: "+str(elapsed)+" "+ str(data_delimiter/end*100)+"% parsed, current x: "+str(x))
                start = now

                results_x = np.append(results_x, sx)
                results_y = np.append(results_y, sy)
                sx = np.zeros((data_delimiter), dtype='uint64')
                sy = np.zeros((data_delimiter), dtype='uint64')

                intersect = np.intersect1d(results_x, results_y)
                intersect = intersect[np.where((intersect != 0))]
                intersect = intersect[np.where((intersect != 1))]
                print("intersect = "+ str(intersect))
                if (intersect.size > 0): break
                print("resuming...")

        results_x = np.append(results_x, sx)
        results_y = np.append(results_y, sy)

        intersect = np.intersect1d(results_x, results_y)
        #intersect = np.sort(intersect, order='descending')
        #print("intersect = "+ str(intersect))
        intersect = intersect[np.where((intersect != 0))]
        intersect = intersect[np.where((intersect != 1))]
        if intersect.size > 0:

            coeff = intersect[0]
            print("intermediate result is: "+str(coeff))
            xxx = np.where(results_x[:] == coeff)
            yyy = np.where(results_y == coeff)
            #print(xxx[0][0])
            #print(end - 1 - yyy[0][0])
            value = (xxx[0][0]+1) * (end - 1 - yyy[0][0])

            return value
        else:
            print("Cannot find valid intersect, value might not be a valid RSA key")
            return -1

    def Encrypt(self, N, E, M):
        return M**E % N

    def Decipher(self,N,E,C):
    # p and q large prime
    # n = pq
    # e > 2, lcd(e,(p-1)(q-1)) = 1
    # d = 1/e(mod(p-1)(q-1))

        # first, find the RSA group
        #phiN = self.phi_N(N)
        #print("bitlength, "+str(N.bit_length()) + " "+ str(E.bit_length()))


        # e-th root attack
        # https://crypto.stackexchange.com/questions/33561/cube-root-attack-rsa-with-low-exponent
        if (C**E < N):
            print("using N-th root attack!")
            return self.__ethRoot(C,E)
        elif N.bit_length() < 51:
            expectedRuntime = int(math.ceil(math.sqrt(N))) //1000000 * 10 / 60
            print("N length is reasonable for an exhaustive attack\nExpected runtime: "+"{:.1f}".format(expectedRuntime)+" minutes")
            return self.__meet_in_middle(N,E,C)
        else:
            print("cannot perform attack on such RSA within reasonable timeframe.")
            return "OPERATION ABORTED"

    # public key: n, e
    # private key: d

    # Encrypt(m) = m^e(modn)
    # Decrypt(m) = m^d(modn)
        #pass
    def int_to_str(self, int):
        # Reference: https://www.geeksforgeeks.org/python-program-to-covert-decimal-to-binary-number/
        charCount = math.ceil(int.bit_length() / 8)
        string = ""

        # Reference : https://docs.python.org/3/library/stdtypes.html
        c = int.to_bytes(charCount, byteorder='big')
        # print("chara count "+str(charCount))
        
        array = []

        for x in range(charCount):
            array.append(c[x])
            string += chr(c[x])

        #nparray = np.array(array)
        #print(nparray)
        #print(np.unique(nparray, return_counts=True))

        return string