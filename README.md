# 🧠 Krigeage & Optimisation Génomique – Mini-projet RESA ENSAM

## 📌 Description

Ce projet vise à modéliser et optimiser le comportement d'une catapulte soumise à incertitudes, en combinant méthodes de krigeage (géostatistique) et algorithmes génétiques (optimisation inverse). Il a été réalisé dans le cadre de l’UE RESA – Résolution de problèmes en Simulation et Analyse – à l’ENSAM Metz.

## 🛠️ Technologies utilisées

- **Langage principal :** Python 3.11+
- **Librairies clés :**
  - `numpy`, `pandas`, `matplotlib`
  - `scikit-learn`, `scipy`
  - `openpyxl` (pour lecture Excel)
- **IDE recommandé :** VSCode ou PyCharm

## 📂 Structure du dépôt




## 🚀 Installation et exécution

### 1. Clonage du dépôt

```bash
git clone https://github.com/<votre-utilisateur>/Mini-projet-RESA.git
cd Mini-projet-RESA
2. Création d’un environnement virtuel (optionnel mais recommandé)
bash
Copy
Edit
python -m venv venv
source venv/bin/activate    # (Windows) venv\Scripts\activate
3. Installation des dépendances
bash
Copy
Edit
pip install -r requirements.txt
4. Exécution du projet
Lancer le pipeline principal :

bash
Copy
Edit
python pjt5_3.py
Ou exécuter l’étude de variogramme :

bash
Copy
Edit
python etude_variogrammes.py


📈 Résultats principaux
Prédiction de distance avec erreur absolue moyenne < 7.4 cm

Coefficient de détermination du modèle de krigeage : R² = 0.98

Modèle optimal de variogramme sélectionné : Gaussien avec C=3.019, a=26.969, nugget=0.222

Génération automatique de la configuration optimale en moins de 50 générations

🖥️ Interface future (perspective)
Une extension est en cours de développement pour proposer une interface Web ou graphique :

Permet à l’utilisateur de charger un fichier Excel avec ses propres données

Calcule automatiquement les distances, ajuste le variogramme et fournit la configuration optimale

Basé sur Flask ou Streamlit

✏️ Auteurs
👨‍🔬 Salah-Eddine MAIMOUNI – ENSAM Casablanca × Metz – Gadz’Arts 2026

👨‍🔬 Mohamed ES-SALHY – ENSAM Casablanca × Metz
