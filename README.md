# CheapShark CLI 🎮
 
Ein Python-Projekt das Spiele-Deals von der [CheapShark API](https://apidocs.cheapshark.com/) abruft und in einer lokalen SQLite-Datenbank speichert.
 
---
 
## Projektbeschreibung
 
Dieses Projekt wurde im Rahmen eines Schulprojekts entwickelt. Es zeigt wie man:
- Daten von einer REST-API abruft
- Die Daten in JSON-Format verarbeitet
- Die Daten in einer relationalen SQL-Datenbank speichert
- Ein CLI-Menü zur Benutzerinteraktion baut
 
---
 
## Projektstruktur
 
```
Schulprojekt/
│
├── api/
│   ├── __init__.py
│   └── fetch_data.py       # API-Abfragen zur CheapShark API
│
├── db/
│   ├── __init__.py
│   ├── create_tables.py    # Erstellt die Datenbanktabellen
│   └── insert_data.py      # Fügt Daten in die Datenbank ein
│
├── tests/
│   ├── test_api.py         # Tests für die API-Abfragen
│   └── test_db.py          # Tests für die Datenbank
│
├── docs/
│   └── er_modell.html      # ER-Diagramm der Datenbankstruktur
│
├── main.py                 # Einstiegspunkt / CLI-Menü
└── README.md
```
 
---
 
## Installation
 
**1. Repository klonen**
```bash
git clone https://github.com/kushyme/schulprojekt.git
cd Schulprojekt
```
 
**2. Datenbank erstellen**
```bash
python3 db/create_tables.py
```
 
---
 
## Verwendung
 
Programm starten:
```bash
python3 main.py
```
 
Das CLI-Menü bietet folgende Optionen:
 
| Option | Beschreibung |
|--------|-------------|
| `1` | Alle Stores anzeigen |
| `2` | Aktuelle Deals anzeigen |
| `3` | Deal per ID suchen |
| `4` | Spiele per Titel suchen |
| `5` | Spiel per ID suchen |
| `6` | Preisalarm setzen |
| `7` | Preisalarm löschen |
| `0` | Beenden |
 
---
 
## Datenbankstruktur
 
Das Projekt verwendet drei Tabellen mit folgenden Beziehungen:
 
```
stores  ──1:n──►  deals  ◄──n:1──  games
```
 
- **stores** — alle verfügbaren Shops (Steam, GOG, Fanatical, etc.)
- **games** — Spieltitel mit günstigstem Preis
- **deals** — einzelne Angebote mit Preis, Rabatt und Bewertung
 
---
 
## Tests
 
API-Tests ausführen:
```bash
python3 -m unittest tests/test_api.py -v
```
 
Datenbank-Tests ausführen:
```bash
python3 -m unittest tests/test_db.py -v
```
 
---
 
## Verwendete Technologien
 
- **Python 3** — Programmiersprache
- **requests** — HTTP-Anfragen an die API
- **sqlite3** — lokale Datenbank (in Python eingebaut)
- **unittest** — Tests (in Python eingebaut)
 
---
 
## API
 
Dieses Projekt verwendet die [CheapShark API](https://apidocs.cheapshark.com/):
- Keine Authentifizierung notwendig
- Kostenfrei nutzbar
- Gibt Daten im JSON-Format zurück
