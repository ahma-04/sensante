"""
Lab 2 : Entraîner le modèle RandomForest pour SénSanté
"""
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score

print("=== Entraînement du modèle SénSanté ===")

df = pd.read_csv("data/patients_dakar.csv")
print(f"Dataset : {len(df)} patients, {df['diagnostic'].nunique()} classes")
print(df["diagnostic"].value_counts())

encoder_sexe = LabelEncoder()
encoder_region = LabelEncoder()
df["sexe_enc"] = encoder_sexe.fit_transform(df["sexe"])
df["region_enc"] = encoder_region.fit_transform(df["region"])

feature_cols = ["age", "sexe_enc", "region_enc", "temperature", "tension",
                "toux", "fatigue", "maux_tete", "frissons", "courbatures", "nausees"]

X = df[feature_cols]
y = df["diagnostic"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\nAccuracy : {acc:.2%}")
print("\nRapport de classification :")
print(classification_report(y_test, y_pred))

os.makedirs("models", exist_ok=True)
with open("models/model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("models/encoder_sexe.pkl", "wb") as f:
    pickle.dump(encoder_sexe, f)
with open("models/encoder_region.pkl", "wb") as f:
    pickle.dump(encoder_region, f)
with open("models/feature_cols.pkl", "wb") as f:
    pickle.dump(feature_cols, f)

print("\nModèles sauvegardés dans models/")
print(f"Classes : {list(model.classes_)}")
