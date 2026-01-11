import json
import os
import random
from datetime import datetime

# --- CONFIGURATION DU MODELE ---
HISTORY_FILE = 'data/history_2020_2025.json'
CURRENT_STATE_FILE = 'data/current_state.json'
REPORT_DIR = 'reports'
REPORT_OUTPUT = os.path.join(REPORT_DIR, 'rapport_mensuel.md')

# Les 9 Piliers de la Psychohistoire
PILLARS = [
    "energie", "environnement", "espace",              # Physique
    "demographie_social", "sante_bio", "geopolitique", # Humain
    "technologie_ia", "finance", "information"         # Abstrait
]

class PsychohistoryModel:
    def __init__(self):
        self.history = self.load_json(HISTORY_FILE)
        
    def load_json(self, filepath):
        if not os.path.exists(filepath):
            print(f"Attention: Fichier {filepath} introuvable. Utilisation de données vides.")
            return []
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def calculate_momentum(self, pillar_name):
        """Calcule la vitesse de changement d'un pilier sur les 3 dernières années."""
        if len(self.history) < 3:
            return 0
        
        # Récupération des scores des 3 dernières années
        last_3_years = self.history[-3:]
        # Sécurité si un pilier manque dans l'historique
        try:
            scores = [year['pillars'][pillar_name]['score'] for year in last_3_years]
        except KeyError:
            return 0
        
        # Vélocité : (Dernière année - Année-2) + tendance récente
        velocity = (scores[2] - scores[0]) / 2
        return velocity

    def apply_interdependencies(self, future_scores):
        """
        Le coeur du modèle : Comment les piliers s'influencent.
        """
        # Loi 1 : Si l'Environnement chute, le Social et la Géopolitique chutent
        if future_scores['environnement'] < 30:
            future_scores['demographie_social'] -= 5
            future_scores['geopolitique'] -= 3

        # Loi 2 : Si la Technologie/IA explose (>90), le Social chute (choc du futur) mais l'Espace monte
        if future_scores['technologie_ia'] > 90:
            future_scores['demographie_social'] -= 2
            future_scores['espace'] += 4
            future_scores['information'] -= 5 # (Confusion réel/virtuel)

        # Loi 3 : Si l'Énergie monte (>60), la Finance se stabilise
        if future_scores['energie'] > 60:
            future_scores['finance'] += 2

        return future_scores

    def predict_next_month(self):
        # Sécurité si l'historique est vide
        if not self.history:
            print("Erreur critique : Pas d'historique chargé.")
            return {}, 0

        last_year = self.history[-1]
        future_state = {}
        
        # 1. Projection linéaire basée sur le momentum historique
        print("--- Calcul des trajectoires ---")
        for pillar in PILLARS:
            momentum = self.calculate_momentum(pillar)
            current_score = last_year['pillars'][pillar]['score']
            
            # Facteur Chaos (incertitude de l'avenir) +/- 2%
            chaos = random.uniform(-2, 2)
            
            # Projection (divisé par 12 pour ramener à une échelle mensuelle)
            next_score = current_score + (momentum / 12) + chaos
            
            # Bornage entre 0 et 100
            next_score = max(0, min(100, next_score))
            future_state[pillar] = round(next_score, 2)
            
            print(f"Pilier {pillar}: {current_score} -> {future_state[pillar]} (Momentum: {momentum:.2f})")

        # 2. Application des interdépendances systémiques
        future_state = self.apply_interdependencies(future_state)
        
        # 3. Calcul de l'Indice de Stabilité Mondiale (Moyenne pondérée)
        # La géopolitique et l'environnement pèsent double dans la stabilité
        weighted_sum = sum(future_state.values()) + future_state['geopolitique'] + future_state['environnement']
        stability_index = round(weighted_sum / (len(PILLARS) + 2), 2)
        
        return future_state, stability_index

    def generate_report(self, future_state, stability_index):
        now = datetime.now().strftime("%Y-%m-%d")
        
        # Détection des alertes
        alerts = []
        if stability_index < 40: alerts.append("🔴 ALERTE ROUGE : Risque d'effondrement systémique.")
        if future_state['technologie_ia'] > 95: alerts.append("⚠️ ALERTE SINGULARITÉ : L'IA dépasse les seuils de régulation.")
        if future_state['geopolitique'] < 20: alerts.append("⚔️ ALERTE GUERRE : Tensions critiques.")

        report = f"""
# 🔮 Rapport Psychohistorique - {now}

## 📊 Indice de Stabilité Mondiale : {stability_index}/100

### 🚨 Alertes Prioritaires
{chr(10).join(['- ' + a for a in alerts]) if alerts else "- Aucune alerte critique."}

### 📈 État des 9 Piliers (Prévision M+1)
| Pilier | Score | Tendance |
|--------|-------|----------|
| ⚡ Énergie | {future_state['energie']} | {'🟢' if future_state['energie'] > 50 else '🔴'} |
| 🌍 Environnement | {future_state['environnement']} | {'🟢' if future_state['environnement'] > 50 else '🔴'} |
| 🚀 Espace | {future_state['espace']} | {'🟢' if future_state['espace'] > 50 else '🔴'} |
| 👥 Social | {future_state['demographie_social']} | {'🟢' if future_state['demographie_social'] > 50 else '🔴'} |
| 🧬 Santé | {future_state['sante_bio']} | {'🟢' if future_state['sante_bio'] > 50 else '🔴'} |
| ⚔️ Géopolitique | {future_state['geopolitique']} | {'🟢' if future_state['geopolitique'] > 50 else '🔴'} |
| 🤖 Tech & IA | {future_state['technologie_ia']} | {'🟢' if future_state['technologie_ia'] < 90 else '⚠️'} |
| 💰 Finance | {future_state['finance']} | {'🟢' if future_state['finance'] > 50 else '🔴'} |
| 🧠 Information | {future_state['information']} | {'🟢' if future_state['information'] > 50 else '🔴'} |

---
*Généré par le Noyau Psychohistorique V1*
"""
        return report

    def run(self):
        print("Initialisation du modèle...")
        
        # Création du dossier reports s'il n'existe pas
        if not os.path.exists(REPORT_DIR):
            os.makedirs(REPORT_DIR)
            
        future_state, stability_index = self.predict_next_month()
        
        if not future_state:
            return

        # Sauvegarde des données JSON
        output_data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "stability_index": stability_index,
            "pillars": future_state
        }
        with open(CURRENT_STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)
            
        # Génération du rapport Markdown
        report_content = self.generate_report(future_state, stability_index)
        with open(REPORT_OUTPUT, 'w', encoding='utf-8') as f:
            f.write(report_content)
            
        print("✅ Analyse terminée. Rapport généré.")

if __name__ == "__main__":
    model = PsychohistoryModel()
    model.run()
    
