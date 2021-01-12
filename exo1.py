# TP1 

def convert(liste):
   
   chaine = liste[3][0].upper() # standartizing
   chaine += liste[3][1:]
    
   for i in range(4, len(liste)):
       chaine +=  ' ' 
       chaine += liste[i]

    
   return chaine 

def affichage(dicto):
    """ Function sorts dictionnary keys and separate integers from strings 
    """

    keys =list(dicto.keys())
    keys.sort()
    lenght = len(keys)
    for i in range(lenght):
        sublenght = len(keys[i]) - 1
        j = sublenght
        while(keys[i][j].isdigit()): # separating integers
            j -=  1
        
        if(j != sublenght):
            keys[i] = keys[i][:j + 1] + " " + keys[i][j + 1:]

     
    return keys


def create_rgb():
    " Creating dictionnary with keys - colour name and key-value - RGB code " 

    dico = dict()
    with open("/etc/X11/rgb.txt", "r") as f:
        f.readline()
        for line in f:
            tmp = line.split()
            tmpl = tmp[:3]
            ltmp = list(map(int, tmpl))           
            dico[convert(tmp)] = ltmp     
   
    return dico

if __name__ == '__main__':

   dic =  create_rgb()
   #affichage(dic)
