import json
import random
from datetime import datetime

# --- CONFIGURATION ---
# Facteurs d'influence (Poids des piliers)
WEIGHTS = {
    "technologie_ia": 1.5,      # L'IA accélère tout
    "environnement": 1.2,       # Le mur climatique
    "energie": 1.0,
    "geopolitique": 1.3,        # Facteur de chaos
    "demographie_social": 1.0,
    "finance": 1.1,
    "sante_bio": 1.0,
    "espace": 0.8,
    "information": 0.9
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
        json.dump(data, f, indent=4)

def calculate_stability(pillars):
    """Calcule l'index de stabilité global (0-100)"""
    total_score = 0
    total_weight = 0
    
    for key, val in pillars.items():
        # Gère si c'est un objet ou un int direct
        score = val['score'] if isinstance(val, dict) else val
        weight = WEIGHTS.get(key, 1.0)
        
        total_score += score * weight
        total_weight += weight
        
    return round(total_score / total_weight)

def analyze_trend(history):
    """Analyse simple de la tendance sur les 3 dernières années"""
    if len(history) < 2:
        return 0
    last = calculate_stability(history[-1]['pillars'])
    prev = calculate_stability(history[-2]['pillars'])
    return last - prev

def generate_projections(current_state, years=10):
    """
    Génère 3 scénarios (Optimiste, Tendantielle, Pessimiste)
    Basé sur la tendance actuelle + facteur chaos grandissant avec le temps
    """
    current_score = current_state['stability_index']
    current_year = 2026 # Année de départ de la projection
    
    # Structure de sortie
    projections = {
        "optimiste": [],
        "tendantielle": [],
        "pessimiste": []
    }
    
    # Simulation
    for i in range(1, years + 1):
        year = str(current_year + i)
        
        # Facteur d'incertitude (Le cône s'élargit avec le temps)
        uncertainty = i * 1.5 
        
        # 1. TENDANTIELLE (Baseline)
        # On suppose une légère dégradation cyclique (entropie) si rien ne change
        trend_drift = -0.5 * i 
        base_val = max(0, min(100, current_score + trend_drift))
        
        # Ajout d'une "Crise cyclique" autour de 2028-2029 (i=2 ou 3)
        if i in [2, 3]: 
            base_val -= 5 # Choc temporaire

        projections["tendantielle"].append({
            "year": year,
            "stability_index": round(base_val)
        })
        
        # 2. OPTIMISTE (Tech Salvation)
        # La technologie résout les problèmes + Sursaut conscience
        opti_val = base_val + (uncertainty * 1.2) + (i * 0.5)
        projections["optimiste"].append({
            "year": year,
            "stability_index": round(min(98, opti_val)) # Max 98%
        })
        
        # 3. PESSIMISTE (Collapse)
        # Effet domino négatif
        pess_val = base_val - (uncertainty * 1.5) - (i * 0.5)
        projections["pessimiste"].append({
            "year": year,
            "stability_index": round(max(5, pess_val)) # Min 5%
        })
        
    return {"scenarios": projections}

# --- MAIN EXECUTION ---

def update_seldon():
    print("🔮 Seldon Bot Initialized...")
    
    # 1. Charger l'état actuel et l'historique
    current = load_json('data/current_state.json')
    history = load_json('data/history_2020_2025.json')
    
    if not current:
        print("❌ Erreur: current_state.json introuvable")
        return

    # 2. Recalculer le score global actuel (au cas où)
    new_score = calculate_stability(current['pillars'])
    current['stability_index'] = new_score
    current['date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 3. Générer des alertes intelligentes
    alerts = []
    trend = analyze_trend(history)
    
    # Alertes basées sur les scores
    if current['pillars']['environnement']['score'] < 40:
        alerts.append("⚠️ CLIMAT : Point de bascule imminent")
    if current['pillars']['geopolitique']['score'] < 35:
        alerts.append("⚔️ GÉOPOLITIQUE : Risque de conflit majeur élevé")
    if current['pillars']['technologie_ia']['score'] > 85:
        alerts.append("📈 SINGULARITÉ : Accélération technologique critique")
    if current['pillars']['demographie_social']['score'] < 45:
        alerts.append("🔥 SOCIAL : Tensions civiles détectées")

    # Alerte Tendance
    if trend < -2:
        alerts.append("📉 DÉGRADATION RAPIDE DU SYSTÈME (-2% / an)")
    elif trend > 1:
        alerts.append("✅ RÉTABLISSEMENT PROGRESSIF")
        
    # Prédiction de crise (Hardcodée pour la narration Seldon)
    # Dans un vrai système IA, ceci viendrait d'un modèle prédictif complexe
    alerts.append("📅 2028 : Convergence des courbes de stress (Risque 88%)")

    current['alerts'] = alerts
    
    # 4. Sauvegarder l'état actuel mis à jour
    save_json('data/current_state.json', current)
    print(f"✅ État actuel mis à jour (Score: {new_score}%)")

    # 5. Générer et Sauvegarder les Projections (Le Trident)
    projections = generate_projections(current, years=10)
    save_json('data/projection_2036.json', projections)
    print("✅ Projections 2026-2036 générées (3 Scénarios)")

if __name__ == "__main__":
    update_seldon()
