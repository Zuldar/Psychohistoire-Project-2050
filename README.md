```markdown
# 🔮 Projet Psychohistoire : Horizon 2050

![ISM](https://img.shields.io/badge/ISM-48%25-yellow?style=for-the-badge)
![Accuracy](https://img.shields.io/badge/Accuracy-96%25-brightgreen?style=for-the-badge)
![Last Update](https://img.shields.io/badge/Last%20Update-Jan%202026-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

> *"La seule façon de prédire l'avenir est de le calculer."* — Hari Seldon

---

## 📊 Vue d'ensemble

**Projet Psychohistoire** est un modèle prédictif qui analyse **9 piliers fondamentaux** de la civilisation humaine pour calculer un **Indice de Stabilité Mondiale (ISM)** et détecter les points de rupture systémiques entre 2026 et 2050.

### 🎯 Objectifs
- **Modéliser** les trajectoires de l'humanité avec des données mensuelles
- **Détecter** les signaux faibles de crises systémiques
- **Projeter** 3 scénarios probabilistes (Optimiste / Tendanciel / Pessimiste)
- **Alerter** sur les convergences de risques

### 📈 État actuel (Janvier 2026)
- **ISM Global :** 48/100 ⚠️ (Instabilité croissante)
- **Précision du modèle :** 96% ✅
- **Tendance :** Stabilisation relative après 5 ans à 45%
- **Prochaine mise à jour :** 15 février 2026

---

## 🏗️ Les 9 Piliers du Modèle

Le modèle agrège des données mensuelles structurées en 3 niveaux :

### I. La Base Physique (Le "Hardware")

| Pilier | Score | Poids | État |
|--------|-------|-------|------|
| **⚡ Énergie** | 52/100 | 1.0 | 🟡 Transition énergétique sous tension |
| **🌍 Environnement** | 36/100 | 1.2 | 🔴 Seuil critique franchi |
| **🚀 Espace** | 38/100 | 0.8 | 🟡 Militarisation orbitale |

### II. La Base Humaine (Le "Software")

| Pilier | Score | Poids | État |
|--------|-------|-------|------|
| **👥 Démographie & Social** | 40/100 | 1.0 | 🟡 Polarisation croissante |
| **🧬 Santé & Biologie** | 62/100 | 1.0 | 🟢 Stabilité post-pandémique |
| **⚔️ Géopolitique** | 28/100 | 1.3 | 🔴 Tensions maximales |

### III. La Base Abstraite (Le Système d'Exploitation)

| Pilier | Score | Poids | État |
|--------|-------|-------|------|
| **🤖 Technologie & IA** | 85/100 | 1.5 | 🟡 Pragmatisation de l'IA |
| **💰 Finance** | 45/100 | 1.1 | 🟡 Dette mondiale insoutenable |
| **🧠 Information** | 38/100 | 0.9 | 🔴 Guerre hybride numérique |

**Légende :**
- 🟢 **60-100** : Stable
- 🟡 **40-59** : Instable
- 🔴 **0-39** : Critique

---

## 🔬 Méthodologie

### Calcul de l'ISM
```
ISM = Σ (Score_pilier × Poids_pilier) / Σ (Poids_pilier)
```

**Exemple de calcul (Janvier 2026) :**
```
ISM = (85×1.5 + 36×1.2 + 52×1.0 + 28×1.3 + 40×1.0 + 45×1.1 + 62×1.0 + 38×0.8 + 38×0.9) / 9.8
    = 471.2 / 9.8
    = 48%
