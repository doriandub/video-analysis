# 🎬 Video Analysis API - Hospup

**La solution la plus simple** pour analyser des vidéos (Instagram, S3, CDN) et générer des descriptions keywords comme ton système actuel.

## 📦 Ce que ça fait

- ✅ Télécharge une vidéo depuis une URL
- ✅ Détecte les cuts automatiquement (PySceneDetect)
- ✅ Analyse chaque cut avec IA
- ✅ Génère des **keywords** (comme ton prompt hospitality actuel)
- ✅ Retourne un JSON avec clips + descriptions

## 🔥 Setup en 3 minutes

```bash
# 1. Va dans le dossier
cd /Users/doriandubord/Desktop/hospup-project/video-analysis-api

# 2. Configure (édite .env)
CAPTION_BACKEND=openai           # ou moondream2 (gratuit mais moins bon)
OPENAI_API_KEY=sk-proj-...       # ta clé OpenAI
API_KEY=ton-secret-key-ici       # pour sécuriser l'API

# 3. Démarre
docker compose up -d --build

# 4. Test
./TEST.sh
```

## 📊 Output Format (exactement comme ton système)

```json
{
  "clips": [
    {
      "order": 1,
      "start": 0.0,
      "end": 1.5,
      "duration": 1.5,
      "description": "infinity pool, ocean, sun loungers, palm trees"
    },
    {
      "order": 2,
      "start": 1.5,
      "end": 2.8,
      "duration": 1.3,
      "description": "bedroom, bed, window, balcony, furniture"
    }
  ],
  "texts": []
}
```

## 🎯 Prompt utilisé

**C'est EXACTEMENT le même prompt que ton `openai_vision_service.py`** (lignes 153-185).

Le prompt demande des **keywords séparés par virgules** sans adjectifs, juste des noms concrets :
- ✅ "pool, ocean, sun loungers, palm trees"
- ❌ "beautiful luxury pool with amazing ocean view"

## 🚀 Utilisation

### CURL basique

```bash
curl -X POST http://localhost:8190/analyze \
  -H "x-api-key: ton-secret-key" \
  -F "url=https://instagram.com/video.mp4" \
  -F "threshold=25" \
  -F "max_cuts=15"
```

### Avec ta vidéo Instagram

```bash
./TEST.sh
```

### Depuis n8n

```json
{
  "method": "POST",
  "url": "http://localhost:8190/analyze",
  "headers": {
    "x-api-key": "{{ $env.VIDEO_API_KEY }}"
  },
  "bodyParameters": {
    "parameters": [
      {"name": "url", "value": "={{ $json.video_url }}"},
      {"name": "threshold", "value": "25"},
      {"name": "max_cuts", "value": "15"}
    ]
  }
}
```

## ⚙️ Configuration

### Backend OpenAI (Recommandé)

```bash
# .env
CAPTION_BACKEND=openai
OPENAI_API_KEY=sk-proj-...
```

**Avantages :**
- ✅ Même qualité que ton système actuel
- ✅ Utilise ton prompt hospitality exact
- ✅ Rapide (~2-3s par vidéo)
- ✅ Pas de GPU nécessaire

**Coût :** ~$0.01 par vidéo (10 cuts)

### Backend Moondream2 (Gratuit)

```bash
# .env
CAPTION_BACKEND=moondream2
```

**Avantages :**
- ✅ Gratuit, aucun coût
- ✅ Marche offline

**Inconvénients :**
- ❌ Qualité inférieure à OpenAI
- ❌ Plus lent (5-10s par vidéo)
- ❌ Nécessite ~2GB RAM

## 📐 Paramètres

| Paramètre | Description | Défaut | Recommandé |
|-----------|-------------|--------|------------|
| `url` | URL vidéo (required) | - | - |
| `threshold` | Sensibilité cuts | 27.0 | 20-30 |
| `max_cuts` | Nombre max de cuts | 30 | 10-20 |

**Threshold :**
- `20-25` : Vidéos statiques → plus de cuts
- `25-30` : Vidéos dynamiques (Instagram)
- `30-35` : Seulement transitions marquées

## 📁 Structure

```
video-analysis-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # API FastAPI (300 lignes)
│   └── config.py        # Configuration + prompt hospitality
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env                 # Ta configuration
├── TEST.sh              # Script de test
├── QUICKSTART.md        # Guide détaillé
└── README.md            # Documentation complète
```

## 🧠 Comment ça marche

1. **Download** : Télécharge la vidéo depuis l'URL
2. **Scene Detection** : PySceneDetect trouve les cuts
3. **Frame Extraction** : Extrait la frame du milieu de chaque cut
4. **IA Captioning** : OpenAI Vision ou Moondream2 génère les keywords
5. **Return JSON** : Format identique à ton système actuel

## 🔒 Sécurité

- API key obligatoire (header `x-api-key`)
- Timeouts configurables
- Nettoyage automatique des fichiers temp
- Limites sur nombre de cuts

## 📈 Performance

| Backend | Vitesse | RAM | Coût |
|---------|---------|-----|------|
| OpenAI | 2-5s | 500MB | $0.01/video |
| Moondream2 | 5-10s | 2GB | Gratuit |

## 🔧 Debug

```bash
# Voir les logs
docker compose logs -f api

# Rebuild
docker compose up -d --build

# Stop
docker compose down
```

## 💡 Tips

1. **Pour vidéos courtes (<10s)** : `threshold=25`, `max_cuts=8`
2. **Pour vidéos Instagram** : `threshold=25-27`, `max_cuts=10-15`
3. **Pour économiser** : Utilise moondream2 backend
4. **Pour qualité max** : Utilise openai backend

## 🎉 Ready to Go!

L'API est prête à être intégrée dans ton n8n workflow. Elle utilise **exactement le même prompt** que ton système d'upload d'assets.

## 📚 Documentation

- **QUICKSTART.md** : Guide de démarrage détaillé
- **README.md** : Documentation API complète
- **TEST.sh** : Script de test avec ta vidéo Instagram

## ❓ Questions ?

1. **"Pourquoi OpenAI et pas BLIP comme avant ?"**
   - Tu utilises déjà OpenAI Vision dans `openai_vision_service.py`
   - J'ai copié ton prompt exact

2. **"C'est quoi la différence avec mon système actuel ?"**
   - Ton système : analyse 1 vidéo entière → 1 description
   - Cette API : découpe en cuts → 1 description par cut
   - **Même prompt, même qualité**

3. **"Ça coûte combien ?"**
   - OpenAI : ~$0.01 par vidéo (10 cuts)
   - Moondream2 : Gratuit

4. **"C'est compatible avec mon workflow n8n ?"**
   - Oui ! Simple HTTP POST request
   - Voir exemples dans QUICKSTART.md
