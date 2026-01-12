import json
import os
import random
from datetime import datetime

# --- CONFIGURATION ---
HISTORY_FILE = 'data/history_full.json'
CURRENT_STATE_FILE = 'data/current_state.json'
PROJECTION_FILE = 'data/projection_2036.json'

WEIGHTS = {
    "technologie_ia": 1.5, "environnement": 1.2, "energie": 1.0,
    "geopolitique": 1.3, "demographie_social": 1.0, "finance": 1.1,
    "sante_bio": 1.0, "espace": 0.8, "information": 0.9
}

SELDON_TERMS = {
    "energie": "l'épuisement énergétique", "environnement": "l'entropie climatique",
    "espace": "la stagnation exosphérique", "demographie_social": "la dissonance sociale",
    "sante_bio": "la dégradation biologique", "geopolitique": "l'instabilité géopolitique",
    "technologie_ia": "la variance technologique", "finance": "l'effondrement économique",
    "information": "la corruption de la noosphère"
}

# --- GÉNÉRATEUR D'HISTOIRE (1900-2025) ---
def generate_full_history():
    print("📜 Génération des archives 1900-2025...")
    history = []
    
    # Événements clés pour simuler la réalité
    key_events = {
        1914: 30, 1918: 25, # WWI
        1929: 20, # Krach
        1939: 15, 1945: 10, # WWII (Point bas)
        1969: 70, # Lune (Pic d'espoir)
        1991: 60, # Fin guerre froide
        2001: 50, # Dotcom/Terrorisme
        2008: 40, # Subprimes
        2020: 35, # Covid
    }

    base_score = 50
    for year in range(1900, 2026):
        str_year = str(year)
        
        # Si c'est une année clé, on force le score, sinon on évolue doucement
        if year in key_events:
            target = key_events[year]
            base_score = target
        else:
            # Légère variation aléatoire (drift)
            change = random.uniform(-2, 3)
            # On tend à remonter après une guerre
            if base_score < 40: change += 1
            base_score += change
            base_score = max(10, min(90, base_score))

        # Création des piliers fictifs pour cette année
        pillars = {k: base_score + random.uniform(-5, 5) for k in WEIGHTS.keys()}
        
        history.append({
            "year": str_year,
            "pillars": pillars,
            "stability_index": round(base_score)
        })
    
    # On sauvegarde
    os.makedirs('data', exist_ok=True)
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)
    return history

# --- FONCTIONS UTILITAIRES ---

def load_json(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def calculate_stability(pillars):
    total_score = 0; total_weight = 0
    for key, val in pillars.items():
        score = val['score'] if isinstance(val, dict) else val
        weight = WEIGHTS.get(key, 1.0)
        total_score += score * weight
        total_weight += weight
    return round(total_score / total_weight)

# --- COEUR DU SYSTÈME ---

def update_seldon():
    print("🔮 Seldon Bot Initialized...")
    
    # 1. Charger ou Créer l'Histoire
    history = load_json(HISTORY_FILE)
    if not history:
        history = generate_full_history()
    
    current = load_json(CURRENT_STATE_FILE)
    if not current: return

    # 2. Mise à jour du présent
    new_score = calculate_stability(current['pillars'])
    current['stability_index'] = new_score
    current['date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 3. Analyser les "Archives" (Trouver les crises passées)
    past_crises = []
    for entry in history:
        if entry['stability_index'] < 35: # Seuil de crise historique
            # On évite de spammer toutes les années d'une guerre (on prend le début ou le pire)
            if not past_crises or int(entry['year']) > int(past_crises[-1]['year']) + 5:
                past_crises.append({"year": entry['year'], "score": entry['stability_index']})
    
    # On ajoute ces archives au fichier current pour l'affichage
    current['archives'] = past_crises

    # 4. Préparer les données pour le Graphique (Seulement 2021-2025 + Present)
    # On prend les 5 derniers éléments de l'historique
    recent_history = history[-5:] 
    # On sauvegarde ça dans un fichier temporaire pour le JS (ou on l'injecte direct)
    save_json('data/recent_history.json', recent_history)

    # 5. Prophétie & Alertes (Code inchangé mais robuste)
    stress_factors = []
    for key, val in current['pillars'].items():
        score = val['score'] if isinstance(val, dict) else val
        if key != 'technologie_ia' and score < 50: stress_factors.append((key, score))
        elif key == 'technologie_ia' and score > 85: stress_factors.append((key, score))
    stress_factors.sort(key=lambda x: x[1])
    
    prophecy = ""
    if len(stress_factors) >= 2:
        c1 = SELDON_TERMS.get(stress_factors[0][0], "l'inconnu")
        c2 = SELDON_TERMS.get(stress_factors[1][0], "l'inconnu")
        prophecy = f"Les équations sont formelles : la résonance entre {c1} et {c2} atteint un seuil critique."
    else:
        prophecy = "Stabilité précaire détectée. Aucune convergence immédiate."

    alerts = []
    if current['pillars']['environnement']['score'] < 40: alerts.append("⚠️ Ω_BIOSPHERE : Seuil critique")
    if current['pillars']['geopolitique']['score'] < 35: alerts.append("⚔️ Σ_CONFLICT : Friction max")
    if current['pillars']['technologie_ia']['score'] > 85: alerts.append("📈 Δ_SINGULARITY : Variance exponentielle")
    
    alerts.append(f"📅 2028 : {prophecy}")
    current['alerts'] = alerts
    
    save_json(CURRENT_STATE_FILE, current)

    # 6. Projections (Futur)
    current_year = 2026
    projections = { "optimiste": [], "tendantielle": [], "pessimiste": [] }
    for i in range(1, 11): # 10 ans
        year = str(current_year + i)
        drift = -0.5 * i
        base = max(0, min(100, new_score + drift))
        if i in [2, 3]: base -= 5
        
        projections["tendantielle"].append({ "year": year, "stability_index": round(base) })
        projections["optimiste"].append({ "year": year, "stability_index": round(min(98, base + i*2)) })
        projections["pessimiste"].append({ "year": year, "stability_index": round(max(5, base - i*2)) })

    save_json(PROJECTION_FILE, {"scenarios": projections})
    print("✅ Mises à jour effectuées avec succès (Archives + Graphique).")

if __name__ == "__main__":
    update_seldon()
    
