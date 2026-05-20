# KARO Benefits HR-Leistungsverwaltung

[![license](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE.md)

Eine webbasierte HR-Benefits-Management-App für die KARO GmbH mit DATEV-Export für die Lohnabrechnung.

## 🎯 Features

- **Admin-Dashboard:** Mitarbeitende, Leistungskatalog, Buchungen verwalten
- **Flexibler DATEV-Export:** Lohnart-Nummern direkt im Admin-Panel eingeben (kein Code-Redeploy nötig)
- **Freibetrag-Prüfung:** Automatische Warnung bei Sachbezügen > €50
- **Mitarbeiter-Portal:** Eigene Leistungsübersicht + PDF-Download
- **PWA:** Offline-Funktionalität und Installation auf dem Startbildschirm
- **Native Apps:** Capacitor ermöglicht Android & iOS Apps
- **Audit-Logging:** Vollständige Änderungsverfolgung
- **Rollenbasierte Zugriffe:** Admin vs. Mitarbeiter

## 🛠 Tech-Stack

- **Backend:** Python 3.11+ | FastAPI | SQLite
- **Frontend:** React 18 | Vite | Tailwind CSS
- **Mobile:** PWA + Capacitor (Android & iOS)
- **Auth:** JWT + bcrypt
- **Export:** DATEV Lodas CSV (Windows-1252)

## 📦 Quick Start (Lokal)

### Voraussetzungen
- Python 3.11+
- Node.js 18+
- `pip` und `npm`

### 1. Backend starten

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Datenbank initialisieren und Demo-Daten laden
python seed.py

# FastAPI starten
uvicorn app.main:app --reload
```

Server läuft unter: **http://localhost:8000**

API-Docs: **http://localhost:8000/docs**

### 2. Frontend starten (neues Terminal)

```bash
cd frontend
npm install
npm run dev
```

App läuft unter: **http://localhost:5173**

### 3. Anmelden

```
Email:    admin@karo-gmbh.de
Passwort: KaroAdmin2026!
```

---

## 🚀 Docker-Deployment

```bash
docker-compose up -d
```

- Backend: http://localhost:8000
- Frontend: http://localhost:5173

---

## 📋 Datenbankschema

### Haupttabellen

| Tabelle | Beschreibung |
|---------|------------|
| `employees` | Mitarbeitende (Personalnummer, E-Mail, Abteilung) |
| `benefit_types` | Leistungskatalog (Name, Kategorie, Max.-Betrag, DATEV-Lohnart-Nr.) |
| `benefit_assignments` | Monatliche Leistungszuweisungen |
| `users` | Anmeldedaten (Admin + Mitarbeiter) |
| `audit_log` | Audit-Trail aller Änderungen |
| `export_log` | DATEV-Export-Historie |

---

## 🔑 Admin-Workflow

### 1. Leistungskatalog konfigurieren

1. Im Admin-Panel → **Leistungskatalog**
2. Leistungsart anlegen oder öffnen
3. **DATEV-Lohnart-Nr.** eintragen (z.B. "0280")
   - Format: Genau 4 Ziffern
   - Kann jederzeit nachgetragen werden (Inline-Bearbeitung mit ✎-Icon)

### 2. Mitarbeitende verwalten

- **Admin** → **Mitarbeitende**
- Mitarbeiter anlegen, bearbeiten, deaktivieren
- Personalnummer (DATEV-Feld) ist erforderlich

### 3. Leistungen zuweisen

- **Admin** → **Buchungen** → **Neue Buchung**
- Monat, Mitarbeiter, Leistungsart, Betrag
- System warnt vor Freibetrag-Überschreitung (SACHBEZUG > €50)

### 4. DATEV-Export

- **Admin** → **DATEV-Export**
- Zeitraum und ggf. Mitarbeitende filtern
- **Vorschau** anzeigen (zeigt Warnungen bei fehlenden Lohnart-Nummern)
- **CSV herunterladen**
  - Format: Windows-1252 (ANSI)
  - Dezimaltrennzeichen: Komma
  - Semikolon als Trennzeichen

---

## 📱 Mobile Nutzung

### PWA (Browser)

1. App öffnen: **http://localhost:5173**
2. Im mobilen Chrome/Safari auf Menu → **"Zum Startbildschirm"** oder **"Zur Home hinzufügen"**
3. App läuft offline (gecachte Inhalte)

### Android-App (native)

Voraussetzung: Android Studio

```bash
cd frontend
npm run build
npx cap add android  # einmalig
npx cap sync
npx cap open android # öffnet Android Studio
```

In Android Studio: **Run** → wählt Device/Emulator

### iOS-App (native)

Voraussetzung: macOS, Xcode, Apple Developer Account

```bash
cd frontend
npm run build
npx cap add ios  # einmalig, nur macOS
npx cap sync
npx cap open ios  # öffnet Xcode
```

In Xcode: **Product** → **Run** oder Simulator

---

## 🔐 Sicherheit

- ✓ Passwörter: bcrypt mit Salt
- ✓ JWT Tokens: HS256, 8h Gültigkeit
- ✓ Rollenprüfung: Serverseitig auf jedem Endpunkt
- ✓ Parametrisierte Queries: SQLAlchemy ORM (kein SQL-Injection)
- ✓ Secrets: Nur über `.env` (nicht in Code)

### Produktionssetup

1. **JWT_SECRET_KEY** in `.env` setzen
2. **HTTPS** aktivieren
3. **CORS** nur für deine Domain erlauben
4. **Database URL** auf echten Datenbankserver ändern
5. Environment `DEBUG=False`

---

## 📊 API-Übersicht

### Authentication
- `POST /api/auth/login`
- `POST /api/auth/refresh`
- `POST /api/auth/change-password`

### Admin Endpoints
- `GET/POST /api/employees`
- `GET/POST /api/benefit-types`
- `GET/POST /api/assignments`
- `GET /api/export/preview` + `GET /api/export/csv`
- `GET /api/dashboard/stats`
- `GET /api/audit`

### Employee Endpoints
- `GET /api/me/assignments`
- `GET /api/me/assignments/summary`
- `GET /api/me/assignments/pdf`

---

## 🔧 Umgebungsvariablen

### Backend (`.env`)
```
DATABASE_URL=sqlite:///./karo_benefits.db
JWT_SECRET_KEY=your-super-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=8
```

### Frontend (`.env.local`)
```
VITE_API_URL=http://localhost:8000
```

---

## 📝 Initialdaten

Die `seed.py` erstellt:

- **Admin-User:** `admin@karo-gmbh.de` / `KaroAdmin2026!`
- **5 Leistungstypen:** SACHBEZUG, VERPFLEGUNG, MOBILITAET, GESUNDHEIT, SONSTIGES
  - *Hinweis:* DATEV-Lohnart-Nummern sind initial **NULL** und müssen im Admin-Panel eingegeben werden

Seeding ausführen:
```bash
cd backend
python seed.py
```

---

## 🎓 Empfohlene DATEV-Lohnart-Nummern

Diese Nummern müssen mit der Lohnbuchhaltung abgestimmt werden:

| Leistung | Empfehlung | Kategorie |
|----------|-----------|----------|
| Sachbezug Gutscheinkarte | 0280 | SACHBEZUG |
| Essenszuschuss | 0281 | VERPFLEGUNG |
| Jobticket | 0282 | MOBILITAET |
| Gesundheitsförderung | 0283 | GESUNDHEIT |
| Aufmerksamkeit | 0284 | SONSTIGES |

**WICHTIG:** Diese sind Vorschläge! Die tatsächlichen Nummern müssen mit eurem DATEV-Administrator / Lohnbuchhalter abgestimmt werden.

---

## ⚖️ Haftungsausschluss

Diese App ist **kein zertifiziertes DATEV-Produkt**. 

**Vor Produktiveinsatz:**
1. ✓ Alle CSV-Exporte mit der Lohnbuchhaltung prüfen lassen
2. ✓ Test-Lauf in der DATEV mit Beispieldaten durchführen
3. ✓ Datensicherung (Backups) einrichten
4. ✓ Zugriff und Berechtigungen absichern

---

## 🐛 Testing

```bash
cd backend
pytest tests/
```

---

## 📄 Lizenz

MIT © 2026 KARO GmbH

---

## 🤝 Support

Bei Fragen oder Fehlern öffne ein [Issue](https://github.com/Miriaparicio/KARO-Benefits/issues).

---

**Viel Erfolg mit KARO Benefits! 🎉**