```

### Système d'auto-calibration
Le modèle ajuste automatiquement ses pondérations en fonction de l'écart entre :
- **ISM prédit** (projection du mois précédent)
- **ISM réel** (observation actuelle)

**Précision actuelle :** 96% (historique : [97%, 97%, 94%, 97%])

### Seuils d'interprétation

| Plage | État | Interprétation |
|-------|------|----------------|
| **80-100** | 🟢 Stabilité élevée | Système résilient, croissance durable |
| **60-79** | 🟡 Stabilité modérée | Tensions gérables, risques identifiés |
| **40-59** | 🟠 Instabilité croissante | **← POSITION ACTUELLE** - Fragmentation systémique |
| **20-39** | 🔴 Instabilité critique | Effondrement partiel, risque de cascade |
| **0-19** | ⚫ Effondrement | Dysfonctionnement généralisé |

---

## 🔮 Projections 2027-2036

Le modèle génère 3 scénarios probabilistes à partir de l'état actuel :

### Scénario Tendanciel (Baseline)
- **2027 :** 48% → Stagnation
- **2030 :** 36% → **Point de rupture climatique + énergétique**
- **2036 :** 43% → Stabilisation basse

### Scénario Optimiste
- **2027 :** 50% → Légère amélioration
- **2030 :** 45% → Évitement de la crise majeure
- **2036 :** 66% → Transition réussie

### Scénario Pessimiste (Effondrement)
- **2027 :** 45% → Dégradation
- **2030 :** 25% → **Crise systémique majeure**
- **2036 :** 15% → Effondrement partiel

**Prédiction actuelle :** 
> *"2030 : l'Entropie Climatique catalyse la Friction Géopolitique. Probabilité de rupture de la chaîne causale : 52%."*

---

## 📂 Structure du Projet

```
Psychohistoire-Project-2050/
│
├── .github/workflows/
│   └── update_model.yml        # Automatisation mensuelle (15 du mois à 10h UTC)
│
├── data/
│   ├── current_state.json      # État actuel (ISM + piliers + alertes)
│   ├── weights.json            # Pondérations des piliers
│   ├── history_full_v3.json    # Historique 1900-2026 (126 ans)
│   ├── recent_history.json     # Historique récent (2021-2026)
│   ├── projection_2036.json    # Projections 3 scénarios
│   ├── bot_memory.json         # Mémoire du modèle (accuracy)
│   └── monthly/                # Archives mensuelles (créées automatiquement)
│       ├── 2026-01.json
│       └── 2026-02.json (à venir)
│
├── src/
│   └── Seldon.py               # Moteur de calcul V36
│
├── docs/
│   └── METHODOLOGY.md          # Documentation méthodologique complète
│
├── index.html                  # Interface Prime Radiant
├── aide.html                   # Guide des métriques
├── style.css                   # Design Dark Neon V24
├── bg.gif                      # Fond animé
└── README.md                   # Ce fichier
```

---

## 🚀 Installation & Utilisation

### Prérequis
- Python 3.9+
- Navigateur web moderne

### Lancement local
```bash
# Cloner le dépôt
git clone https://github.com/Zuldar/Psychohistoire-Project-2050.git
cd Psychohistoire-Project-2050

# Lancer le modèle manuellement
python src/Seldon.py

