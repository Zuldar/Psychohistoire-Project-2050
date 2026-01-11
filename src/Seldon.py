import json
import random
from datetime import datetime

# --- CONFIGURATION ---
WEIGHTS = {
    "technologie_ia": 1.5,
    "environnement": 1.2,
    "energie": 1.0,
    "geopolitique": 1.3,
    "demographie_social": 1.0,
    "finance": 1.1,
    "sante_bio": 1.0,
    "espace": 0.8,
    "information": 0.9
}

# DICTIONNAIRE DE PHRASÉ SELDONIEN (Narratif)
SELDON_TERMS = {
    "energie": "l'épuisement énergétique",
    "environnement": "l'entropie climatique",
    "espace": "la stagnation exosphérique",
    "demographie_social": "la dissonance sociale",
    "sante_bio": "la dégradation biologique",
    "geopolitique": "l'instabilité géopolitique",
    "technologie_ia": "la variance technologique non-contrôlée",
    "finance": "l'effondrement des vecteurs économiques",
    "information": "la corruption de la noosphère"
}

# --- FONCTIONS ---

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
    total_score = 0
    total_weight = 0
    for key, val in pillars.items():
        score = val['score'] if isinstance(val, dict) else val
        weight = WEIGHTS.get(key, 1.0)
        total_score += score * weight
        total_weight += weight
    return round(total_score / total_weight)

def analyze_trend(history):
    if len(history) < 2: return 0
    last = calculate_stability(history[-1]['pillars'])
    prev = calculate_stability(history[-2]['pillars'])
    return last - prev

def generate_projections(current_state, years=10):
    current_score = current_state['stability_index']
    current_year = 2026
    projections = { "optimiste": [], "tendantielle": [], "pessimiste": [] }
    
    for i in range(1, years + 1):
        year = str(current_year + i)
        uncertainty = i * 1.5 
        
        # Tendantielle
        trend_drift = -0.5 * i 
        base_val = max(0, min(100, current_score + trend_drift))
        if i in [2, 3]: base_val -= 5 # Choc 2028
        projections["tendantielle"].append({ "year": year, "stability_index": round(base_val) })
        
        # Optimiste
        opti_val = base_val + (uncertainty * 1.2) + (i * 0.5)
        projections["optimiste"].append({ "year": year, "stability_index": round(min(98, opti_val)) })
        
        # Pessimiste
        pess_val = base_val - (uncertainty * 1.5) - (i * 0.5)
        projections["pessimiste"].append({ "year": year, "stability_index": round(max(5, pess_val)) })
        
    return {"scenarios": projections}

# --- MAIN EXECUTION ---

def update_seldon():
    print("🔮 Seldon Bot Initialized...")
    
    current = load_json('data/current_state.json')
    history = load_json('data/history_2020_2025.json')
    
    if not current: return

    # 1. Recalcul score
    new_score = calculate_stability(current['pillars'])
    current['stability_index'] = new_score
    current['date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 2. Construction de la phrase Prophétique
    stress_factors = []
    for key, val in current['pillars'].items():
        score = val['score'] if isinstance(val, dict) else val
        
        # On identifie les vecteurs de faiblesse
        if key != 'technologie_ia' and score < 50: # Seuil un peu relevé pour capter plus de causes
            stress_factors.append((key, score))
        elif key == 'technologie_ia' and score > 85:
            stress_factors.append((key, score))

    stress_factors.sort(key=lambda x: x[1]) # Les pires d'abord
    
    # On prend les 2 causes principales
    if len(stress_factors) >= 2:
        cause_1 = SELDON_TERMS.get(stress_factors[0][0], "l'inconnu")
        cause_2 = SELDON_TERMS.get(stress_factors[1][0], "l'inconnu")
        
        prophecy = f"Les équations du Radiant sont formelles : la résonance entre {cause_1} et {cause_2} atteint un seuil critique, rendant la rupture systémique mathématiquement inévitable."
    
    elif len(stress_factors) == 1:
        cause_1 = SELDON_TERMS.get(stress_factors[0][0], "l'inconnu")
        prophecy = f"Les équations du Radiant sont formelles : l'amplification exponentielle de {cause_1} mène à une asymptote de rupture inévitable."
    
    else:
        prophecy = "Les équations montrent une stabilité précaire, mais aucune convergence critique immédiate n'est détectée dans le Prime Radiant."

    # 3. Générer alertes
    alerts = []
    trend = analyze_trend(history)
    
    # Alertes secondaires (classiques)
    if current['pillars']['environnement']['score'] < 40: alerts.append("⚠️ Ω_BIOSPHERE : Seuil critique atteint")
    if current['pillars']['geopolitique']['score'] < 35: alerts.append("⚔️ Σ_CONFLICT : Friction tectonique max")
    if current['pillars']['technologie_ia']['score'] > 85: alerts.append("📈 Δ_SINGULARITY : Variance exponentielle")
    
    # LA PROPHÉTIE FINALE (Formatée pour le front-end)
    # Le format "📅 2028 :" permet au HTML de créer le badge doré
    alerts.append(f"📅 2028 : {prophecy}")

    current['alerts'] = alerts
    
    save_json('data/current_state.json', current)
    print(f"✅ Prophétie générée : {prophecy}")

    projections = generate_projections(current, years=10)
    save_json('data/projection_2036.json', projections)

if __name__ == "__main__":
    update_seldon()
    
