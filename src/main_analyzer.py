import json
import os
import random
import copy
from datetime import datetime

# --- CONFIGURATION ---
HISTORY_FILE = 'data/history_2020_2025.json'
CURRENT_STATE_FILE = 'data/current_state.json'
PROJECTION_FILE = 'data/projection_2036.json'
REPORT_DIR = 'reports'

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

    # --- LE MOTEUR NARRATIF (NOUVEAU) ---
    def get_analysis_text(self, pillar, score):
        """Génère un commentaire contextuel basé sur le score."""
        analyses = {
            "energie": {
                "low": "⚠️ Pénurie Critique. Blackouts mondiaux et rationnement strict.",
                "mid": "⚡ Transition instable. Prix élevés, tensions sur les ressources fossiles.",
                "high": "🟢 Abondance. La fusion nucléaire et le solaire spatial couvrent 100% des besoins."
            },
            "environnement": {
                "low": "☠️ Effondrement. Zones tropicales inhabitables, réfugiés climatiques massifs.",
                "mid": "⚠️ Point de bascule. Catastrophes fréquentes, biodiversité en chute libre.",
                "high": "🟢 Régénération. Le climat se stabilise, retour de la biomasse sauvage."
            },
            "espace": {
                "low": "⛔ Bloqué au sol. Syndrome de Kessler (débris) ou perte technologique.",
                "mid": "🚀 Orbite Basse. Stations spatiales actives mais pas de colonisation.",
                "high": "🌌 Civilisation Multi-planétaire. Colonies sur Mars et la Lune autonomes."
            },
            "demographie_social": {
                "low": "🔥 Guerre Civile. Émeutes de la faim, effondrement des états-providence.",
                "mid": "⚠️ Tensions. Inégalités extrêmes, grèves générales, méfiance des élites.",
                "high": "🤝 Harmonie. Revenu universel mondial, criminalité proche de zéro."
            },
            "sante_bio": {
                "low": "☣️ Pandémie Majeure. Espérance de vie en chute, résistance aux antibiotiques.",
                "mid": "💊 Lutte constante. Progrès médicaux réservés aux riches, crises sanitaires.",
                "high": "🧬 Transhumanisme. Maladies éradiquées, espérance de vie > 120 ans."
            },
            "geopolitique": {
                "low": "☢️ Guerre Mondiale. Conflits nucléaires tactiques ou invasions massives.",
                "mid": "⚔️ Guerre Froide. Blocs hostiles, cyber-guerre permanente, proxy wars.",
                "high": "🕊️ Paix Perpétuelle. Gouvernance mondiale unifiée et fonctionnelle."
            },
            "technologie_ia": {
                "low": "📉 Stagnation. Fin de la loi de Moore, pénurie de puces.",
                "mid": "🤖 Automatisation. L'IA remplace les cols blancs, mais reste un outil.",
                "high": "⚠️ SINGULARITÉ. L'IA s'améliore seule. L'humain n'a plus le contrôle."
            },
            "finance": {
                "low": "💸 Hyperinflation. La monnaie ne vaut rien, retour au troc.",
                "mid": "📉 Récession. Dette insoutenable, krachs boursiers fréquents.",
                "high": "💎 Post-Rareté. Économie stable gérée par algos, prospérité partagée."
            },
            "information": {
                "low": "🧠 Obscurantisme. Impossible de distinguer le vrai du faux (Deepfakes totaux).",
                "mid": "📢 Désinformation. Propagande d'état et bulles de filtres.",
                "high": "🌐 Noosphère Claire. Information vérifiée, transparente et libre."
            }
        }
        
        if score < 40: return analyses[pillar]["low"]
        if score > 80: return analyses[pillar]["high"]
        return analyses[pillar]["mid"]

    def calculate_momentum(self, history_data, pillar_name):
        if len(history_data) < 3: return 0
        last_3 = history_data[-3:]
        try:
            scores = [year['pillars'][pillar_name]['score'] if isinstance(year['pillars'][pillar_name], dict) else year['pillars'][pillar_name] for year in last_3]
            return (scores[2] - scores[0]) / 2
        except: return 0

    def apply_interdependencies(self, state):
        if state['environnement'] < 20:
            state['geopolitique'] -= 2; state['demographie_social'] -= 1.5
        if state['technologie_ia'] > 95:
            state['demographie_social'] -= 2; state['espace'] += 3
            state['information'] -= 3; state['sante_bio'] += 2
        if state['espace'] > 90: state['energie'] += 2
        for k in state: state[k] = max(0, min(100, state[k]))
        return state

    def simulate_future(self, start_state):
        future_timeline = []
        current_sim_state = copy.deepcopy(start_state)
        for year in range(2027, 2037):
            next_step = {}
            for pillar in PILLARS:
                momentum = self.calculate_momentum(self.history, pillar)
                decay = 0.9 
                chaos = random.uniform(-3, 3)
                new_val = current_sim_state[pillar] + (momentum * decay) + chaos
                next_step[pillar] = max(0, min(100, new_val))
            next_step = self.apply_interdependencies(next_step)
            weighted_sum = sum(next_step.values()) + next_step['geopolitique'] + next_step['environnement']
            stability = round(weighted_sum / (len(PILLARS) + 2), 2)
            
            future_timeline.append({
                "year": year,
                "stability_index": stability,
                "pillars": copy.deepcopy(next_step)
            })
            current_sim_state = next_step
            self.history.append({'pillars': next_step})
        return future_timeline

    def run(self):
        # Récupération état actuel (simulation rapide pour M+1)
        current_year_state = self.history[-1]['pillars']
        clean_start = {}
        output_pillars = {}
        
        # On prépare les données enrichies (Score + Commentaire)
        for p in PILLARS:
            # Récupération valeur
            val = current_year_state[p]['score'] if isinstance(current_year_state[p], dict) else current_year_state[p]
            
            # Calcul M+1 simple
            momentum = self.calculate_momentum(self.history, p)
            next_val = max(0, min(100, val + (momentum/12) + random.uniform(-1, 1)))
            
            clean_start[p] = next_val # Pour la simulation futur
            
            # Construction de l'objet enrichi pour le JSON
            output_pillars[p] = {
                "score": round(next_val, 2),
                "comment": self.get_analysis_text(p, next_val)
            }

        # Simulation 10 ans
        projection = self.simulate_future(clean_start)
        
        # Calcul Stabilité Actuelle
        weighted_sum = sum([v['score'] for v in output_pillars.values()]) + output_pillars['geopolitique']['score'] + output_pillars['environnement']['score']
        stability_index = round(weighted_sum / (len(PILLARS) + 2), 2)

        # Sauvegarde Current State (Structure modifiée !)
        current_state_data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "stability_index": stability_index,
            "pillars": output_pillars # Contient maintenant {score, comment}
        }
        
        if not os.path.exists('data'): os.makedirs('data')
        
        with open(CURRENT_STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(current_state_data, f, indent=2)
            
        with open(PROJECTION_FILE, 'w', encoding='utf-8') as f:
            json.dump(projection, f, indent=2)

        print("✅ Analyse avec commentaires générée.")

if __name__ == "__main__":
    PsychohistoryModel().run()
    
