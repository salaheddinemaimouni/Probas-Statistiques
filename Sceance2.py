from pjt5_1 import *
import os

# Importer
    # Obtenir le chemin absolu du fichier Excel situé dans le même dossier que le script
chemin_fichier = os.path.join(os.path.dirname(__file__), "donnees_sim.xlsx")
    # Appel de la fonction avec le chemin dynamique
x, z = importer_donnees(chemin_fichier, "Train")

# Normaliser
x_norm = normaliser_donnees(x)


# Calcul de distance
dist = creer_matrice_distance(x_norm)

# Afficher la matrice de distance
plt.figure(figsize=(8, 6))
plt.imshow(dist, cmap='viridis', interpolation='nearest')
plt.title("Matrice de distance normalisée")
plt.colorbar(label='Distance')  # Ajoute une barre de couleur à droite indiquant l'échelle des distances
plt.xlabel("Point i")   # Étiquette de l'axe des abscisses
plt.ylabel("Point j")   # Étiquette de l'axe des ordonnées
plt.tight_layout() # Ajuste automatiquement les marges pour une meilleure mise en page
plt.show()


# Calcul variogramme
variogramme, h_vals = calculer_variogramme_experimental(dist, z, h_pas=1)

# Traçage 
tracer_variogramme(variogramme, h_vals)


# Combiner les valeurs h et γ(h) dans un tableau 2D
resultats_variogramme = np.column_stack((h_vals, variogramme))

# Exporter vers Excel
exporter_vers_excel(resultats_variogramme, "variogramme_experimental")
