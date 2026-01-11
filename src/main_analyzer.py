import json
import os
import random
import copy
from datetime import datetime

# --- CONFIGURATION ---
HISTORY_FILE = 'data/history_2020_2025.json'
CURRENT_STATE_FILE = 'data/current_state.json'
PROJECTION_FILE = 'data/projection_2036.json' # Nouveau fichier
REPORT_DIR = 'reports'
REPORT_OUTPUT = os.path.join(REPORT_DIR, 'rapport_mensuel.md')

PILLARS = [
    "energie", "environnement", "espace",
    "demographie_social", "sante_bio", "geopolitique",
    "technologie_ia", "finance", "information"
]

class PsychohistoryModel:
    def __init__(self):
        self.history = self.load_json(HISTORY_FILE)
        
    def load_json(self, filepath):
        if not os.path.exists(filepath): return []
        with open(filepath, 'r', encoding='utf-8') as f: return json.load(f)

    def calculate_momentum(self, history_data, pillar_name):
        """Calcule la vitesse basée sur les 3 dernières années connues"""
        if len(history_data) < 3: return 0
        last_3 = history_data[-3:]
        try:
            scores = [year['pillars'][pillar_name]['score'] if 'score' in year['pillars'][pillar_name] else year['pillars'][pillar_name] for year in last_3]
            return (scores[2] - scores[0]) / 2
        except: return 0

    def apply_interdependencies(self, state):
        """Les Lois de la Psychohistoire (Version Simulation)"""
        # Loi 1 : Effondrement Climatique = Guerre + Crise Sociale
        if state['environnement'] < 20:
            state['geopolitique'] -= 2
            state['demographie_social'] -= 1.5

        # Loi 2 : Singularité IA = Chaos Social mais Boom Spatial
        if state['technologie_ia'] > 95:
            state['demographie_social'] -= 2 # Chômage de masse
            state['espace'] += 3             # Robots dans l'espace
            state['information'] -= 3        # On ne sait plus ce qui est vrai
            state['sante_bio'] += 2          # L'IA trouve des remèdes

        # Loi 3 : Boom Spatial = Energie infinie
        if state['espace'] > 90:
            state['energie'] += 2

        # Bornage 0-100
        for k in state: state[k] = max(0, min(100, state[k]))
        return state

    def simulate_future(self, start_state):
        print("--- Démarrage Simulation 2026-2036 ---")
        future_timeline = []
        
        # On clone l'état de départ pour ne pas le modifier
        current_sim_state = copy.deepcopy(start_state)
        
        # On simule 10 ans
        for year in range(2027, 2037):
            next_step = {}
            for pillar in PILLARS:
                # 1. Inertie (Momentum)
                momentum = self.calculate_momentum(self.history, pillar)
                # On atténue le momentum avec le temps (l'histoire ne va pas toujours tout droit)
                decay = 0.9 
                
                # 2. Ajout d'un Chaos croissant (plus on va loin, moins on est sûr)
                chaos = random.uniform(-3, 3)
                
                new_val = current_sim_state[pillar] + (momentum * decay) + chaos
                next_step[pillar] = max(0, min(100, new_val))

            # 3. Application des lois
            next_step = self.apply_interdependencies(next_step)
            
            # 4. Calcul Stabilité
            weighted_sum = sum(next_step.values()) + next_step['geopolitique'] + next_step['environnement']
            stability = round(weighted_sum / (len(PILLARS) + 2), 2)

            # Enregistrement
            future_timeline.append({
                "year": year,
                "stability_index": stability,
                "pillars": copy.deepcopy(next_step)
            })
            
            # L'état de cette année devient le départ de l'année suivante
            current_sim_state = next_step
            self.history.append({'pillars': next_step}) # On nourrit l'histoire temporaire pour le momentum

        return future_timeline

    def run(self):
        # 1. Calcul du mois prochain (Janvier 2026) comme avant
        # (J'ai simplifié ici pour utiliser la logique de simulation directement)
        current_year_state = self.history[-1]['pillars']
        # On extrait les valeurs brutes
        clean_start = {}
        for p in PILLARS:
            clean_start[p] = current_year_state[p]['score'] if isinstance(current_year_state[p], dict) else current_year_state[p]

        # Simulation sur 10 ans
        projection = self.simulate_future(clean_start)
        
        # Le premier élément de la projection est notre "Mois Prochain" (State Actuel)
        current_state_data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "stability_index": projection[0]['stability_index'],
            "pillars": projection[0]['pillars']
        }
        
        # Sauvegardes
        if not os.path.exists('data'): os.makedirs('data')
        
        # Save Current
        with open(CURRENT_STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(current_state_data, f, indent=2)
            
        # Save Projection 10 ans
        with open(PROJECTION_FILE, 'w', encoding='utf-8') as f:
            json.dump(projection, f, indent=2)

        print("✅ Simulation 2036 terminée.")

if __name__ == "__main__":
    PsychohistoryModel().run()
    
