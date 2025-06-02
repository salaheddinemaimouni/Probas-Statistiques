import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import r2_score
from pjt5_1 import *

#%% - Fonction : variogramme théorique (polynôme ajusté)
def variogramme_theorique(h):
    h = np.array(h)
    #gamma = 0.0025 * h**2 + 0.1045 * h - 0.0754
    #variogramme Gaussien
    C, a, nugget = 3.019, 26.969, 0.222
    gamma = C*(1-np.exp(-3*(h/a)**2))+nugget
    gamma = np.maximum(gamma, 0)  # On s'assure que gamma ≥ 0 (physiquement plausible)
    return gamma

#%% - Inversion de la matrice de krigeage étendue
def inverse(matrice_distance):
    """
    Construit puis inverse la matrice de krigeage (avec contrainte λ_i = 1).
    """
    n = matrice_distance.shape[0]
    Gamma = variogramme_theorique(matrice_distance)  # Application du variogramme théorique
    Gamma_ext = np.zeros((n + 1, n + 1))              # Matrice étendue (n+1 x n+1)
    Gamma_ext[:n, :n] = Gamma                         # Bloc principal
    Gamma_ext[n, :n] = 1                              # Dernière ligne = 1
    Gamma_ext[:n, n] = 1                              # Dernière colonne = 1
    Gamma_ext[n, n] = 0                               # Coin bas droite = 0
    Gamma_inv = np.linalg.inv(Gamma_ext)              # Inversion de la matrice
    return Gamma_inv

#%% - Construction du vecteur gamma (γ) pour un point à prédire
def vecteur_variogramme(obs, to_pred):
    obs = np.array(obs)
    to_pred = np.array(to_pred)
    distances = np.linalg.norm(obs - to_pred, axis=1)  # Distance euclidienne point-par-point
    gamma_vect = variogramme_theorique(distances)      # Application du variogramme
    vect_ext = np.append(gamma_vect, 1)                # Ajout de la contrainte (1)
    return vect_ext.reshape(-1, 1)                      # Retour sous forme colonne

#%% - Résolution : calcul des lambdas (poids) et multiplicateur de Lagrange
def lambdas(matrice_inv, vect_var):
    res = matrice_inv @ vect_var            # Multiplication : inverse × vecteur
    lambdas = res[:-1].flatten()            # Poids associés aux observations
    mu = res[-1, 0]                         # Multiplicateur de Lagrange
    print(f"[lambdas] Multiplicateur de Lagrange mu : {mu}")
    return lambdas, mu

#%% - Estimation du point cible
def estimation(lambdas, Z):
    Z = np.array(Z)
    est = np.sum(lambdas * Z)
    print(f"[estimation] Estimation calculée : {est}")
    return est

#%% - Calcul de la variance associée à l’estimation
def variance(lambdas, vect_var, mu):
    """
    Calcule l'incertitude (variance) de l'estimation par krigeage.
    """
    gamma_vect = vect_var[:-1].flatten()
    var = np.sum(lambdas * gamma_vect) + mu
    print(f"[variance] Variance calculée : {var}")
    return var

#%% - Coefficient de détermination R²
def coefficient_determination(z_test, z_estime):
    """
    Évalue la qualité du modèle en comparant les vraies valeurs aux estimations.
    """
    r2 = r2_score(z_test, z_estime)
    print(f"[coefficient_determination] R² calculé : {r2}")
    return r2

