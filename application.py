import tkinter as tk
import math
import numpy as np
import time 
from exo1 import * # for dictionnary X11 colours
from partie2 import *
from tkinter import ttk
from tkinter import messagebox
from dice import *
from  affiche  import *
### Variable globales #################

DICE_6 = Dice('N',"red", 6)
DICES = list()
DICES.append([DICE_6]) # default
TABLE = False # table de resultat

colours = create_rgb() # dictonnaire avec les noms des coleurs et les valeurs rgb
for key in colours.keys():
    colours[key] = convert2(colours[key]) # conversion vers hexadecimal 
    


##################### FONCTIONS INTERNES ########################
def draw_points(canvas, point, r, colour):
    """ Dessin des disques avec des 
        coordonnees de centres coords
        et rayon r 
    """     
    canvas.create_oval(point[0]-r, point[1]-r, point[0]+r, point[1]+r, fill=colour, tags="points")


def points_dice(canvas, coord):
    """ Fonction qui retourne une liste de coord
        des  points de de 6 (x,y)
    """
    
    res = list() 
    xmoy = abs(coord[0]-coord[2])/2 + coord[0] 
    ymoy = abs(coord[1] - coord[3])/2 + coord[1]
    res.append([xmoy, ymoy])
    poidsx = 3*(xmoy - coord[0])/4
    poidsy = 3/4*(ymoy - coord[1])
     
    for i in range(2):
        ytmp = ymoy +  poidsy*(-1)**i 
        for j in range(2):
            xtmp = xmoy + poidsx*(-1)**j
            res.append([xtmp, ytmp])
    
    # derniers 2 points au tour de centre du de 
    res.append([xmoy - poidsx, ymoy])
    res.append( [xmoy + poidsx, ymoy])    
   
    return res

###################### BINDINGS #########################3

def change_a_to_b(event, a, b): 
    """ Unpacking frame a and packing frame b
        a,b peuvent prendre - 1,2,3. 1 pour 
        frame 1(menu),2- frame options
        3 pour frame play
    """ 
    global root 
    global DICES, DICE_6, TABLE
    
    if (a == 2 and b == 1):
        root.fenetre_options.pack_forget()
        root.fenetre_acceuil.pack(fill="both", expand=True) 
        root.fenetre_acceuil.animmation(0.01)
    
    elif(a == 1 and b == 2):
        root.fenetre_acceuil.pack_forget()
        root.fenetre_options.pack(fill="both", expand=True)

    elif(a == 2 and b == 3):
            
        root.fenetre_options.pack_forget()
        root.fenetre_play.pack(fill="both", expand=True)
        root.fenetre_play.create_dices()
        
    elif(a == 3 and b == 2): 
        
        root.fenetre_play.pack_forget()
        root.fenetre_options.pack(fill="both", expand=True)
    
    elif(a == 3 and b == 1):
        answer = tk.messagebox.askquestion("Quit", "Vous-voulez sortir?")
        if answer ==  "yes":
            root.fenetre_play.clean()
            root.fenetre_play.pack_forget()
            root.fenetre_acceuil.pack(fill="both", expand=True)
            root.fenetre_acceuil.animmation(0.01)
            TABLE=False 
    
    elif(a == 1 and b == 3):

        root.fenetre_acceuil.pack_forget()
        DICES = list()
        DICES.append([DICE_6])
        root.fenetre_play.pack(fill="both", expand=True)
        root.fenetre_play.create_dices()
         

####################### CLASSES INTERNES ######################3

