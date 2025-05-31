# 🎯 Mini-Projet 4 - Modélisation et optimisation d'une catapulte

Ce projet s'inscrit dans le cadre de l'UE RESA à l'ENSAM Metz. Il consiste à modéliser le comportement d'une catapulte à partir de données de simulation, puis à inverser le modèle afin de déterminer les paramètres optimaux pour atteindre une distance cible à l'aide de techniques de krigeage et d'algorithmes génétiques.

## 📁 Structure des fichiers

- `pjt5_1.py` : Importation, normalisation, calculs de distance et de variogramme
- `pjt5_2.py` : Méthodes de krigeage (inverse, estimation, variance)
- `pjt5_3.py` : Algorithme génétique (initialisation, sélection, mutation, fitness, etc.)
- `Sceance2.py` : Construction du variogramme expérimental
- `séance3.py` : Krigeage sur jeu de test + visualisation
- `séance4.py` : Optimisation inverse via algorithme génétique
- `donnees_sim.xlsx` : Données d'entraînement et de test (fichier attendu dans le dossier)

## 🧪 Environnement Python requis

- Python >= 3.8
- Bibliothèques nécessaires :

```bash
pip install numpy pandas matplotlib scikit-learn
