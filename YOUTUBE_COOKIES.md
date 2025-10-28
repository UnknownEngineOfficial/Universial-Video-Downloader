# YouTube Cookies für Video-Downloader

## Warum werden Cookies benötigt?

YouTube erfordert manchmal eine Anmeldung, um sicherzustellen, dass der Benutzer kein Bot ist. Dies ist Teil von YouTubes Schutzmaßnahmen gegen automatisierte Downloads. Um dieses Problem zu umgehen, können Sie Cookies von einem angemeldeten YouTube-Konto verwenden.

## Methode 1: Direkte Browser-Cookies verwenden (Empfohlen)

Diese Methode ist am einfachsten und erfordert keine manuelle Cookie-Extraktion:

1. Melden Sie sich in Ihrem Browser bei YouTube an

2. Aktualisieren Sie die `.env`-Datei im Backend-Verzeichnis:
   ```
   YOUTUBE_COOKIES_FROM_BROWSER=chrome  # oder firefox, edge, opera, safari, chromium, brave, vivaldi
   # Optional: Wenn Sie ein spezielles Browser-Profil verwenden:
   # YOUTUBE_COOKIES_BROWSER_PROFILE=/pfad/zum/profil
   ```

3. Starten Sie die Docker-Services neu:
   ```bash
   docker-compose down && docker-compose up -d --build
   ```

## Methode 2: Cookies-Datei verwenden

### Option A: Verwendung der Browser-Erweiterung "Get cookies.txt"

1. Installieren Sie die Browser-Erweiterung "Get cookies.txt" für [Chrome](https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid) oder [Firefox](https://addons.mozilla.org/de/firefox/addon/cookies-txt/)

2. Melden Sie sich bei Ihrem YouTube-Konto an

3. Besuchen Sie eine beliebige YouTube-Seite

4. Klicken Sie auf das Erweiterungssymbol und wählen Sie "Export cookies for this domain"

5. Speichern Sie die Datei als `cookies.txt`

### Option B: Manuelles Exportieren (Chrome)

1. Öffnen Sie Chrome und melden Sie sich bei YouTube an

2. Drücken Sie F12, um die Entwicklertools zu öffnen

3. Gehen Sie zum Tab "Application" (Anwendung)

4. Klicken Sie im linken Bereich auf "Cookies" und dann auf "https://www.youtube.com"

5. Klicken Sie mit der rechten Maustaste auf die Cookie-Tabelle und wählen Sie "Save as HAR with content"

6. Verwenden Sie ein Tool wie [EditThisCookie](https://www.editthiscookie.com/) oder einen Online-Converter, um die Cookies in das Netscape-Format (cookies.txt) zu konvertieren

### Verwendung der Cookies-Datei

1. Platzieren Sie die `cookies.txt`-Datei im Backend-Verzeichnis

2. Aktualisieren Sie die `.env`-Datei im Backend-Verzeichnis:
   ```
   YOUTUBE_COOKIES_FILE=/app/cookies.txt
   ```

3. Starten Sie die Docker-Services neu:
   ```bash
   docker-compose down && docker-compose up -d --build
   ```

## Wichtige Hinweise

- **Browser-Cookies-Methode**: Diese Methode ist am einfachsten und sollte zuerst probiert werden
- **Datenschutz**: Die Cookies enthalten sensible Informationen. Geben Sie sie niemals an Dritte weiter
- **Ablauf**: Cookies laufen nach einiger Zeit ab. Sie müssen sich gelegentlich neu bei YouTube anmelden
- **Sicherheit**: Verwenden Sie nur eigene Konten und beachten Sie die YouTube-Nutzungsbedingungen

## Alternative: Proxy verwenden

Wenn Sie keine Cookies verwenden möchten, können Sie auch einen Proxy konfigurieren:

```
YOUTUBE_PROXY=http://proxy-server:port
```

## Wichtige Hinweise

- **Datenschutz**: Die Cookies-Datei enthält sensible Informationen. Geben Sie sie niemals an Dritte weiter.
- **Ablauf**: Cookies laufen nach einiger Zeit ab. Sie müssen sie gelegentlich erneuern.
- **Sicherheit**: Verwenden Sie nur eigene Konten und beachten Sie die YouTube-Nutzungsbedingungen.

## Alternative Lösungen

Wenn Sie keine Cookies verwenden möchten, können Sie auch:

1. **Proxies verwenden**: Konfigurieren Sie Proxies in der `.env`-Datei:
   ```
   YOUTUBE_PROXY=http://proxy-server:port
   ```

2. **User-Agent-Rotation**: Diese wird automatisch vom System gehandhabt, aber Sie können sie anpassen, indem Sie die yt-dlp-Optionen erweitern.