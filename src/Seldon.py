import json
import os
import random
from datetime import datetime

# --- 1. CONFIGURATION ---
HISTORY_FILE = 'data/history_full.json'
CURRENT_STATE_FILE = 'data/current_state.json'
RECENT_HISTORY_FILE = 'data/recent_history.json'
PROJECTION_FILE = 'data/projection_2036.json'
MEMORY_FILE = 'data/bot_memory.json'
WEIGHTS_FILE = 'data/weights.json' # NOUVEAU : Le cerveau mutable

# Vocabulaire Seldonien
SELDON_TERMS = {
    "energie": "l'épuisement énergétique", "environnement": "l'entropie climatique",
    "espace": "la stagnation exosphérique", "demographie_social": "la dissonance sociale",
    "sante_bio": "la dégradation biologique", "geopolitique": "l'instabilité géopolitique",
    "technologie_ia": "la variance technologique", "finance": "l'effondrement économique",
    "information": "la corruption de la noosphère"
}

# --- 2. GESTION DES POIDS (AUTO-ADAPTATION) ---

def get_weights():
    # Si le fichier de poids existe, on le charge
    if os.path.exists(WEIGHTS_FILE):
        with open(WEIGHTS_FILE, 'r') as f:
            return json.load(f)
    
    # Sinon, on crée les poids par défaut
    default_weights = {
        "technologie_ia": 1.5, "environnement": 1.2, "energie": 1.0,
        "geopolitique": 1.3, "demographie_social": 1.0, "finance": 1.1,
        "sante_bio": 1.0, "espace": 0.8, "information": 0.9
    }
    save_json(WEIGHTS_FILE, default_weights)
    return default_weights

def recalibrate_weights(current_score, predicted_score, current_pillars):
    """
    C'est ici que le robot apprend.
    Si l'écart est trop grand, il modifie l'importance des piliers.
    """
    weights = get_weights()
    delta = current_score - predicted_score
    
    # Seuil d'apprentissage : on ne change rien si l'erreur est < 5 points
    if abs(delta) < 5:
        return weights, False

    print(f"🧠 RECALIBRATION REQUISE (Delta: {delta})")
    
    # Si Réalité < Prédiction (Le robot était trop optimiste)
    # -> Il faut donner plus de poids aux piliers qui vont mal (pour "voir" la crise venir)
    if delta < 0:
        # On trouve le pilier le plus faible actuellement
        weakest_pillar = min(current_pillars, key=lambda k: current_pillars[k]['score'] if isinstance(current_pillars[k], dict) else current_pillars[k])
        # On augmente son poids
        weights[weakest_pillar] = round(weights[weakest_pillar] + 0.1, 2)
        print(f"🔧 Ajustement : Importance de {weakest_pillar} augmentée à {weights[weakest_pillar]}")
    
    # Si Réalité > Prédiction (Le robot était trop pessimiste)
    # -> Il faut donner moins de poids au pilier le plus fort (il nous a trop rassuré ?)
    # Ou diminuer le poids du pilier qui plombait le score
    else:
        strongest_pillar = max(current_pillars, key=lambda k: current_pillars[k]['score'] if isinstance(current_pillars[k], dict) else current_pillars[k])
        # On augmente son poids (car c'est lui qui tire vers le haut, on l'a sous-estimé)
        weights[strongest_pillar] = round(weights[strongest_pillar] + 0.1, 2)
        print(f"🔧 Ajustement : Importance de {strongest_pillar} augmentée à {weights[strongest_pillar]}")

    save_json(WEIGHTS_FILE, weights)
    return weights, True

# --- 3. FONCTIONS UTILITAIRES ---

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

# --- 4. GÉNÉRATEUR D'HISTOIRE ---
def generate_full_history():
    print("📜 CRÉATION DES ARCHIVES (1900-2025)...")
    history = []
    key_events = { 1900:60, 1914:30, 1918:25, 1929:20, 1939:15, 1945:10, 1969:75, 1989:65, 2001:50, 2008:40, 2020:35, 2025:45 }
    current_val = key_events[1900]
    
    for year in range(1900, 2026):
        if year in key_events: current_val = key_events[year]
        else:
            next_y = min([k for k in key_events if k > year], default=year)
            prev_y = max([k for k in key_events if k < year], default=year)
            if next_y != prev_y:
                progress = (year - prev_y) / (next_y - prev_y)
                current_val = key_events[prev_y] + (key_events[next_y] - key_events[prev_y]) * progress
            current_val += random.uniform(-3, 3)

        current_val = max(5, min(98, current_val))
        pillars = {}
        for k in SELDON_TERMS.keys():
            var = random.uniform(-8, 8)
            if year < 1940 and k == 'technologie_ia': var -= 20
            if year == 1929 and k == 'finance': var -= 30
            pillars[k] = max(5, min(100, current_val + var))

        history.append({ "year": str(year), "stability_index": round(current_val), "pillars": pillars })
    
    save_json(HISTORY_FILE, history)
    return history