# Ouvrir l'interface
open index.html  # (ou double-clic sur le fichier)
```

### Mise à jour automatique
Le projet se met à jour automatiquement chaque **15 du mois à 10h UTC** via GitHub Actions.

**Workflow :**
1. Exécution de `Seldon.py`
2. Mise à jour de `current_state.json`
3. Génération des projections
4. Archivage mensuel dans `data/monthly/`
5. Commit et push automatique

---

## 📊 Visualisations

### Interface Prime Radiant
![Interface](https://via.placeholder.com/800x400/020205/00f3ff?text=PRIME+RADIANT+TERMINAL)

**Fonctionnalités :**
- 📈 **Graphique temporel** : Historique 2021-2026 + Projections 2027-2036
- 🎯 **Score HUD** : ISM global en temps réel
- 🔮 **Alertes Seldon** : Prédictions de ruptures systémiques
- 📊 **Cartes de piliers** : État détaillé des 9 piliers
- 📜 **Archives historiques** : Crises passées (1914-2022)
- 🎨 **Design Dark Neon** : Thème cyberpunk inspiré de Foundation

---

## 📚 Documentation

### Guides disponibles
- **[METHODOLOGY.md](docs/METHODOLOGY.md)** : Méthodologie complète, formules, sources
- **[aide.html](aide.html)** : Guide d'interprétation des métriques (interface web)

### Sources de données
- **Géopolitique** : CFR, International Crisis Group, Eurasia Group, ACLED
- **Environnement** : Copernicus Climate, GIEC/IPCC, NOAA
- **Énergie** : EIA, IEA, Bloomberg Energy
- **Finance** : IMF GFSR, World Bank, BIS
- **Santé** : OMS/WHO, The Lancet
- **Tech/IA** : MIT Tech Review, arXiv, OpenAI
- **Espace** : SpaceNews, ESA, NASA
- **Information** : RSF, Freedom House, IFCN
- **Démographie** : UN Population, World Inequality Database

---

## 🛣️ Roadmap

### Phase 1 : Baseline (2026-2027) ✅ En cours
- ✅ Initialisation du modèle (Janvier 2026)
- ✅ Système de pondération dynamique
- ✅ Auto-calibration et tracking de précision
- 🔄 Collecte de 12 mois de données (2/12)
- ⏳ Validation de la précision prédictive

### Phase 2 : Expansion (2027-2030)
- Modélisation des corrélations entre piliers
- Intégration d'indicateurs quantitatifs automatisés
- Développement d'un système de confiance par prédiction
- Dashboard interactif avancé (D3.js)

### Phase 3 : Intelligence (2030-2050)
- Machine learning pour scoring automatique
- Analyse de Monte Carlo
- Système d'alerte précoce automatisé
- Publication scientifique des résultats

---

## 🤝 Contribution

Ce projet est open source et accueille les contributions :

### Comment contribuer ?
1. **Fork** le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commit (`git commit -m 'Ajout fonctionnalité X'`)
4. Push (`git push origin feature/amelioration`)
5. Ouvrir une **Pull Request**

### Suggestions bienvenues
- Nouvelles sources de données
- Amélioration des algorithmes de scoring
- Développement de visualisations
- Analyses et rapports

**Contact :** Via [GitHub Issues](https://github.com/Zuldar/Psychohistoire-Project-2050/issues)

---

## 📜 Licence & Inspiration

**Licence :** MIT License - Open Source  
**Créé en :** Janvier 2026  
**Inspiré par :** Isaac Asimov - Foundation Series (Psychohistoire)

### Références théoriques
- **Isaac Asimov** - Foundation Series (Psychohistoire)
- **Ray Dalio** - Principles for Navigating Big Debt Crises
- **Nassim Nicholas Taleb** - The Black Swan
- **Peter Turchin** - Ages of Discord

---

## 📞 Contact & Liens

- **GitHub Repository :** [Psychohistoire-Project-2050](https://github.com/Zuldar/Psychohistoire-Project-2050)
- **Interface Live :** [Prime Radiant Terminal](https://zuldar.github.io/Psychohistoire-Project-2050/)
- **Documentation :** [METHODOLOGY.md](docs/METHODOLOGY.md)

---

## 🏆 Statistiques du Projet

- **Historique analysé :** 126 ans (1900-2026)
- **Fréquence de mise à jour :** Mensuelle (15 du mois)
- **Précision actuelle :** 96%
- **Piliers surveillés :** 9
- **Scénarios projetés :** 3 (Optimiste / Tendanciel / Pessimiste)
- **Horizon de projection :** 2050 (24 ans)

---

**Dernière mise à jour :** 15 Janvier 2026  
**Prochaine mise à jour :** 15 Février 2026  
**Version du modèle :** Seldon V36

---

*"Le chaos n'est que de l'ordre incompris."* — Hari Seldon
```

---

## 📄 **2. WORKFLOW DE MISE À JOUR - 15 FÉVRIER 2026**

Crée un nouveau fichier `docs/WORKFLOW_MISE_A_JOUR.md` :

