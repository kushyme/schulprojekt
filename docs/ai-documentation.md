## Datum: 04.05.2026

- Nix pkgs unfree license (mongodb, monge-ce)
- gelöst durch docker-compose.yml
- DB-Verbindung getestet -> funktioniert
- lokales testen mit mongosh (mongodb kennenlernen, abfragen testen etc.)  (https://gist.github.com/bradtraversy/f407d642bdc3b31681bc7e56d95485b6)


#### KI-Nutzung:
- Prompt: bitte hilf mir eine mongodb mit hilfe von docker compose aufzusetzen
- Prompt: ich habe eine docker compose mit mongodb am laufen. Bitte schreibe ein kleines python file welches pymongo verwendet um sich zu der db zu verbinden und einen eintrag zu schreiben.

## Datum: 05.05.2026
- cli-interface bearbeitet -> Menü für den Nutzer erstellt
- Menüoptionen getestet -> funktioniert
- Funktionen aktuell noch mit Placeholdern gefüllt: https://github.com/kushyme/flashcard-cli/commit/b9ac548b2354cfcf17b98641400a2ab9ad1c6f48
- mit dem Grundgerüst eine Datenstruktur überlegt -> Vorder-,Rückseite,Deck
- API funktioniert noch nicht 



#### KI-Nutzung:
-Du erhältst eine Python CLI-Flashcard-App. Implementiere alle Funktionen, die aktuell nur als Gerüst bestehen. Die gesamte Interaktion läuft über die Kommandozeile (keine GUI).
Die App kommuniziert ausschließlich über eine externe REST-API. Basis-URL: http://localhost:1337. Alle Daten werden über HTTP-Requests abgerufen und gespeichert – es gibt keine lokale Datenhaltung. Verwende die requests-Bibliothek.
Implementiere folgende Funktionen vollständig:

study() – Zeigt dem Nutzer alle verfügbaren Decks zur Auswahl (GET /decks). Nach der Auswahl werden alle Flashcards des Decks abgerufen (GET /decks/{id}/flashcards) und nacheinander angezeigt: zuerst nur die Frage, dann kann der Nutzer die Karte „umdrehen" (Eingabe bestätigen), woraufhin die Lösung erscheint. Danach folgt die nächste Karte, bis alle Karten des Decks durchgegangen sind.
edit_flashcard() – Der Nutzer gibt eine UUID ein. Die Flashcard wird abgerufen (GET /flashcards/{uuid}) und anschließend kann er Frage und/oder Lösung bearbeiten. Die Änderungen werden gespeichert (PUT /flashcards/{uuid}).
create_flashcard() – Alle vorhandenen Decks werden aufgelistet (GET /decks). Der Nutzer wählt ein Deck aus und gibt Frage und Lösung ein. Die neue Flashcard wird erstellt (POST /flashcards).
delete_flashcard() – Der Nutzer gibt eine UUID ein. Die entsprechende Flashcard wird gelöscht (DELETE /flashcards/{uuid}).
edit_category() – Der Nutzer gibt eine UUID ein. Die Category wird abgerufen (GET /categories/{uuid}) und anschließend kann er sie bearbeiten. Die Änderungen werden gespeichert (PUT /categories/{uuid}).
create_category() – Der Nutzer gibt einen Namen ein. Die neue Category wird erstellt (POST /categories).
delete_category() – Der Nutzer gibt eine UUID ein. Die entsprechende Category wird gelöscht (DELETE /categories/{uuid}).
show_flashcards() – Alle Categories werden aufgelistet (GET /categories). Der Nutzer wählt eine aus und bekommt alle Flashcards dieser Category mit UUID angezeigt (GET /categories/{uuid}/flashcards).
show_decks() – Alle vorhandenen Categories werden mit UUID aufgelistet (GET /categories).

Allgemeine Hinweise:

Behalte die bestehende Struktur und alle vorhandenen Funktionen bei – ändere nur die Gerüst-Funktionen.
Nutze ausschließlich CLI-Eingaben (input()) und Ausgaben (print()).
Validiere UUIDs und gib sinnvolle Fehlermeldungen aus, wenn eine UUID nicht gefunden wird oder die API einen Fehler zurückgibt (z. B. HTTP 404, 500).
Behandle Verbindungsfehler zur API sauber mit einer verständlichen Fehlermeldung.
Halte den Code sauber, lesbar und konsistent mit dem bestehenden Stil.


## Datum: 06.05.2026

- API gefixt -> mithilfe von GitHub Co-Pilot
- docker-compose angepasst 
- Anpassungen nötig nachdem wir einen client hatten welcher auf eine http rest api ausgelegt war, wir uns aber unstimmig waren und uns dann für eine lokale mit python exports entschieden haben


#### KI-Nutzung
- GitHub Copilot das gesamte Repo als kontext gegeben, er konnte sich alle files angucken und hat daraus eine passende API generiert