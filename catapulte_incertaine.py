# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 10:45:02 2023
@author: Alain ETIENNE, Arts et Métiers, Campus de Metz
"""

__version__ = "1.0"


import math
import random as rng
import tkinter as Tk
import tkinter.ttk as Ttk
import tkinter.messagebox as msg
import tkinter.filedialog as fil
import numpy as np

# TODO : Générer un cas ou n cas (on fait des paramètres dans une plage données)
# TODO : Afficher la trajectoire
# TODO : Mettre une incertitude sur les frottements de l'air

class UI():
    def __init__(self) -> None:
        # Definition de l'interface et de ses composants
        self._donnees_groupes = {}
        self._windows = Tk.Tk()
        self._windows.title("Simulation de tirs de catapulte - Statatapulte")
        
        # Definition des variables d'interface et de leurs valeurs initiales
        self._nb_essai = Tk.IntVar()
        self._nb_essai.set(1)
        self._angle_charge = Tk.DoubleVar()
        self._angle_relache = Tk.DoubleVar()
        self._pos_fixe = Tk.DoubleVar()
        self._pos_mobile = Tk.DoubleVar()
        self._pos_masse = Tk.DoubleVar()
        
        # Définition des windgets de l'interface et de leur remplissage
        Tk.Label(self._windows, text = "Veuillez sélectionner votre groupe (obligatoire) :").grid(row=0, column=0, columnspan=2, sticky = "W", padx = 5, pady = 5)
        self._choix_equipe = Ttk.Combobox(self._windows)
        self._choix_equipe.grid(row = 0, column = 2, padx = 5, pady = 5, sticky = "WE")
        self.chargement_données_équipes()
        
        Tk.Label(self._windows, text = "Veuillez définir la configuration de votre catapulte :").grid(row=1, column=0, columnspan=3, sticky = "W", padx = 5, pady = 5)
        Tk.Label(self._windows, text = "Angle de charge (A2)").grid(row=3, column=0, sticky = "NE", padx = 5, pady = 5)
        Tk.Label(self._windows, text = "Angle de relaché (A1)").grid(row=2, column=0, sticky = "NE", padx = 5, pady = 5)
        Tk.Label(self._windows, text = "Position élastique point fixe (L1)").grid(row=4, column=0, sticky = "NE", padx = 5, pady = 5)
        Tk.Label(self._windows, text = "Position élastique point mobile (L2)").grid(row=5, column=0, sticky = "NE", padx = 5, pady = 5)
        Tk.Label(self._windows, text = "Position masse mobile (L3)").grid(row=6, column=0, sticky = "NE", padx = 5, pady = 5)
        
        Tk.Scale(self._windows,orient = "horizontal", variable = self._angle_charge, from_ = 90 , to = 180, resolution = 0.5).grid(row = 3, column = 1)
        Tk.Scale(self._windows,orient = "horizontal", variable = self._angle_relache, from_ = 90 , to = 180, resolution = 0.5).grid(row = 2, column = 1)
        Tk.Scale(self._windows,orient = "horizontal", variable = self._pos_fixe, from_ = 0.1 , to = 0.2, resolution = 0.005).grid(row = 4, column = 1)
        Tk.Scale(self._windows,orient = "horizontal", variable = self._pos_mobile, from_ = 0.1 , to = 0.2, resolution = 0.005).grid(row = 5, column = 1)
        Tk.Scale(self._windows,orient = "horizontal", variable = self._pos_masse, from_ = 0.201 , to = 0.3, resolution = 0.005).grid(row = 6, column = 1)
        
        illustration = Tk.PhotoImage(file = "Statatapulte.gif")
        Tk.Label(self._windows, image = illustration, borderwidth = 2, relief="groove").grid(row = 2, column = 2, rowspan = 5, padx = 5, pady = 5)

        Tk.Spinbox(self._windows, from_ = 1, to = 200, width = 5, textvariable = self._nb_essai).grid(row = 7, column = 0, sticky = "E", padx = 5, pady = 5)
        Tk.Button(self._windows,text = "Lancer la simulation", command = self.lancer_simulations).grid(row = 7, column = 1, columnspan = 2, sticky = "WENS", padx = 5, pady = 5)
        
        # Gestion des evenement (surtout pour les curseurs pour éviter qu'ils aboutissent à des configurations incompatibles)
        
        
        # Lancement de l'interface
        self._windows.mainloop()
        
    def chargement_données_équipes(self):
        # On vérifie l'existance du fichier, puis on le charge des informations de groupes
        import os
        import xml.etree.ElementTree as xml
        if os.path.exists("groupes.xml"):
            arbreXML = xml.parse("groupes.xml")
            tronc = arbreXML.getroot()
            self._choix_equipe.delete(0, "end")
            valeurs = []
            for _el in tronc.findall("Groupe"):
                self._donnees_groupes[_el.attrib["Nom"]] = {i:j for i,j in _el.items() if i != "Nom"}
                valeurs.append(_el.attrib["Nom"])
            self._choix_equipe['values'] = valeurs
            self._choix_equipe.current(0)
            del(tronc)
        else:
            msg.showerror("Fichier inexistant", "Le fichier xml de configuration des groupes n'éxiste pas")
            print("Le fichier xml de configuration des groupes n'éxiste pas")
        
    def lancer_simulations(self):
        # On vérifie qu'un groupe est bien sélectionné !
        if self._choix_equipe.get() != None:
            # On vérifie que la configuration de la simulation est ok et on instancie une catapulte
            if self._angle_relache.get() < self._angle_charge.get():
                if self._pos_masse.get() >= self._pos_mobile.get():
                    # Instantiation de la catapulte, puis définition de ses caractéristiques incertaines
                    une_catapulte = Catapulte_Incertaine(self._angle_relache.get(), self._angle_charge.get(), self._pos_fixe.get(), self._pos_mobile.get(), self._pos_masse.get())
                    une_catapulte.definir_ecarts_type(self._donnees_groupes[self._choix_equipe.get()])
                    
                    # Génération des simulations et stockage du.des résultat.s
                    resultats = une_catapulte.calculer_trajectoires(0.1, False, self._nb_essai.get())
                                        
                    # On demande le fichier d'enregistrement et on propose un nom de fichier généré sur date + heure + confuration
                    filename = "A1-{}_A2-{}_L1-{}_L2-{}_L3-{}".format(self._angle_relache.get(), self._angle_charge.get(), self._pos_fixe.get(), self._pos_mobile.get(), self._pos_masse.get())
                    path = fil.asksaveasfile(initialfile = '{}.csv'.format(filename), defaultextension=".csv", filetypes=[("Csv files","*.csv")])
                    resultats = np.array(resultats)
                    resultats.tofile(path, sep =";")
                else:
                    msg.showerror("Problème positions", "Une incompatibilité des positions de la masse et du ressort mobile a été détectée")
                    print("Une incompatibilité des positions de la masse et du ressort mobile a été détectée")
            else:
                msg.showerror("Problème angles", "Une incompatibilité d'angle a été détectée, veuillez la corriger")
                print("Une incompatibilité d'angle a été détectée, veuillez la corriger")
        
    def generer_plan_exp(self):
        #TODO : A voir pour une prochaine version
        pass

class Catapulte():
    def __init__(self, angle_butee : float, angle_charge : float, pos_ressort_fixe : float, pos_ressort_bras : float, pos_masse : float):
        
        # Paramètres descriptifs de la catapulte
        self._angle_butee = 90.0  #°
        if float(angle_butee) >= 90.0 and float(angle_butee) <= 180 : self._angle_butee = float(angle_butee)
        self._angle_charge = 180.0 #°
        if float(angle_charge) > self._angle_butee and float(angle_charge) <= 180 : self._angle_charge = float(angle_charge)
        self._h_ressort_fixe = 0.1 #m
        if float(pos_ressort_fixe) >= 0.1 and float(pos_ressort_fixe) <= 0.2 : self._h_ressort_fixe = float(pos_ressort_fixe)
        self._r_ressort_bras = 0.1 #m
        if float(pos_ressort_bras) >= 0.1 and float(pos_ressort_bras) <= 0.2 : self._r_ressort_bras = float(pos_ressort_bras)
        self._r_masse = 0.201 #m
        if float(pos_masse) >= 0.201 and float(pos_masse) <= 0.3 : self._r_masse = float(pos_masse)
        
        # Paramètres non modifiable dans le plan d'expériences
        self._raideur_elastique = 30 #N.m
        self._masse_projectile = 1E-2 #kg
        self._g = 9.81 #m.s-2 accélération de pesanteur
        self._entraxe = 0.2 #m
    
    # Jeu d'accesseurs et de mutateurs pour modifier la configuration du système
    # TODO : gérer les écarts via les accesseurs (loi gaussiennes)
    
    def __repr__(self):
        return f"Catapulte_nominale : @butee = {self._angle_butee}, @charge = {self._angle_charge}, pos_ressort_fixe = {self._h_ressort_fixe}, pos_ressort_bras = {self._r_ressort_bras}, pos_masse_bras{self._r_masse}"
    
    # Fonctions de convertion des angles de la catapulte
    def _retourner_angle_butee_rad(self):
        return self._angle_butee * math.pi / 180.0
    angle_butee_rad = property(_retourner_angle_butee_rad)
    def _retourner_angle_charge_rad(self):
        return self._angle_charge * math.pi / 180.0
    angle_charge_rad = property(_retourner_angle_charge_rad)
    
    def calculer_trajectoire(self, pas : float = 0.01, plot : bool = False): # -> tuple[list[float],list[float],list[float],float]:
        
        def _calculer_positions() -> dict:
            positions = dict()
            positions['pos_res_butee'] = (self._r_ressort_bras * math.cos(self.angle_butee_rad), self._r_ressort_bras * math.sin(self.angle_butee_rad))
            positions['pos_res_charge'] = (self._r_ressort_bras * math.cos(self.angle_charge_rad), self._r_ressort_bras * math.sin(self.angle_charge_rad))
            positions['pos_masse_butee'] = (self._r_masse * math.cos(self.angle_butee_rad), self._r_masse * math.sin(self.angle_butee_rad))
            positions['pos_masse_charge'] = (self._r_masse * math.cos(self.angle_charge_rad), self._r_masse * math.sin(self.angle_charge_rad))
            
            return positions
          
        def _calculer_norme_vitesse_sortie() -> list[float]:
            pos = _calculer_positions()
            L_ressort_butee = ((pos['pos_res_butee'][0] - self._entraxe)**2+(pos['pos_res_butee'][1] - self._h_ressort_fixe)**2)**0.5
            L_ressort_charge = ((pos['pos_res_charge'][0] - self._entraxe)**2+(pos['pos_res_charge'][1] - self._h_ressort_fixe)**2)**0.5
            
            # Calcul de la norme de la vitesse par transformation complète de l'énergie potentielle en énergie cinétique
            # V0² = k * (Lc-Lb)²/m - g*yb_masse
            # On été négligées : les forces de frottement
            # Vérifications que l'énergie potentielle élastique est suffisante pour lancer la masse => Sinon, on met à 0 la vitesse de sortie
            if self._raideur_elastique/self._masse_projectile*(L_ressort_charge - L_ressort_butee)**2 > self._g*(pos['pos_masse_butee'][1] - pos['pos_masse_charge'][1]):
                return (self._raideur_elastique/self._masse_projectile*(L_ressort_charge - L_ressort_butee)**2 - self._g*(pos['pos_masse_butee'][1] - pos['pos_masse_charge'][1]))**0.5 
            else:
                return 0.0
        
        # t solution de y(t) == 0 est la suivante : (-b + (b²-4ac)**.5) / 2a où : c = y0 ; b = v0*sin(angle_butée -90) ; a = -1/2*g
        V0 = _calculer_norme_vitesse_sortie()
        b = V0 * math.sin(self.angle_butee_rad - math.pi/2)
        a = -0.5*self._g
        x0, y0 = _calculer_positions()['pos_masse_butee']
        
        def y(t : float) -> float:
            # y(t) = - 1/2*g*t² + v0*sin(angle_butée - 90)*t + y0
            return y0 + V0*math.sin(self.angle_butee_rad - math.pi/2)*t - 0.5*self._g*(t**2)
        def x(t : float) -> float:
            # x(t) = x0 + v0*cos(angle_butée - 90)*t
            return x0 + V0*math.cos(self.angle_butee_rad - math.pi/2)*t
        
        # print(f"a : {a} - b : {b}")
        # print(f'b**2 - 4*a*y0 : {b**2 - 4*a*y0}')
        # print(f"v0 {V0}")
        
        t = 0.
        T = [0.]
        Xt = [x0]
        Yt = [y0]
        while Yt[-1]>0:
            t+= pas
            T.append(t)
            Xt.append(x(t))
            Yt.append(y(t))
        
        # Résolution par dichotomie du zéro de la fonction y(t) :
        ta = T[-2]
        tb = T[-1]
        tc = 0.0
        while abs(ta-tb) > 0.0001:
            #print(ta, tb ,tc)
            tc = (ta + tb) / 2
            if y(ta)*y(tc) < 0:
                tb = tc
            else:
                ta = tc
        
        # Mise à jour des données par ajout du temps de vol et de la distance parcourue par le projectile
        T[-1] = tc
        Yt[-1] = y(tc)
        Xt[-1] = x(tc)
        
        if plot:
            import matplotlib.pyplot as plt
            plt.plot(Xt,Yt)
        
        return T, Xt, Yt

class Catapulte_Incertaine(Catapulte):
    def __init__(self, angle_butee : float, angle_charge : float, pos_ressort_fixe : float, pos_ressort_bras : float, pos_masse : float):
        # Récupération des caractéristique de la catapulte nominale
        super().__init__(angle_butee, angle_charge, pos_ressort_fixe, pos_ressort_bras, pos_masse)
        
        # Définition des écarts type des paramètres clefs.
        self._dev_angle_butee = 0.5
        self._dev_angle_charge =  0.5
        self._dev_h_ressort_fixe = 1E-4
        self._dev_r_ressort_bras = 1E-4
        self._dev_r_masse = 1E-3
        self._dev_raideur_elastique = 0.1
        self._dev_masse_projectile = 5E-4
        self._dev_g = 0.1
        
        # Définition des paramètres réels
        self._angle_butee_reel = None
        self._angle_charge_reel = None
        self._h_ressort_fixe_reel = None
        self._r_ressort_bras_reel = None
        self._r_masse_reel = None
        self._raideur_elastique_reel = None
        self._masse_projectile_reel = None
        self._g_reel = None
        
        # Quantification des paramètres réels
        self._generer_valeurs_reelles()
        
    def __repr__(self) -> str:
        nominal = f"Catapulte_nominale : @butee = {self._angle_butee}, @charge = {self._angle_charge}, pos_ressort_fixe = {self._h_ressort_fixe}, pos_ressort_bras = {self._r_ressort_bras}, pos_masse_bras = {self._r_masse}"
        reel = f"Catapulte_nominale : @butee = {self._angle_butee_reel}, @charge = {self._angle_charge_reel}, pos_ressort_fixe = {self._h_ressort_fixe_reel}, pos_ressort_bras = {self._r_ressort_bras_reel}, pos_masse_bras = {self._r_masse_reel}" # TODO : Mettre les valeurs réelles
        return nominal + "\n" + reel
       
    def definir_ecarts_type(self, definitions : dict):
        # Définir les écarts types des paramètres de configuraiton de la catapulte
        # Si l'information n'est pas disponible, on garde la valeur initiale. Aucun autre contrôle sur les grandeurs n'est réalisé
        if isinstance(definitions, dict):
            if "dev_a_b" in definitions : self._dev_angle_butee = float(definitions["dev_a_b"])
            if "dev_a_c" in definitions : self._dev_angle_charge = float(definitions["dev_a_c"])
            if "dev_h_r_f" in definitions : self._dev_h_ressort_fixe = float(definitions["dev_h_r_f"])
            if "dev_r_r_b" in definitions : self._dev_r_ressort_bras = float(definitions["dev_r_r_b"])
            if "dev_r_m" in definitions : self._dev_r_masse = float(definitions["dev_r_m"])
            if "dev_r_e" in definitions : self._dev_raideur_elastique = float(definitions["dev_r_e"])
            if "dev_m" in definitions : self._dev_masse_projectile = float(definitions["dev_m"])
            if "dev_g" in definitions : self._dev_g = float(definitions["dev_g"])
       
    def _generer_valeurs_reelles(self) -> dict:
        # Génération aléatoire des valeurs réelles, dans le domaine de définition des paramètres
        self._angle_butee_reel = rng.gauss(self._angle_butee, self._dev_angle_butee)
        self._angle_charge_reel = rng.gauss(self._angle_charge, self._dev_angle_charge)
        if self._angle_charge_reel > 180.0 : self._angle_charge_reel = 180.0
        if self._angle_charge_reel < self._angle_charge_reel: self._angle_charge_reel = self._angle_charge_reel
        self._h_ressort_fixe_reel = rng.gauss(self._h_ressort_fixe, self._dev_h_ressort_fixe)
        self._r_ressort_bras_reel = rng.gauss(self._r_ressort_bras, self._dev_r_ressort_bras)
        self._r_masse_reel = rng.gauss(self._r_masse, self._dev_r_masse)
        if self._r_ressort_bras_reel > self._r_masse_reel : self._r_ressort_bras_reel = self._r_masse_reel
        self._raideur_elastique_reel = rng.gauss(self._raideur_elastique, self._dev_raideur_elastique)
        self._masse_projectile_reel = rng.gauss(self._masse_projectile, self._dev_masse_projectile)
        self._g_reel = rng.gauss(self._g, self._dev_g)
        
        # A des fins de débug ou de contrôle on retourne les valeurs calculées
        return {"@butee_reel" :  self._angle_butee_reel, 
                "@charge_reel" : self._angle_charge_reel,
                "position_ressort_fixe" : self._h_ressort_fixe_reel,
                "position_ressort_bras" : self._r_ressort_bras_reel,
                "position_masse_arbre" : self._r_masse_reel,
                "raideur_ressort" : self._raideur_elastique_reel,
                "masse" : self._masse_projectile_reel,
                "g" : self._g_reel}
    # Fonctions de convertion des angles de la catapulte - Surcharge pour le cas incertain
    def _retourner_angle_butee_rad(self):
        return self._angle_butee_reel * math.pi / 180.0
    angle_butee_rad = property(_retourner_angle_butee_rad)
    def _retourner_angle_charge_rad(self):
        return self._angle_charge_reel * math.pi / 180.0
    angle_charge_rad = property(_retourner_angle_charge_rad)
    
    def calculer_trajectoire(self, pas : float = 0.01, plot : bool = False): #-> tuple[list[float],list[float],list[float],float]
        
        def _calculer_positions() -> dict:
            positions = dict()
            positions['pos_res_butee'] = (self._r_ressort_bras_reel * math.cos(self.angle_butee_rad), self._r_ressort_bras_reel * math.sin(self.angle_butee_rad))
            positions['pos_res_charge'] = (self._r_ressort_bras_reel * math.cos(self.angle_charge_rad), self._r_ressort_bras_reel * math.sin(self.angle_charge_rad))
            positions['pos_masse_butee'] = (self._r_masse_reel * math.cos(self.angle_butee_rad), self._r_masse_reel * math.sin(self.angle_butee_rad))
            positions['pos_masse_charge'] = (self._r_masse_reel * math.cos(self.angle_charge_rad), self._r_masse_reel * math.sin(self.angle_charge_rad))
            
            return positions
          
        def _calculer_norme_vitesse_sortie() -> list:
            pos = _calculer_positions()
            L_ressort_butee = ((pos['pos_res_butee'][0] - self._entraxe)**2+(pos['pos_res_butee'][1] - self._h_ressort_fixe_reel)**2)**0.5
            L_ressort_charge = ((pos['pos_res_charge'][0] - self._entraxe)**2+(pos['pos_res_charge'][1] - self._h_ressort_fixe_reel)**2)**0.5
            
            # Calcul de la norme de la vitesse par transformation complète de l'énergie potentielle en énergie cinétique
            # V0² = k * (Lc-Lb)²/m - g*yb_masse
            # On été négligées : les forces de frottement
            # Vérifications que l'énergie potentielle élastique est suffisante pour lancer la masse => Sinon, on met à 0 la vitesse de sortie
            if self._raideur_elastique_reel/self._masse_projectile_reel*(L_ressort_charge - L_ressort_butee)**2 > self._g_reel*(pos['pos_masse_butee'][1] - pos['pos_masse_charge'][1]):
                return (self._raideur_elastique_reel/self._masse_projectile_reel*(L_ressort_charge - L_ressort_butee)**2 - self._g_reel*(pos['pos_masse_butee'][1] - pos['pos_masse_charge'][1]))**0.5 
            else:
                return 0.0
        
        # t solution de y(t) == 0 est la suivante : (-b + (b²-4ac)**.5) / 2a où : c = y0 ; b = v0*sin(angle_butée -90) ; a = -1/2*g
        V0 = _calculer_norme_vitesse_sortie()
        b = V0 * math.sin(self.angle_butee_rad - math.pi/2)
        a = -0.5*self._g_reel
        x0, y0 = _calculer_positions()['pos_masse_butee']
        
        def y(t : float) -> float:
            # y(t) = - 1/2*g*t² + v0*sin(angle_butée - 90)*t + y0
            return y0 + V0*math.sin(self.angle_butee_rad - math.pi/2)*t - 0.5*self._g_reel*(t**2)
        def x(t : float) -> float:
            # x(t) = x0 + v0*cos(angle_butée - 90)*t
            return x0 + V0*math.cos(self.angle_butee_rad - math.pi/2)*t
        
        #print(f"a : {a} - b : {b}")
        #print(f'b**2 - 4*a*y0 : {b**2 - 4*a*y0}')
        #print(f"v0 {V0}")
        
        t = 0.
        T = [0.]
        Xt = [x0]
        Yt = [y0]
        while Yt[-1]>0:
            t+= pas
            T.append(t)
            Xt.append(x(t))
            Yt.append(y(t))
        
        # Résolution par dichotomie du zéro de la fonction y(t) :
        ta = T[-2]
        tb = T[-1]
        tc = 0.0
        while abs(ta-tb) > 0.0001:
            #print(ta, tb ,tc)
            tc = (ta + tb) / 2
            if y(ta)*y(tc) < 0:
                tb = tc
            else:
                ta = tc
        
        # Mise à jour des données par ajout du temps de vol et de la distance parcourue par le projectile
        T[-1] = tc
        Yt[-1] = y(tc)
        Xt[-1] = x(tc)
        
        if plot:
            import matplotlib.pyplot as plt
            plt.plot(Xt,Yt)
        
        return T, Xt, Yt
    
    def calculer_trajectoires(self, pas : float, plot : bool, nb_repetition : int) -> list:
        resultats = []
        for _iter in range(nb_repetition):
            self._generer_valeurs_reelles()
            resultats.append(self.calculer_trajectoire(pas, plot))
        return [round(_res[1][-1],4) for _res in resultats]

# data = []
# for butee in range(90,180):
#     for lache in range(180,butee,-1):
#         toto = Catapulte(butee,lache,0.2,0.2,0.3)
#         data.append((butee, lache, toto._calculer_norme_vitesse_sortie()))

# import matplotlib.pyplot as plt        
# ax = plt.axes(projection='3d')

# # Data for a three-dimensional line
# zline = [element[2] for element in data]
# xline = [element[0] for element in data]
# yline = [element[1] for element in data]
# ax.plot3D(xline, yline, zline, 'gray')

# for butee in range(90,170,5):
#     toto = Catapulte(butee,180,0.2,0.2,0.3)
#     toto.calculer_trajectoire(0.01, True)

# Interface = UI()
# print(Catapulte_Incertaine(90,180,0.1,0.1,0.301).calculer_trajectoire()[1][-1])
    

# print("avg :", np.mean(I))
# print("std :", np.std(I))
# print("6_sigma :", 300*np.std(I), "cm")
