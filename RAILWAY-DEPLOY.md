# 🚂 Déploiement Railway - Video Analysis API

## Méthode 1: Depuis GitHub (Recommandé)

### 1. Push vers GitHub

```bash
cd /Users/doriandubord/Desktop/hospup-project/video-analysis-api

# Initialise git si pas déjà fait
git init
git add .
git commit -m "Video Analysis API with hospitality prompt"

# Crée un repo GitHub et push
gh repo create video-analysis-api --private --source=. --push
# OU si tu préfères manual:
# git remote add origin https://github.com/TON-USERNAME/video-analysis-api.git
# git push -u origin main
```

### 2. Déploie sur Railway

1. Va sur https://railway.app
2. Click **"New Project"**
3. Click **"Deploy from GitHub repo"**
4. Sélectionne `video-analysis-api`
5. Railway détecte automatiquement le `Dockerfile`

### 3. Configure les variables

Dans Railway Dashboard → Variables:

```bash
API_KEY=ton-secret-key-super-secure
CAPTION_BACKEND=openai
# OPENAI_API_KEY est déjà configuré ✅
```

**C'est tout !** Railway build et deploy automatiquement. 🎉

---

## Méthode 2: Depuis CLI Railway

```bash
# Install Railway CLI
brew install railway

# Login
railway login

# Link to project (ou crée un nouveau)
railway link

# Deploy
railway up

# Configure variables
railway variables set API_KEY=ton-secret-key
railway variables set CAPTION_BACKEND=openai
# OPENAI_API_KEY déjà présent ✅
```

---

## 📋 Variables d'environnement requises

| Variable | Valeur | Déjà sur Railway ? |
|----------|--------|-------------------|
| `OPENAI_API_KEY` | sk-proj-... | ✅ Déjà configuré |
| `API_KEY` | ton-secret-key | ❌ À ajouter |
| `CAPTION_BACKEND` | openai | ❌ À ajouter |
| `PORT` | (auto) | ✅ Railway le set |

**Donc tu dois juste ajouter:**
1. `API_KEY` (pour sécuriser ton API)
2. `CAPTION_BACKEND=openai`

---

## 🔗 Après déploiement

Railway te donnera une URL type:
```
https://video-analysis-api-production.up.railway.app
```

### Test

```bash
# Health check
curl https://TON-URL.railway.app/health

# Analyze video
curl -X POST https://TON-URL.railway.app/analyze \
  -H "x-api-key: ton-secret-key" \
  -F "url=https://instagram.com/video.mp4" \
  -F "threshold=25" \
  -F "max_cuts=15"
```

---

## 💰 Coûts Railway

- **Hobby Plan**: $5/mois - 500h incluses
- Cette API consomme: ~0.5GB RAM, minimal CPU
- Estimation: **<$1/mois** en plus de ton usage actuel

---

## 🔧 Configuration avancée (optionnel)

### Ressources

Railway détecte automatiquement mais tu peux ajuster:

```toml
# railway.toml (déjà créé)
[build]
builder = "dockerfile"

[deploy]
healthcheckPath = "/health"
restartPolicyType = "on_failure"
```

### Logs

```bash
railway logs
```

### Redeploy

```bash
# Auto sur chaque git push
git push

# Ou manual
railway up
```

---

## 🎯 Intégration n8n

Une fois déployé, utilise l'URL Railway dans n8n:

```json
{
  "url": "https://TON-URL.railway.app/analyze",
  "headers": {
    "x-api-key": "{{ $env.VIDEO_API_KEY }}"
  }
}
```

---

## 🐛 Troubleshooting

### Build failed

```bash
# Vérifie les logs
railway logs

# Souvent: requirements.txt incomplet
# → Rebuild: railway up --detach
```

### "Invalid API key"

- Vérifie que `API_KEY` est bien défini dans Railway Variables
- Match avec le header `x-api-key` dans ta requête

### "OPENAI_API_KEY not configured"

- Vérifie que `CAPTION_BACKEND=openai` est défini
- Vérifie que `OPENAI_API_KEY` existe (devrait déjà être là)

---

## ✅ Checklist déploiement

- [ ] Code pushed sur GitHub
- [ ] Projet créé sur Railway
- [ ] Variables configurées (API_KEY, CAPTION_BACKEND)
- [ ] Build réussi (voir Railway dashboard)
- [ ] Health check OK: `curl https://URL/health`
- [ ] Test analyze: `curl -X POST https://URL/analyze ...`
- [ ] Intégré dans n8n

**C'est prêt !** 🚀