```markdown
# 📅 Workflow de Mise à Jour Mensuelle

> Guide complet pour la mise à jour du 15 de chaque mois

---

## ⏰ Rappel : Prochaine mise à jour

**Date :** 15 Février 2026  
**Heure :** 10h00-11h00  
**Durée :** 60 minutes

---

## 🎯 PHASE 1 : RECHERCHE D'INFORMATIONS (30 min)

### 🔍 Sources à consulter par pilier

#### ⚔️ GÉOPOLITIQUE (10 min)
**Sources principales :**
- [Council on Foreign Relations - Conflict Tracker](https://www.cfr.org/global-conflict-tracker)
- [International Crisis Group](https://www.crisisgroup.org/)
- [ACLED Dashboard](https://acleddata.com/dashboard/)
- [Doomsday Clock](https://thebulletin.org/doomsday-clock/)

**Rechercher :**
- Nouveaux conflits armés ou escalades
- Tensions nucléaires (Inde-Pakistan, Corée du Nord, etc.)
- Changements d'alliances (OTAN, BRICS, etc.)
- Incidents militaires majeurs

**Questions clés :**
- Y a-t-il eu de nouveaux conflits ce mois-ci ?
- Le risque nucléaire a-t-il augmenté ?
- Les tensions sont-elles en hausse ou en baisse ?

---

#### 🌍 ENVIRONNEMENT (5 min)
**Sources principales :**
- [Copernicus Climate](https://climate.copernicus.eu/)
- [NOAA Global Climate](https://www.noaa.gov/climate)
- [GIEC/IPCC Reports](https://www.ipcc.ch/)

**Rechercher :**
- Anomalie de température globale du mois
- Événements climatiques extrêmes (canicules, ouragans, inondations)
- Politiques climatiques (COP, Accord de Paris, etc.)
- Stress hydrique et ressources critiques

**Questions clés :**
- Quel a été l'écart de température vs baseline préindustrielle ?
- Combien de catastrophes climatiques majeures ?
- Les USA sont-ils toujours hors de l'Accord de Paris ?

---

#### ⚡ ÉNERGIE (5 min)
**Sources principales :**
- [EIA Short-Term Energy Outlook](https://www.eia.gov/outlooks/steo/)
- [IEA Data](https://www.iea.org/data-and-statistics)
- [Bloomberg Energy](https://www.bloomberg.com/energy)

**Rechercher :**
- Prix du pétrole (Brent, WTI)
- Prix du gaz naturel
- Coût de l'électricité
- Avancées en fusion nucléaire ou SMR

**Questions clés :**
- Le prix du pétrole est-il stable, en hausse ou en baisse ?
- Y a-t-il des pénuries énergétiques régionales ?
- Des percées technologiques en énergie propre ?

---

#### 💰 FINANCE (5 min)
**Sources principales :**
- [IMF Global Financial Stability Report](https://www.imf.org/en/Publications/GFSR)
- [World Bank Data](https://data.worldbank.org/)
- [BIS Statistics](https://www.bis.org/statistics/)

**Rechercher :**
- Dette mondiale (% du PIB global)
- Performances boursières (S&P 500, MSCI World)
- Crises bancaires ou défauts souverains
- Inflation et taux d'intérêt

**Questions clés :**
- La dette mondiale a-t-elle augmenté ?
- Y a-t-il eu des corrections boursières majeures ?
- L'inflation est-elle maîtrisée ?

---

#### 🤖 TECHNOLOGIE & IA (3 min)
**Sources principales :**
- [MIT Technology Review](https://www.technologyreview.com/)
- [arXiv AI Papers](https://arxiv.org/list/cs.AI/recent)
- [OpenAI Blog](https://openai.com/blog/)

**Rechercher :**
- Nouveaux modèles d'IA (GPT-X, Claude-X, etc.)
- Régulations de l'IA (EU AI Act, USA, Chine)
- Avancées en informatique quantique
- Taux d'automatisation

**Questions clés :**
- Y a-t-il eu des percées majeures en IA ce mois-ci ?
- De nouvelles régulations ont-elles été annoncées ?
- Le scaling des LLMs continue-t-il ou stagne-t-il ?

---

#### 🧬 SANTÉ & BIOLOGIE (2 min)
**Sources principales :**
- [OMS/WHO Updates](https://www.who.int/emergencies)
- [The Lancet](https://www.thelancet.com/)

**Rechercher :**
- Risques pandémiques (H5N1, etc.)
- Santé mentale globale (études récentes)
- Avancées en bio-ingénierie (CRISPR, etc.)

**Questions clés :**
- Y a-t-il de nouvelles menaces pandémiques ?
- La santé mentale s'améliore-t-elle ou se dégrade-t-elle ?

---

#### 🚀 ESPACE (2 min)
**Sources principales :**
- [SpaceNews](https://spacenews.com/)
- [NASA Updates](https://www.nasa.gov/news/)
- [ESA News](https://www.esa.int/Newsroom)

**Rechercher :**
- Lancements de satellites (militaires vs commerciaux)
- Débris spatiaux (nombre d'objets > 10cm)
- Projets de colonisation (Lune, Mars)

**Questions clés :**
- La militarisation de l'espace a-t-elle augmenté ?
- Y a-t-il eu des incidents orbitaux (collisions, débris) ?

---

#### 🧠 INFORMATION (2 min)
**Sources principales :**
- [RSF Press Freedom Index](https://rsf.org/en)
- [Freedom House](https://freedomhouse.org/)
- [IFCN Fact-Checkers](https://www.poynter.org/ifcn/)

**Rechercher :**
- Censure numérique (Chine, Russie, Iran)
- Désinformation massive (élections, guerres)
- Cyberattaques majeures

**Questions clés :**
- La liberté de la presse a-t-elle reculé ?
- Y a-t-il eu des campagnes de désinformation majeures ?

---

#### 👥 DÉMOGRAPHIE & SOCIAL (1 min)
**Sources principales :**
- [UN Population Data](https://population.un.org/wpp/)
- [World Inequality Database](https://wid.world/)

**Rechercher :**
- Migrations massives (crises humanitaires)
- Mouvements sociaux (manifestations, grèves)
- Inégalités (coefficient de Gini)

**Questions clés :**
- Y a-t-il eu des crises migratoires ce mois-ci ?
- Des mouvements sociaux majeurs ?

---

## 🎯 PHASE 2 : SCORING & ANALYSE (15 min)

### Grille de notation par pilier

Pour chaque pilier, attribuer un score de **0 à 100** selon cette logique :

#### Échelle générale
- **80-100** : Excellent état, tendances positives
- **60-79** : Bon état, quelques tensions
- **40-59** : État dégradé, risques identifiés
- **20-39** : État critique, crises actives
- **0-19** : Effondrement partiel

#### Ajustements mensuels
**Si amélioration nette :** +5 à +10 points  
**Si légère amélioration :** +2 à +4 points  
**Si stagnation :** 0 à ±1 point  
**Si légère dégradation :** -2 à -4 points  
**Si dégradation nette :** -5 à -10 points

### Exemple de notation : Géopolitique

**Score actuel (Janvier 2026) :** 28/100

**Événements de février :**
- ✅ Amélioration : Désescalade Inde-Pakistan → +3
- ❌ Dégradation : Nouveau conflit au Sahel → -2
- ❌ Dégradation : Tensions en Mer de Chine → -1

**Nouveau score :** 28 + 3 - 2 - 1 = **28/100** (stagnation)

**Commentaire :** *"Tensions géopolitiques maintenues. Léger apaisement Inde-Pakistan compensé par escalades ailleurs."*

---

### Calculer le nouvel ISM

**Formule :**
```
ISM = Σ (Score_pilier × Poids_pilier) / Σ (Poids_pilier)
```

**Poids actuels :**
```json
{
    "technologie_ia": 1.5,
    "geopolitique": 1.3,
    "environnement": 1.2,
    "finance": 1.1,
    "energie": 1.0,
    "demographie_social": 1.0,
    "sante_bio": 1.0,
    "information": 0.9,
    "espace": 0.8
}
```

**Total des poids :** 9.8

**Exemple :**
```
ISM = (85×1.5 + 28×1.3 + 36×1.2 + ... + 38×0.9) / 9.8
```

---

### Identifier les nouvelles alertes

**Types d'alertes :**

1. **🔮 Prédictions Seldon** (date de crise calculée automatiquement)
2. **🚨 Alertes critiques** (pilier < 35)
3. **⚠️ Alertes de vigilance** (pilier entre 35-45)
4. **✅ Stabilité** (pilier > 60)

**Exemples :**
- `"⚠️ Ω_BIOSPHERE : Seuil critique atteint"` si Environnement < 40
- `"⚔️ Σ_CONFLICT : Tensions maximales"` si Géopolitique < 35
- `"📅 2030 : l'Entropie Climatique catalyse la Friction Géopolitique. Probabilité : XX%"`

---

## 🎯 PHASE 3 : MISE À JOUR TECHNIQUE (15 min)

### 1️⃣ Modifier `current_state.json`

**Ouvrir le fichier et mettre à jour :**

```json
{
    "date": "2026-02-15 10:00",  // ← NOUVELLE DATE
    "stability_index": 47,        // ← NOUVEL ISM
    "model_accuracy": 96,         // ← Laissé tel quel (calculé auto)
    "global_analysis": "...",     // ← NOUVELLE ANALYSE (2-3 phrases)
    "pillars": {
        "technologie_ia": {
            "score": 83,          // ← NOUVEAU SCORE
            "comment": "..."      // ← NOUVEAU COMMENTAIRE
        },
        // ... tous les autres piliers
    },
    "alerts": [
        "📅 2030 : ...",          // ← NOUVELLES ALERTES
        "⚠️ Ω_BIOSPHERE : ..."
    ],
    "archives": [...]             // ← Ne pas toucher
}
```

---

### 2️⃣ Tester localement (optionnel)

```bash
# Exécuter le script Python pour vérifier
python src/Seldon.py

# Vérifier que les fichiers sont créés
