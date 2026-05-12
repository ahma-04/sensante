# notebooks/exercice2_temperature.py
# Exercice 2 - Tester le meme appel avec temperature=0.0, 0.5 et 1.0

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """Tu es un assistant medical senegalais.
Tu recois un diagnostic et des donnees patient.
Explique le resultat en francais simple,
comme un medecin parlerait a son patient.
Sois rassurant mais recommande toujours une consultation medicale.
Maximum 3 phrases.
Ne fais JAMAIS de diagnostic toi-meme."""

USER_PROMPT = """Patient : Femme, 28 ans, region Dakar
Temperature : 39.5 C
Diagnostic du modele : paludisme (probabilite 72%)
Explique ce resultat au patient."""

temperatures = [0.0, 0.5, 1.0]

print("=" * 60)
print("EXERCICE 2 - Comparaison des temperatures LLM")
print("Meme prompt, meme patient — seule la temperature change")
print("=" * 60)

for temp in temperatures:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": USER_PROMPT}
        ],
        max_tokens=200,
        temperature=temp
    )

    print(f"\n{'='*60}")
    print(f"temperature = {temp}")
    print(f"{'='*60}")
    print(response.choices[0].message.content)
    print(f"[Tokens : {response.usage.total_tokens}]")

print("\n" + "=" * 60)
print("FIN EXERCICE 2")
print("=" * 60)
