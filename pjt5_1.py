# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 09:34:51 2024

@author: Wahb
"""

#%% - importation de libs
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

#%% - Fonctions de prétraitement de données

# Fonction pour importer les données
def importer_donnees(chemin_fichier, nom_feuil):
    """
    Charger les données depuis un fichier Excel.

    Parameters:
        chemin_fichier (str): Chemin vers le fichier Excel.
        nom_feuil (str): Nom de la feuil Excel.

    Returns:
        tuple: Les pramètres d'entrée (X) et le pramètre sortie (z = dernière colonne).
    """
    df = pd.read_excel(str(chemin_fichier), sheet_name = str(nom_feuil))
    X = df.iloc[:,:-1]; z = df.iloc[:,-1]
   
    return X,z

def normaliser_formule(valeur, Min, Max, inverse = False):
    """
    Normalise une valeur donnée en utilisant la formule de mise à l'échelle Min-Max.

    Parameters:
    - valeur (float): La valeur à normaliser.
    - Min (float): La valeur minimale possible.
    - Max (float): La valeur maximale possible.
    - inverse (bool): Indique si la normalisation inverse doit être effectuée.

    Returns:
    - float: La valeur normalisée.
    """
    if inverse == False:
        return 10*(valeur - Min)/(Max - Min)
    else :
        return 0.1*valeur*(Max - Min) + Min


# Fonction pour normaliser les données
def normaliser_donnees(donnees, inverse=False):
    """
    Utiliser la mise à l'échelle Min-Max pour la normalisation des données entre 0 et 10.

    Parameters:
        donnees (array): Données à normaliser.
        inverse (bool): Indique si la normalisation inverse doit être effectuée.

    Returns:
        array: Données normalisées.
    """
    
    mins = [90, 140, 0.1, 0.1, 0.201]
    maxs = [130, 180, 0.2, 0.2, 0.301]
    
    donnees_ = np.copy(np.asarray(donnees))    
    for i in range(5):
        donnees_[:,i] = normaliser_formule(donnees_[:,i], mins[i], maxs[i], inverse = inverse)
    return donnees_

# Fonction pour exporter les données vers Excel
def exporter_vers_excel(donnees, nom_fichier):
    """
    Exporter les données vers un fichier Excel.

    Parameters:
        donnees (array): Données à exporter.
        nom_fichier (str): Nom du fichier Excel (sans extension).
    """
    assert type(nom_fichier) == str, 'nom_fichier doit être une chaîne de caractères'
    df = pd.DataFrame(data = donnees)
    writer = pd.ExcelWriter(nom_fichier+'.xlsx', engine='xlsxwriter') 
    df.to_excel(writer, index=False, sheet_name = nom_fichier)
    writer.close()

#%% - Fonctions à compléter

# Fonction qui calcule la distance euclidienne entre deux vecteurs arr1 et arr2
def calculer_distance_euclidienne(arr1, arr2):
    return np.sqrt(np.sum((arr1 - arr2) ** 2))  # racine(somme(x_i - y_i)²)

# Crée une matrice de distance symétrique à partir d’un tableau X (chaque ligne = un point)
def creer_matrice_distance(X):
    n = X.shape[0]  # nombre d’échantillons
    dist_matrix = np.zeros((n, n))  # matrice carrée vide
    for i in range(n):
        for j in range(i + 1, n):  # on évite les doublons et la diagonale
            d = calculer_distance_euclidienne(X[i], X[j])  # distance entre point i et j
            dist_matrix[i, j] = dist_matrix[j, i] = d  # matrice symétrique
    return dist_matrix

# Calcule la demi-variance moyenne γ(h) pour un intervalle [h_min, h_max[
def calculer_variogramme_intervalle(dist, Z, h_min, h_max):
    n = len(Z)
    valeurs = []  # liste pour stocker les demi-variances valides
    for i in range(n):
        for j in range(i + 1, n):  # tous les couples (i,j)
            d = dist[i, j]  # distance entre les points i et j
            if h_min <= d < h_max:  # si elle tombe dans l’intervalle
                valeurs.append(0.5 * (Z[i] - Z[j]) ** 2)
    if valeurs:
        return np.mean(valeurs)  # moyenne des demi-variances
    else:
        return np.nan  # pas de données valides dans l’intervalle


# Construit le variogramme expérimental en appelant la fonction précédente sur chaque intervalle de h
def calculer_variogramme_experimental(dist, Z, h_pas):
    h_max_total = np.nanmax(dist)  # distance max dans le jeu de données
    h_values = np.arange(0, h_max_total, h_pas)  # découpage régulier
    variogramme = []  # valeurs de γ(h)
    for h in h_values:
        gamma_h = calculer_variogramme_intervalle(dist, Z, h, h + h_pas)
        variogramme.append(gamma_h)
    return np.array(variogramme), h_values  # γ(h), h


# Affiche le variogramme expérimental (γ en fonction de h)
def tracer_variogramme(var, h_pas):
    plt.figure(figsize=(8, 5))
    plt.plot(h_pas, var, marker='o', linestyle='-')  # courbe pointillée
    plt.title("Variogramme Expérimental")
    plt.xlabel("Distance h")
    plt.ylabel("γ(h)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()  # affichage graphique



















