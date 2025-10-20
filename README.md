# Video Analysis API 🎥

Ultra-simple API pour analyser des vidéos, détecter les cuts et générer des descriptions IA.

## 🚀 Quick Start

```bash
# 1. Configuration
cp .env.example .env
# Edite .env et change API_KEY

# 2. Démarrage
docker compose up -d

# 3. Test
curl -H "x-api-key: your-secret-key" http://localhost:8190/health
```

## 📡 API Endpoints

### Health Check

```bash
curl http://localhost:8190/health
```

**Response:**
```json
{
  "ok": true,
  "model_loaded": false
}
```

### Analyze Video

```bash
curl -X POST http://localhost:8190/analyze \
  -H "x-api-key: your-secret-key" \
  -F "url=https://example.com/video.mp4" \
  -F "threshold=27.0" \
  -F "max_cuts=30"
```

**Parameters:**
- `url` (required): URL de la vidéo (Instagram, S3, CDN, etc.)
- `threshold` (optional): Sensibilité de détection des cuts (default: 27.0)
  - Plus bas = plus de cuts détectés
  - Recommandé: 25-30 pour vidéos dynamiques, 20-25 pour vidéos statiques
- `max_cuts` (optional): Nombre maximum de cuts à analyser (default: 30)

**Response:**
```json
{
  "clips": [
    {
      "order": 1,
      "start": 0.0,
      "end": 1.5,
      "duration": 1.5,
      "description": "a small pool surrounded by trees and bushes"
    },
    {
      "order": 2,
      "start": 1.5,
      "end": 2.8,
      "duration": 1.3,
      "description": "a person holding a cup of tea and a book"
    }
  ],
  "texts": []
}
```

## 🔧 Configuration

### Variables d'environnement

| Variable | Description | Default |
|----------|-------------|---------|
| `API_KEY` | Clé API pour authentification | `your-secret-key` |
| `PORT` | Port exposé | `8190` |
| `CAPTION_PROMPT` | Prompt personnalisé pour l'IA | Prompt par défaut |

### Personnaliser le prompt IA

Édite `.env` pour changer le prompt selon ton cas d'usage :

```bash
# Pour hôtels de luxe
CAPTION_PROMPT="Describe this luxury hotel scene in one sentence, emphasizing elegance, comfort and premium amenities."

# Pour restaurants
CAPTION_PROMPT="Describe this dining scene in one sentence, highlighting the food presentation, ambiance and culinary details."

# Pour voyages/aventure
CAPTION_PROMPT="Describe this travel scene in one sentence, capturing the destination, atmosphere and sense of adventure."
```

## 🔬 Exemples avec n8n

### Node HTTP Request

```json
{
  "method": "POST",
  "url": "http://localhost:8190/analyze",
  "headers": {
    "x-api-key": "your-secret-key"
  },
  "bodyParameters": {
    "parameters": [
      {
        "name": "url",
        "value": "={{ $json.video_url }}"
      },
      {
        "name": "threshold",
        "value": "27"
      },
      {
        "name": "max_cuts",
        "value": "20"
      }
    ]
  },
  "options": {
    "timeout": 300000
  }
}
```

### Exemple avec vidéo Instagram

```bash
curl -X POST http://localhost:8190/analyze \
  -H "x-api-key: your-secret-key" \
  -F "url=https://scontent-lax3-1.cdninstagram.com/o1/v/t16/f2/m86/AQMhQBW9nNDrEg76Om3itggV6htOVUFu4jpcQQPKnoIDo3tTiuxJwSIsTxjp9Ch-SN90UdfZh-GGXLZmpeFkj80TjcFgg6vd9edLXz4.mp4?stp=dst-mp4&efg=eyJxZV9ncm91cHMiOiJbXCJpZ193ZWJfZGVsaXZlcnlfdnRzX290ZlwiXSIsInZlbmNvZGVfdGFnIjoidnRzX3ZvZF91cmxnZW4uY2xpcHMuYzIuNzIwLmJhc2VsaW5lIn0&_nc_cat=110&vs=1783337319281816_1984711560" \
  -F "threshold=25" \
  -F "max_cuts=15"
```

## 🐛 Troubleshooting

### Le modèle est lent à charger

Le premier appel prend 30-60 secondes (téléchargement du modèle moondream2). Les appels suivants sont rapides (~2-5s par vidéo).

### Erreur "Failed to download video"

- Vérifie que l'URL est accessible
- Pour Instagram, les URLs expirent après quelques heures
- Certains CDNs bloquent le user-agent de `requests`

### Out of Memory

Réduis `max_cuts` ou augmente la RAM du container :

```yaml
# docker-compose.yml
mem_limit: 6g  # Au lieu de 4g
```

## 📊 Performance

- **Premier appel:** 30-60s (chargement modèle)
- **Appels suivants:** 2-5s pour vidéo de 10 secondes
- **RAM:** ~2-3 GB avec modèle chargé
- **CPU:** Optimisé pour CPU (pas de GPU requis)

## 🔐 Sécurité

- Toujours utiliser `x-api-key` header
- Ne jamais commit `.env` avec vraie clé
- Limiter l'accès réseau au container en production

## 📝 Logs

```bash
# Voir les logs
docker compose logs -f api

# Voir uniquement les erreurs
docker compose logs api | grep ERROR
```

## 🛠️ Development

```bash
# Rebuild après changement de code
docker compose up -d --build

# Mode dev avec hot reload
docker compose -f docker-compose.dev.yml up
```
