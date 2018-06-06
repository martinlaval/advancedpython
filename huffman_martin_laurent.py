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

CARACTERES = [                                  # Tableau des caracteres
    ' ', 'a', 'b', 'c', 'd', 'e', 'f',
    'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z']

PROBA = [                                       # Tableau des probabilités
    0.1835, 0.0640, 0.0064, 0.0259, 0.0260, 0.1486, 0.0078,
    0.0083, 0.0061, 0.0591, 0.0023, 0.0001, 0.0465, 0.0245,
    0.0623, 0.0459, 0.0256, 0.0081, 0.0555, 0.0697, 0.0572,
    0.0506, 0.0100, 0.0000, 0.0031, 0.0021, 0.0008]

CODE = {} # Association code binaire/caractère (dictionnaire code Huffman)

def frequences():
    """
    Fonction permettant d'associer les fréquences d'apparition à chacun
    des caractères.
    """
    table = {}                          # Table d'association caractère/proba
    nb_carac = len(CARACTERES)          #
    for i in range(nb_carac):               # Boucle permettant l'association
        table[CARACTERES[i]] = PROBA[i]     # des caractères à la proba
                                            # correspondante.
    return table                            # On retourne la table.

###  la classe Arbre

class Arbre:
    """
    Classe Arbre.
    """
    def __init__(self, lettre, gauche=None, droit=None):# variables d'instance
        self.gauche = gauche                            # arbre gauche
        self.droit = droit                              # arbre droit
        self.lettre = lettre                            # lettre associée
    def est_feuille(self):
        """
        Fonction permettant de savoir si l'arbre est une feuille.
        """
        return self.gauche is None is self.droit == None    # True or False
    def est_vide(self):
        """
        Fonction permettant de savoir si l'arbre est vide.
        """
        return self is None                                 # True or False
    def __str__(self):                  # Méthode formatage String
        return '<'+ str(self.lettre)+'.'+str(self.gauche)+'.'+str(self.droit)+'>'


###  Ex.1  construction de l'arbre d'Huffamn utilisant la structure de "tas binaire"
def arbre_huffman(tab_freq):
    """
    Fonction permettant de construire l'arbre d'Huffman.
    """
    heap = []                                   # Définition du tas
    for carac, freq in tab_freq.items():        # Remplissage du tas
        heappush(heap, [freq, carac, Arbre(carac, None, None)])

    while len(heap) > 1:                        # Construction de l'arbre
        triplet1 = heappop(heap)
        triplet2 = heappop(heap)
        addition_freq = triplet1[0] + triplet2[0]
        concat_etiquette = triplet1[1] + triplet2[1]
        triplet_final = [addition_freq, concat_etiquette,
                         Arbre(concat_etiquette, triplet1, triplet2)]
        heappush(heap, triplet_final)

    return heappop(heap)[2]

###  Ex.2  construction du code d'Huffman

def parcours(arbre, prefixe, code):
    """
    Fonction récursive permettant de parcourir l'arbre d'Huffman.
    """
    if arbre.est_feuille():
        code[arbre.lettre] = prefixe   # Si l'arbre est une feuille, on
                                        # associe le préfixe au caractère.
    else:
        parcours(arbre.gauche[2], prefixe + "0", code)  # On ajoute "0" au
                                                    # préfixe si on va à gauche
        parcours(arbre.droit[2], prefixe + "1", code)   # On ajoute "1" au
                                                    # préfixe si on va à droite

def code_huffman(arbre):
    """
    Fonction permettant de remplir le dictionnaire du code d'Huffman
    en parcourant l'arbre.
    """
    #code = {}
    parcours(arbre, "", CODE)       # Remplissage du dictionnaire.
    #return code


###  Ex.3  encodage d'un texte contenu dans un fichier