# --- 5. EXÉCUTION PRINCIPALE ---

def update_seldon():
    print("🔮 Démarrage Seldon Bot...")
    
    # 0. Charger les Poids (Le Cerveau)
    weights = get_weights()

    # A. HISTOIRE
    history = load_json(HISTORY_FILE)
    if not history: history = generate_full_history()
    
    # B. ÉTAT ACTUEL
    current = load_json(CURRENT_STATE_FILE)
    if not current: return

    # C. SCORE
    new_score = calculate_stability(current['pillars'], weights)
    current['stability_index'] = new_score
    current['date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # D. AUTO-CORRECTION & MÉMOIRE
    memory = load_json(MEMORY_FILE) or { "last_run_date": None, "predicted_score_for_today": None, "accuracy_history": [] }
    
    divergence_msg = None
    accuracy = 100
    was_recalibrated = False

    if memory.get("predicted_score_for_today"):
        predicted = memory["predicted_score_for_today"]
        delta = abs(new_score - predicted)
        accuracy = max(0, 100 - (delta * 3)) # Pénalité de précision
        
        memory["accuracy_history"].append(accuracy)
        if len(memory["accuracy_history"]) > 10: memory["accuracy_history"].pop(0)
        avg_acc = int(sum(memory["accuracy_history"]) / len(memory["accuracy_history"]))
        
        # --- C'EST ICI QUE LE ROBOT SE RÉAJUSTE SEUL ---
        weights, was_recalibrated = recalibrate_weights(new_score, predicted, current['pillars'])
        
        if delta > 8: divergence_msg = f"⚠️ DIVERGENCE SELDON (Delta: {delta})"
        if was_recalibrated: divergence_msg = "🔧 PROTOCOLE DE RECALIBRATION ACTIVÉ"

        current['model_accuracy'] = avg_acc
    else:
        current['model_accuracy'] = 100

    # Prédiction pour demain (pour la prochaine correction)
    memory["predicted_score_for_today"] = new_score + random.choice([-1, 0, 1])
    save_json(MEMORY_FILE, memory)

    # E. ARCHIVES & UI
    past_crises = []
    last_yr = 0
    for e in history:
        yr = int(e['year'])
        if e['stability_index'] < 38 and yr > last_yr + 5:
            past_crises.append({"year": str(yr), "score": e['stability_index']})
            last_yr = yr
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
        n1 = SELDON_TERMS.get(stress_factors[0][0], "facteur X")
        n2 = SELDON_TERMS.get(stress_factors[1][0], "facteur Y")
        alerts.append(f"📅 2028 : Les équations indiquent une résonance critique entre {n1} et {n2}.")
    else:
        alerts.append("📅 2028 : Aucune convergence systémique immédiate.")

    if current['pillars']['environnement']['score'] < 40: alerts.append("⚠️ Ω_BIOSPHERE : Seuil critique")
    if current['pillars']['geopolitique']['score'] < 35: alerts.append("⚔️ Σ_CONFLICT : Tensions maximales")
    
    current['alerts'] = alerts
    save_json(CURRENT_STATE_FILE, current)

    # G. PROJECTIONS
    projections = { "optimiste": [], "tendantielle": [], "pessimiste": [] }
    uncertainty = (100 - current.get('model_accuracy', 100)) / 5 # Plus on se trompe, plus le cône s'ouvre
    
    for i in range(1, 11):
        y = str(2026 + i)
        drift = -0.5 * i
        base = max(0, min(100, new_score + drift))
        if i in [2, 3]: base -= 6
        
        projections["tendantielle"].append({ "year": y, "stability_index": round(base) })
        projections["optimiste"].append({ "year": y, "stability_index": round(min(98, base + i*(1.5 + uncertainty))) })
        projections["pessimiste"].append({ "year": y, "stability_index": round(max(5, base - i*(2.0 + uncertainty))) })
        
    save_json(PROJECTION_FILE, {"scenarios": projections})
    print("✅ Cycle Seldon terminé. Poids recalibrés si nécessaire.")

if __name__ == "__main__":
    update_seldon()
    
