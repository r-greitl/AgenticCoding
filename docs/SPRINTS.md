Sprint 3 wird freigegeben.

Feature:
Optionale Kontaktkategorien

Freigabegrund:
- Akzeptanzkriterien erfüllt
- Architekturregeln eingehalten
- unabhängiger Review erfolgreich
- 41 automatische Tests bestanden
- 6 zusätzliche Kategorienfälle unabhängig geprüft
- keine freigaberelevanten offenen Probleme

Bekannte Einschränkungen:
- unbekannte Kategorien werden als "keine Kategorie" behandelt
- mehrere Kategorien werden nicht unterstützt
- GUI-Interaktionen wurden nicht automatisiert getestet

Freigabe erteilt.
## Sprint 4 – Kontaktfotos

### Ziel

Kontakte können optional genau ein Foto besitzen.

### Qualitätssicherung

- Planning Agent eingesetzt
- Coding Agent eingesetzt
- unabhängiger Review Agent eingesetzt
- Review-Blocker korrigiert und erneut unabhängig geprüft
- 60 automatische Tests erfolgreich
- `git diff --check` erfolgreich
- manuelle GUI-Akzeptanztests erfolgreich

### Bekannte Einschränkungen

- nur PNG und GIF
- keine Inhaltsvalidierung der Bilddateien
- keine hochwertige Bildskalierung
- fehlgeschlagene Bildlöschungen werden nicht protokolliert

### Freigabe

Status: FREIGEGEBEN

Automatische und manuelle Akzeptanztests wurden erfolgreich abgeschlossen.

Datum: 17.08.2026
## Sprint 5 – GUI entkoppeln und testbar machen

Status: abgeschlossen

Umgesetzt:
- GUI-Startlogik vom Modulimport entkoppelt
- `import kontaktbuch_gui` startet keine GUI mehr
- Kontakte werden beim Import nicht geladen
- Tkinter-Fenster und Widgets werden erst beim Programmstart erzeugt
- explizite Initialisierung von Laufzeitdaten, Oberfläche und Ereignissen
- Start über `main()` und `if __name__ == "__main__":`
- bestehende globale Callback-Struktur bewusst beibehalten
- keine App-Klasse eingeführt

Qualitätssicherung:
- 66 automatische Tests bestanden
- unabhängiger Review: FREIGEBEN
- Syntaxprüfung erfolgreich
- `git diff --check` erfolgreich
- manuelle GUI-Regressionstests erfolgreich
- headless Import ohne GUI-Nebenwirkungen geprüft

Bekannter, nicht durch Sprint 5 verursachter Fehler:
- bestimmte kommagetrennte Outlook-CSV-Dateien können bei fehlgeschlagener
  automatischer Trennzeichenerkennung nicht importiert werden
- separater Bugfix vorgesehen

Freigabe erteilt.