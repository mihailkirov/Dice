from tkinter import *
from exo1 import create_rgb  
#initialisation du systeme graphique

NUMBCOL = 10 # number of colours per line
LARGEUR, HAUTEUR = 400, 300


def convert2(liste): 
    
    res = "#"
    for dig in liste: 
        tmp = str(hex(dig))
        if(len(tmp)) < 4:
            res += '0'
        res += tmp[2:] 

    return res
        

    

def draw_rect(width, height):
    """ Function drawing rectangles with rgb system file
        colours """
    
    coldictk = create_rgb() # key-colour name
    hexacol = list()
    for k in coldictk.keys():
        hexacol.append(convert(coldictk[k]))
        
    i, ecart = 0, 10
    k= list(coldictk.keys())
    ncol = len(hexacol)
    objl = list() # container for rectangular objects
    posy = 0
    while i < ncol:
        j = 0
        posx, curr = 0, 0
        while i < ncol and j < NUMBCOL:
            objl.append(canvas.create_rectangle(posx, posy, posx + width, posy+height,
                fill=hexacol[i], tags=(hexacol[i], k[i])))
            
            posx += width
            i += 1
            j += 1
     
        posy += height  

    
    return objl


# BINDINGS
def change_colour(event): # if ok buttons is pressed
    
    global colour
    root.configure(background=colour)


def select_col(event):
    global colour 
    id = canvas.find_withtag("current")
    colour = canvas.gettags(id)[0] # the hexadecimal represantation of the colour


def affiche_text(event):
    """ Function displaying colours """
    
    global p
    id = canvas.find_withtag("current")
    p.set(canvas.gettags(id))

def kill_it(event): #closing the toplevel window
    w.destroy()


##################################################################
if __name__ == '__main__':

# Window
    root = Tk()
    root.geometry("500x375+300+30")
    root.title("Une fenetre") # titre de la fenetre

# Second window
    w = Toplevel()
    w.geometry("400x300+30+30")
    w.title("Fenetre2")

# Variables for widgets 
    p = StringVar()
    p.set("Hello!")
    colour = str() # for saving the colour 
    
# label 
    label = Label(w, textvariable=p)
    label.pack()

# Frame 1
   # TopFrame = Frame(w)
   # TopFrame.pack()

#Frame 2
    BottomFrame = Frame(w)
    BottomFrame.pack()

# Canvas widget 
    canvas = Canvas(w, width = 400, height = 300, bg = "white")
    obj =  draw_rect(40, 15) 
   
 
# scrollbar
    hbar = Scrollbar(w)
    hbar.pack(side=RIGHT, fill=Y)
    hbar.config(command=canvas.yview)
    canvas.config(scrollregion=canvas.bbox("all"), yscrollcommand=hbar.set)

    canvas.pack()  
            
# Buttons 
    button1 = Button(BottomFrame, text = "OK", fg = "red")
    button1.pack(side = LEFT)
    button2 = Button(BottomFrame, text = "Annuler", fg = "red")
    button2.pack(side = LEFT)
    canvas.bind("<Motion>", affiche_text)
    canvas.bind("<Button-1>", select_col) # the selected colour with a mouse click will be saved 
    button1.bind('<Button-1>', change_colour)
    button2.bind('<Button-1>', kill_it)
    root.mainloop()


