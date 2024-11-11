from crypt import *

class treeNode:
    def __init__(self, dict):
        self.dict = dict
        self.child = []
        self.isPossible = True
        self.parent = None
        self.activeNode = 0


    def add_child(self, dict):
        self.child.append(dict)

    def setImpossible(self):
        self.isPossible = False

    def getChildCount(self):
        return len(self.child)

    def getDict(self):
        return self.dict

    def getDictSize(self):
      return len(self.dict)

    def getParent(self):
      return self.parent

    def setParent(self, parent):
      self.parent = parent

    def nextChild(self):
      self.activeNode = self.activeNode + 1

    def getActiveNode(self):
      return self.activeNode


def set_up_tree(C, n_gram, dictionary, symboleMap, bitMap):
    # foundWord = False
    root = treeNode(dictionary)
    cur = root
    while True:
        if cur.isPossible:
          # if cur.getParent() == 25:
          #   foundWord = True

          if cur.getDictSize() < len(bitMap):
            dict = cur.getDict()
            i = cur.getDictSize()
            temp = cur.getActiveNode()
            if temp >=len(symboleMap):
               cur.setImpossible()
               continue
            newDict = dict.copy()
            bits = bitMap[i][0]
            for j in range(temp, len(symboleMap)):
              symbole = symboleMap[j][0]
              if not inDictionary(symbole, newDict):
                break

            newDict.update({bits: symbole})
            node = treeNode(newDict)
            node.setParent(cur)

            cur.add_child(node)
            cur = node
            new = replace_mapping(C, node.getDict())
            if not validate(n_gram, new):
              cur.setImpossible()

          else:
            M = replace_mapping(C, cur.getDict())
            return M

        else:
          cur = cur.getParent()
          cur.nextChild()

def inDictionary(symbole, dictionary):
  for key, value in dictionary.items():
    if (symbole == value):
      return True
  return False
def create_proba_map():
    i = 0
    index = [13846, 4650]
    text = ""
    for i in index:
        try:
            url = "https://www.gutenberg.org/ebooks/" + str(i) + ".txt.utf-8"
            text += load_text_from_web(url)
        except:
            print("text:" + url + " couldn't be loaded")
    n = len(text)
    characters_map = Counter(text)
    bicharacters_map = Counter(cut_string_into_pairs(text)).most_common(256 - len(characters_map))
    proba_map = {}
    for i in bicharacters_map:
        bicharacter = i[0]
        occurence = i[1]
        characters_map[bicharacter[0]] -= occurence
        characters_map[bicharacter[1]] -= occurence
        proba_map[bicharacter] = occurence
    for i in proba_map:
        proba_map[i] = round(proba_map.get(i) / (len(text) - 1) * 100, 4)
    for i in characters_map:
        characters_map[i] = round(characters_map.get(i) / (len(text)) * 100, 4)
    proba_map.update(characters_map)
    return proba_map


def find_C_map(C):
    n = 0
    start = 0
    end = 0
    symbol = []
    not_crypt = set()
    for i in range(len(C)):
        if end - start == 8:
            symbol.append(C[start:end])
            n += 1
            start = end
        if C[end] != '1' and C[end] != '0':
            start = end + 1
            symbol.append(C[end])
            not_crypt.add(C[end])
            n += 1
        end += 1
    C_map = Counter(symbol)
    proba_map = {key: round(count / n * 100, 4) for key, count in C_map.items()}
    return proba_map


def decrypt(C):
    # entrez votre code ici.
    # Vous pouvez créer des fonctions auxiliaires et adapter le code à votre façon mais decrypt dois renvoyer le message décrypté
    #tri = set_up_tri()
    index = [13846,4650]
    text = ""
    for i in index:
      try:
        url = "https://www.gutenberg.org/ebooks/"+str(i)+".txt.utf-8"
        text += load_text_from_web(url)
      except:
        print("text:"+url+" couldn't be loaded")

    n_gram = get_n_gram(4,text)
    n_gram.update(get_n_gram(5,text))
    proba_map = create_proba_map()
    C_map = find_C_map(C)
    most_Common_C_map = Counter(C_map).most_common(len(C_map))
    most_Common_proba_map = Counter(proba_map).most_common(len(proba_map))

    index = set()
    dictionary = {}
    dictionary[most_Common_C_map[0][0]] = most_Common_proba_map[0][0]
    M = set_up_tree(C, n_gram, dictionary, most_Common_proba_map, most_Common_C_map)
    print(M)
    return M

def get_n_gram(n,M):
  left = 0
  right = n
  map = {}
  while right < len(M):
    n_gram = M[left:right]
    if map.get(n_gram) is None:
      map[n_gram] = 0
    map[n_gram]+=1
    left+=1
    right+=1
  return map
def validate(possible,M):
  left = 0
  right = 4
  while right < len(M):
    temp = M[left:right]
    if '1' in temp or '0' in temp:
       right+=1
       left+=1
       continue
    if possible.get(temp) is None:
      return False
    right+=1
    temp = M[left:right]
    if '1' in temp or '0' in temp:
       left+=1
       continue
    if possible.get(temp) is None:
      return False
    left+=1
  return True

def replace_mapping(M, dict):
    temp = ""
    result = ""
    for i in M:
        temp += i
        if len(temp) == 8:
            if dict.get(temp) != None:
                result += dict[temp]
            else:
                result += temp
            temp = ""
        if i not in '01':
            result += temp
            temp = ""
    return result
