# notebooks/exercice1_wolof.py
# Exercice 1 - Prompt engineering : reponses en wolof
# Tester avec plusieurs diagnostics

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT_WOLOF = """Tu es un assistant medical senegalais bilingue wolof-francais.
Tu recois un diagnostic medical et des donnees patient.
Reponds en melangeant le wolof simple et le francais,
comme un agent de sante senegalais parlerait a son patient au village.
Utilise des expressions wolof courantes : Jaam nga am (tu es en paix),
Na nga def (comment tu vas), Yendoo (maladie), Feebar (fievre).
Sois rassurant et recommande une consultation medicale.
Maximum 3 phrases.
Ne fais JAMAIS de diagnostic toi-meme."""

print("=" * 60)
print("EXERCICE 1 - Prompt engineering : Reponses en Wolof")
print("=" * 60)

cas = [
    {
        "label": "Cas 1 - Paludisme (F, 28 ans, Dakar, 39.5 C, 72%)",
        "data": {
            "sexe": "F", "age": 28, "region": "Dakar",
            "temperature": 39.5, "diagnostic": "paludisme", "probabilite": 0.72
        }
    },
    {
        "label": "Cas 2 - Patient sain (M, 35 ans, Thies, 36.8 C, 100%)",
        "data": {
            "sexe": "M", "age": 35, "region": "Thies",
            "temperature": 36.8, "diagnostic": "sain", "probabilite": 1.0
        }
    },
    {
        "label": "Cas 3 - Typhoide (M, 45 ans, Ziguinchor, 40.2 C, 88%)",
        "data": {
            "sexe": "M", "age": 45, "region": "Ziguinchor",
            "temperature": 40.2, "diagnostic": "typhoide", "probabilite": 0.8875
        }
    },
]

for cas_test in cas:
    d = cas_test["data"]
    user_prompt = (
        f"Patient : {d['sexe']}, {d['age']} ans, region {d['region']}\n"
        f"Temperature : {d['temperature']} C\n"
        f"Diagnostic du modele : {d['diagnostic']} (probabilite {d['probabilite']:.0%})\n"
        f"Explique ce resultat au patient en wolof et francais."
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT_WOLOF},
            {"role": "user",   "content": user_prompt}
        ],
        max_tokens=200,
        temperature=0.3
    )

    print(f"\n--- {cas_test['label']} ---")
    print(response.choices[0].message.content)
    print(f"[Tokens : {response.usage.total_tokens}]")

print("\n" + "=" * 60)
print("FIN EXERCICE 1")
print("=" * 60)
