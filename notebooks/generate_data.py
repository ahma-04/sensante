"""
Génère patients_dakar.csv : données synthétiques médicales
Diagnostics : palu, grippe, typh, sain
"""
import pandas as pd
import numpy as np

np.random.seed(42)
N = 400  # 100 par classe

regions = ["Dakar", "Thies", "Ziguinchor", "Saint-Louis", "Kaolack", "Diourbel"]
sexes = ["M", "F"]

def make_patients(diag, n):
    rows = []
    for _ in range(n):
        sexe = np.random.choice(sexes)
        age = int(np.random.randint(5, 70))
        region = np.random.choice(regions)

        if diag == "palu":
            temp = round(np.random.uniform(38.5, 41.0), 1)
            tension = int(np.random.randint(90, 130))
            toux = int(np.random.choice([0, 1], p=[0.4, 0.6]))
            fatigue = 1
            maux_tete = 1
            frissons = 1
            courbatures = int(np.random.choice([0, 1], p=[0.3, 0.7]))
            nausees = int(np.random.choice([0, 1], p=[0.4, 0.6]))
        elif diag == "grippe":
            temp = round(np.random.uniform(38.0, 39.5), 1)
            tension = int(np.random.randint(100, 135))
            toux = 1
            fatigue = 1
            maux_tete = int(np.random.choice([0, 1], p=[0.3, 0.7]))
            frissons = int(np.random.choice([0, 1], p=[0.4, 0.6]))
            courbatures = 1
            nausees = int(np.random.choice([0, 1], p=[0.5, 0.5]))
        elif diag == "typh":
            temp = round(np.random.uniform(39.0, 41.5), 1)
            tension = int(np.random.randint(85, 120))
            toux = int(np.random.choice([0, 1], p=[0.6, 0.4]))
            fatigue = 1
            maux_tete = 1
            frissons = int(np.random.choice([0, 1], p=[0.5, 0.5]))
            courbatures = int(np.random.choice([0, 1], p=[0.4, 0.6]))
            nausees = 1
        else:  # sain
            temp = round(np.random.uniform(36.0, 37.5), 1)
            tension = int(np.random.randint(110, 140))
            toux = int(np.random.choice([0, 1], p=[0.85, 0.15]))
            fatigue = int(np.random.choice([0, 1], p=[0.8, 0.2]))
            maux_tete = int(np.random.choice([0, 1], p=[0.8, 0.2]))
            frissons = 0
            courbatures = int(np.random.choice([0, 1], p=[0.9, 0.1]))
            nausees = int(np.random.choice([0, 1], p=[0.9, 0.1]))

        rows.append({
            "age": age, "sexe": sexe, "region": region,
            "temperature": temp, "tension": tension,
            "toux": toux, "fatigue": fatigue, "maux_tete": maux_tete,
            "frissons": frissons, "courbatures": courbatures, "nausees": nausees,
            "diagnostic": diag
        })
    return rows

data = []
for d in ["palu", "grippe", "typh", "sain"]:
    data.extend(make_patients(d, 100))

df = pd.DataFrame(data)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
df.to_csv("data/patients_dakar.csv", index=False)
print(f"Dataset créé : {len(df)} patients")
print(df["diagnostic"].value_counts())
print(df.head())
