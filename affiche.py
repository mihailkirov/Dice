from dice import *
# Module table d'affichage et d'autre fonctons lies au l'affichage


class Table():
    """ Table qui stockera et affichera 
        les resultats de n lancees des des 
    """

    def __init__(self):
         self.results = list()
         self.numlanc = 0 

    def get_results_tour(self, n):
        """ Retourne les resultats 
            de lancer n 
        """
        return self.results[n] 
    
    def add_result(self, ldes): # res - une liste
        """ Add le resultat de lancer n dans 
            le dico res
        """ 
        tmp = [des.valeur for des in ldes]  
        self.results.append(tmp)
        self.numlanc += 1
    
    def __str__(self):
        x = str()
        for elem in range(self.numlanc):
            x +=  "Tour - {} - {}\n".format(elem, self.results[elem]) 
        return x
    
    def get_result(self):
        
        return self.results

