# 🧠 Krigeage & Optimisation Génomique – Mini-projet RESA ENSAM

## 📌 Description

Ce projet vise à modéliser et optimiser le comportement d'une catapulte soumise à incertitudes, en combinant méthodes de krigeage (géostatistique) et algorithmes génétiques (optimisation inverse). Il a été réalisé dans le cadre de l’UE RESA – Résolution de problèmes en Simulation et Analyse – à l’ENSAM Metz.

## 💠 Technologies utilisées

* **Langage principal :** Python 3.11+
* **Librairies clés :**

  * `numpy`, `pandas`, `matplotlib`
  * `scikit-learn`, `scipy`
  * `openpyxl` (pour lecture Excel)
* **IDE recommandé :** VSCode ou PyCharm

## 📂 Structure du dépôt

```
Mini-projet-RESA/
├── donnees_sim.xlsx              # Données d'apprentissage
├── variogramme_experimental.xlsx # Export du variogramme
├── pjt5_1.py                     # Fonctions de normalisation, distance, variogramme
├── pjt5_2.py                     # Fonctions de krigeage
├── pjt5_3.py                     # Algorithme génétique complet
├── séance2.py                    # Sélection, mutation, croisement
├── séance3.py                    # Phase de krigeage inverse
├── séance4.py                    # Simulation finale
├── etude_variogrammes.py         # Étude comparative gaussien / sphérique / exponentiel
├── README.md                     # Ce fichier
```

## 🚀 Installation et exécution

### 1. Clonage du dépôt

```bash
git clone https://github.com/<votre-utilisateur>/Mini-projet-RESA.git
cd Mini-projet-RESA
```

### 2. Création d’un environnement virtuel (optionnel mais recommandé)

```bash
python -m venv venv
source venv/bin/activate    # (Windows) venv\Scripts\activate
```

### 3. Installation des dépendances

```bash
pip install -r requirements.txt
```

### 4. Exécution du projet

Lancer le pipeline principal :

```bash
python pjt5_3.py
```

Ou exécuter l’étude de variogramme :

```bash
python etude_variogrammes.py
```

## 📈 Résultats principaux

* Prédiction de distance avec erreur absolue moyenne < **7.4 cm**
* Coefficient de détermination du modèle de krigeage : **R² = 0.98**
* Modèle optimal de variogramme sélectionné : **Gaussien** avec C=3.019, a=26.969, nugget=0.222
* Génération automatique de la configuration optimale en moins de 50 générations

## 💻 Interface future (perspective)

Une extension est en cours de développement pour proposer une interface Web ou graphique :

* Permet à l’utilisateur de charger un fichier Excel avec ses propres données
* Calcule automatiquement les distances, ajuste le variogramme et fournit la configuration optimale
* Basé sur Flask ou Streamlit

## ✏️ Auteurs

* 👨‍🔬 Salah-Eddine MAIMOUNI – ENSAM Casablanca × Metz – Gadz’Arts 2026
* 👨‍🔬 Mohamed ES-SALHY – ENSAM Casablanca × Metz

## 📄 Licence

Ce projet est diffusé sous licence MIT. Vous pouvez l'utiliser, le modifier ou le redistribuer librement sous réserve de citer les auteurs.

