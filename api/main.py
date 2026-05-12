<<<<<<< HEAD
# api/main.py
# SenSante API - Assistant pre-diagnostic medical
# Lab 3 - Integration de Modeles IA - ESP/UCAD

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import numpy as np
import os
from dotenv import load_dotenv
from groq import Groq

# Charger les variables d'environnement
load_dotenv()

# Client Groq (charge au demarrage)
groq_client = None
groq_api_key = os.getenv("GROQ_API_KEY")
if groq_api_key:
    groq_client = Groq(api_key=groq_api_key)
    print("Client Groq initialise.")
else:
    print("ATTENTION : GROQ_API_KEY non trouvee. "
          "/explain sera desactive.")

# --- Schemas Pydantic ---
class PatientInput(BaseModel):
    age: int = Field(..., ge=0, le=120)
    sexe: str = Field(...)
    temperature: float = Field(..., ge=35.0, le=42.0)
    tension_sys: int = Field(..., ge=60, le=250)
    toux: bool = Field(...)
    fatigue: bool = Field(...)
    maux_tete: bool = Field(...)
    frissons: bool = Field(...)
    nausee: bool = Field(...)
    region: str = Field(...)

class DiagnosticOutput(BaseModel):
    diagnostic: str
    probabilite: float
    confiance: str
    message: str

class ExplainInput(BaseModel):
    diagnostic: str = Field(...,
        description="Diagnostic predit par le modele")
    probabilite: float = Field(...,
        description="Probabilite du diagnostic")
    age: int = Field(...)
    sexe: str = Field(...)
    temperature: float = Field(...)
    region: str = Field(...)

class ExplainOutput(BaseModel):
    explication: str = Field(...,
        description="Explication en francais")
    modele_llm: str = Field(
        default="llama-3.1-8b-instant",
        description="Modele LLM utilise")

# --- Application FastAPI ---
app = FastAPI(
    title="SenSante API",
    description="Assistant pre-diagnostic medical pour le Senegal",
    version="0.2.0"
)

# Autoriser les requetes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Chargement du modele (une seule fois) ---
print("Chargement du modele...")
model = joblib.load("models/model.pkl")
le_sexe = joblib.load("models/encoder_sexe.pkl")
le_region = joblib.load("models/encoder_region.pkl")
feature_cols = joblib.load("models/feature_cols.pkl")
print(f"Modele charge : {list(model.classes_)}")

# --- Routes ---
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "SenSante API is running"}

@app.post("/predict", response_model=DiagnosticOutput)
def predict(patient: PatientInput):
    # Encoder
    try:
        sexe_enc = le_sexe.transform([patient.sexe])[0]
    except ValueError:
        return DiagnosticOutput(
            diagnostic="erreur", probabilite=0.0,
            confiance="aucune",
            message=f"Sexe invalide : {patient.sexe}")
    try:
        region_enc = le_region.transform([patient.region])[0]
    except ValueError:
        return DiagnosticOutput(
            diagnostic="erreur", probabilite=0.0,
            confiance="aucune",
            message=f"Region inconnue : {patient.region}")

    # Features
    features = np.array([[
        patient.age, sexe_enc, patient.temperature,
        patient.tension_sys, int(patient.toux),
        int(patient.fatigue), int(patient.maux_tete),
        int(patient.frissons), int(patient.nausee),
        region_enc
    ]])

    # Prediction
    diagnostic = model.predict(features)[0]
    proba_max = float(model.predict_proba(features)[0].max())
    confiance = ("haute" if proba_max >= 0.7
        else "moyenne" if proba_max >= 0.4
        else "faible")

    messages = {
        "palu": "Suspicion de paludisme. Consultez rapidement.",
        "grippe": "Suspicion de grippe. Repos et hydratation.",
        "typh": "Suspicion de typhoide. Consultation necessaire.",
        "sain": "Pas de pathologie detectee."
    }

    return DiagnosticOutput(
        diagnostic=diagnostic,
        probabilite=round(proba_max, 2),
        confiance=confiance,
        message=messages.get(diagnostic, "Consultez un medecin.")
    )

# --- Route LLM ---
SYSTEM_PROMPT = """Tu es un assistant medical senegalais.
Tu recois un diagnostic et des donnees patient.
Explique le resultat en francais simple,
comme un medecin parlerait a son patient.
Sois rassurant mais recommande toujours
une consultation medicale.
Maximum 3 phrases.
Ne fais JAMAIS de diagnostic toi-meme.
Tu expliques uniquement le diagnostic fourni."""

@app.post("/explain", response_model=ExplainOutput)
def explain(data: ExplainInput):
    """Expliquer un diagnostic en francais avec un LLM."""
    if not groq_client:
        return ExplainOutput(
            explication="Service d'explication indisponible. "
                        "Cle API non configuree.",
            modele_llm="aucun"
        )

    user_prompt = (
        f"Patient : {data.sexe}, {data.age} ans, "
        f"region {data.region}\n"
        f"Temperature : {data.temperature} C\n"
        f"Diagnostic du modele : {data.diagnostic} "
        f"(probabilite {data.probabilite:.0%})\n"
        f"Explique ce resultat au patient."
    )

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=200,
            temperature=0.3
        )
        explication = response.choices[0].message.content
    except Exception as e:
        explication = f"Erreur lors de l'appel au LLM : {str(e)}"

    return ExplainOutput(explication=explication)
=======
"""
SénSanté API - Lab 5 : ML + LLM via Groq
"""
import os
import pickle
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from groq import Groq

