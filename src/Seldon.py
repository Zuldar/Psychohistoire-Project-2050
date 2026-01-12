import json
import os
import random
from datetime import datetime

# --- 1. CONFIGURATION ---
# Chemins des fichiers (relatifs à la racine du projet)
HISTORY_FILE = 'data/history_full.json'
CURRENT_STATE_FILE = 'data/current_state.json'
RECENT_HISTORY_FILE = 'data/recent_history.json'
PROJECTION_FILE = 'data/projection_2036.json'

# Poids des piliers
WEIGHTS = {
    "technologie_ia": 1.5, "environnement": 1.2, "energie": 1.0,
    "geopolitique": 1.3, "demographie_social": 1.0, "finance": 1.1,
    "sante_bio": 1.0, "espace": 0.8, "information": 0.9
}

# Vocabulaire Seldonien
SELDON_TERMS = {
    "energie": "l'épuisement énergétique", "environnement": "l'entropie climatique",
    "espace": "la stagnation exosphérique", "demographie_social": "la dissonance sociale",
    "sante_bio": "la dégradation biologique", "geopolitique": "l'instabilité géopolitique",
    "technologie_ia": "la variance technologique", "finance": "l'effondrement économique",
    "information": "la corruption de la noosphère"
}

# --- 2. GÉNÉRATEUR D'HISTOIRE (1900-2025) ---
# Cette fonction se lance toute seule si le fichier d'histoire n'existe pas
def generate_full_history():
    print("📜 CRÉATION DES ARCHIVES (1900-2025)...")
    history = []
    
    # Dates clés et scores approximatifs
    key_events = {
        1900: 60, 1914: 30, 1918: 25, 1929: 20, 
        1939: 15, 1945: 10, 1969: 75, 1989: 65, 
        2001: 50, 2008: 40, 2020: 35, 2025: 45
    }

    current_val = key_events[1900]
    
    for year in range(1900, 2026):
        # Interpolation simple pour relier les dates clés
        if year in key_events:
            current_val = key_events[year]
        else:
            # On cherche la prochaine date clé
            next_year = min([k for k in key_events if k > year], default=year)
            prev_year = max([k for k in key_events if k < year], default=year)
            if next_year != prev_year:
                target = key_events[next_year]
                start = key_events[prev_year]
                progress = (year - prev_year) / (next_year - prev_year)
                current_val = start + (target - start) * progress
            
            # Ajout d'un peu de chaos aléatoire (+/- 3%)
            current_val += random.uniform(-3, 3)

        # Bornage
        current_val = max(5, min(98, current_val))
        
        # Génération des piliers
        pillars = {}
        for k in WEIGHTS:
            var = random.uniform(-8, 8)
            # Quelques ajustements historiques
            if year < 1940 and k == 'technologie_ia': var -= 20
            if year == 1929 and k == 'finance': var -= 30
            pillars[k] = max(5, min(100, current_val + var))

        history.append({
            "year": str(year),
            "stability_index": round(current_val),
            "pillars": pillars
        })
    
    # Sauvegarde du fichier géant
    os.makedirs('data', exist_ok=True) # Crée le dossier data s'il manque
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)
    
    return history

# --- 3. FONCTIONS UTILITAIRES ---

def load_json(filename):
    try:
        with open(filename, 'r') as f: return json.load(f)
    except FileNotFoundError: return None

def save_json(filename, data):
    os.makedirs('data', exist_ok=True)
    with open(filename, 'w') as f: json.dump(data, f, indent=4, ensure_ascii=False)

def calculate_stability(pillars):
    total = 0; weight_sum = 0
    for k, v in pillars.items():
        score = v['score'] if isinstance(v, dict) else v
        w = WEIGHTS.get(k, 1.0)
        total += score * w; weight_sum += w
    return round(total / weight_sum)

# --- 4. EXÉCUTION PRINCIPALE ---

def update_seldon():
    print("🔮 Démarrage Seldon Bot...")
    
    # A. GESTION DE L'HISTOIRE
    history = load_json(HISTORY_FILE)
    if not history:
        # C'est ici que la magie opère : si pas de fichier, on le crée !
        history = generate_full_history()
    
    # B. CHARGEMENT ÉTAT ACTUEL
    current = load_json(CURRENT_STATE_FILE)
    if not current: 
        print("❌ Erreur: current_state.json introuvable.")
        return

    # C. MISE À JOUR DU SCORE
    new_score = calculate_stability(current['pillars'])
    current['stability_index'] = new_score
    current['date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # D. EXTRACTION DES ARCHIVES (CRISES PASSÉES)
    # On scanne l'histoire pour trouver les années < 35%
    past_crises = []
    last_crisis_year = 0
    for entry in history:
        yr = int(entry['year'])
        sc = entry['stability_index']
        if sc < 38: # Seuil de crise historique
            # Anti-doublon (pour pas avoir 1940, 1941, 1942...)
            if yr > last_crisis_year + 5: 
                past_crises.append({"year": str(yr), "score": sc})
                last_crisis_year = yr
    
    current['archives'] = past_crises # On injecte ça dans le fichier lu par le site

    # E. CRÉATION DU FICHIER "RÉCENT" (POUR LE GRAPHIQUE)
    # On ne garde que les 6 dernières années pour le zoom du graphique
    save_json(RECENT_HISTORY_FILE, history[-6:])

    # F. GÉNÉRATION DES ALERTES & PROPHÉTIES
    alerts = []
    stress_factors = []
    for k, v in current['pillars'].items():
        s = v['score'] if isinstance(v, dict) else v
        if k != 'technologie_ia' and s < 50: stress_factors.append((k, s))
        elif k == 'technologie_ia' and s > 85: stress_factors.append((k, s))
    stress_factors.sort(key=lambda x: x[1])

    # Prophecy Logic
    if len(stress_factors) >= 2:
        n1 = SELDON_TERMS.get(stress_factors[0][0], "facteur inconnu")
        n2 = SELDON_TERMS.get(stress_factors[1][0], "facteur inconnu")
        alerts.append(f"📅 2028 : Les équations indiquent une résonance critique entre {n1} et {n2}.")
    else:
        alerts.append("📅 2028 : Aucune convergence systémique immédiate détectée.")

    # Alertes classiques
    if current['pillars']['environnement']['score'] < 40: alerts.append("⚠️ Ω_BIOSPHERE : Seuil critique")
    if current['pillars']['geopolitique']['score'] < 35: alerts.append("⚔️ Σ_CONFLICT : Tensions maximales")
    if current['pillars']['technologie_ia']['score'] > 85: alerts.append("📈 Δ_SINGULARITY : Risque systémique")
    
    current['alerts'] = alerts
    save_json(CURRENT_STATE_FILE, current)

    # G. PROJECTIONS 2026-2036
    projections = { "optimiste": [], "tendantielle": [], "pessimiste": [] }
    for i in range(1, 11):
        y = str(2026 + i)
        drift = -0.5 * i
        base = max(0, min(100, new_score + drift))
        if i in [2, 3]: base -= 6 # Choc simulé en 2028
        
        projections["tendantielle"].append({ "year": y, "stability_index": round(base) })
        projections["optimiste"].append({ "year": y, "stability_index": round(min(98, base + i*1.5)) })
        projections["pessimiste"].append({ "year": y, "stability_index": round(max(5, base - i*2.0)) })
        
    save_json(PROJECTION_FILE, {"scenarios": projections})
    print("✅ Tout est mis à jour : Histoire, Archives, Graphique et Alertes.")

if __name__ == "__main__":
    update_seldon()
    