def encodage(dico, fichier):
    """
    Fonction permettant de compresser un fichier.
    """
    f_read = open(fichier, "r")             # Ouverture du fichier à compresser
    contenu = f_read.read()                 # Lecture du fichier à compresser
    f_write = open("compressed_file.txt", "wb") # Création du fichier compressé

    print("Texte en clair :")
    print(contenu)

    suite_bits = ""
    for caractere in contenu:       # On parcourt le contenu du fichier
                                    # lettre par lettre
        if caractere not in dico: # Si le caractère n'est pas dans le
            caractere = ' '       # dictionnaire on le remplace par un espace.
        suite_bits += dico[caractere]   # on concatène la suite de bits
                                        # correspondant au caractère.

    # Lors de notre compression, nous voulons convertir les bits en char
    # octet par octet (8 bits par 8 bits). Pour nous faciliter la tâche
    # nous allons ajouter un nombre de 0 à la fin du fichier (qui seront
    # enlevés lors de la décompression) afin d'obtenir un multiple de 8.
    # Ainsi, nous pourrons convertir chaque groupe de 8 bits en char.

    nbre0 = 0   # compteur du nombre de 0 à ajouter à la fin du fichier.

    while len(suite_bits) % 8 != 0: # Tant que le nombre de bits n'est pas un
        suite_bits += "0"           # multiple de 8, on ajoute des 0 à la fin
        nbre0 = nbre0 + 1           # du fichier, et on incrémente le compteur.

    suite_bits += format(nbre0, '08b')  # on ajoute un octet à la fin du
                                        # fichier nous indiquant le nombre de
                                        # 0 à enlever lors de la décompression
    # exemple : Cinq 0 à enlever -> octet supplémentaire = "00000101"
    # Il faudra donc enlever à l'octet supplémentaire + cinq 0 lors de la
    # décompression.

    suite_char = ""         # concaténation des char générés par la conversion
                            # des octets.
    octet = ""              # Octet à convertir en char
    for bit in suite_bits:      # On parcourt les bits dans la suite
        if len(octet) != 8:
            octet += bit
        elif len(octet) == 8:   # Lorsqu'on obtient un paquet de 8 bits
            suite_char += chr(int(octet, 2))    # on le convertit en char puis
                                            # on le place dans suite_char.
            octet = bit      # On n'oublie pas d'initialiser le premier bit du
                            # prochain octet par le bit courant.
    suite_char += chr(int(octet, 2)) # rajout du dernier octet dans suite_char

    f_write.write(suite_char.encode('utf8'))    # Il faut encoder les
                                            # pour les écrire dans le fichier.
    f_write.close() # Fermeture des fichiers
    f_read.close()

# Exercice 4 : Décodage

def decodage(dico, fichier):
    """
    Fonction permettant de décompresser un fichier.
    """
    f_read = open(fichier, "rb")            # Ouverture du fichier compressé
    suite_char = f_read.read()              # Lecture du fichier compressé
    f_write = open("decoded_file.txt", "w") # Ouverture du fichier décompressé
    suite_char = suite_char.decode('utf8')  # Décodage du fichier en char.
    suite_bits = ""             # Préparation à la reconversion en bits
    for char in suite_char:     # Pour chaque char dans la suite de char
        integer = ord(char)     # On convertit le char en int
        suite_bits += format(integer, '08b')    # on convertit l'int en binaire
    nbre_bits_a_degager = 8 + int(suite_bits[-8:], 2) # on calcule le nombre
    # de bits à enlever du
    # du fichier (rappel : un octet (qui convertit en décimal, donne le
    # nombre de 0 à enlever ensuite) + le nombre de zéros à enlever)

    suite_bits = suite_bits[:-nbre_bits_a_degager] # Suite de bits réelle
                                    # sans les ajouts lors de la compression

    binlettre = "" # binaire correspondant à une lettre
    clear_text = "" # variable qui stockera le texte en clair
    for elt in suite_bits: # on parcourt la suite de buts
        binlettre = binlettre + elt # On concatène les bits jusqu'à trouver
                                    # une correspondance dans le dictionnaire.
        for key in dico:              # On parcourt le dictionnaire
            if dico[key] == binlettre:    # Si on trouve la suite binaire dans
                                        # le dictionnaire
                clear_text += key       # On prend la lettre associée à la
                                        # suite binaire et on la concatène
                                        # au texte en clair.
                binlettre = ""      # On reinitialise la variable binlettre.
    f_write.write(clear_text)       # On écrit le texte en clair dans le
                                    # fichier décompressé.
    f_read.close()      # Fermeture des fichiers.
    f_write.close()
    return clear_text


def main():
    """
    Fonction principale.
    """
    freq = frequences()        # association caractères/fréquences d'apparition
    arbre = arbre_huffman(freq)     # construction de l'arbre Huffman
    code_huffman(arbre)             # construction du dictionnaire
    encodage(CODE, "leHorla.txt")   # compression du fichier.
    print("\nDécodage :")
    decode = decodage(CODE, "compressed_file.txt") # décompression du fichier
    print(decode)

main()  # Execution du main
