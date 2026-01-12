import json
import os
import random
from datetime import datetime

# --- 1. CONFIGURATION ---
# Changement de nom pour forcer la régénération propre avec les textes
HISTORY_FILE = 'data/history_full_v2.json' 
CURRENT_STATE_FILE = 'data/current_state.json'
RECENT_HISTORY_FILE = 'data/recent_history.json'
PROJECTION_FILE = 'data/projection_2036.json'
MEMORY_FILE = 'data/bot_memory.json'
WEIGHTS_FILE = 'data/weights.json'

# Vocabulaire Seldonien (Futur)
SELDON_TERMS = {
    "energie": "l'épuisement énergétique", "environnement": "l'entropie climatique",
    "espace": "la stagnation exosphérique", "demographie_social": "la dissonance sociale",
    "sante_bio": "la dégradation biologique", "geopolitique": "l'instabilité géopolitique",
    "technologie_ia": "la variance technologique", "finance": "l'effondrement économique",
    "information": "la corruption de la noosphère"
}

# ARCHIVES HISTORIQUES (Passé) - NOUVEAU !
HISTORICAL_EVENTS = {
    "1914": "Rupture de l'équilibre des alliances (Guerre Totale)",
    "1918": "Effondrement démographique viral (Grippe Espagnole)",
    "1929": "Dislocation des vecteurs de crédit (Grande Dépression)",
    "1939": "Friction cinétique globale (Conflit Majeur)",
    "1945": "Entropie géopolitique maximale (Point Zéro)",
    "1962": "Tension nucléaire critique (Crise des Missiles)",
    "1973": "Choc des ressources fossiles (Crise Pétrolière)",
    "2001": "Asymétrie sécuritaire globale (Choc Terroriste)",
    "2008": "Toxicité des actifs financiers (Subprimes)",
    "2020": "Pandémie systémique de classe 4 (Covid-19)",
    "2022": "Retour de la guerre haute intensité (Ukraine)"
}

# --- 2. GESTION DES POIDS ---

def get_weights():
    if os.path.exists(WEIGHTS_FILE):
        with open(WEIGHTS_FILE, 'r') as f: return json.load(f)
    default_weights = {
        "technologie_ia": 1.5, "environnement": 1.2, "energie": 1.0,
        "geopolitique": 1.3, "demographie_social": 1.0, "finance": 1.1,
        "sante_bio": 1.0, "espace": 0.8, "information": 0.9
    }
    save_json(WEIGHTS_FILE, default_weights)
    return default_weights

def recalibrate_weights(current_score, predicted_score, current_pillars):
    weights = get_weights()
    delta = current_score - predicted_score
    if abs(delta) < 5: return weights, False
    
    print(f"🧠 RECALIBRATION (Delta: {delta})")
    if delta < 0: # Trop optimiste
        weakest = min(current_pillars, key=lambda k: current_pillars[k]['score'] if isinstance(current_pillars[k], dict) else current_pillars[k])
        weights[weakest] = round(weights[weakest] + 0.1, 2)
    else: # Trop pessimiste
        strongest = max(current_pillars, key=lambda k: current_pillars[k]['score'] if isinstance(current_pillars[k], dict) else current_pillars[k])
        weights[strongest] = round(weights[strongest] + 0.1, 2)
    save_json(WEIGHTS_FILE, weights)
    return weights, True

# --- 3. UTILITAIRES ---
def load_json(filename):
    try:
        with open(filename, 'r') as f: return json.load(f)
    except FileNotFoundError: return None

def save_json(filename, data):
    os.makedirs('data', exist_ok=True)
    with open(filename, 'w') as f: json.dump(data, f, indent=4, ensure_ascii=False)

def calculate_stability(pillars, weights):
    total = 0; weight_sum = 0
    for k, v in pillars.items():
        score = v['score'] if isinstance(v, dict) else v
        w = weights.get(k, 1.0)
        total += score * w; weight_sum += w
    return round(total / weight_sum)

# --- 4. GÉNÉRATEUR D'HISTOIRE (V31 - NARRATIF) ---
def generate_full_history():
    print("📜 CRÉATION DES ARCHIVES NARRATIVES (1900-2025)...")
    history = []
    # Dates clés (Score)
    key_scores = { 
        1900:60, 1914:30, 1918:25, 1929:20, 1939:15, 1945:10, 
        1962:40, 1969:75, 1989:65, 2001:50, 2008:40, 2020:35, 2025:45 
    }
    current_val = key_scores[1900]
    
    for year in range(1900, 2026):
        # Calcul du score (Interpolation)
        if year in key_scores: current_val = key_scores[year]
        else:
            next_y = min([k for k in key_scores if k > year], default=year)
            prev_y = max([k for k in key_scores if k < year], default=year)
            if next_y != prev_y:
                progress = (year - prev_y) / (next_y - prev_y)
                current_val = key_scores[prev_y] + (key_scores[next_y] - key_scores[prev_y]) * progress
            current_val += random.uniform(-2, 2)
        
        current_val = max(5, min(98, current_val))
        
        # Piliers
        pillars = {}
        for k in SELDON_TERMS.keys():
            var = random.uniform(-8, 8)
            if year < 1940 and k == 'technologie_ia': var -= 20
            if year == 1929 and k == 'finance': var -= 30
            pillars[k] = max(5, min(100, current_val + var))

        # NOUVEAU : Ajout de la description textuelle si elle existe
        event_desc = HISTORICAL_EVENTS.get(str(year), "")
        
        history.append({ 
            "year": str(year), 
            "stability_index": round(current_val), 
            "pillars": pillars,
            "description": event_desc # Champ ajouté
        })
    
    save_json(HISTORY_FILE, history)
    return history

