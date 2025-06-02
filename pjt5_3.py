# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 14:41:15 2024

@author: Wahb
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from random import randint
import catapulte_incertaine as cat
from pjt5_2 import *
from pjt5_1 import normaliser_donnees
from pjt5_1 import importer_donnees
#%% fonctions (2) : algorithme générique
from pjt5_1 import normaliser_donnees
from pjt5_1 import importer_donnees

#%% - fonctions (1) : algorithme générique
def first_pop(pop_size):


    '''
    Génère une première population encodée.

    Parameters:
    - pop_size (int): Taille de la population.

    Returns:
    - array: Population encodée.
    '''
    pop_size = 2*int((pop_size+1)*0.5)
    a1_1 = np.random.randint(4, size=(pop_size, 1)) 
    a1_2 = np.random.randint(10, size=(pop_size, 1)) 
    
    a2_1 = np.random.randint(4, size=(pop_size, 1)) 
    a2_2 = np.random.randint(10, size=(pop_size, 1))
    
    l1 = np.random.randint(10, size=(pop_size, 2)) 
    l2 = np.random.randint(10, size=(pop_size, 2))
    l3 = np.random.randint(10, size=(pop_size, 2))
    
    pop = np.hstack((a1_1, a1_2, a2_1, a2_2, l1, l2, l3))
    
    return pop

def decodage(pop, normalisee = False):
    '''
    Décodage d'une population encodée.

    Parameters:
    - pop (array): Population encodée.
    - normalisee (bool): Indique si la normalisation doit être effectuée.

    Returns:
    - array: Population décodée.
    '''
    pop_d = np.zeros((len(pop), 5))
    pop_d[:,0] = pop[:,0]*10 + pop[:,1] + 90
    pop_d[:,1] = pop[:,2]*10 + pop[:,3] + 140
    pop_d[:,2] = pop[:,4]*0.01 + pop[:,5]*0.001 + 0.1
    pop_d[:,3] = pop[:,6]*0.01 + pop[:,7]*0.001 + 0.1
    pop_d[:,4] = pop[:,8]*0.01 + pop[:,9]*0.001 + 0.2
    
    if normalisee == False :
        return pop_d
    elif normalisee == True:
        return normaliser_donnees(pop_d)

def fitness(Z_cible, pop, X_train, z_train):
    # Décodage de la population (passage d'entiers encodés → réels normalisés)
    pop_n = decodage(pop, normalisee=True)

    # Construction de la matrice des distances entre points d'entraînement
    dist_matrix = creer_matrice_distance(X_train)

    # Inversion de la matrice de krigeage (matrice Gamma étendue)
    Gamma_inv = inverse(dist_matrix)

    # Initialisation de la matrice des résultats [gènes + fitness]
    pop_fit = np.zeros((pop.shape[0], pop.shape[1] + 1))

    # Copie de la population encodée dans les premières colonnes
    pop_fit[:,:-1] = pop

    # Boucle d’évaluation sur chaque individu
    for i, individu in enumerate(pop_n):
        # Construction du vecteur de variogramme entre individu et données d'entraînement
        vect = vecteur_variogramme(X_train, individu)

        # Résolution du système de krigeage → poids λ et multiplicateur μ
        lmb, mu = lambdas(Gamma_inv, vect)

        # Estimation de la sortie (distance atteinte) pour cet individu
        z_estime = estimation(lmb, z_train)

        # Calcul de l’erreur absolue par rapport à la cible (fitness)
        pop_fit[i, -1] = abs(z_estime - Z_cible)

    # Retourne la population avec erreur absolue ajoutée à la dernière colonne
    return pop_fit




def selection(pop_fit):
    taille_pop = len(pop_fit)               # Nombre d’individus
    n_col = pop_fit.shape[1]                # Nombre total de colonnes (gènes + fitness)

    pop_selec = np.zeros((taille_pop, n_col))  # Nouvelle population sélectionnée
    r = np.zeros((3, n_col))                  # Matrice temporaire pour stocker 3 candidats

    for i in range(taille_pop):               # Pour chaque individu à sélectionner
        for j in range(3):                    # On tire 3 individus au hasard
            rdm = randint(0, taille_pop - 1)
            r[j, :] = pop_fit[rdm, :]         # Stockage du candidat

        indice_meilleur = np.argmin(r[:, -1]) # On prend celui avec la meilleure fitness (min erreur)
        pop_selec[i, :] = r[indice_meilleur, :]  # Ajout à la population sélectionnée

    return pop_selec                          # Retourne la nouvelle population




def croisement(pop_selec):
    taille_pop = pop_selec.shape[0]             # Nombre d’individus
    pop_cross = np.zeros_like(pop_selec)        # Initialisation de la nouvelle population

    for i in range(0, taille_pop, 2):           # On traite 2 individus à la fois
        parent1 = pop_selec[i, :-1]             # Gènes du parent 1 (hors fitness)
        parent2 = pop_selec[i+1, :-1]           # Gènes du parent 2

        enfant1 = np.copy(parent1)              # Copie parent 1
        enfant2 = np.copy(parent2)              # Copie parent 2

        for j in range(10):                     # 10 gènes par individu
            if np.random.rand() < 0.5:          # 50% de chance d’échanger le gène
                enfant1[j], enfant2[j] = parent2[j], parent1[j]

        pop_cross[i, :-1] = enfant1             # Remplir la population avec les enfants
        pop_cross[i+1, :-1] = enfant2

    return pop_cross                            # Population après croisement



def mutation(pop_cross):
    # Taille de la population
    taille_pop = len(pop_cross)
    
    # Crée une copie de la population après croisement
    pop_mut = np.copy(pop_cross)  
    
    # Parcours de chaque individu de la population
    for i in range(taille_pop):
        # Sélectionne aléatoirement un indice à muter parmi les 10 gènes
        rdm = randint(0, 9)
        
        # Si l'individu est dans les positions 0 ou 2, la mutation est restreinte à 4 valeurs
        if i in {0, 2}:
            pop_mut[i, rdm] = randint(0, 3)
        # Sinon, la mutation peut prendre n'importe quelle valeur entre 0 et 9
        else:
            pop_mut[i, rdm] = randint(0, 9)
    
    return pop_mut


def tri(pop_fit):
    indice_min = np.argmin(pop_fit[:, -1])     # Index du plus petit écart à la cible
    meilleur_individu = pop_fit[indice_min, :] # Extraction de la ligne complète (paramètres + fitness)
    return meilleur_individu

#%% - Simulation catapulte
def catapulte_sim(a1,a2,l1,l2,l3):
    '''simuler une configuration de catapulte'''
    d = cat.Catapulte_Incertaine(a1,a2,l1,l2,l3).calculer_trajectoire()[1][-1]
    return round(d,2)

#%% - Main : part 3





"""
mes remarques 

Z_cible = 2 
pop_iniy = first_pop(100)
popedecode =decodage(pop_init, normalisee = False )

 3. Implémenteles fonctions de : sélection, croisement, et mutation.
"""
