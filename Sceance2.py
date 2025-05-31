from pjt5_1 import *


# Importer
x, z = importer_donnees(r"C:\Users\salah\Desktop\myfiles\PGE\GIE2\RESA\Mini projet 4 RESA/donnees_sim.xlsx", "Train")

# Normaliser
x_norm = normaliser_donnees(x)


# Calcul de distance
dist = creer_matrice_distance(x_norm)


# Calcul variogramme
variogramme, h_vals = calculer_variogramme_experimental(dist, z, h_pas=1)

# Traçage 
tracer_variogramme(variogramme, h_vals)


# Combiner les valeurs h et γ(h) dans un tableau 2D
resultats_variogramme = np.column_stack((h_vals, variogramme))

# Exporter vers Excel
exporter_vers_excel(resultats_variogramme, "variogramme_experimental")
