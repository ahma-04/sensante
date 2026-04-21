import pandas as pd
import numpy as np

df = pd.read_csv("data/patients_dakar.csv")

print(f"Dataset : {df.shape[0]} patients, {df.shape[1]} colonnes")
print(f"\nColonnes : {list(df.columns)}")
print(f"\nDiagnostics :\n{df['diagnostic'].value_counts()}")



from sklearn.preprocessing import LabelEncoder

le_sexe = LabelEncoder()
le_region = LabelEncoder()

df['sexe_encoded'] = le_sexe.fit_transform(df['sexe'])
df['region_encoded'] = le_region.fit_transform(df['region'])

feature_cols = ['age', 'sexe_encoded', 'temperature', 'tension_sys',
                'toux', 'fatigue', 'maux_tete', 'frissons', 'nausee', 'region_encoded']

X = df[feature_cols]
y = df['diagnostic']

print(f"Features : {X.shape}")
print(f"Cible : {y.shape}")

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print(f"Entrainement : {X_train.shape[0]} patients")
print(f"Test : {X_test.shape[0]} patients")




from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

print("Modele entraine !")
print(f"Nombre d'arbres : {model.n_estimators}")
print(f"Nombre de features : {model.n_features_in_}")
print(f"Classes : {list(model.classes_)}")



from sklearn.ensemble import RandomForestClassifier

# Creer le modele
model = RandomForestClassifier(
    n_estimators=100,   # 100 arbres de decision
    random_state=42     # Reproductibilite
)

# Entrainer
model.fit(X_train, y_train)

print("Modele entraine !")
print(f"Nombre d'arbres : {model.n_estimators}")
print(f"Nombre de features : {model.n_features_in_}")
print(f"Classes : {list(model.classes_)}")

# Predire sur les donnees de test
y_pred = model.predict(X_test)

# Comparer les 10 premieres predictions
comparison = pd.DataFrame({
    'Vrai diagnostic': y_test.values[:10],
    'Prediction': y_pred[:10]
})
print(comparison)

from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy : {accuracy:.2%}")

from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# Matrice de confusion
cm = confusion_matrix(y_test, y_pred, labels=model.classes_)
print("Matrice de confusion :")
print(cm)

# Rapport de classification
print("\nRapport de classification :")
print(classification_report(y_test, y_pred))

import os
os.makedirs("figures", exist_ok=True)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=model.classes_,
            yticklabels=model.classes_)
plt.xlabel('Prediction du modele')
plt.ylabel('Vrai diagnostic')
plt.title('Matrice de confusion - SenSante')
plt.tight_layout()
plt.savefig('figures/confusion_matrix.png', dpi=150)
plt.show()
print("Figure sauvegardee dans figures/confusion_matrix.png")

# ============ ETAPE 6.1 : SERIALISER LE MODELE ============
import joblib
import os

# Creer le dossier models/
os.makedirs("models", exist_ok=True)

# Serialiser le modele
joblib.dump(model, "models/model.pkl")

# Verifier la taille
size = os.path.getsize("models/model.pkl")
print(f"Modele sauvegarde : models/model.pkl")
print(f"Taille : {size/1024:.1f} Ko")

# ============ ETAPE 6.2 : SAUVEGARDER LES ENCODEURS ============
joblib.dump(le_sexe, "models/encoder_sexe.pkl")
joblib.dump(le_region, "models/encoder_region.pkl")
joblib.dump(feature_cols, "models/feature_cols.pkl")

print("Encodeurs et metadata sauvegardes.")

# ============ ETAPE 7.1 : RECHARGER LE MODELE ============
model_loaded = joblib.load("models/model.pkl")
le_sexe_loaded = joblib.load("models/encoder_sexe.pkl")
le_region_loaded = joblib.load("models/encoder_region.pkl")

print(f"Modele recharge : {type(model_loaded).__name__}")
print(f"Classes : {list(model_loaded.classes_)}")


# ============ ETAPE 7.2 : PREDIRE NOUVEAU PATIENT ============
import pandas as pd

nouveau_patient = {
    'age': 28,
    'sexe': 'F',
    'temperature': 39.5,
    'tension_sys': 110,
    'toux': True,
    'fatigue': True,
    'maux_tete': True,
    'frissons': True,
    'nausee': False,
    'region': 'Dakar'
}

# Encoder les valeurs categoriques
sexe_enc = le_sexe_loaded.transform([nouveau_patient['sexe']])[0]
region_enc = le_region_loaded.transform([nouveau_patient['region']])[0]