# Charger les variables d'environnement
load_dotenv()

app = FastAPI(
    title="SénSanté API",
    description="API de pré-diagnostic médical avec LLM",
    version="4.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Chargement du modèle ML ──────────────────────────────────────────────────
print("Chargement du modele...")
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE, "models", "model.pkl"), "rb") as f:
    model = pickle.load(f)
with open(os.path.join(BASE, "models", "encoder_sexe.pkl"), "rb") as f:
    encoder_sexe = pickle.load(f)
with open(os.path.join(BASE, "models", "encoder_region.pkl"), "rb") as f:
    encoder_region = pickle.load(f)
with open(os.path.join(BASE, "models", "feature_cols.pkl"), "rb") as f:
    feature_cols = pickle.load(f)

print(f"Modele charge : {list(model.classes_)}")

# ── Client Groq (chargé au démarrage) ────────────────────────────────────────
groq_client = None
groq_api_key = os.getenv("GROQ_API_KEY")
if groq_api_key:
    groq_client = Groq(api_key=groq_api_key)
    print("Client Groq initialise.")
else:
    print("ATTENTION : GROQ_API_KEY non trouvee. /explain sera desactive.")

# ── Schémas Pydantic ──────────────────────────────────────────────────────────
class PatientInput(BaseModel):
    age: int = Field(..., ge=0, le=120)
    sexe: str = Field(..., pattern="^[MF]$")
    region: str = Field(...)
    temperature: float = Field(..., ge=35.0, le=45.0)
    tension: int = Field(..., ge=50, le=200)
    toux: int = Field(..., ge=0, le=1)
    fatigue: int = Field(..., ge=0, le=1)
    maux_tete: int = Field(..., ge=0, le=1)
    frissons: int = Field(..., ge=0, le=1)
    courbatures: int = Field(..., ge=0, le=1)
    nausees: int = Field(..., ge=0, le=1)

class DiagnosticOutput(BaseModel):
    diagnostic: str
    probabilite: float
    confiance: str
    toutes_probabilites: dict

class ExplainInput(BaseModel):
    diagnostic: str = Field(..., description="Diagnostic predit par le modele")
    probabilite: float = Field(..., description="Probabilite du diagnostic")
    age: int = Field(...)
    sexe: str = Field(...)
    temperature: float = Field(...)
    region: str = Field(...)

class ExplainOutput(BaseModel):
    explication: str = Field(..., description="Explication en francais")
    modele_llm: str = Field(default="llama-3.1-8b-instant", description="Modele LLM utilise")

# ── System prompt médical ─────────────────────────────────────────────────────
SYSTEM_PROMPT = """Tu es un assistant medical senegalais.
Tu recois un diagnostic et des donnees patient.
Explique le resultat en francais simple,
comme un medecin parlerait a son patient.
Sois rassurant mais recommande toujours
une consultation medicale.
Maximum 3 phrases.
Ne fais JAMAIS de diagnostic toi-meme.
Tu expliques uniquement le diagnostic fourni.
Termine TOUJOURS par : 'Ne prenez aucun medicament sans consulter un medecin ou un agent de sante qualifie.'"""

# ── Endpoints ─────────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    """Vérifier que l'API est en marche."""
    return {
        "status": "ok",
        "version": "4.0.0",
        "modele_ml": "RandomForest",
        "llm": "llama-3.1-8b-instant" if groq_client else "desactive",
        "classes": list(model.classes_)
    }


@app.post("/predict", response_model=DiagnosticOutput)
def predict(patient: PatientInput):
    """Prédire le diagnostic d'un patient."""
    try:
        sexe_enc = encoder_sexe.transform([patient.sexe])[0]
    except ValueError:
        sexe_enc = 0
    try:
        region_enc = encoder_region.transform([patient.region])[0]
    except ValueError:
        region_enc = 0

    X = np.array([[
        patient.age, sexe_enc, region_enc,
        patient.temperature, patient.tension,
        patient.toux, patient.fatigue, patient.maux_tete,
        patient.frissons, patient.courbatures, patient.nausees
    ]])

    proba = model.predict_proba(X)[0]
    classes = model.classes_
    idx = int(np.argmax(proba))
    diag = classes[idx]
    prob = float(proba[idx])

    confiance = "haute" if prob >= 0.70 else ("moyenne" if prob >= 0.50 else "faible")

    return DiagnosticOutput(
        diagnostic=diag,
        probabilite=round(prob, 4),
        confiance=confiance,
        toutes_probabilites={c: round(float(p), 4) for c, p in zip(classes, proba)}
    )


@app.post("/explain", response_model=ExplainOutput)
def explain(data: ExplainInput):
    """Expliquer un diagnostic en francais avec un LLM."""
    if not groq_client:
        return ExplainOutput(
            explication="Service d'explication indisponible. Cle API non configuree.",
            modele_llm="aucun"
        )

    user_prompt = (
        f"Patient : {data.sexe}, {data.age} ans, region {data.region}\n"
        f"Temperature : {data.temperature} C\n"
        f"Diagnostic du modele : {data.diagnostic} "
        f"(probabilite {data.probabilite:.0%})\n"
        f"Explique ce resultat au patient."
    )

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=200,
            temperature=0.3
        )
        explication = response.choices[0].message.content
    except Exception as e:
        explication = f"Erreur lors de l'appel au LLM : {str(e)}"

    return ExplainOutput(explication=explication)
>>>>>>> 98dbce0c38a598024846676fd0c80a6f1de1f03a
