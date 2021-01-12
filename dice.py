# Module pour les differents des - Grim, Fudge et de normal 

from copy import *
from random import randrange
import math

from abc import * 
class Dice():
    """ Class  des avec 
        des methodes associees """

    # constructor
    def __init__(self, typed='N', couleur = "white", faces=6,  probas=[], valeur=1):
        
        # si le de est de type GRIM 
        if typed is 'G':
            self._valeur = valeur%6 + 1 
            self._faces = 6
            
            if couleur is "green":
                self._couleur = couleur
                self._probas = [1/6, 0, 0, 5/6, 0, 0]
            
            elif couleur is "blue":
                self._couleur = couleur
                self._probas = [0, 3/6, 0, 0, 3/6, 0]
            
            else:
                self._couleur = "red"
                self._probas = [0, 0, 5/6, 0, 0, 1/6] 

        else:
            self._valeur = valeur % faces # dans le cas de mauvais input
            self._faces = faces
            length = len(probas)
            
            if(length ==  0 or length < faces): # assurant le bon input
                equiprob = 1/faces
                self._probas = [equiprob for i in range(faces)] # equiproba dans le cas d'une liste de
            #  de proba vide               
            else:
                self._probas = [i for i in probas]
            
            self._couleur = couleur
    
    #special methods
    def __str__(self):
        print(self.probas)
        return "faces - %d  valeur - %d, couleur - %s " % (self._faces, self._valeur, self._couleur)
    
    # Accessors , a utiliser avec property!
    def  get_valeur(self):
        return self._valeur
    
    def get_faces(self):
        return self._faces
    
    def get_couleur(self):
        return self._couleur 
    
    def get_probas(self):
        return self._probas
    
    def set_valeur(self, value):
        self._valeur = value

    def set_faces(self, faces):
        self._faces = faces
    
    def set_couleur(self, couleur):
        self._couleur = couleur

    def set_probas(self, probas):
        self._probas = [i for i in probas] # probas has to be a list
    
    def set_faces(self, faces): # faces doit etre un entier!
        self._faces = faces 

    # Indicating methods for protected variables
 
    valeur = property(get_valeur, set_valeur)
    faces = property(get_faces, set_faces)
    couleur = property(get_couleur, set_couleur)
    valeur = property(get_valeur, set_valeur)
    faces = property(get_faces, set_faces)
    probas = property(get_probas, set_probas)
    # Methods
    
    @abstractmethod
    def lancer(self):
        """ Methode qui retourne la face après un lancement aléatoire
        associant la valeur obtenue avec une region de cercle trigo
        """

        alpha = 0
        gamma = randrange(0, 360) # angle au hasard 
        for proba in range(len(self.probas)):
            angle = self.probas[proba]*360 + alpha 
            if  alpha <= gamma < angle:
                self.valeur = proba + 1 # correspond a la face  
                return  
            else:
                alpha = angle
         
    


class Fudge(Dice):
    """ Specification d'une des de type Fudge.
        Le des va avoir seulement 6 faces 
        avec 2 faces positives, 2 negatives et
        2 neutres(0).
    """
    

    # constructor

    def __init__(self, probas=[], couleur="white",nef=(1,2), posf=(3,4), neuf=(5,6),valeur=1):
        super(Fudge, self).__init__('N', couleur, 6, probas, valeur) # initialisation de la classe mere
        # nef, posf, neuf doivent etre des tuples avec deux entiers dedans
        # encapsulation omises , implementee dans la classe de base
        self.nef = nef
        self.posf = posf 
        self.neuf = neuf
    
    # methodes speciales 

    def __str__(self):
        super().__str__()
        return " neg faces - %d %d, pos faces - %d %d, neut faces - %d %d"%(self.nef[0], self.neuf[1], self.posf[0],
                self.posf[1], self.neuf[0], self.nef[1])

    
    # methodes normales

    def lancer(self): # polymorphisum
        """ Lancement de des suivant les regles de lancement 
            d'une des de type Fudge """ 

        super().lancer() # lancement avec le proba associee
        if self._valeur in self.nef:
            self._valuer = -1
        
        elif self._valeur in self.posf:
            self._valeur = 1 
        
        else:
            self._valeur =  0

    # MODERATEUR OMISES , IMPLEMENTEES DANS LA CLASSE BASE


def somme_des(listf): # listf - liste des des de Fudge
    """ La fonction va retourner la somme des des 
        de Fudge ou des dés normaux 
    """ 

    somme = 0
    for de in listf:
        de.lancer()
        somme += de.valeur 
    
    return somme 

   

def game_Grim(dicet1, dicet2): # dicet1&2 - liste des des de type Grim
    """ La fonction retournera 0 (resp 1) en fonction des des 
        gagnant - des de type 1 (resp des de type 2)
    """ 
   
    somme1, somme2 = 0, 0
   # lancement de des 
     
    for couple in zip(dicet1, dicet2):
       for dice in couple:
           dice.lancer()

       somme1 += couple[0].valeur
       somme2 += couple[1].valeur

    return 1 if somme1 > somme2 else 0 
 


