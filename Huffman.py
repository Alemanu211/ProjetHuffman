# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 21:04:29 2022

@author: Alexandre
"""


'''Etape 1 : Détermination de l'alphabet et de ses fréquences de caractères'''

#Fonction qui compte le nb d'occurence d'un caractère dans un texte
def frequence(lettre,fichier):
    fichier = open(fichier, "r")
    freq = 0
    for i in fichier.read():
        if i == lettre:
            freq+=1
    fichier.close()
    return freq
            
#fichier = open("alice.txt", "r")

#Fonction qui renvoi une liste avec tous les caractères présent dans un texte
def alphabet(fichier):
    fichier = open(fichier, "r")
    res = []
    for i in fichier.read():
        if i not in res:
            res.append(i)
    fichier.close()
    return res
    
#Dictionnaire avec les caractères et leur nb d'occurences dans un fichier texte
def dict_alphabet(fichier):
    alph = alphabet(fichier)
    occurences = []
    for i in alph :
        occurences.append(frequence(i,fichier))    
    res = dict(zip(alph,occurences))
    
    res = dict(sorted(res.items(), key=lambda t: t[0])) #Tri ASCII
    return dict(sorted(res.items(), key=lambda t: t[1])) #Tri occurences croissantes


'''Etape 2 : Construction de l'arbre '''

class Node():
    def __init__(self,frequence,caractere,left_child,right_child):
        self.frequence = frequence
        self.caractere = caractere
        self.left_child = left_child
        self.right_child = right_child
        

def CreationFeuilles(fichier):
    listeFeuilles = []
    for i,j in dict_alphabet(fichier).items():
        listeFeuilles.append(Node(j,i,None,None))
    return listeFeuilles

    
def Arbre(fichier):
    
    Arbre = CreationFeuilles(fichier)
    
    while len(Arbre)>1:
        Arbre.append(Node(Arbre[0].frequence + Arbre[1].frequence,None,Arbre[0], Arbre[1] ))
        del Arbre[:2] #Supprime les 2 premiers elements
        sorted(Arbre, key=lambda t: t.frequence)
        
    return Arbre[0] #Correspond à la racine de l'arbre

'''Etape 3 : Codage du texte '''

  
DictionnaireCode = dict()     
def codeCaracteres(Node,fichier,code):
    
    if Node.caractere != None:
        DictionnaireCode[Node.caractere] = code
    else:
        codeCaracteres(Node.left_child,fichier,code + '0')
        codeCaracteres(Node.right_child,fichier,code + '1')
        
#codeCaracteres(Arbre('textesimple.txt'),'textesimple.txt','')       

def codeTexte(fichier):
    
    #On recupère ce que l'on va écrire
    res = ''
    codeCaracteres(Arbre(fichier),fichier,'')  
    fichier = open(fichier, "r")
    for i in fichier.read():
        res = res + str(DictionnaireCode[i])
    fichier.close()
    
    #On écrit ensuite dans un nouveau fichier texte

    file = open("TexteConvertiHuffman.txt", "w") 
    file.write(res) 
    file.close()
    
''' Etape 4 : Determination du taux de Compression '''

def TauxCompression(TexteInitial,TexteApresHuffman):
    fichier1 = open(TexteInitial, "r")
    fichier2 = open(TexteApresHuffman, "r")
    nbOctets = 0
    nbBits = 0
    
    for i in fichier1.read(): #Texte initial avant conversion
        nbOctets += 1
    for i in fichier2.read(): #Texte après conversion
        nbBits += 1
    return (1-nbBits/(nbOctets*8))


''' Etape 5 : Détermination du nombre moyen de bits de stockage d’un caractère du texte compressé '''
        
def nbMoyenBits():
    somme = 0
    for i,j in DictionnaireCode.items() :
        somme += len(j)
    return(somme/len(DictionnaireCode.items()))

''' Mise en forme, acceuil utilisateur '''

Fichier = input("Veuillez entrer le nom de votre fichier texte à convertir : ")
codeTexte(Fichier)
print("\nFichier converti avec succès !")
print("Votre texte est prêt a être consulté sous le nom de TexteConvertiHuffman \n")
print ("Taux de compression : " + str(TauxCompression(Fichier,'TexteConvertiHuffman.txt')))
print ("Nb moyen de bits de stockage d'un caractère du texte : " + str(nbMoyenBits()))     
