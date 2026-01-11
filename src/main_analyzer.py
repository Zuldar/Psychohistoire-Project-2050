import json
import os
import random
import copy
from datetime import datetime

# --- CONFIGURATION ---
HISTORY_FILE = 'data/history_2020_2025.json'
CURRENT_STATE_FILE = 'data/current_state.json'
PROJECTION_FILE = 'data/projection_2036.json'

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

    # --- MOTEUR DE TEXTE ET D'ALERTES (NOUVEAU) ---
    def generate_global_analysis(self, stability_index):
        """Génère le résumé global en haut du dashboard."""
        if stability_index > 60:
            return "✅ STABILITÉ CONFIRMÉE. Le système mondial est robuste. Les indicateurs sociaux et technologiques sont en phase d'harmonisation."
        elif stability_index > 40:
            return "⚠️ STABILITÉ PRÉCAIRE. La puissance technologique masque des fractures sociales et environnementales profondes. Risque de décrochage."
        else:
            return "🚨 DANGER CRITIQUE. Le système est en phase de rupture. Les tensions géopolitiques et climatiques dépassent les capacités de résilience."

    def generate_alerts(self, pillars):
        """Détecte les anomalies et crée la liste des alertes."""
        alerts = []
        
        # Tech
        if pillars['technologie_ia']['score'] > 95:
            alerts.append("⚠️ ALERTE SINGULARITÉ (Tech) : L'IA atteint un seuil critique d'autonomie. Risque systémique pour l'emploi.")
        elif pillars['technologie_ia']['score'] < 20:
            alerts.append("📉 DÉCROISSANCE TECH : Pénurie mondiale de semi-conducteurs.")

        # Environnement
        if pillars['environnement']['score'] < 30:
            alerts.append("🔴 ALERTE CLIMAT (Env) : Anomalies thermiques irréversibles. Crises de l'eau imminentes.")
        
        # Géopolitique
        if pillars['geopolitique']['score'] < 30:
            alerts.append("⚔️ TENSION MAXIMALE (Géo) : Les fronts sont volatils. Risque d'escalade conventionnelle.")
            
        # Social
        if pillars['demographie_social']['score'] < 35:
            alerts.append("🔥 RUPTURE SOCIALE : Le contrat social est rompu. Risque d'insurrection coordonnée.")

        # Information
        if pillars['information']['score'] < 25:
            alerts.append("🧠 DISSOLUTION DU RÉEL : Impossible de distinguer la vérité. La Noosphère est saturée.")

        if not alerts:
            alerts.append("✅ Aucune alerte critique détectée ce mois-ci.")
            
        return alerts

    def get_analysis_text(self, pillar, score):
        # (Version abrégée des commentaires piliers pour gagner de la place ici, 
        # tu peux garder tes textes longs si tu préfères, le principe reste le même)
        analyses = {
            "energie": { "low": "Pénurie critique.", "mid": "Transition difficile.", "high": "Abondance (Fusion)." },
            "environnement": { "low": "Effondrement écologique.", "mid": "Point de bascule.", "high": "Régénération." },
            "espace": { "low": "Syndrome de Kessler.", "mid": "Orbite active.", "high": "Multi-planétaire." },
            "demographie_social": { "low": "Guerre civile.", "mid": "Tensions fortes.", "high": "Harmonie." },
            "sante_bio": { "low": "Pandémie.", "mid": "Lutte sanitaire.", "high": "Transhumanisme." },
            "geopolitique": { "low": "Guerre Mondiale.", "mid": "Guerre Froide.", "high": "Paix Mondiale." },
            "technologie_ia": { "low": "Stagnation.", "mid": "Automatisation.", "high": "SINGULARITÉ." },
            "finance": { "low": "Hyperinflation.", "mid": "Récession.", "high": "Post-Rareté." },
            "information": { "low": "Obscurantisme.", "mid": "Désinformation.", "high": "Transparence." }
        }
        if score < 40: return analyses[pillar]["low"]
        if score > 80: return analyses[pillar]["high"]
        return analyses[pillar]["mid"]

    # --- CALCULS (Identique avant) ---
    def calculate_momentum(self, history_data, pillar_name):
        if len(history_data) < 3: return 0
        last_3 = history_data[-3:]
        try:
            scores = [year['pillars'][pillar_name]['score'] if isinstance(year['pillars'][pillar_name], dict) else year['pillars'][pillar_name] for year in last_3]
            return (scores[2] - scores[0]) / 2
        except: return 0

    def simulate_future(self, start_state):
        # (Code simulation identique à la V3)
        future_timeline = []
        current_sim_state = copy.deepcopy(start_state)
        for year in range(2027, 2037):
            next_step = {}
            for pillar in PILLARS:
                momentum = self.calculate_momentum(self.history, pillar)
                new_val = current_sim_state[pillar] + (momentum * 0.9) + random.uniform(-3, 3)
                next_step[pillar] = max(0, min(100, new_val))
            
            # Lois simplifiées pour simulation
            if next_step['environnement'] < 20: next_step['geopolitique'] -= 2
            if next_step['technologie_ia'] > 95: next_step['demographie_social'] -= 2
            
            weighted_sum = sum(next_step.values()) + next_step['geopolitique'] + next_step['environnement']
            stability = round(weighted_sum / (len(PILLARS) + 2), 2)
            
            future_timeline.append({"year": year, "stability_index": stability, "pillars": copy.deepcopy(next_step)})
            current_sim_state = next_step
            self.history.append({'pillars': next_step})
        return future_timeline

    def run(self):
        current_year_state = self.history[-1]['pillars']
        clean_start = {}
        output_pillars = {}
        
        # Calcul M+1
        for p in PILLARS:
            val = current_year_state[p]['score'] if isinstance(current_year_state[p], dict) else current_year_state[p]
            momentum = self.calculate_momentum(self.history, p)
            next_val = max(0, min(100, val + (momentum/12) + random.uniform(-1, 1)))
            
            clean_start[p] = next_val
            output_pillars[p] = {
                "score": round(next_val, 2),
                "comment": self.get_analysis_text(p, next_val)
            }

        projection = self.simulate_future(clean_start)
        
        weighted_sum = sum([v['score'] for v in output_pillars.values()]) + output_pillars['geopolitique']['score'] + output_pillars['environnement']['score']
        stability_index = round(weighted_sum / (len(PILLARS) + 2), 2)

        # GENERATION DU RAPPORT TEXTUEL
        global_analysis = self.generate_global_analysis(stability_index)
        alerts_list = self.generate_alerts(output_pillars)

        current_state_data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "stability_index": stability_index,
            "global_analysis": global_analysis,  # Nouveau champ
            "alerts": alerts_list,               # Nouveau champ
            "pillars": output_pillars
        }
        
        if not os.path.exists('data'): os.makedirs('data')
        
        with open(CURRENT_STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(current_state_data, f, indent=2)
        with open(PROJECTION_FILE, 'w', encoding='utf-8') as f:
            json.dump(projection, f, indent=2)

        print("✅ Rapport complet généré.")

if __name__ == "__main__":
    PsychohistoryModel().run()
    