class Frame_menu(tk.Frame):
    """ Class frame menu """
    
    decx, decy = 60, 60
    
    def __init__(self, master, width, height, colour="white", releif=tk.FLAT):
        super().__init__(master, bg=colour, relief=releif)
        
        # CANVAS
        self.width_c = width
        self.height_c = height//2 
        self.canv = tk.Canvas(self, width=self.width_c, height=self.height_c, bg="#ccffcc", relief=releif)
        
        
        self.canv.create_rectangle(self.width_c//2-Frame_menu.decx, self.height_c//2 - Frame_menu.decy,
                self.width_c//2+Frame_menu.decx, self.height_c//2 + Frame_menu.decy, fill="white", tags="dice")
        
        self.canv.pack()
        
        # FRAME
        self.frame = tk.Frame(self, bg=colour, relief=tk.FLAT) # se positionnera au-dessous de canvas
        
        self.frame.pack(fill="both", expand=True)
        
        # BUTTONS
        self.button1 = tk.Button(self.frame, text="HELP", fg="black", activebackground="white", borderwidth=2) 
        
        self.button3 = tk.Button(self.frame, text="OPTIONS", fg="black", activebackground="white", borderwidth=2) 
        self.button3.bind('<Button-1>', lambda x: change_a_to_b(x, 1, 2))    
        self.button2 = tk.Button(self.frame, text="PLAY", fg="black", activebackground="white", borderwidth=2)   
        
        self.button2.pack(side=tk.BOTTOM)
        self.button2.bind('<Button-1>', lambda x: change_a_to_b(x, 1, 3))
        self.button1.pack(side=tk.LEFT)

        self.button3.pack(side=tk.RIGHT)
        self.button3.bind('Button-1', lambda x: change_a_to_b(x, 1, 2))
    
       
   
    def animmation(self, t):
        """ Methode pour afficher l'animation
               de rectangle sur le canvas 
        """
        coord = self.canv.coords("dice")
        cords_points = points_dice(self.canv, coord) 
        for i in range(5):
            draw_points(self.canv, cords_points[i], 4,"black")
            time.sleep(t) # 0.3
            self.canv.update_idletasks()



class Frame_options(tk.Frame):
    """ Frame pour les options 
        de l'applications
    """
    
    def __init__(self, master, width, height, colour="white", rel=tk.FLAT):
        super().__init__(master, bg=colour, relief=rel)
    
       #################  FRAME1  ########################
        
        self.frame1 = tk.Frame(self, bg=colour, relief=rel) 
        self.frame1.pack(expand=1)
        
        # RADIO BOUTONS
        col = 2
        self.var = tk.IntVar() # pour type de jeu
        radio = tk.Radiobutton(self.frame1, text = "normal".capitalize(), variable=self.var, relief=rel, bg=colour,
                value=0 ,command= self.change_game)
        radio.grid(column=2*col, row=0, padx=4) 
        
        col += 1 
        radio = tk.Radiobutton(self.frame1, text = "grim".capitalize(), variable=self.var, relief=rel, bg=colour, value=1,
                command=self.change_game)
        radio.grid(column=2*col, row=0, padx=4) 
        
        col += 1 
        radio = tk.Radiobutton(self.frame1, text = "fudge".capitalize(), variable=self.var, relief=rel, bg=colour, value=2,
                command= self.change_game)
        radio.grid(column=2*col, row=0, padx=4) 
        
        # Table resultat
        self.table_check = tk.BooleanVar()
        self.table_check.set("False")
        self.table_result = tk.Checkbutton(self.frame1, text="Table Resultat", relief=rel, bg=colour,
                var=self.table_check)
        self.table_result.grid(column = 2*(col+1), row=0, padx=4)
    

###################  FRAME 2 ################################## 
        self.frame2 = tk.Frame(self, bg=colour, relief=rel)
        self.frame2.pack( expand=1)


######################  labelling ########################## 
        for i in range(2, 10):
            txt = "D" + str(i)
            tk.Label(self.frame2, text=txt, bg=colour).grid(column=(i)*2, row=2, padx=10)
             

################ buttons colour ########################
    
        self.buttons_id_colour = dict() # association d'un button couleur avec la couleur selectionnee  
            
        
        for i in range(2, 10):
            tmp = tk.Button(self.frame2, text="Colour", activebackground="white", borderwidth=2, width=2,
            state='disabled')
            tmp.bind('<Button-1>', self.dice_colour)
            tmp.grid(column=(i)*2, row=4, padx=10, pady=10)
            
            self.buttons_id_colour[tmp] = [tk.StringVar() for i in range(10)]   
            #  default
            for elem in self.buttons_id_colour[tmp]:
               elem.set("Snow") 
    
        self.buttons_id = list(self.buttons_id_colour.keys())

############### BUTTONS POIDS ########################
        self.buttonp = dict()            
        for i in range(2, 10):
             tmp = tk.Button(self.frame2, text="Poids", activebackground="white", borderwidth=2, width=2,
             state='disabled')
             
             tmp.bind('<Button-1>', self.poids_select) 
             tmp.grid(column=(i)*2, row=5, padx=5, pady=10)
             # par defaut 
             self.buttonp[tmp] = [[] for i in range(10)] # [] pour le nombre maximum de des 
            
        self.buttpoids_id = list(self.buttonp.keys())

############################### bonus malus ###############
        self.bonus_id = dict()
        for i in range(2, 10):
             tmp = tk.Button(self.frame2, text="bonus", activebackground="white", borderwidth=2, width=2,
             state='disabled')
             self.bonus_id[tmp] = [tk.IntVar() for i in range(2)]
             for var in self.bonus_id[tmp]:
                 var.set(0)

             tmp.bind('<Button-1>', lambda x: self.bonus(x)) 
             tmp.grid(column=(i)*2, row=6, padx=5, pady=10)
        
        self.bonus_but_id = list(self.bonus_id.keys())

##################### spinboxes ##########################3
        self.spinbox = list() # liste pour sauvegarde des spinboxes spinboxes
        self.numb_spinbox = 0
        self.spinbox_vars = [tk.IntVar(name =str(i)) for i in range(8)]
        for i in range(8):
            self.spinbox_vars[i].trace("w", self.change)
        
        for i in range(2, 10): 
            tmp = tk.Spinbox(self.frame2, from_=0, to=10, increment=1, insertborderwidth=1, selectborderwidth=2, width=3,
                    textvariable=self.spinbox_vars[i-2])
            
            self.spinbox.append(tmp)
            tmp.grid(column=(i)*2, row=3, padx=10, pady=10)
            self.numb_spinbox += 1


######################## Frame 3 ########################### 
        self.frame3 = tk.Frame(self, bg=colour, relief=rel)
        self.frame3.pack(expand=1)
        tmp = tk.Button(self.frame3, text="Retour", activebackground="white", width=6)
        tmp.bind('<Button-1>', lambda x: change_a_to_b(x, 2, 1))
        tmp.pack(side=tk.LEFT)
        self.button_apply = tk.Button(self.frame3, text="Appliquer", activebackground="white", width=6)
        self.button_apply.bind('<Button-1>', lambda x:self.apply_changes(x)) # initialisation
        self.button_apply.pack(side=tk.RIGHT)
        
        self.button_play = tk.Button(self.frame3, text="Play", activebackground="white", width=6, state=tk.DISABLED)
        self.button_play.bind('<Button-1>', lambda x: change_a_to_b(x, 2, 3))
        self.button_play.pack(expand=1, fill="none")

    def change(self, *args):
        """ Methode modifiant l'accesibilite des boutons 
            associes aux certains des apres un changement 
            de la valeur de la spinbox associee 
        """
        variable_ind = int(args[0])
        value = self.spinbox_vars[variable_ind].get()
        if value:
           self.buttons_id[variable_ind].configure(state='normal')
           self.buttpoids_id[variable_ind].configure(state='normal')
           self.bonus_but_id[variable_ind].configure(state='normal') 
        else:
           self.buttons_id[variable_ind].configure(state='disabled')
           self.buttpoids_id[variable_ind].configure(state='disabled')
           self.bonus_but_id[variable_ind].configure(state='disabled') 
            
            
         
    def couleur_sauvegarde(self, event, widget, master, liste):#liste - liste de string vars
        """ Modification de l'attribut couleur du de en fonction
            de la valeur choisie dans le combobox 
        """
        index = 0
        for elem in liste:
            self.buttons_id_colour[widget][index].set(elem.get())
            index += 1
        master.destroy()
    
    def dice_colour(self, event):
        """ Listbox pour changement de la 
            couleur d'un de
        """
        window = tk.Toplevel()
        window.geometry("400x300+30+30")
        index = list(self.buttons_id_colour.keys()).index(event.widget)         
        # spinbox value 
        value = int(self.spinbox[index].get())%10 # en cas de mauvais input
        # Variable pour recuperer les informations des spinboxes
        liste_colours =  list() 
        liste_spinbox = list()
        
        for i in range(value):
            tk.Label(window, text="dé" + str(i+1)).grid(column=0, row=i, padx=5)
            col_act = self.buttons_id_colour[event.widget][i].get() # to show
            col_choisi = tk.StringVar() # to be modified
            col_choisi.set(col_act)
            tmp=ttk.Combobox(window, text='Choisissez la couleur :', values=list(colours.keys()),
                    textvariable=col_choisi, width=15, state='readonly')
            # identities
            liste_spinbox.append(tmp) 
            liste_colours.append(col_choisi)
            
            liste_spinbox[i].bind("<<ComboboxSelected>>", lambda x: liste_colours[i].set((liste_spinbox[i].get()))) 
            tmp.grid(column=1, row=i, padx=5) 
            
        
        butok =tk.Button(window, text="Ok")
        butok.bind('<Button-1>',lambda x: self.couleur_sauvegarde(x, event.widget, window, liste_colours))

        
        butok.grid(row=value, column=0, pady=5, sticky="nsew")        
        tk.Button(window, text="Annuler", command=window.destroy, width=3).grid(row=value, column=1, padx=3, pady=5,
                sticky="nsew") 
     
    
    def get_entries(self, master, widget, liste_entr):
        """ Methode qui enregistre
            dans le dictionnaire des butons poids
            le contenu des entryboxes dans la liste liste_entr  associees au widget. Fermeture de master window 
        """
        liste_probas = list()
        for dice_i in liste_entr:
            liste_probas_tmp = list()
            for elem in dice_i:
                if (elem.get().isdigit()):
                    liste_probas_tmp.append(int(elem.get()))
                else:
                    liste_probas_tmp.append(0)

            liste_probas.append(liste_probas_tmp)
        
        somme = [sum(dice) for dice in liste_probas] 
        for i in range(len(liste_probas)):
            liste_probas[i] = list(map(lambda x: x/somme[i], liste_probas[i]))
        self.buttonp[widget] = liste_probas
        master.destroy()
            


    def poids_select(self, event):
        """ Binding pour la selection des poids """

        window = tk.Toplevel()
        window.geometry("400x300+30+30")
        
        buttonspoids_tmp = list(self.buttonp.keys())
        nombre_faces = buttonspoids_tmp.index(event.widget) 
        liste_entries = list() # pour obtenir la valeur des enrys
        number_dice = int(self.spinbox[nombre_faces].get())
        
        # LABELS
        for i in range(nombre_faces + 2):
            tk.Label(window, text="f" + str(i+1)).grid(row=0, column=i+1)  
        for i in range(1, number_dice+1):
            tk.Label(window, text="de" + str(i)).grid(row=i, column=0)
            liste_entries_tmp = list()
            for j in range(nombre_faces + 2):
                tmp = tk.Entry(window, width=2)
                liste_entries_tmp.append(tmp)
                tmp.grid(row=i, column=j+1, padx=3, pady =3)
            
            liste_entries.append(liste_entries_tmp) 
        
        # Buttons 
        butok =tk.Button(window, text="Ok")
        butok.bind('<Button-1>', lambda x: self.get_entries(window, event.widget, liste_entries)) 
        butok.grid(row=number_dice+1, column=0, pady=5, sticky="nsew") 
        tk.Button(window, text="Annuler", command=window.destroy).grid(row=number_dice+1, column=1, padx=3, pady=5,sticky="nsew")

    def change_game(self):
            
            index = 0
            if self.var.get() == 0:  # si jeu normal
                for i in range(self.numb_spinbox):
                    tmp = int(self.spinbox[i].get())
                    self.spinbox[i].config(state="normal", from_=0, to=10, increment=1)
                    if tmp != 0: # de numero 6 
                                
                        self.buttons_id[i].config(state='normal')
                        self.buttpoids_id[i].config(state='normal')

                        self.bonus_but_id[i].config(state='normal')          
             
            else: 
                # Mettre en inactive tout les bouttons couleur, poids 
                # et les spinboxes qui ne sont pas destines au de 6 faces
                index = 0 
                for i in range(self.numb_spinbox):
                    if i != 4: # de numero 6 
                        self.spinbox[i].config(state="disabled")
                        self.buttons_id[i].config(state='disabled')
                        self.buttpoids_id[i].config(state='disabled')
                        self.bonus_but_id[i].config(state='disabled')          
                
                if self.var.get() == 1: # grim game 
                    self.spinbox[4].config(from_=0, to=4, increment=2)
                        
                else:
                    
                    self.spinbox[4].config(from_=0, to=10, increment=2)
            
    def get_bonus(self, master, widget, liste):
            index=0
            for i in liste:
                self.bonus_id[widget][index].set(i.get())   
            master.destroy()
    
    def bonus(self, event):
        """ Methode pour appliquer les bonus"""
                
        window = tk.Toplevel()
        window.geometry("400x300+30+30")
        
        #bonus
        liste_bonus = list()
        tk.Label(window, text="bonus").grid(column=0, row=0, padx=5)
        tmp = tk.IntVar()
        tmp.set(self.bonus_id[event.widget][0].get())
        tmp = tk.Entry(window, width=2, textvariable=tmp)
        liste_bonus.append(tmp)
        tmp.grid(column=1, row=0, padx=5)
        
        # seuil
        
        tmp = tk.IntVar()
        tmp.set(self.bonus_id[event.widget][1].get())
        tk.Label(window, text="seuil").grid(column=0, row=1, padx=5)
        tmp = tk.Entry(window, width=2, textvariable=tmp)
        liste_bonus.append(tmp)
        tmp.grid(column=1, row=1, padx=5)
        
        butok =tk.Button(window, text="Ok")
        butok.bind('<Button-1>', lambda x: self.get_bonus(window, event.widget, liste_bonus)) 
        butok.grid(row=2, column=0, pady=5, sticky="nsew") 
        tk.Button(window, text="Annuler", command=window.destroy).grid(row=2, column=1, padx=3, pady=5,sticky="nsew")


 
    
    def apply_changes(self, event):
        """ Initialisation des de a partir
            des choix de utilisateur 
        """ 
        global DICES, TABLE 
        if self.var.get() == 0: # jeu normal
            buttonscol_tmp = list(self.buttons_id_colour.keys())
            buttonpoids_tmp = list(self.buttonp.keys()) 
            selected_dice = list() # stockage
            for i  in range(self.numb_spinbox):
                number = int(self.spinbox[i].get())  
                if number != 0 :
                    tmp = list()
                    for k in range(number):
                            col = self.buttons_id_colour[buttonscol_tmp[i]][k].get() # get la colueur k de button poids
                            poids = self.buttonp[buttonpoids_tmp[i]][k]
                            tmp.append(Dice('N', colours[col], i+2, poids))
                    selected_dice.append(tmp)        
                    self.button_play.configure(state='normal')
                    DICES = selected_dice


        # FUDGE 
        elif self.var.get() == 2: 
            buttonscol_tmp = list(self.buttons_id_colour.keys())
            buttonpoids_tmp = list(self.buttonp.keys()) 
            number = int(self.spinbox[4].get())
            if number != 0 :    
                tmp = list()
                for k in range(number):
                    col = self.buttons_id_colour[buttonscol_tmp[4]][k].get() # get la colueur k de button 
                    poids = self.buttonp[buttonpoids_tmp[4]][k]
                    tmp_fudge = Fudge(poids, colours[col]) 
                    tmp.append(tmp_fudge)
                
                DICES = tmp
                self.button_play.configure(state='normal')
                
        if self.table_check:
                TABLE = True
        else:
            TABLE = False
        


class Frame_play(tk.Frame):

    def __init__(self, master, height, width, col, rel):
        
        super().__init__(master)
        self.canv = tk.Canvas(self, width=500, height=height, bg=col, relief=rel)
        hbar = tk.Scrollbar(self.canv, orient=tk.VERTICAL) 
        hbar.pack(side=tk.RIGHT, fill=tk.Y)
        hbar.config(command=self.canv.yview)
        
        self.canv.config(yscrollcommand=hbar.set)
        self.canv.pack(fill="both", expand=1, side=tk.LEFT)
        self.frame = tk.Frame(self, relief=rel, bg="red", width=width/3)
        self.frame.pack(side=tk.RIGHT, fill="both")
        # row
        self.button_row = tk.Button(self.frame, text="row", width=6)
        self.button_row.bind('<Button-1>', lambda x :self.row_dice(x))
        self.button_row.pack(side=tk.BOTTOM)
        
        #options
        tmp = tk.Button(self.frame, text="Options", activebackground="white", width=6)
        tmp.bind('<Button-1>', lambda x: change_a_to_b(x, 3, 2))
        tmp.pack(side=tk.BOTTOM)
        # menu
        tmp = tk.Button(self.frame, text="Menu", activebackground="white", width=6)

        tmp.bind('<Button-1>', lambda x: change_a_to_b(x, 3, 1))
        tmp.pack(side=tk.BOTTOM)
        self.button_res = tk.Button(self.frame, text="Resultats", activebackground="white", width=6, state='disabled')
        self.button_res.pack(side=tk.BOTTOM)
        
        self.entry = tk.IntVar() # pour automatiser les lances
        tk.Entry(self.frame, width=6, textvariable=self.entry).pack(side=tk.BOTTOM)

            
    
    def create_dices(self):
        """ Positionnement des 'dices' de la liste DICES"""
        
        self.canv.delete("lines","circles","text","oval") 
        global DICES, TABLE
        
        if TABLE == True:
            self.table_res = Table()
            self.button_res.configure(state='normal')
            self.button_res.bind('<Button-1>', lambda x: self.show_res(x))

        else:
            self.button_res.configure(state='disabled')
            self.n_lances = 1 
            self.button_res.unbind('<Button-1>')


        x, y = 1, 1
        dim = 60
        for face in DICES:
            for dice in face:
                if not x%11:
                    x = 1   
                    y += 2 
                 
                self.create_dice(dice.faces, 30, x*dim, y*dim, dice.couleur)
                dice.lancer()
                self.create_points(dice, x*dim, y*dim, 5)
                x += 2
    

    
    def create_dice(self, face, r, x, y, col):
                
                self.obj = list()
                # x + 20 -- centre de cercle virtuel, puisque dimention 40 
                if face == 6:
                    n = face//2
                    for i in range(n):
                        x1 = int(x + 30 + r*math.cos(i*2*math.pi/(face/2)))
                        y1 = int(y + 30 + r*math.sin(i*2*math.pi/(face/2)))
                    
                        self.obj.append(self.canv.create_line(x+30, y+30, x1, y1, width=2, fill=col, tags="line"))
                   
                        x2 = int(x + 30 + r*math.cos(i*2*math.pi/(face//2) + 1)) 
                        y2 = int(y + 30 + r*math.sin(i*2*(math.pi)//3 + 1))
                        self.obj.append(self.canv.create_line(x1, y1, x2, y2, width=2, fill=col, tags="line"))
                        
                        x3 = int(x + 30 + r*math.cos(i*2*math.pi/3-1))  
                        y3 = int(y + 30 + r*math.sin(i*2*(math.pi)/3-1)) 
                        self.obj.append(self.canv.create_line(x3, y3, x1, y1, width=2, fill=col, tags="line"))
                         
                elif face == 8:
                    for i in range(face//2):
                        x1 = int(x + 30 + r*math.cos(i*2*math.pi/(face/2)))
                        y1 = int(y + 30 + r*math.sin(i*2*math.pi/(face/2)))
                
                        self.obj.append(self.canv.create_line(x+30, y+30, x1, y1, width=3, fill=col, tags="line"))
                    

                        x2 = int(x + 30 + r*math.cos(i*2*math.pi/(face/2)+1)) 
                        y2 = int(y + 30 + r*math.sin(i*2*(math.pi)/(face/2)+1))
                        self.obj.append(self.canv.create_line(x2, y2, x1, y1, width=3, fill=col, tags="line"))
                         
                        x3 = int(x + 30 + r*math.cos(i*2*math.pi/(face/2)-1))  
                        y3 = int(y + 30 + r*math.sin(i*2*(math.pi)/(face/2)-1)) 
                        self.obj.append(self.canv.create_line(x1, y1, x3, y3, width=3, fill=col, tags="line"))
                
                
                elif face == 4: 
                    for i in range(face - 1):
                        x1 = int(x + 30 + r*math.cos(i*2*math.pi/(face-1)))
                        y1 = int(y + 30 + r*math.sin(i*2*math.pi/(face-1)))
                    
                        self.obj.append(self.canv.create_line(x+20, y+20, x1, y1, width=3, fill=col, tags="line"))
                        x2 = int(x + 30 + r*math.cos(i*2*math.pi/3+2))
                        y2 = int(y + 30 + r*math.sin(i*2*math.pi/3+2))
                        self.obj.append(self.canv.create_line(x1, y1, x2, y2, width=3, fill=col, tags="line"))


                elif face == 2:
                    self.obj.append(self.canv.create_oval(x, y, x+2*r, y+2*r, width=2, fill=col, tags="oval"))
                
                else:
                    for i in range(face):
                        x1 = int(x + 30 + r*math.cos(i*2*math.pi/face))
                        y1 = int(y + 30 + r*math.sin(i*2*(math.pi)/face)) 
                        x2 = int(x + 30 + r*math.cos((i+1)*2*math.pi/face))
                        y2 = int(y + 30 + r*math.sin((i+1)*2*(math.pi)/face)) 
                        self.obj.append(self.canv.create_line(x2, y2, x1, y1, width=2, fill=col, tags="line")) 
                        
                
    def create_points(self,  dice, x, y, r):
            """ Methode pour affichage des points sur les 
                des
            """
        
            self.points_obj = list()
            if dice.valeur == 1:
                self.points_obj.append(self.canv.create_oval(x+30-r, y+30-r, x+30 +r, y+30+r, width=0, fill='black', tags= "circle"))
	    
            elif dice.valeur == 2:
                self.points_obj.append(self.canv.create_oval(x+30-r, y+20-r, x+30+r, y+20+r, width=0, fill='black', tags= "circle"))
                self.points_obj.append(self.canv.create_oval(x+30-r, y+40-r, x+30+r, y+40+r, width=0, fill='black',
                    tags= "circle"))
	
            elif dice.valeur == 3:

                self.points_obj.append(self.canv.create_oval(x+15 +r, y+20+r, x+15-r, y+20-r, width=0, fill='black', tags= "circle"))
                self.points_obj.append(self.canv.create_oval(x+30 +r, y+30+r, x+30-r, y+30-r, width=0, fill='black', tags= "circle"))
	
                self.points_obj.append(self.canv.create_oval(x+45+r, y+40+r, x+45-r, y+40-r, width=0, fill='black', tags= "circle"))
        
            elif dice.valeur == 4:

                self.points_obj.append(self.canv.create_oval(x+15+r, y+20+r, x+15-r, y+20-r, width=0, fill='black', tags= "circle"))
                self.points_obj.append(self.canv.create_oval(x+15+r, y+40+r, x+15-r, y+40-r, width=0, fill='black', tags= "circle"))
                self.points_obj.append(self.canv.create_oval(x+45+r, y+20+r, x+45-r, y+20-r, width=0, fill='black', tags= "circle"))
                self.points_obj.append(self.canv.create_oval(x+45+r, y+40+r, x+45-r, y+40-r, width=0, fill='black', tags= "circle"))
	
            elif dice.valeur == 5:
                
                self.points_obj.append(self.canv.create_oval(x+15+r, y+20+r, x+15-r, y+20-r, width=0, fill='black', tags= "circle"))
                self.points_obj.append(self.canv.create_oval(x+15+r, y+40+r, x+15-r, y+40-r, width=0, fill='black', tags= "circle"))
                self.points_obj.append(self.canv.create_oval(x+30+r, y+30+r, x+30-r, y+30-r, width=0, fill='black', tags= "circle"))
                self.points_obj.append(self.canv.create_oval(x+45+r, y+20+r, x+45-r, y+20-r, width=0, fill='black', tags= "circle"))
                self.points_obj.append(self.canv.create_oval(x+45+r, y+40+r, x+45-r, y+40-r, width=0, fill='black', tags= "circle"))
            
            elif dice.valeur == 6:
                
                self.points_obj.append(self.canv.create_oval(x+15+r, y+20+r, x+15-r, y+20-r, width=0, fill='black', tags= "circle"))
                self.points_obj.append(self.canv.create_oval(x+15+r, y+40+r, x+15-r, y+40-r, width=0, fill='black', tags= "circle"))
                self.points_obj.append(self.canv.create_oval(x+15+r, y+30+r, x+15 -r, y+30-r, width=0, fill='black', tags= "circle"))
                self.points_obj.append(self.canv.create_oval(x+45 +r, y+20+r, x+45 -r, y+20-r, width=0, fill='black', tags= "circle"))
                self.points_obj.append(self.canv.create_oval(x+45+r, y+30+r, x+45-r, y+30-r, width=0, fill='black', tags= "circle"))
                self.points_obj.append(self.canv.create_oval(x+45+r, y+40+r, x+45-r, y+40-r, width=0, fill='black', tags= "circle"))
            
            else:
                self.canv.create_text(x + 30, y+30, fill="black", font="Times 20 italic bold", text="{} {}{}".format(dice.valeur,"/",  dice.faces), tags="text") 

    def row_dice(self, event):
        """ Methode pour lancer le de """
        
        global DICES, TABLE
        
        
        for i in range(int(self.entry.get()) + 1):
            self.canv.delete("circle", "text")
            x, y = 1, 1
            dim = 60
            for face in DICES:
                if(TABLE): # table de resultat
                    self.table_res.add_result(face)
                 
                for dice in face:
                    if not x%11:
                        x = 1   
                        y += 2 
                 
                    dice.lancer()   
                    self.create_points(dice, x*dim, y*dim, 5)
                    x += 2
    
    def clean(self):
        """ Suppression  des elements dans le Canvas 
         """ 
         
        self.canv.delete("all") 
    
    def show_res(self, event):
        """ Table des resultats """ 

        global DICES
        window = tk.Toplevel()
        window.geometry("400x300+30+30")
        listbox = tk.Listbox(window)
        hbar = tk.Scrollbar(listbox, orient=tk.VERTICAL) 
        hbar.pack(side=tk.RIGHT, fill=tk.Y)
        hbar.config(command=listbox.yview)
        listbox.pack(expand=1, fill="both")
        res = self.table_res.get_result()
        for i in range(len(res)): 
            listbox.insert(tk.END, 'Tour {}'.format(i)) 
            for j in range(len(res[i])):
                listbox.insert(tk.END,"Dice {}".format(j))
                listbox.insert(tk.END, res[i][j])
            listbox.insert(tk.END, '-----------') 

class Fenetre(tk.Tk):
    """ Class fenetre qui representera les
        differents frames de l'application
    """

    def __init__(self, width, height):
        super().__init__()
        self.geometry("%dx%d%+d%+d" % (width, height, 250, 50))
        self.minsize(width, height) # taille minimum de la fenetre
        self.maxsize(width, height) # taille maximum de la fenetre
        self.fenetre_acceuil = Frame_menu(self, width, height, "#ccffcc", tk.FLAT) 
        
        self.fenetre_acceuil.pack(fill="both", expand=True)
        self.fenetre_options = Frame_options(self, width, height, "#ccffcc", tk.FLAT)
        self.fenetre_play = Frame_play(self, height, width, "#ccffcc", tk.FLAT)
    
 
if __name__ == '__main__':

    root = Fenetre(700, 550) 
    root.fenetre_acceuil.animmation(0.3)
    root.mainloop() 

