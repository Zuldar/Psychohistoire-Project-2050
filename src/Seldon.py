import json
import os
import random
from datetime import datetime

# --- 1. CONFIGURATION ---
HISTORY_FILE = 'data/history_full_v3.json' 
CURRENT_STATE_FILE = 'data/current_state.json'
RECENT_HISTORY_FILE = 'data/recent_history.json'
PROJECTION_FILE = 'data/projection_2036.json'
MEMORY_FILE = 'data/bot_memory.json'
WEIGHTS_FILE = 'data/weights.json'

# Vocabulaire Seldonien (Phrasé pour les alertes)
SELDON_TERMS = {
    "energie": "l'Epuisement Energétique", 
    "environnement": "l'Entropie Climatique",
    "espace": "la Stagnation Exosphérique", 
    "demographie_social": "la Dissonance Sociale",
    "sante_bio": "la Dégradation Biologique", 
    "geopolitique": "la Friction Géopolitique",
    "technologie_ia": "la Variance Technologique", 
    "finance": "la Volatilité Economique",
    "information": "la Corruption de la Noosphère"
}

# Archives pour le bas de page (Le passé reste le passé)
HISTORICAL_EVENTS = {
    "1914": "Rupture de l'équilibre des alliances",
    "1918": "Effondrement démographique viral",
    "1929": "Dislocation des vecteurs de crédit",
    "1939": "Friction cinétique globale",
    "1945": "Entropie géopolitique maximale",
    "1962": "Tension nucléaire critique",
    "1973": "Choc des ressources fossiles",
    "2001": "Asymétrie sécuritaire globale",
    "2008": "Toxicité des actifs financiers",
    "2020": "Pandémie systémique de classe 4",
    "2022": "Retour de la guerre haute intensité"
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

# --- 4. GÉNÉRATEUR D'HISTOIRE ---
def generate_full_history():
    # ... (Code identique à la V33 pour la génération d'histoire) ...
    # Je le laisse pour qu'il régénère si besoin
    print("📜 CRÉATION DES ARCHIVES...")
    history = []
    base_scores = { 1900:60, 1914:30, 1925:65, 1929:45, 1939:20, 1945:10, 1960:60, 1973:65, 1990:70, 2008:50, 2020:45, 2025:45 }
    current_val = base_scores[1900]
    
    for year in range(1900, 2026):
        if year in base_scores: current_val = base_scores[year]
        else:
            next_y = min([k for k in base_scores if k > year], default=year)
            prev_y = max([k for k in base_scores if k < year], default=year)
            if next_y != prev_y:
                progress = (year - prev_y) / (next_y - prev_y)
                current_val = base_scores[prev_y] + (base_scores[next_y] - base_scores[prev_y]) * progress
            current_val += random.uniform(-2, 2)
        current_val = max(5, min(98, current_val))
        pillars = {}
        for k in SELDON_TERMS.keys():
            p_val = current_val + random.uniform(-10, 10)
            pillars[k] = max(5, min(100, p_val))

        # Injection des faiblesses historiques pour la cohérence
        if str(year) == "1929": pillars["finance"] = 15
        if str(year) == "1973": pillars["energie"] = 20
        if str(year) == "2008": pillars["finance"] = 35
        if str(year) == "2020": pillars["sante_bio"] = 30
        
        event_desc = HISTORICAL_EVENTS.get(str(year), "")
        history.append({ "year": str(year), "stability_index": round(current_val), "pillars": pillars, "description": event_desc })
    
    save_json(HISTORY_FILE, history)
    return history

# --- 5. EXÉCUTION ---
def update_seldon():
    print("🔮 Démarrage Seldon Bot V34 (Analyse Pure)...")
    weights = get_weights()

    # A. CHARGEMENT
    history = load_json(HISTORY_FILE)
    if not history: history = generate_full_history()
    current = load_json(CURRENT_STATE_FILE)
    if not current: return

    # B. SCORE
    new_score = calculate_stability(current['pillars'], weights)
    current['stability_index'] = new_score
    current['date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # C. AUTO-CORRECTION
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

    # D. DATE CRISE DYNAMIQUE
    current_year = 2026
    years_until_crisis = max(1, min(9, int((new_score - 25) / 5)))
    crisis_year = current_year + years_until_crisis

    # E. ARCHIVES
    past_crises = []
    for e in history:
        if e.get('description'):
            past_crises.append({"year": str(e['year']), "score": e['stability_index'], "desc": e['description']})
    current['archives'] = past_crises
    save_json(RECENT_HISTORY_FILE, history[-6:])

    # F. ALERTES SELDONIENNES (V34)
    alerts = []
    if divergence_msg: alerts.append(divergence_msg)
    
    # 1. Identifier les piliers faibles pour construire la phrase
    stress_factors = []
    for k, v in current['pillars'].items():
        s = v['score'] if isinstance(v, dict) else v
        stress_factors.append((k, s))
    
    # On trie du plus faible au plus fort
    stress_factors.sort(key=lambda x: x[1])
    
    # On prend les 2 pires
    worst_1 = stress_factors[0]
    worst_2 = stress_factors[1]
    
    term_1 = SELDON_TERMS.get(worst_1[0], "Facteur Inconnu")
    term_2 = SELDON_TERMS.get(worst_2[0], "Facteur Inconnu")
    
    # 2. Calcul du PSI (Probabilité de rupture)
    # Plus le score global est bas, plus la proba est haute.
    # Ex: Score 40 -> Psi 60%. Mais on ajoute un boost si les pires piliers sont vraiment bas.
    psi_base = 100 - new_score
    psi_boost = 0
    if worst_1[1] < 30: psi_boost += 10
    if worst_2[1] < 30: psi_boost += 10
    psi_total = min(99, psi_base + psi_boost)

    # 3. Construction de la Prophétie
    if new_score > 65:
         alerts.append("📅 HORIZON STABLE : Aucune convergence systémique immédiate.")
    else:
        # Phrase type : "2028 : La Dissonance Sociale catalyse l'Effondrement Economique (Ψ: 85%)"
        seldon_prophecy = f"📅 {crisis_year} : {term_1} catalyse {term_2}. Probabilité de rupture de la chaîne causale : {psi_total}%."
        alerts.append(seldon_prophecy)

    if current['pillars']['environnement']['score'] < 40: alerts.append("⚠️ Ω_BIOSPHERE : Seuil critique atteint")
    if current['pillars']['geopolitique']['score'] < 35: alerts.append("⚔️ Σ_CONFLICT : Tensions maximales")
    
    current['alerts'] = alerts
    save_json(CURRENT_STATE_FILE, current)

    # G. PROJECTIONS
    projections = { "optimiste": [], "tendantielle": [], "pessimiste": [] }
    uncertainty = (100 - current.get('model_accuracy', 100)) / 5
    for i in range(1, 11):
        y = int(current_year + i)
        drift = -0.5 * i
        base = max(0, min(100, new_score + drift))
        if y == crisis_year: base -= 10
        elif y == crisis_year + 1: base -= 5
        projections["tendantielle"].append({ "year": str(y), "stability_index": round(base) })
        projections["optimiste"].append({ "year": str(y), "stability_index": round(min(98, base + i*(1.5 + uncertainty))) })
        projections["pessimiste"].append({ "year": str(y), "stability_index": round(max(5, base - i*(2.0 + uncertainty))) })
        
    save_json(PROJECTION_FILE, {"scenarios": projections})
    print("✅ Seldon V34 terminé.")

if __name__ == "__main__":
    update_seldon()
    
