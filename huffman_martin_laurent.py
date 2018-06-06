#!/usr/bin/python3.4;
# -*- coding: utf-8 -*-

"""
#####################################################
######  Introduction à la cryptographie      ###
#####   Codes de Huffman                     ###
####################################################
"""
from heapq import heappush, heappop

###  distribution de proba sur les lettres

CARACTERES = [
    ' ', 'a', 'b', 'c', 'd', 'e', 'f',
    'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z']

PROBA = [
    0.1835, 0.0640, 0.0064, 0.0259, 0.0260, 0.1486, 0.0078,
    0.0083, 0.0061, 0.0591, 0.0023, 0.0001, 0.0465, 0.0245,
    0.0623, 0.0459, 0.0256, 0.0081, 0.0555, 0.0697, 0.0572,
    0.0506, 0.0100, 0.0000, 0.0031, 0.0021, 0.0008]

def frequences():
    """
    Fonction permettant d'associer les fréquences d'apparition à chacun
    des caractères.
    """
    table = {}
    nb_carac = len(CARACTERES)
    for i in range(nb_carac):
        #print(caracteres[i], proba[i])
        table[CARACTERES[i]] = PROBA[i]
    return table

###  la classe Arbre

class Arbre:
    """
    Classe Arbre.
    """
    def __init__(self, lettre, gauche=None, droit=None):
        self.gauche = gauche
        self.droit = droit
        self.lettre = lettre
    def est_feuille(self):
        """
        Fonction permettant de savoir si l'arbre est une feuille.
        """
        return self.gauche is None is self.droit == None
    def est_vide(self):
        """
        Fonction permettant de savoir si l'arbre est vide.
        """
        return self is None
    def __str__(self):
        return '<'+ str(self.lettre)+'.'+str(self.gauche)+'.'+str(self.droit)+'>'


###  Ex.1  construction de l'arbre d'Huffamn utilisant la structure de "tas binaire"
def arbre_huffman(tab_freq):
    """
    Fonction permettant de construire l'arbre d'Huffman.
    """
    heap = []
    for carac, freq in tab_freq.items():
        heappush(heap, [freq, carac, Arbre(carac, None, None)])

    while len(heap) > 1:
        triplet1 = heappop(heap)
        triplet2 = heappop(heap)
        addition_freq = triplet1[0] + triplet2[0]
        concat_etiquette = triplet1[1] + triplet2[1]
        triplet_final = [addition_freq, concat_etiquette,
                         Arbre(concat_etiquette, triplet1, triplet2)]
        heappush(heap, triplet_final)

    return heappop(heap)[2]

###  Ex.2  construction ducode d'Huffamn

def parcours(arbre, prefixe, code):
    """
    Fonction permettant de parcourir l'arbre d'Huffman.
    """
    if arbre.est_feuille():
        code[arbre.lettre] = prefixe
    else:
        parcours(arbre.gauche[2], prefixe + "0", code)
        parcours(arbre.droit[2], prefixe + "1", code)

def code_huffman(arbre):
    """
    Fonction permettant de remplir le dictionnaire du code d'Huffman
    en parcourant l'arbre.
    """
    code = {}
    parcours(arbre, "", code)
    return code


###  Ex.3  encodage d'un texte contenu dans un fichier

def encodage(dico, fichier):
    """
    Fonction permettant de compresser un fichier.
    """
    f_read = open(fichier, "r")
    contenu = f_read.read()
    f_write = open("compressed_file.txt", "wb")
    suite_bits = ""
    print("Texte en clair :")
    print(contenu)

    for caractere in contenu:
        if caractere not in dico:
            caractere = ' '
        suite_bits += dico[caractere]

    nbre0 = 0

    while len(suite_bits) % 8 != 0:
        suite_bits += "0"
        nbre0 = nbre0 + 1
    suite_bits += format(nbre0, '08b')


    suite_char = ""
    octet = ""
    for bit in suite_bits:
        if len(octet) != 8:
            octet += bit
        elif len(octet) == 8:
            suite_char += chr(int(octet, 2))
            octet = bit
    suite_char += chr(int(octet, 2)) # rajout du dernier octet

    f_write.write(suite_char.encode('utf8'))
    f_write.close()
    f_read.close()

def decodage(dico, fichier):
    """
    Fonction permettant de décompresser un fichier.
    """
    f_read = open(fichier, "rb")
    suite_char = f_read.read()
    f_write = open("decoded_file.txt", "w")
    suite_char = suite_char.decode('utf8')
    suite_bits = ""
    for char in suite_char:
        integer = ord(char)
        suite_bits += format(integer, '08b')
    nbre_bits_a_degager = 8 + int(suite_bits[-8:], 2)
    suite_bits = suite_bits[:-nbre_bits_a_degager] # Récupérer suite_bits réel

    binlettre = ""
    clear_text = ""
    for elt in suite_bits:
        binlettre = binlettre + elt
        for i in dico:
            if dico[i] == binlettre:
                clear_text += i
                binlettre = ""
    f_write.write(clear_text)
    f_read.close()
    f_write.close()
    return clear_text


def main():
    """
    Fonction principale.
    """
    freq = frequences()
    arbre = arbre_huffman(freq)
    code = code_huffman(arbre)
    encodage(code, "leHorla.txt")
    print("\nDécodage :")
    decode = decodage(code, "compressed_file.txt")
    print(decode)

main()
