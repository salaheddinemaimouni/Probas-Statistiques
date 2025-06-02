from pjt5_3 import *
import os

# Chargement des données d'entraînement
chemin_fichier = os.path.join(os.path.dirname(__file__), "donnees_sim.xlsx")

x_train, z_train = importer_donnees(chemin_fichier, "Train")
x_train_n = normaliser_donnees(x_train)

# Initialisation de la population
pop = first_pop(100)

matrice_distance=[]

for i in range(50):  # 50 générations
    # Évaluation de la population actuelle
    pop_fit = fitness(Z_cible=2, pop=pop, X_train=x_train_n, z_train=z_train)

    # Sélection, croisement, mutation
    pop_sel = selection(pop_fit)
    pop_cross = croisement(pop_sel)
    pop = mutation(pop_cross)

    # Meilleur individu de la génération
    best = tri(pop_fit)
    best_fitness = best[-1]
    best_params = decodage(best[:-1].reshape(1, -1), normalisee=False)

    # Affichage
    print(f"Génération {i+1:>3} | Best fitness: {best_fitness:.4f} | Params: {best_params.flatten()}")
    matrice_distance.append("Génération" + str(i+1) + "Best fitness:"+ str(best_fitness) + "Params:" + str(best_params.flatten()))
print(np.array(matrice_distance))


