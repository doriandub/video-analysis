# 🚀 Quick Start - Video Analysis API

API ultra-simple pour analyser des vidéos Instagram/S3/CDN et générer des descriptions **keywords** (comme ton système actuel).

## Installation rapide

```bash
cd /Users/doriandubord/Desktop/hospup-project/video-analysis-api

# 1. Configure ton API key
cp .env.example .env

# Edite .env et ajoute:
# CAPTION_BACKEND=openai
# OPENAI_API_KEY=sk-...
# API_KEY=ton-secret-key

# 2. Build et démarre
docker compose up -d --build

# 3. Test
curl http://localhost:8190/health
```

## 🎯 Exemple avec ta vidéo Instagram

```bash
curl -X POST http://localhost:8190/analyze \
  -H "x-api-key: ton-secret-key" \
  -F "url=https://scontent-lax3-1.cdninstagram.com/o1/v/t16/f2/m86/AQMhQBW9nNDrEg76Om3itggV6htOVUFu4jpcQQPKnoIDo3tTiuxJwSIsTxjp9Ch-SN90UdfZh-GGXLZmpeFkj80TjcFgg6vd9edLXz4.mp4?..." \
  -F "threshold=25" \
  -F "max_cuts=15"
```

**Résultat attendu** (même format que ton exemple) :

```json
{
  "clips": [
    {
      "order": 1,
      "start": 0.0,
      "end": 1.5,
      "duration": 1.5,
      "description": "pool, trees, bushes, water, deck"
    },
    {
      "order": 2,
      "start": 1.5,
      "end": 2.8,
      "duration": 1.3,
      "description": "person, tea cup, book, table, hands"
    }
  ],
  "texts": []
}
```

## 🔧 Configuration Backends

### Option 1: OpenAI Vision (Recommandé - comme ton système actuel)

```bash
# .env
CAPTION_BACKEND=openai
OPENAI_API_KEY=sk-proj-...
```

**Avantages:**
- Même qualité que ton système actuel
- Utilise ton prompt hospitality exact
- Rapide (~2-3s par vidéo)
- Pas besoin de GPU

**Coût:** ~$0.01 par vidéo (10 cuts)

### Option 2: Moondream2 Local (Gratuit mais moins bon)

```bash
# .env
CAPTION_BACKEND=moondream2
```

**Avantages:**
- Gratuit
- Pas d'API externe

**Inconvénients:**
- Qualité inférieure
- Plus lent (5-10s par vidéo)
- Nécessite ~2GB RAM

## 📊 Paramètres

| Paramètre | Description | Défaut | Recommandé |
|-----------|-------------|--------|------------|
| `threshold` | Sensibilité détection cuts | 27.0 | 20-30 |
| `max_cuts` | Nombre max de cuts | 30 | 15-20 |

**Pour threshold:**
- **20-25** : Vidéos statiques (peu de mouvement)
- **25-30** : Vidéos dynamiques (Instagram, TikTok)
- **30-35** : Très peu de cuts (seulement transitions marquées)

## 🔗 Intégration n8n

```json
{
  "method": "POST",
  "url": "http://localhost:8190/analyze",
  "headers": {
    "x-api-key": "{{ $env.VIDEO_API_KEY }}"
  },
  "bodyParameters": {
    "parameters": [
      {
        "name": "url",
        "value": "={{ $json.video_url }}"
      },
      {
        "name": "threshold",
        "value": "25"
      },
      {
        "name": "max_cuts",
        "value": "15"
      }
    ]
  }
}
```

## 🐛 Troubleshooting

### "Invalid API key"
- Vérifie que `x-api-key` header = `API_KEY` dans `.env`

### "OPENAI_API_KEY not configured"
- Ajoute `OPENAI_API_KEY=sk-...` dans `.env`
- Redémarre: `docker compose restart`

### Vidéo Instagram expire
- Les URLs Instagram expirent après ~24h
- Réextrait l'URL depuis Instagram avant chaque call

### Trop lent
- Réduis `max_cuts` à 10-15
- Utilise `threshold=30` pour moins de cuts

## 📝 Logs

```bash
# Voir les logs
docker compose logs -f api

# Voir les descriptions générées
docker compose logs api | grep "✅ OpenAI"
```

## 💡 Tips

1. **Pour vidéos courtes (<10s)** : `threshold=25`, `max_cuts=10`
2. **Pour vidéos longues (>30s)** : `threshold=30`, `max_cuts=20`
3. **Pour économiser** : Utilise moondream2 backend (gratuit)
4. **Pour qualité max** : Utilise openai backend avec gpt-4o-mini

## ⚡ Performance

- **OpenAI Vision:** 2-5s par vidéo (10 cuts)
- **Moondream2:** 5-10s par vidéo (10 cuts)
- **RAM:** 500MB (openai) ou 2GB (moondream2)
- **CPU:** 1-2 cores suffisent

## 🎉 C'est prêt !

Ton API utilise maintenant **exactement le même prompt** que ton système actuel d'upload des assets. Les descriptions sont dans le même format (keywords séparés par virgules).
