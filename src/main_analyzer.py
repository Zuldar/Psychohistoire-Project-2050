import json
import os
import random
import glob
import copy
from datetime import datetime

# --- CONFIGURATION ---
HISTORY_FILE = 'data/history_2020_2025.json'
CURRENT_STATE_FILE = 'data/current_state.json'
PROJECTION_FILE = 'data/projection_2036.json'
ARCHIVE_DIR = 'data/archives'

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

    # --- AUTO-CRITIQUE (Feedback Loop) ---
    def analyze_prediction_error(self, current_pillars):
        if not os.path.exists(ARCHIVE_DIR): return []
        list_of_files = glob.glob(f'{ARCHIVE_DIR}/*.json')
        if not list_of_files: return []
        
        # On prend l'archive la plus récente
        latest_file = max(list_of_files, key=os.path.getctime)
        try:
            with open(latest_file, 'r') as f: past_data = json.load(f)
        except: return []

        current_year = int(datetime.now().year)
        predicted_state = None
        for year_proj in past_data.get('projection_10_years', []):
            if year_proj['year'] == current_year:
                predicted_state = year_proj['pillars']
                break
        
        if not predicted_state: return []

        corrections = []
        total_error = 0
        for p in PILLARS:
            real_val = current_pillars[p]['score']
            pred_val = predicted_state[p]
            delta = real_val - pred_val
            if abs(delta) > 5:
                corrections.append(f"📉 {p.upper()} : Écart de {round(delta)}% vs prévision.")
                total_error += abs(delta)

        if total_error > 0:
            corrections.insert(0, f"⚙️ AUTO-DIAGNOSTIC : Marge d'erreur globale {round(total_error)} pts.")
            
        return corrections

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
            
            # Lois de simulation (Interdépendances)
            if next_step['environnement'] < 25: next_step['geopolitique'] -= 3
            if next_step['technologie_ia'] > 98: next_step['demographie_social'] -= 3
            if next_step['finance'] < 30: next_step['demographie_social'] -= 2

            weighted_sum = sum(next_step.values()) + next_step['geopolitique'] + next_step['environnement']
            stability = round(weighted_sum / (len(PILLARS) + 2), 2)
            
            future_timeline.append({"year": year, "stability_index": stability, "pillars": copy.deepcopy(next_step)})
            current_sim_state = next_step
            self.history.append({'pillars': next_step})
        return future_timeline

    def detect_crisis_dates(self, projection):
        crisis_calendar = []
        for year_data in projection:
            yr = year_data['year']
            p = year_data['pillars']
            if p['environnement'] < 25 and p['geopolitique'] < 35:
                crisis_calendar.append(f"📅 {yr} : GUERRE DE L'EAU (Env < 25% + Géo < 35%)")
                break 
            if p['technologie_ia'] > 98 and p['demographie_social'] < 30:
                crisis_calendar.append(f"📅 {yr} : RÉVOLTE LUDDITE (IA > 98% + Social < 30%)")
                break
            if p['finance'] < 25:
                crisis_calendar.append(f"📅 {yr} : LE GRAND DÉFAUT (Finance < 25%)")
                break
        return crisis_calendar

    def generate_global_analysis(self, stability_index):
        if stability_index > 60: return "✅ STABILITÉ CONFIRMÉE."
        elif stability_index > 40: return "⚠️ STABILITÉ PRÉCAIRE."
        else: return "🚨 DANGER CRITIQUE."

    def generate_alerts(self, pillars, corrections):
        alerts = []
        if corrections: alerts.extend(corrections)
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

        projection = self.simulate_future(clean_start)
        crisis_dates = self.detect_crisis_dates(projection)
        correction_msgs = self.analyze_prediction_error(output_pillars)

        weighted_sum = sum([v['score'] for v in output_pillars.values()]) + output_pillars['geopolitique']['score'] + output_pillars['environnement']['score']
        stability_index = round(weighted_sum / (len(PILLARS) + 2), 2)

        final_alerts = self.generate_alerts(output_pillars, correction_msgs)
        final_alerts.extend(crisis_dates)

        current_state_data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "stability_index": stability_index,
            "global_analysis": self.generate_global_analysis(stability_index),
            "alerts": final_alerts,
            "pillars": output_pillars
        }
        
        if not os.path.exists('data'): os.makedirs('data')
        with open(CURRENT_STATE_FILE, 'w', encoding='utf-8') as f: json.dump(current_state_data, f, indent=2)
        with open(PROJECTION_FILE, 'w', encoding='utf-8') as f: json.dump(projection, f, indent=2)

        # Archivage
        if not os.path.exists(ARCHIVE_DIR): os.makedirs(ARCHIVE_DIR)
        archive_filename = f"rapport_{datetime.now().strftime('%Y-%m-%d')}.json"
        archive_path = os.path.join(ARCHIVE_DIR, archive_filename)
        full_archive = { "meta_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "current_state": current_state_data, "projection_10_years": projection }
        with open(archive_path, 'w', encoding='utf-8') as f: json.dump(full_archive, f, indent=2)

        print(f"✅ Rapport généré et archivé.")

if __name__ == "__main__":
    PsychohistoryModel().run()
    
