# AGENT.md

# Projekt

Mein Kontaktbuch

Desktop-Anwendung zur Verwaltung persönlicher Kontakte.

Programmiersprache:
Python 3

GUI:
Tkinter

Datenspeicherung:
JSON

---

# Projektziel

Das Kontaktbuch soll einfach zu bedienen sein und langfristig
erweiterbar bleiben.

Neue Funktionen dürfen bestehende Funktionen nicht verschlechtern.

---

# Architektur

kontaktbuch_gui.py
→ Benutzeroberfläche

datei.py
→ Laden und Speichern

kontaktlogik.py
→ Suche, Sortierung, Dublettenprüfung

kontaktfelder.py
→ zentrale Felddefinitionen

dialoge.py
→ alle Messageboxen

kontaktexport.py
→ Export

kontaktimport.py
→ Import

validierung.py
→ Eingabeprüfung

styles.py
→ Farben und Layout

---

# Architekturregeln

Keine GUI-Logik außerhalb der GUI.

Keine Messagebox außerhalb dialoge.py.

Keine JSON-Zugriffe außerhalb datei.py.

Keine doppelten Felddefinitionen.

Alle Kontaktfelder ausschließlich aus:

kontaktfelder.py

Neue Funktionen möglichst in eigenen Modulen entwickeln.

---

# Coding Style

Kurze Funktionen.

Aussagekräftige Funktionsnamen.

Keine unnötigen Kommentare.

Keine Duplikate.

PEP8 beachten.

casefold() statt lower().

---

# Vor jeder Änderung

Agent analysiert zuerst:

- Projektstruktur
- betroffene Module
- Abhängigkeiten

Danach:

Implementierungsplan erstellen.

Noch keinen Code ändern.

---

# Vor Abschluss

Der Agent prüft mindestens:

✓ Programm startet

✓ Neuer Kontakt

✓ Bearbeiten

✓ Löschen

✓ Suche

✓ Import

✓ Export

✓ Datensicherung

---

# Abschlussbericht

Immer dokumentieren:

- geänderte Dateien

- Architekturentscheidungen

- Tests

- offene Risiken