# Charger les feature_cols exactes
feature_cols_loaded = joblib.load("models/feature_cols.pkl")

# Preparer le dictionnaire avec TOUTES les valeurs
patient_dict = {
    'age': nouveau_patient['age'],
    'sexe_encoded': sexe_enc,
    'temperature': nouveau_patient['temperature'],
    'tension_sys': nouveau_patient['tension_sys'],
    'toux': int(nouveau_patient['toux']),
    'fatigue': int(nouveau_patient['fatigue']),
    'maux_tete': int(nouveau_patient['maux_tete']),
    'frissons': int(nouveau_patient['frissons']),
    'nausee': int(nouveau_patient['nausee']),
    'region_encoded': region_enc
}

# Creer le DataFrame avec les bonnes colonnes dans le bon ordre
patient_df = pd.DataFrame([patient_dict])[feature_cols_loaded]

# Predire
diagnostic = model_loaded.predict(patient_df)[0]
probas = model_loaded.predict_proba(patient_df)[0]
proba_max = probas.max()

print(f"\n--- Resultat du pre-diagnostic ---")
print(f"Patient : {nouveau_patient['sexe']}, {nouveau_patient['age']} ans")
print(f"Diagnostic : {diagnostic}")
print(f"Probabilite : {proba_max:.1%}")
print(f"\nProbabilites par classe :")
for classe, proba in zip(model_loaded.classes_, probas):
    bar = '#' * int(proba * 30)
    print(f"  {classe:8s} : {proba:.1%} {bar}")

    # ============ EXERCICE 1 : IMPORTANCE DES FEATURES ============
importances = model.feature_importances_
for name, imp in sorted(zip(feature_cols, importances),
                        key=lambda x: x[1], reverse=True):
    print(f"  {name:20s} : {imp:.3f}")


    # ============ EXERCICE 2 : 3 PATIENTS FICTIFS ============
patients_test = [
    {
        'nom': 'Patient 1 - Jeune sans symptomes',
        'age': 18, 'sexe': 'M', 'temperature': 37.0,
        'tension_sys': 120, 'toux': False, 'fatigue': False,
        'maux_tete': False, 'frissons': False, 'nausee': False,
        'region': 'Dakar'
    },
    {
        'nom': 'Patient 2 - Adulte forte fievre',
        'age': 35, 'sexe': 'F', 'temperature': 40.5,
        'tension_sys': 95, 'toux': True, 'fatigue': True,
        'maux_tete': True, 'frissons': True, 'nausee': True,
        'region': 'Dakar'
    },
    {
        'nom': 'Patient 3 - Personne agee avec toux',
        'age': 65, 'sexe': 'M', 'temperature': 38.5,
        'tension_sys': 150, 'toux': True, 'fatigue': True,
        'maux_tete': False, 'frissons': False, 'nausee': False,
        'region': 'Dakar'
    }
]

print("\n========= EXERCICE 2 : 3 PATIENTS FICTIFS =========")
for p in patients_test:
    sexe_enc = le_sexe_loaded.transform([p['sexe']])[0]
    region_enc = le_region_loaded.transform([p['region']])[0]

    patient_dict = {
        'age': p['age'],
        'sexe_encoded': sexe_enc,
        'temperature': p['temperature'],
        'tension_sys': p['tension_sys'],
        'toux': int(p['toux']),
        'fatigue': int(p['fatigue']),
        'maux_tete': int(p['maux_tete']),
        'frissons': int(p['frissons']),
        'nausee': int(p['nausee']),
        'region_encoded': region_enc
    }

    patient_df = pd.DataFrame([patient_dict])[feature_cols_loaded]
    diagnostic = model_loaded.predict(patient_df)[0]
    probas = model_loaded.predict_proba(patient_df)[0]
    proba_max = probas.max()

    print(f"\n--- {p['nom']} ---")
    print(f"Diagnostic : {diagnostic} ({proba_max:.1%})")

    # ============ EXERCICE 3 : REFLEXION ============
# Un modele avec 89% d'accuracy dans un contexte medical reel
# n'est pas suffisant car 11% d'erreurs peut mettre des vies en danger.
# Par exemple, un faux negatif de paludisme peut retarder un traitement
# urgent et entrainer des complications graves.
# Ce modele doit etre utilise uniquement comme aide a la decision,
# jamais comme diagnostic definitif sans validation d'un medecin.