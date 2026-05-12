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
Tu expliques uniquement le diagnostic fourni."""

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
