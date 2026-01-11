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

    # --- TEXTES COURTS ---
    def get_analysis_text(self, pillar, score):
        analyses = {
            "energie": { "low": "⚠️ Pénurie Critique.", "mid": "⚡ Transition instable.", "high": "🟢 Abondance (Fusion)." },
            "environnement": { "low": "☠️ Effondrement.", "mid": "⚠️ Point de bascule.", "high": "🟢 Régénération." },
            "espace": { "low": "⛔ Bloqué au sol.", "mid": "🚀 Orbite active.", "high": "🌌 Multi-planétaire." },
            "demographie_social": { "low": "🔥 Guerre Civile.", "mid": "⚠️ Tensions fortes.", "high": "🤝 Harmonie." },
            "sante_bio": { "low": "☣️ Pandémie Majeure.", "mid": "💊 Lutte constante.", "high": "🧬 Transhumanisme." },
            "geopolitique": { "low": "☢️ Guerre Mondiale.", "mid": "⚔️ Guerre Froide.", "high": "🕊️ Paix Perpétuelle." },
            "technologie_ia": { "low": "📉 Stagnation.", "mid": "🤖 Automatisation.", "high": "⚠️ SINGULARITÉ." },
            "finance": { "low": "💸 Hyperinflation.", "mid": "📉 Récession.", "high": "💎 Post-Rareté." },
            "information": { "low": "🧠 Obscurantisme.", "mid": "📢 Désinformation.", "high": "🌐 Noosphère Claire." }
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

    def simulate_future(self, start_state):
        future_timeline = []
        current_sim_state = copy.deepcopy(start_state)
        for year in range(2027, 2037):
            next_step = {}
            for pillar in PILLARS:
                momentum = self.calculate_momentum(self.history, pillar)
                new_val = current_sim_state[pillar] + (momentum * 0.9) + random.uniform(-2, 2)
                next_step[pillar] = max(0, min(100, new_val))
            
            # Lois de simulation
            if next_step['environnement'] < 25: next_step['geopolitique'] -= 3
            if next_step['technologie_ia'] > 98: next_step['demographie_social'] -= 3
            if next_step['finance'] < 30: next_step['demographie_social'] -= 2

            weighted_sum = sum(next_step.values()) + next_step['geopolitique'] + next_step['environnement']
            stability = round(weighted_sum / (len(PILLARS) + 2), 2)
            
            future_timeline.append({"year": year, "stability_index": stability, "pillars": copy.deepcopy(next_step)})
            current_sim_state = next_step
            self.history.append({'pillars': next_step})
        return future_timeline

    # --- NOUVEAU : LE DÉTECTEUR DE DATES DE CRISE ---
    def detect_crisis_dates(self, projection):
        """Scanne le futur pour trouver l'année exacte de la rupture."""
        crisis_calendar = []
        
        for year_data in projection:
            yr = year_data['year']
            p = year_data['pillars']
            
            # Scénario 1 : La Crise de l'Eau (Environnement + Géo)
            if p['environnement'] < 20 and p['geopolitique'] < 30:
                crisis_calendar.append(f"📅 {yr} : GUERRE DE L'EAU (Env < 20% + Géo < 30%)")
                break # On ne signale la crise qu'une fois
            
            # Scénario 2 : La Grande Révolte (IA + Social)
            if p['technologie_ia'] > 99 and p['demographie_social'] < 25:
                crisis_calendar.append(f"📅 {yr} : RÉVOLTE LUDDITE (IA > 99% + Social < 25%)")
                break
                
            # Scénario 3 : L'Effondrement Financier
            if p['finance'] < 20:
                crisis_calendar.append(f"📅 {yr} : LE GRAND DÉFAUT (Finance < 20%)")
                break

        if not crisis_calendar:
            crisis_calendar.append("Aucune crise majeure datée sur 10 ans.")
            
        return crisis_calendar

    def generate_global_analysis(self, stability_index):
        if stability_index > 60: return "✅ STABILITÉ CONFIRMÉE."
        elif stability_index > 40: return "⚠️ STABILITÉ PRÉCAIRE."
        else: return "🚨 DANGER CRITIQUE."

    def generate_alerts(self, pillars):
        alerts = []
        if pillars['technologie_ia']['score'] > 95: alerts.append("⚠️ SINGULARITÉ (Tech)")
        if pillars['environnement']['score'] < 30: alerts.append("🔴 CLIMAT (Env)")
        if pillars['geopolitique']['score'] < 30: alerts.append("⚔️ GUERRE (Géo)")
        if not alerts: alerts.append("✅ Aucune alerte immédiate.")
        return alerts

    def run(self):
        current_year_state = self.history[-1]['pillars']
        clean_start = {}
        output_pillars = {}
        
        for p in PILLARS:
            val = current_year_state[p]['score'] if isinstance(current_year_state[p], dict) else current_year_state[p]
            momentum = self.calculate_momentum(self.history, p)
            next_val = max(0, min(100, val + (momentum/12) + random.uniform(-0.5, 0.5)))
            
            clean_start[p] = next_val
            output_pillars[p] = { "score": round(next_val, 2), "comment": self.get_analysis_text(p, next_val) }

        # Simulation du futur
        projection = self.simulate_future(clean_start)
        
        # Détection des dates de crise
        crisis_dates = self.detect_crisis_dates(projection)

        weighted_sum = sum([v['score'] for v in output_pillars.values()]) + output_pillars['geopolitique']['score'] + output_pillars['environnement']['score']
        stability_index = round(weighted_sum / (len(PILLARS) + 2), 2)

        # On ajoute les dates de crise aux alertes pour l'affichage
        final_alerts = self.generate_alerts(output_pillars)
        final_alerts.extend(crisis_dates) # On fusionne les alertes immédiates et les prédictions futures

        current_state_data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "stability_index": stability_index,
            "global_analysis": self.generate_global_analysis(stability_index),
            "alerts": final_alerts, # Contient maintenant les dates !
            "pillars": output_pillars
        }
        
        if not os.path.exists('data'): os.makedirs('data')
        with open(CURRENT_STATE_FILE, 'w', encoding='utf-8') as f: json.dump(current_state_data, f, indent=2)
        with open(PROJECTION_FILE, 'w', encoding='utf-8') as f: json.dump(projection, f, indent=2)
        print("✅ Rapport Seldon avec DATATION généré.")

if __name__ == "__main__":
    PsychohistoryModel().run()
    
