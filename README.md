# Universial-Video-Downloader

## Projektstruktur
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

