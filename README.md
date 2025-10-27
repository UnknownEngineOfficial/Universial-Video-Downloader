# 🎥 Universal Video Downloader

Ein leistungsstarker Video-Downloader, der Videos von über 1000+ Plattformen herunterladen kann. Basierend auf **yt-dlp** mit einem modernen FastAPI-Backend und einer benutzerfreundlichen Web-Oberfläche.

## ✨ Features

- 🌐 **1000+ Plattformen**: YouTube, Vimeo, Dailymotion, TikTok, Instagram, Twitter, Pornhub und viele mehr
- 🎬 **Mehrere Qualitäten**: Wähle zwischen verschiedenen Video-Qualitäten und Formaten
- 🚀 **Schnell & Zuverlässig**: Basiert auf yt-dlp, dem besten Video-Downloader
- 🎨 **Moderne UI**: Schöne, responsive Web-Oberfläche
- 🐳 **Docker-Ready**: Einfache Installation mit Docker Compose
- 🔒 **CORS-Sicher**: Nginx Reverse Proxy löst alle CORS-Probleme

## 🚀 Schnellstart

### Mit Docker (Empfohlen)

```bash
# Repository klonen
git clone https://github.com/UnknownEngineOfficial/Universial-Video-Downloader.git
cd Universial-Video-Downloader

# Setup-Script ausführen
chmod +x setup.sh
./setup.sh
```

Das war's! Die Anwendung läuft jetzt auf:
- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **API Dokumentation**: http://localhost:8000/docs

### Manuell (ohne Docker)

```bash
# Backend starten
cd backend
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Frontend (in neuem Terminal)
cd frontend
python -m http.server 3000
```

## 📖 Verwendung

1. Öffne http://localhost im Browser
2. Füge eine Video-URL ein (z.B. von YouTube)
3. Klicke auf "Analysieren"
4. Wähle die gewünschte Qualität
5. Download startet automatisch

## 🏗️ Projektstruktur
```
video-downloader/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI application
│   │   ├── config.py                  # Configuration & environment variables
│   │   ├── models.py                  # Pydantic models
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── download.py            # Download endpoints
│   │       └── info.py                # Info endpoints
│   ├── extractors/
│   │   ├── __init__.py
│   │   ├── base.py                    # Base extractor class
│   │   ├── pornhub.py                 # Pornhub extractor
│   │   ├── youtube.py                 # YouTube extractor
│   │   └── generic.py                 # Generic extractor
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── validators.py
│   │   └── downloader.py
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
│
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   ├── app.js
│   │   ├── api.js
│   │   └── ui.js
│   └── assets/
│       └── images/
│
├── docker-compose.yml
├── nginx.conf
├── README.md
└── .gitignore
```

## Architektur-Diagramm
```
┌─────────────────┐
│   Browser       │
│   (Frontend)    │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│   Nginx         │ ◄── CORS, SSL, Rate Limiting
│   Reverse Proxy │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   FastAPI       │
│   Backend       │ ◄── Video extraction logic
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌─────────────┐
│yt-dlp  │ │  Custom     │
│        │ │  Extractors │
└────────┘ └─────────────┘
    │            │
    └────┬───────┘
         ▼
┌─────────────────┐
│ Video Platforms │
└─────────────────┘
```

## 🛠️ Technologie-Stack

**Backend:**
- Python 3.11+
- FastAPI (Web Framework)
- yt-dlp (Video Extraktion)
- Pydantic (Datenvalidierung)
- Uvicorn (ASGI Server)

**Frontend:**
- Vanilla JavaScript (ES6+)
- HTML5 & CSS3
- Responsive Design

**Infrastructure:**
- Docker & Docker Compose
- Nginx (Reverse Proxy)

## 📡 API Endpunkte

### Health Check
```http
GET /api/health
```

### Video Information extrahieren
```http
POST /api/info/extract
Content-Type: application/json

{
  "url": "https://www.youtube.com/watch?v=..."
}
```

### Direkter Download
```http
GET /api/download/direct?url=VIDEO_URL&format_id=FORMAT_ID
```

## 🔧 Konfiguration

Bearbeite `backend/.env` für eigene Einstellungen:

```env
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
CORS_ORIGINS=http://localhost,http://localhost:80
LOG_LEVEL=INFO
MAX_VIDEO_SIZE_MB=1000
```

## 🐳 Docker Befehle

```bash
# Starten
docker-compose up -d

# Logs anzeigen
docker-compose logs -f

# Stoppen
docker-compose down

# Neu bauen
docker-compose up -d --build

# Nur Backend neu starten
docker-compose restart backend
```

## 🧪 Entwicklung

```bash
# Backend entwickeln
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend entwickeln
cd frontend
# Öffne index.html im Browser oder nutze einen lokalen Server
python -m http.server 3000
```

## 📝 Unterstützte Plattformen (Auswahl)

- YouTube
- Vimeo
- Dailymotion
- TikTok
- Instagram
- Twitter/X
- Facebook
- Reddit
- Twitch
- Pornhub
- und 1000+ weitere...

Vollständige Liste: [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)

## 🤝 Beitragen

Contributions sind willkommen! Bitte erstelle einen Pull Request oder öffne ein Issue.

## 📄 Lizenz

Siehe [LICENSE](LICENSE) Datei.

## ⚠️ Haftungsausschluss

Dieses Tool ist nur für den persönlichen Gebrauch bestimmt. Respektiere die Urheberrechte und Nutzungsbedingungen der Video-Plattformen.

## 🙏 Credits

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Das Herzstück dieses Projekts
- [FastAPI](https://fastapi.tiangolo.com/) - Modernes Python Web Framework
- [Nginx](https://nginx.org/) - Reverse Proxy Server

---

Made with ❤️ by [UnknownEngineOfficial](https://github.com/UnknownEngineOfficial)

