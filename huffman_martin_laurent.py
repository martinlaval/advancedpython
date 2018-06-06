#!/usr/bin/python3.4;
#####################################################
######  Introduction à la cryptographie  	###
#####   Codes de Huffman             		###
####################################################

from heapq import *
import binascii

###  distribution de proba sur les letrres

caracteres = [
    ' ', 'a', 'b', 'c', 'd', 'e', 'f',
    'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z' ]

proba = [
    0.1835, 0.0640, 0.0064, 0.0259, 0.0260, 0.1486, 0.0078,
    0.0083, 0.0061, 0.0591, 0.0023, 0.0001, 0.0465, 0.0245,
    0.0623, 0.0459, 0.0256, 0.0081, 0.0555, 0.0697, 0.0572,
    0.0506, 0.0100, 0.0000, 0.0031, 0.0021, 0.0008  ]

def frequences() :
    table = {}
    n = len(caracteres)
    for i in range(n) :
        print(caracteres[i], proba[i])
        table[caracteres[i]] = proba[i]
    return table

###  la classe Arbre

class Arbre :
    def __init__(self, lettre, gauche=None, droit=None):
        self.gauche=gauche
        self.droit=droit
        self.lettre=lettre
    def estFeuille(self):
        return self.gauche == None and self.droit == None
    def estVide(self):
        return self == None
    def __str__(self):
        return '<'+ str(self.lettre)+'.'+str(self.gauche)+'.'+str(self.droit)+'>'


###  Ex.1  construction de l'arbre d'Huffamn utilisant la structure de "tas binaire"
def arbre_huffman(frequences) :
    heap = []
    for carac, freq in frequences.items():
        heappush(heap, [freq, carac, Arbre(carac, None, None)])
    
    while len(heap) > 1:
        triplet1 = heappop(heap)
        triplet2 = heappop(heap)
        additionFreq = triplet1[0] + triplet2[0]
        concatEtiquette = triplet1[1] + triplet2[1]
        tripletFinal = [additionFreq, concatEtiquette, Arbre(concatEtiquette, triplet1, triplet2)]
        #print(tripletFinal)
        heappush(heap, tripletFinal)
    print("\n")

    return heappop(heap)[2]

###  Ex.2  construction ducode d'Huffamn

def parcours(arbre, prefixe, code):
    if arbre.estFeuille():
       code[arbre.lettre] = prefixe
    else:
        parcours(arbre.gauche[2], prefixe + "0", code)
        parcours(arbre.droit[2], prefixe + "1", code)
        
def code_huffman(arbre) :
    # on remplit le dictionnaire du code d'Huffman en parcourant l'arbre
    code = {}
    parcours(arbre, "", code)
    return code


###  Ex.3  encodage d'un texte contenu dans un fichier

def encodage(dico,fichier):
    f_read  = open(fichier, "r")
    contenu = f_read.read()
    f_write = open("compressed_file.txt","wb")
    suite_bits = ""

    for caractere in contenu:
        if caractere not in dico:
            caractere = ' '
        suite_bits += dico[caractere]
    
    nbre0 = 0

    while len(suite_bits) % 8 != 0:
        suite_bits += "0"
        nbre0 = nbre0 + 1
    
    octet = ""

    suite_char=""
    if(nbre0 > 0):
        suite_bits += format(nbre0, '08b')

    print(suite_bits)
    
    for bit in suite_bits:
        if len(octet) != 8:
            octet += bit
        elif len(octet) == 8:
            suite_char += chr(int(octet, 2))
            octet = bit
    suite_char += chr(int(octet,2)) # rajout du dernier octet
            
            
    f_write.write(suite_char.encode('utf8'))
    f_write.close()
    f_read.close()

def decodage(dico,fichier):
    f_read  = open(fichier, "rb")
    suite_char = f_read.read()
    f_write = open("decoded_file.txt","w")
    suite_char = suite_char.decode('utf8')
    suite_bits = ""
    for char in suite_char:
        integer = ord(char)
        #print(integer)
        #print(format(integer, '08b'))
        suite_bits+=format(integer, '08b')
    nbreBitsADegager = 8 + int(suite_bits[-8:], 2)
    suite_bits = suite_bits[:-nbreBitsADegager]
    print(suite_bits)
    
    binlettre = ""
    str=""
    for elt in suite_bits:
        binlettre = binlettre + elt
        for i in dico:
            if dico[i] == binlettre:
                str+=i
                binlettre = ""
    f_write.write(str)
    f_read.close()
    f_write.close()

"""
decode = decodage(H,'leHorlaEncoded.txt')
print(decode)
"""

def main():
    F = frequences()
    arbre = arbre_huffman(F)
    code = code_huffman(arbre)
    print(code)
    encodage(code, "leHorla.txt")
    print("decodage")
    decodage(code, "compressed_file.txt")
    

main()