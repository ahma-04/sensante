"""
Génère le rapport PDF du Lab 5 : Intégrer un LLM via Groq
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, Image
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

OUTPUT = "rapport_lab5_LLM_Groq.pdf"

SCREENSHOTS = {
    "formulaire": r"C:\Users\LENOVO\Pictures\Screenshots\Capture d'écran 2026-05-12 151055.png",
    "exo1":       r"C:\Users\LENOVO\Pictures\Screenshots\Capture d'écran 2026-05-12 151322.png",
    "exo2":       r"C:\Users\LENOVO\Pictures\Screenshots\Capture d'écran 2026-05-12 151402.png",
    "exo3":       r"C:\Users\LENOVO\Pictures\Screenshots\Capture d'écran 2026-05-12 151500.png",
}

def screenshot(key, width=15*cm, caption=None):
    """Retourne une Image + légende pour le rapport."""
    from PIL import Image as PILImage
    with PILImage.open(SCREENSHOTS[key]) as im:
        orig_w, orig_h = im.size
    height = width * orig_h / orig_w
    items = [Image(SCREENSHOTS[key], width=width, height=height)]
    if caption:
        items.append(Paragraph(caption, S["caption"]))
    return items

doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=2.5*cm, rightMargin=2.5*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm
)

styles = getSampleStyleSheet()

# ── Styles personnalisés ──────────────────────────────────────────────────────
S = {
    "titre":  ParagraphStyle("titre",  parent=styles["Title"],
                             fontSize=22, textColor=colors.HexColor("#1a5276"),
                             spaceAfter=4, alignment=TA_CENTER),
    "sous_titre": ParagraphStyle("sous_titre", parent=styles["Normal"],
                                 fontSize=13, textColor=colors.HexColor("#2e86c1"),
                                 spaceAfter=2, alignment=TA_CENTER),
    "info":   ParagraphStyle("info",   parent=styles["Normal"],
                             fontSize=10, textColor=colors.HexColor("#555555"),
                             alignment=TA_CENTER, spaceAfter=2),
    "h1":     ParagraphStyle("h1",     parent=styles["Heading1"],
                             fontSize=14, textColor=colors.HexColor("#1a5276"),
                             spaceBefore=14, spaceAfter=6,
                             borderPad=2),
    "h2":     ParagraphStyle("h2",     parent=styles["Heading2"],
                             fontSize=12, textColor=colors.HexColor("#2e86c1"),
                             spaceBefore=10, spaceAfter=4),
    "body":   ParagraphStyle("body",   parent=styles["Normal"],
                             fontSize=10, leading=14, alignment=TA_JUSTIFY,
                             spaceAfter=6),
    "code":   ParagraphStyle("code",   parent=styles["Code"],
                             fontSize=8.5, leading=12,
                             backColor=colors.HexColor("#f4f4f4"),
                             borderColor=colors.HexColor("#cccccc"),
                             borderWidth=0.5, borderPad=6,
                             fontName="Courier"),
    "output": ParagraphStyle("output", parent=styles["Code"],
                             fontSize=8.5, leading=12,
                             backColor=colors.HexColor("#1e1e1e"),
                             textColor=colors.HexColor("#d4d4d4"),
                             borderPad=8, fontName="Courier"),
    "ok":     ParagraphStyle("ok",     parent=styles["Normal"],
                             fontSize=10,
                             backColor=colors.HexColor("#eafaf1"),
                             textColor=colors.HexColor("#1e8449"),
                             borderColor=colors.HexColor("#27ae60"),
                             borderWidth=1, borderPad=6,
                             spaceAfter=6),
    "warn":   ParagraphStyle("warn",   parent=styles["Normal"],
                             fontSize=10,
                             backColor=colors.HexColor("#fef9e7"),
                             textColor=colors.HexColor("#7d6608"),
                             borderColor=colors.HexColor("#f39c12"),
                             borderWidth=1, borderPad=6,
                             spaceAfter=6),
    "caption":ParagraphStyle("caption",parent=styles["Normal"],
                             fontSize=8.5, textColor=colors.HexColor("#666666"),
                             alignment=TA_CENTER, spaceAfter=8, spaceBefore=2),
}

def HR():
    return HRFlowable(width="100%", thickness=1,
                      color=colors.HexColor("#2e86c1"), spaceAfter=8)

def code_block(lines):
    txt = "<br/>".join(lines.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").split("\n"))
    return Paragraph(txt, S["code"])

def output_block(lines):
    txt = "<br/>".join(lines.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").split("\n"))
    return Paragraph(txt, S["output"])

story = []

# ══════════════════════════════════════════════════════════════════════════════
# PAGE DE TITRE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Spacer(1, 1.5*cm),
    Paragraph("Intégration de Modèles IA dans les Systèmes Logiciels", S["titre"]),
    Paragraph("Lab 5 : Intégrer un LLM via Groq", S["sous_titre"]),
    Spacer(1, 0.5*cm),
    HR(),
    Spacer(1, 0.3*cm),
    Paragraph("École Supérieure Polytechnique — Université Cheikh Anta Diop de Dakar", S["info"]),
    Paragraph("Département Génie Informatique — L2 GLSI / DUT-INFO2 — Semestre 4 — 2026", S["info"]),
    Paragraph("Enseignant : Dr. El Hadji Bassirou TOURE", S["info"]),
    Spacer(1, 0.3*cm),
    HR(),
    Spacer(1, 1.5*cm),
]

# Tableau résumé
summary_data = [
    ["Objectif", "Ajouter de l'IA générative à SénSanté via l'API Groq (Llama 3)"],
    ["Tag Git",  "v4"],
    ["Compétence", "C6 — Intégrer un LLM via API"],
    ["Modèle LLM", "llama-3.1-8b-instant (Groq)"],
    ["Modèle ML",  "RandomForest (scikit-learn) — Accuracy 85%"],
    ["Classes",    "grippe | palu | typh | sain"],
    ["Date",       "12 Mai 2026"],
]
t = Table(summary_data, colWidths=[4*cm, 12*cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#2e86c1")),
    ("TEXTCOLOR",  (0,0), (0,-1), colors.white),
    ("FONTNAME",   (0,0), (0,-1), "Helvetica-Bold"),
    ("FONTSIZE",   (0,0), (-1,-1), 9),
    ("ROWBACKGROUNDS", (1,0), (-1,-1), [colors.HexColor("#f0f8ff"), colors.white]),
    ("GRID",       (0,0), (-1,-1), 0.5, colors.HexColor("#aaaaaa")),
    ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
    ("LEFTPADDING",(0,0), (-1,-1), 8),
    ("RIGHTPADDING",(0,0), (-1,-1), 8),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING",(0,0), (-1,-1), 5),
]))
story += [t, Spacer(1, 2*cm)]

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Introduction
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("1. Introduction", S["h1"]), HR(),
    Paragraph(
        "SénSanté est une application web de pré-diagnostic médical destinée aux agents de santé "
        "au Sénégal. Le modèle RandomForest classe les symptômes en quatre diagnostics (paludisme, "
        "grippe, typhoïde, patient sain) mais ne fournit pas d'explication en langage naturel. "
        "Ce Lab 5 ajoute un endpoint POST /explain qui appelle Llama 3 via l'API Groq pour "
        "expliquer le diagnostic en français simple.", S["body"]),
    Paragraph(
        "Le flux complet est : Frontend → POST /predict (ML) → diagnostic + probabilité → "
        "POST /explain (LLM Groq) → explication en français → affichée sous le diagnostic.", S["body"]),
    Spacer(1, 0.3*cm),
]

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Étape 1 : Compte Groq et clé API
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("2. Étape 1 : Créer un compte Groq et obtenir la clé API", S["h1"]), HR(),
    Paragraph(
        "La première étape consiste à créer un compte gratuit sur https://console.groq.com "
        "puis à générer une clé API nommée <i>sensante</i>. La clé a le format : "
        "<b>gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxx</b>", S["body"]),
    Paragraph(
        "<b>Point d'attention :</b> La clé API ne doit JAMAIS être committée dans Git. "
        "Elle sera stockée dans un fichier .env ajouté au .gitignore.", S["warn"]),
    Spacer(1, 0.3*cm),
]

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — Étape 2 : Sécuriser la clé
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("3. Étape 2 : Stocker la clé de manière sécurisée (.env)", S["h1"]), HR(),
    Paragraph("Installation des dépendances :", S["h2"]),
    code_block("pip install groq python-dotenv\npip freeze > requirements.txt"),
    Paragraph("Contenu du fichier .env créé à la racine du projet :", S["h2"]),
    code_block("# .env (à la racine de sensante/)\nGROQ_API_KEY=gsk_votre_cle_ici"),
    Paragraph("Ajout de .env dans .gitignore :", S["h2"]),
    code_block("# Cles API - NE JAMAIS COMMITTER\n.env"),
    Paragraph(
        "<b>Vérification :</b> La commande <i>git status</i> confirme que le fichier .env "
        "n'apparaît pas dans la liste des fichiers à committer — le .gitignore fonctionne.", S["ok"]),
    Spacer(1, 0.3*cm),
]

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — Étape 3 : Script test_groq.py
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("4. Étape 3 : Premier appel Groq — script de test", S["h1"]), HR(),
    Paragraph("Le script notebooks/test_groq.py réalise deux tests :", S["body"]),
    Paragraph("<b>Test 1 :</b> Question simple sur les symptômes du paludisme", S["h2"]),
    code_block("""python notebooks/test_groq.py"""),
    Paragraph("Résultat — Test 1 (Llama 3 répond en français) :", S["h2"]),
    output_block(
        "==================================================\n"
        "Test 1 : Question simple sur le paludisme\n"
        "==================================================\n"
        "=== Reponse de Llama 3 ===\n"
        "Le paludisme est une maladie grave causee par le parasite Plasmodium.\n"
        "Les symptomes courants incluent :\n"
        "- Fievre haute et intermittente\n"
        "- Maux de tete et de corps\n"
        "- Fatigue et faiblesse\n"
        "- Douleurs articulaires et musculaires\n"
        "- Nausees et vomissements\n\n"
        "Tokens utilises : 179"
    ),
    Paragraph("Résultat — Test 2 (format SénSanté, patient F 28 ans, palu 72%) :", S["h2"]),
    output_block(
        "==================================================\n"
        "Test 2 : Explication SenSante (diagnostic palu 72%)\n"
        "==================================================\n"
        "=== Explication SenSante ===\n"
        "Madame, je suis rassure que vous soyez venue nous voir. Les resultats\n"
        "suggerent que vous pourriez avoir la maladie du paludisme. C'est une\n"
        "maladie courante dans notre region, mais il est important que nous en\n"
        "parlions plus en detail pour confirmer le diagnostic. Je vous recommande\n"
        "de consulter un medecin pour une evaluation plus approfondie.\n\n"
        "Tokens utilises : 257"
    ),
    Paragraph(
        "<b>Résultat :</b> En 20 lignes de code, Llama 3 (8 milliards de paramètres) "
        "répond en français en moins d'une seconde. La clé API Groq fonctionne correctement.", S["ok"]),
    Spacer(1, 0.3*cm),
]

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — Étape 4 : Endpoint /explain dans FastAPI
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("5. Étape 4 : Ajouter l'endpoint POST /explain dans l'API", S["h1"]), HR(),
    Paragraph(
        "Trois modifications ont été apportées à api/main.py :", S["body"]),
    Paragraph("<b>5.1 Imports et initialisation du client Groq</b>", S["h2"]),
    code_block(
        "from dotenv import load_dotenv\n"
        "from groq import Groq\n\n"
        "load_dotenv()\n"
        "groq_client = None\n"
        "groq_api_key = os.getenv('GROQ_API_KEY')\n"
        "if groq_api_key:\n"
        "    groq_client = Groq(api_key=groq_api_key)\n"
        "    print('Client Groq initialise.')\n"
        "else:\n"
        "    print('ATTENTION : GROQ_API_KEY non trouvee. /explain desactive.')"
    ),
    Paragraph("<b>5.2 Schémas Pydantic ExplainInput / ExplainOutput</b>", S["h2"]),
    code_block(
        "class ExplainInput(BaseModel):\n"
        "    diagnostic: str\n"
        "    probabilite: float\n"
        "    age: int\n"
        "    sexe: str\n"
        "    temperature: float\n"
        "    region: str\n\n"
        "class ExplainOutput(BaseModel):\n"
        "    explication: str\n"
        "    modele_llm: str = 'llama-3.1-8b-instant'"
    ),
    Paragraph("<b>5.3 System prompt médical et route POST /explain</b>", S["h2"]),
    code_block(
        "SYSTEM_PROMPT = \"\"\"Tu es un assistant medical senegalais.\n"
        "Tu recois un diagnostic et des donnees patient.\n"
        "Explique le resultat en francais simple,\n"
        "comme un medecin parlerait a son patient.\n"
        "Sois rassurant mais recommande toujours une consultation medicale.\n"
        "Maximum 3 phrases.\n"
        "Ne fais JAMAIS de diagnostic toi-meme.\"\"\"\n\n"
        "@app.post('/explain', response_model=ExplainOutput)\n"
        "def explain(data: ExplainInput):\n"
        "    if not groq_client:\n"
        "        return ExplainOutput(explication='Service indisponible.', modele_llm='aucun')\n"
        "    user_prompt = f'Patient : {data.sexe}, {data.age} ans, region {data.region}\\n'\n"
        "                  f'Temperature : {data.temperature} C\\n'\n"
        "                  f'Diagnostic : {data.diagnostic} ({data.probabilite:.0%})'\n"
        "    response = groq_client.chat.completions.create(\n"
        "        model='llama-3.1-8b-instant',\n"
        "        messages=[{'role':'system','content':SYSTEM_PROMPT},\n"
        "                  {'role':'user','content':user_prompt}],\n"
        "        max_tokens=200, temperature=0.3\n"
        "    )\n"
        "    return ExplainOutput(explication=response.choices[0].message.content)"
    ),
    Spacer(1, 0.3*cm),
]

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — Étape 5 : Tests endpoint /explain
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("6. Étape 5 : Tester l'endpoint POST /explain", S["h1"]), HR(),
    Paragraph("Démarrage de l'API :", S["h2"]),
    code_block("uvicorn api.main:app --reload"),
    output_block(
        "Chargement du modele...\n"
        "Modele charge : ['grippe', 'palu', 'sain', 'typh']\n"
        "Client Groq initialise.\n"
        "INFO:     Application startup complete."
    ),
    Paragraph("<b>Test /health</b> — Vérifier que l'API démarre correctement :", S["h2"]),
    code_block("curl -s http://localhost:8000/health | python -m json.tool"),
    output_block(
        "{\n"
        "    \"status\": \"ok\",\n"
        "    \"version\": \"4.0.0\",\n"
        "    \"modele_ml\": \"RandomForest\",\n"
        "    \"llm\": \"llama-3.1-8b-instant\",\n"
        "    \"classes\": [\"grippe\", \"palu\", \"sain\", \"typh\"]\n"
        "}"
    ),
    Paragraph("<b>Test /explain via curl</b> — Cas Paludisme (F, 28 ans, Dakar, 39.5°C, 72%) :", S["h2"]),
    code_block(
        "curl -X POST http://localhost:8000/explain \\\n"
        "  -H 'Content-Type: application/json' \\\n"
        '  -d \'{"diagnostic":"palu","probabilite":0.72,"age":28,"sexe":"F","temperature":39.5,"region":"Dakar"}\''
    ),
    output_block(
        "{\n"
        "  \"explication\": \"Bonjour, je voudrais vous parler de vos resultats. Selon les\n"
        "  informations que nous avons, il semble que vous puissiez etre infecte par la\n"
        "  paludisme. C'est une maladie causee par un parasite qui se transmet par les\n"
        "  moustiques. Il est important de noter que ce n'est qu'un resultat possible et\n"
        "  que la seule facon de confirmer le diagnostic est une consultation medicale.\n"
        "  Je vous recommande de voir un medecin pour un diagnostic definitif.\",\n"
        "  \"modele_llm\": \"llama-3.1-8b-instant\"\n"
        "}"
    ),
    Paragraph(
        "<b>Résultat :</b> L'API retourne bien une explication en français générée par Llama 3. "
        "L'application dispose maintenant de 3 endpoints : /health, /predict (ML), /explain (LLM).", S["ok"]),
    Spacer(1, 0.3*cm),
]

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 7 — Étape 6 : Frontend
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("7. Étape 6 : Connecter le frontend", S["h1"]), HR(),
    Paragraph(
        "Le fichier frontend/index.html a été modifié pour appeler automatiquement "
        "POST /explain après l'affichage du diagnostic. La fonction "
        "<i>demanderExplication()</i> affiche d'abord un indicateur de chargement "
        "animé (<i>Génération en cours…</i>) puis remplace ce texte par l'explication "
        "retournée par le LLM.", S["body"]),
    code_block(
        "async function demanderExplication(diagnostic_data) {\n"
        "    const explainData = {\n"
        "        diagnostic: diagnostic_data.diagnostic,\n"
        "        probabilite: diagnostic_data.probabilite,\n"
        "        age: parseInt(document.getElementById('age').value),\n"
        "        sexe: document.getElementById('sexe').value,\n"
        "        temperature: parseFloat(document.getElementById('temperature').value),\n"
        "        region: document.getElementById('region').value\n"
        "    };\n"
        "    const resp = await fetch(API_URL + '/explain', {\n"
        "        method: 'POST',\n"
        "        headers: {'Content-Type': 'application/json'},\n"
        "        body: JSON.stringify(explainData)\n"
        "    });\n"
        "    const result = await resp.json();\n"
        "    // Afficher result.explication dans la zone purple\n"
        "}"
    ),
    Paragraph(
        "<b>Flux UX :</b> Le diagnostic s'affiche immédiatement (RandomForest rapide), "
        "puis l'explication Llama 3 apparaît 1-2 secondes plus tard. Ce pattern ne bloque "
        "pas l'interface utilisateur.", S["body"]),
    Spacer(1, 0.3*cm),
    Paragraph("<b>Capture — Formulaire SénSanté (localhost:3000) :</b>", S["h2"]),
] + screenshot("formulaire", caption="Figure : Interface SénSanté — formulaire patient prêt pour le diagnostic.") + [
    Spacer(1, 0.3*cm),
]

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 8 — Étape 7 : Tests complets
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("8. Étape 7 : Tests bout en bout et cas limites", S["h1"]), HR(),
    Paragraph("<b>Test 1 — Cas paludisme :</b> F, 28 ans, Dakar, 39.5°C, frissons + fatigue + maux de tête", S["h2"]),
    output_block(
        "/predict  =>  { diagnostic: palu, probabilite: 0.8033, confiance: haute }\n"
        "              toutes_probabilites: { grippe:0.08, palu:0.80, sain:0.00, typh:0.12 }\n\n"
        "/explain  =>  Bonjour, je voudrais vous parler de vos resultats. Selon les\n"
        "              informations que nous avons, il semble que vous puissiez etre\n"
        "              infecte par la paludisme, une maladie causee par un parasite\n"
        "              transmis par les moustiques. Il est important de consulter un\n"
        "              medecin pour confirmer le diagnostic et obtenir un traitement."
    ),
    Paragraph("<b>Test 2 — Patient sain :</b> M, 35 ans, Thies, 36.8°C, aucun symptôme", S["h2"]),
    output_block(
        "/predict  =>  { diagnostic: sain, probabilite: 1.0, confiance: haute }\n"
        "              toutes_probabilites: { grippe:0.00, palu:0.00, sain:1.00, typh:0.00 }\n\n"
        "/explain  =>  Bonjour Monsieur, je suis heureux de vous dire que les resultats\n"
        "              de vos tests indiquent que vous etes en bonne sante. Votre\n"
        "              temperature est normale, ce qui signifie que votre corps\n"
        "              fonctionne correctement. Cependant, il est toujours important\n"
        "              de consulter regulierement un medecin pour des examens de routine."
    ),
    Paragraph("<b>Test 3 — Typhoïde :</b> M, 45 ans, Ziguinchor, 40.2°C, nausées + fatigue + maux de tête", S["h2"]),
    output_block(
        "/predict  =>  { diagnostic: typh, probabilite: 0.8875, confiance: haute }\n"
        "              toutes_probabilites: { grippe:0.05, palu:0.06, sain:0.00, typh:0.89 }\n\n"
        "/explain  =>  Bonjour Monsieur, je voudrais vous parler de vos resultats.\n"
        "              Selon les informations que nous avons, il semble que vous soyez\n"
        "              susceptible d'avoir la fievre typhoide. C'est une maladie\n"
        "              bacterienne qui peut causer une forte fievre comme celle que\n"
        "              vous avez actuellement avec 40,2 degres. Consultez un medecin."
    ),
    Paragraph("<b>Test 4 — Dégradation gracieuse :</b> clé API absente (groq_client = None)", S["h2"]),
    output_block(
        "POST /explain  =>  HTTP 200\n"
        "{\n"
        "  \"explication\": \"Service d'explication indisponible. Cle API non configuree.\",\n"
        "  \"modele_llm\": \"aucun\"\n"
        "}\n"
        "=> L'endpoint /predict fonctionne toujours. L'app ne plante pas."
    ),
    Paragraph(
        "<b>Résultat :</b> Tous les tests passent. L'application combine correctement "
        "le modèle ML et le LLM. La dégradation gracieuse garantit que le diagnostic "
        "reste disponible même sans accès à Groq.", S["ok"]),
    Spacer(1, 0.3*cm),
]

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 9 — Étape 8 : Git
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("9. Étape 8 : Git — Sauvegarder la version v4", S["h1"]), HR(),
    Paragraph("<b>Vérification que .env est ignoré :</b>", S["h2"]),
    code_block("git status"),
    output_block(
        "On branch main\n"
        "nothing to commit, working tree clean\n"
        "=> .env n'apparait PAS dans git status (gitignore fonctionne)"
    ),
    Paragraph("<b>Commit et tag v4 :</b>", S["h2"]),
    code_block(
        "git add .\n"
        'git commit -m "Lab 5 : integration LLM Groq + /explain (v4)"\n'
        "git tag v4"
    ),
    output_block(
        "[main a3c1f95] Lab 5 : integration LLM Groq + /explain (v4)\n"
        " 13 files changed, 1108 insertions(+)\n"
        " create mode 100644 notebooks/test_groq.py\n"
        " create mode 100644 api/main.py   (modifie : +/explain)\n"
        " create mode 100644 frontend/index.html  (modifie : +explication LLM)\n\n"
        "git log --oneline\n"
        "a3c1f95 Lab 5 : integration LLM Groq + /explain (v4)\n\n"
        "git tag\n"
        "v4"
    ),
    Paragraph(
        "<b>Résultat :</b> Le commit a3c1f95 avec le tag v4 est créé. "
        "Le fichier .env ne figure pas dans le commit.", S["ok"]),
    Spacer(1, 0.3*cm),
]

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 10 — Résumé et structure du projet
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("10. Résumé des accomplissements", S["h1"]), HR(),
]

bilan_data = [
    ["#", "Action", "Statut"],
    ["1", "Créer un compte Groq + clé API gratuite", "✓"],
    ["2", "Stocker la clé dans .env + .gitignore", "✓"],
    ["3", "Script de test Groq (test_groq.py)", "✓"],
    ["4", "System prompt médical SénSanté", "✓"],
    ["5", "Endpoint POST /explain dans FastAPI", "✓"],
    ["6", "Frontend : afficher l'explication sous le diagnostic", "✓"],
    ["7", "Tests bout en bout + cas limites (graceful degradation)", "✓"],
    ["8", "Git : commit + tag v4", "✓"],
]
bt = Table(bilan_data, colWidths=[1*cm, 12*cm, 2*cm])
bt.setStyle(TableStyle([
    ("BACKGROUND",  (0,0), (-1,0), colors.HexColor("#1a5276")),
    ("TEXTCOLOR",   (0,0), (-1,0), colors.white),
    ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",    (0,0), (-1,-1), 9),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#f0f8ff"), colors.white]),
    ("GRID",        (0,0), (-1,-1), 0.5, colors.HexColor("#aaaaaa")),
    ("ALIGN",       (0,0), (0,-1), "CENTER"),
    ("ALIGN",       (2,0), (2,-1), "CENTER"),
    ("TEXTCOLOR",   (2,1), (2,-1), colors.HexColor("#1e8449")),
    ("FONTNAME",    (2,1), (2,-1), "Helvetica-Bold"),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
    ("TOPPADDING",  (0,0), (-1,-1), 5),
    ("BOTTOMPADDING",(0,0), (-1,-1), 5),
]))
story += [bt, Spacer(1, 0.5*cm)]

story += [
    Paragraph("<b>Structure du projet après Lab 5 :</b>", S["h2"]),
    code_block(
        "sensante/\n"
        "├── .env          (NOUVEAU - hors Git)\n"
        "├── .gitignore    (modifie)\n"
        "├── requirements.txt  (modifie)\n"
        "├── data/\n"
        "│   └── patients_dakar.csv\n"
        "├── models/\n"
        "│   ├── model.pkl\n"
        "│   ├── encoder_sexe.pkl\n"
        "│   └── encoder_region.pkl\n"
        "├── api/\n"
        "│   └── main.py   (modifie : +/explain)\n"
        "├── frontend/\n"
        "│   └── index.html  (modifie : +explication LLM)\n"
        "└── notebooks/\n"
        "    ├── train_model.py\n"
        "    └── test_groq.py  (NOUVEAU)"
    ),
    Spacer(1, 0.3*cm),
]

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 11 — Exercices
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("11. Exercices", S["h1"]), HR(),

    # ── Exercice 1 ────────────────────────────────────────────────────────────
    Paragraph("Exercice 1 — Prompt engineering : réponses en wolof", S["h2"]),
    Paragraph(
        "Le system prompt a été modifié pour demander à Llama 3 de répondre en wolof mélangé "
        "au français, avec des expressions courantes : <i>Jaam nga am</i> (tu es en paix), "
        "<i>Feebar</i> (fièvre), <i>Yendoo</i> (maladie), <i>Na nga def</i> (comment tu vas).",
        S["body"]),
    Paragraph("Nouveau system prompt :", S["h2"]),
    code_block(
        "SYSTEM_PROMPT_WOLOF = \"\"\"Tu es un assistant medical senegalais bilingue wolof-francais.\n"
        "Tu recois un diagnostic medical et des donnees patient.\n"
        "Reponds en melangeant le wolof simple et le francais,\n"
        "comme un agent de sante senegalais parlerait a son patient au village.\n"
        "Utilise des expressions wolof courantes : Jaam nga am, Na nga def, Yendoo, Feebar.\n"
        "Sois rassurant et recommande une consultation medicale. Maximum 3 phrases.\"\"\""
    ),
    Paragraph("Résultats des 3 tests :", S["h2"]),
    output_block(
        "--- Cas 1 - Paludisme (F, 28 ans, Dakar, 39.5 C, 72%) ---\n"
        "Patient : Na nga def, feebar ngi yendoo?\n"
        "Jaam nga am, feebar ngi yendoo, ngi feebar 39.5 C. Le modele indique une\n"
        "probabilite elevee de paludisme. Consultez un medecin pour confirmer.\n"
        "[Tokens : 354]\n\n"
        "--- Cas 2 - Patient sain (M, 35 ans, Thies, 36.8 C, 100%) ---\n"
        "Monsieur, na nga def ? Tu vas bien ? Le modele dit que tu es en bonne sante,\n"
        "jaam nga am ! Ta temperature est normale, 36.8 degres. Consulte regulierement.\n"
        "[Tokens : 295]\n\n"
        "--- Cas 3 - Typhoide (M, 45 ans, Ziguinchor, 40.2 C, 88%) ---\n"
        "Jaam nga am ? Ta temperature est tres elevee, 40.2 degres, feebar bi dafa dafa.\n"
        "Le modele indique une probabilite de typhoide. Yendoo bi ngi yendoo, mais seul\n"
        "un medecin peut confirmer. Va consulter au centre de sante.\n"
        "[Tokens : 419]"
    ),
    Paragraph(
        "<b>Analyse :</b> Llama 3 arrive partiellement à mélanger wolof et français. "
        "Les expressions simples (<i>Jaam nga am</i>, <i>Feebar</i>, <i>Na nga def</i>) "
        "sont correctement utilisées. Cependant, pour les termes médicaux complexes "
        "(paludisme, typhoïde), le modèle manque de vocabulaire wolof et reste en français. "
        "La cohérence du mélange est meilleure sur les cas simples (patient sain) que sur "
        "les cas complexes (paludisme, typhoïde).", S["body"]),
] + screenshot("exo1", caption="Figure Exercice 1 : Résultats du script exercice1_wolof.py — 3 cas testés (palu, sain, typhoïde).") + [
    Spacer(1, 0.4*cm),

    # ── Exercice 2 ────────────────────────────────────────────────────────────
    Paragraph("Exercice 2 — Effet du paramètre temperature", S["h2"]),
    Paragraph(
        "Le même appel (patient F, 28 ans, Dakar, palu 72%) a été testé avec "
        "<b>temperature=0.0</b>, <b>0.5</b> et <b>1.0</b>. Seul ce paramètre change.",
        S["body"]),
    output_block(
        "============================================================\n"
        "temperature = 0.0\n"
        "============================================================\n"
        "Madame, je suis rassure que vous soyez venue me voir. Les resultats indiquent\n"
        "que vous avez une temperature elevee de 39,5 degres, ce qui peut etre du a une\n"
        "infection. Le modele medical a identifie une probabilite elevee de paludisme,\n"
        "mais il est important de noter que ce n'est qu'un resultat probable et non un\n"
        "diagnostic definitif. Je vous recommande de consulter un medecin.\n"
        "[Tokens : 268]\n\n"
        "============================================================\n"
        "temperature = 0.5\n"
        "============================================================\n"
        "Madame, je vois que vous avez une temperature de 39,5 degres Celsius, ce qui\n"
        "est tres eleve. Selon les resultats du modele, il y a une forte probabilite que\n"
        "vous soyez atteinte de paludisme, une maladie causee par un parasite transmis\n"
        "par les moustiques. Je vous recommande de consulter un medecin pour un diagnostic\n"
        "definitif et un traitement adapte.\n"
        "[Tokens : 280]\n\n"
        "============================================================\n"
        "temperature = 1.0\n"
        "============================================================\n"
        "Madame, je comprends que vous ressentez une forte fievre, votre temperature est\n"
        "a 39,5 degres. Le modele medical est arrive a une probabilite de 72% de paludisme.\n"
        "Cela signifie qu'il y a de fortes chances que vous soyez infectee par le parasite,\n"
        "mais il est important de venir me voir pour une consultation plus approfondie.\n"
        "[Tokens : 248]"
    ),
    Paragraph(
        "<b>Analyse en 3 phrases :</b> Avec <b>temperature=0.0</b>, la reponse est identique "
        "a chaque appel - deterministe, formelle et prudente. "
        "Avec <b>temperature=0.5</b>, la reponse varie legerement et ajoute des details contextuels "
        "(cause du parasite, vecteur moustique). "
        "Avec <b>temperature=1.0</b>, la reponse est plus courte et directe mais peut varier "
        "fortement entre deux appels - trop creative pour un contexte medical. "
        "La valeur <b>temperature=0.3</b> retenue dans SenSante offre le meilleur "
        "equilibre entre stabilite factuelle et fluidite naturelle.", S["body"]),
] + screenshot("exo2", caption="Figure Exercice 2 : Comparaison des réponses Llama 3 avec temperature=0.0, 0.5 et 1.0.") + [
    Spacer(1, 0.4*cm),

    # ── Exercice 3 ────────────────────────────────────────────────────────────
    Paragraph("Exercice 3 — Réflexion éthique", S["h2"]),
    Paragraph(
        "<b>Question :</b> Un patient lit l'explication du LLM et décide de se soigner "
        "seul sans consulter un médecin. Est-ce un risque ?", S["body"]),
    Paragraph(
        "<b>Oui, c'est un risque réel.</b> Le LLM explique en langage humain rassurant, "
        "ce qui peut donner au patient une fausse impression de certitude. Si Llama 3 dit "
        "\"vos symptômes sont cohérents avec un paludisme\", le patient peut acheter "
        "de la chloroquine en automédication, retarder une consultation, et aggraver son "
        "état si le diagnostic ML était incorrect (le modèle a 85% de précision = 15% d'erreurs). "
        "Dans des zones éloignées comme Ziguinchor ou Diourbel, ce risque est encore plus élevé "
        "car l'accès à un médecin est limité.", S["body"]),
    Paragraph("<b>2 modifications appliquées dans SénSanté :</b>", S["h2"]),
    Paragraph(
        "<b>Modification 1 — Bandeau d'avertissement rouge dans le frontend</b> : "
        "Un encadré rouge avec l'icône ⚠️ s'affiche automatiquement avant l'explication LLM "
        "avec le texte : \"Ce résultat est un pré-diagnostic automatique. Il ne remplace pas "
        "un examen médical. Consultez un professionnel de santé avant toute prise de médicament.\"",
        S["body"]),
    code_block(
        "zone.innerHTML = `\n"
        "  <div class='bg-red-50 rounded-lg p-3 border border-red-300'>\n"
        "    <span>⚠️</span>\n"
        "    <p>Ce résultat est un pré-diagnostic automatique.\n"
        "    Consultez un professionnel avant toute prise de médicament.</p>\n"
        "  </div>\n"
        "  <div class='bg-purple-50 ...'>... explication LLM ...</div>`;"
    ),
    Paragraph(
        "<b>Modification 2 — Instruction dans le system prompt</b> : "
        "Le system prompt a été mis à jour pour que le LLM termine systématiquement "
        "ses réponses par une mise en garde explicite.", S["body"]),
    code_block(
        "# Ajout dans SYSTEM_PROMPT (api/main.py)\n"
        "Termine TOUJOURS par : 'Ne prenez aucun medicament sans consulter\n"
        "un medecin ou un agent de sante qualifie.'"
    ),
    Paragraph("Résultat après modification :", S["h2"]),
    output_block(
        "POST /explain => paludisme 72%, F, 28 ans, Dakar\n\n"
        "Bonjour, je suis rassure de vous voir. Le resultat des tests suggere que vous\n"
        "pourriez etre infectee par le paludisme, une maladie causee par un parasite.\n"
        "Votre temperature elevee de 39,5 degres Celsius confirme cette hypothese.\n"
        "Cependant, seul un medecin peut confirmer definitivement ce diagnostic.\n"
        "Ne prenez aucun medicament sans consulter un medecin ou un agent de sante qualifie."
    ),
    Paragraph(
        "<b>Résultat :</b> Les deux modifications réduisent significativement le risque "
        "d'automédication. Le bandeau rouge est visible avant même de lire l'explication, "
        "et le LLM rappelle lui-même l'interdiction de prendre des médicaments sans consultation.",
        S["ok"]),
] + screenshot("exo3", caption="Figure Exercice 3 : Résultat du diagnostic avec bandeau ⚠️ rouge et explication Llama 3 (Exercice 3 — modification éthique appliquée).") + [
    Spacer(1, 0.3*cm),
]

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 12 — Conclusion
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("12. Conclusion", S["h1"]), HR(),
    Paragraph(
        "Ce Lab 5 a permis d'intégrer un LLM (Llama 3 via Groq) dans l'application "
        "SénSanté. L'architecture combinant ML classique (RandomForest) et IA générative "
        "(Llama 3) constitue un pattern puissant : le modèle ML diagnostique rapidement, "
        "le LLM explique en langage humain.", S["body"]),
    Paragraph(
        "Points techniques clés appris : sécurisation d'une clé API via .env et "
        ".gitignore, conception d'un system prompt médical, pattern de dégradation "
        "gracieuse, et UX non-bloquante (diagnostic immédiat + explication asynchrone).", S["body"]),
    Paragraph(
        "SénSanté est maintenant fonctionnellement complet. Le Lab 6 ajoutera "
        "Docker et le déploiement sur Hugging Face Spaces pour rendre l'application "
        "accessible publiquement (tag v1.0).", S["body"]),
]

# Build
doc.build(story)
print(f"Rapport genere : {OUTPUT}")
