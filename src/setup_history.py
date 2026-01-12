import json
import os
import random

# --- CONFIGURATION ---
OUTPUT_FILE = 'data/history_full.json'

# Poids des piliers (identique au bot principal pour la cohérence)
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

def generate_history():
    print("📜 Initialisation des Archives du Radiant (1900-2025)...")
    
    history = []
    
    # ÉVÉNEMENTS CLÉS (Points de repère pour la courbe)
    # Le script va "lisser" les valeurs entre ces dates
    key_events = {
        1900: 60, # Belle Époque
        1914: 30, # WWI (Début)
        1918: 25, # WWI (Fin/Grippe Espagnole)
        1925: 55, # Années Folles
        1929: 20, # Krach Boursier
        1933: 25, # Montée des périls
        1939: 15, # WWII (Début)
        1945: 10, # WWII (Fin / Point le plus bas)
        1950: 45, # Reconstruction
        1969: 75, # Conquête de la Lune (Optimisme max)
        1973: 60, # Choc Pétrolier
        1989: 65, # Chute du Mur
        2001: 50, # 11 Septembre / Bulle Internet
        2008: 40, # Crise Subprimes
        2015: 55, # Accalmie relative
        2020: 35, # Pandémie COVID
        2025: 45  # Aujourd'hui (Incertitude)
    }

    current_score = key_events[1900]
    
    for year in range(1900, 2026):
        # 1. Calcul du Score Global
        if year in key_events:
            # Si c'est une année clé, on force le score
            target_score = key_events[year]
            current_score = target_score
        else:
            # Sinon, on évolue doucement vers la prochaine année clé connue
            # (Interpolation simple + un peu de bruit aléatoire)
            next_key_year = min([k for k in key_events.keys() if k > year], default=year)
            prev_key_year = max([k for k in key_events.keys() if k < year], default=year)
            
            if next_key_year != prev_key_year:
                # Calcul de la pente
                start_val = key_events[prev_key_year]
                end_val = key_events[next_key_year]
                progress = (year - prev_key_year) / (next_key_year - prev_key_year)
                
                # Valeur théorique lissée
                smooth_val = start_val + (end_val - start_val) * progress
                
                # On ajoute du "bruit" (aléatoire) pour faire vivant
                noise = random.uniform(-3, 3)
                current_score = smooth_val + noise
            
        # Bornage 0-100
        current_score = max(5, min(98, current_score))
        
        # 2. Génération des Piliers basés sur ce score global
        # Chaque pilier gravite autour du score global, mais avec sa propre "personnalité"
        pillars = {}
        for key in WEIGHTS.keys():
            variation = random.uniform(-10, 10)
            
            # Ajustements historiques spécifiques
            if year < 1945 and key == "technologie_ia": variation -= 20 # Pas d'IA avant 1945
            if year == 1929 and key == "finance": variation -= 30 # Krach spécifique
            if year == 2020 and key == "sante_bio": variation -= 25 # Covid spécifique
            
            p_score = current_score + variation
            pillars[key] = round(max(5, min(100, p_score)), 1)

        # Ajout à l'historique
        entry = {
            "year": str(year),
            "stability_index": round(current_score),
            "pillars": pillars
        }
        history.append(entry)

    # Sauvegarde
    os.makedirs('data', exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(history, f, indent=4)
        
    print(f"✅ Génération terminée : {len(history)} années archivées dans {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_his
tory()