# --- 5. EXÉCUTION ---
def update_seldon():
    print("🔮 Démarrage Seldon Bot V31...")
    weights = get_weights()

    # A. HISTOIRE
    history = load_json(HISTORY_FILE)
    if not history: history = generate_full_history()
    
    # B. CURRENT
    current = load_json(CURRENT_STATE_FILE)
    if not current: return

    # C. SCORE
    new_score = calculate_stability(current['pillars'], weights)
    current['stability_index'] = new_score
    current['date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # D. AUTO-CORRECTION
    memory = load_json(MEMORY_FILE) or { "last_run_date": None, "predicted_score_for_today": None, "accuracy_history": [] }
    accuracy = 100
    divergence_msg = None
    was_recalibrated = False

    if memory.get("predicted_score_for_today"):
        predicted = memory["predicted_score_for_today"]
        delta = abs(new_score - predicted)
        accuracy = max(0, 100 - (delta * 3))
        memory["accuracy_history"].append(accuracy)
        if len(memory["accuracy_history"]) > 10: memory["accuracy_history"].pop(0)
        avg_acc = int(sum(memory["accuracy_history"]) / len(memory["accuracy_history"]))
        weights, was_recalibrated = recalibrate_weights(new_score, predicted, current['pillars'])
        if delta > 8: divergence_msg = f"⚠️ DIVERGENCE SELDON (Delta: {delta})"
        if was_recalibrated: divergence_msg = "🔧 PROTOCOLE DE RECALIBRATION ACTIVÉ"
        current['model_accuracy'] = avg_acc
    else: current['model_accuracy'] = 100

    memory["predicted_score_for_today"] = new_score + random.choice([-1, 0, 1])
    save_json(MEMORY_FILE, memory)

    # E. ARCHIVES (AVEC TEXTES)
    past_crises = []
    # On force l'ajout des années clés définies dans HISTORICAL_EVENTS
    # + les années où le score est très bas, même sans texte
    for e in history:
        yr = str(e['year'])
        # Si c'est une année avec un événement nommé
        if e.get('description'):
            past_crises.append({"year": yr, "score": e['stability_index'], "desc": e['description']})
        # Sinon, si c'est une crise grave non nommée (pour combler les trous)
        elif e['stability_index'] < 30:
            # On vérifie qu'on n'a pas déjà ajouté une année très proche (anti-doublon)
            if not past_crises or int(yr) > int(past_crises[-1]['year']) + 5:
                past_crises.append({"year": yr, "score": e['stability_index'], "desc": "Instabilité systémique critique"})

    current['archives'] = past_crises
    save_json(RECENT_HISTORY_FILE, history[-6:])

    # F. ALERTES
    alerts = []
    if divergence_msg: alerts.append(divergence_msg)
    stress_factors = []
    for k, v in current['pillars'].items():
        s = v['score'] if isinstance(v, dict) else v
        if k != 'technologie_ia' and s < 50: stress_factors.append((k, s))
        elif k == 'technologie_ia' and s > 85: stress_factors.append((k, s))
    stress_factors.sort(key=lambda x: x[1])

    if len(stress_factors) >= 2:
        n1 = SELDON_TERMS.get(stress_factors[0][0], "X")
        n2 = SELDON_TERMS.get(stress_factors[1][0], "Y")
        alerts.append(f"📅 2028 : Les équations indiquent une résonance critique entre {n1} et {n2}.")
    else: alerts.append("📅 2028 : Aucune convergence systémique immédiate.")

    if current['pillars']['environnement']['score'] < 40: alerts.append("⚠️ Ω_BIOSPHERE : Seuil critique")
    if current['pillars']['geopolitique']['score'] < 35: alerts.append("⚔️ Σ_CONFLICT : Tensions maximales")
    
    current['alerts'] = alerts
    save_json(CURRENT_STATE_FILE, current)

    # G. PROJECTIONS
    projections = { "optimiste": [], "tendantielle": [], "pessimiste": [] }
    uncertainty = (100 - current.get('model_accuracy', 100)) / 5
    for i in range(1, 11):
        y = str(2026 + i)
        drift = -0.5 * i
        base = max(0, min(100, new_score + drift))
        if i in [2, 3]: base -= 6
        projections["tendantielle"].append({ "year": y, "stability_index": round(base) })
        projections["optimiste"].append({ "year": y, "stability_index": round(min(98, base + i*(1.5 + uncertainty))) })
        projections["pessimiste"].append({ "year": y, "stability_index": round(max(5, base - i*(2.0 + uncertainty))) })
        
    save_json(PROJECTION_FILE, {"scenarios": projections})
    print("✅ Seldon V31 terminé.")

if __name__ == "__main__":
    update_seldon()
    
