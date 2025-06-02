import matplotlib.pyplot as plt
from pjt5_1 import importer_donnees, normaliser_donnees, creer_matrice_distance
from pjt5_2 import inverse, vecteur_variogramme, lambdas, estimation, variance, coefficient_determination
import os

# 1. Importer données d'entraînement
    # Obtenir le chemin absolu du fichier Excel situé dans le même dossier que le script
chemin_fichier = os.path.join(os.path.dirname(__file__), "donnees_sim.xlsx")
    # Appel de la fonction avec le chemin dynamique
x, z = importer_donnees(chemin_fichier, "Train")

# 2. Normaliser coordonnées
x_norm = normaliser_donnees(x)

# 3. Calcul matrice distances entre points connus
dist = creer_matrice_distance(x_norm)

# 4. Calculer matrice inverse étendue de krigeage
Gamma_inv = inverse(dist)

# 5. Import données test et normalisation
x_test, z_test = importer_donnees(chemin_fichier, "Test")
x_test_norm = normaliser_donnees(x_test)

# 6. Prédictions et calcul des variances
estimations = []
variances = []
for i, s0 in enumerate(x_test_norm):
    v_var = vecteur_variogramme(x_norm, s0)
    lmb, mu = lambdas(Gamma_inv, v_var)
    est = estimation(lmb, z)
    var = variance(lmb, v_var, mu)
    estimations.append(est)
    variances.append(var)
    print("----------------------------")

# 7. Évaluation finale du modèle
r2 = coefficient_determination(z_test, estimations)

# tracer comparaison valeurs réelles/estimées
import matplotlib.pyplot as plt
plt.plot(z_test, label='Valeurs réelles')
plt.plot(estimations, label='Estimations krigeage')
plt.legend()
plt.title('Comparaison valeurs réelles et estimées')
plt.show()
