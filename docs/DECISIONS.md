# Architekturentscheidungen

## ADR-001: Projektdokumentation im docs/-Ordner

### Status
Akzeptiert

### Kontext
Die Anzahl der Projektdokumente wird im Laufe des Workshops wachsen.

### Entscheidung
Alle Projektdokumente außer README.md werden im Ordner `docs/` abgelegt.

### Konsequenzen
- Das Hauptverzeichnis bleibt übersichtlich.
- Dokumentation ist zentral organisiert.
- Neue Dokumente können ergänzt werden, ohne die Projektstruktur zu verändern.

## ADR-002: Geschlossene, optionale Kontaktkategorien

### Status
Akzeptiert

### Kontext
Kontakte sollen optional genau einer von fünf vorgesehenen Kategorien
zugeordnet werden können. Bestehende Kontakte und externe Importdateien
enthalten das neue Feld nicht oder können unbekannte Kategorien enthalten.

### Entscheidung
Die erlaubten Kategorien werden ausschließlich als `KATEGORIEN` in
`kontaktfelder.py` definiert. Ein Kontakt speichert mit `kategorie` genau
einen skalaren Textwert. Der leere Text bedeutet "keine Kategorie".

Fehlende Kategorien in bestehenden JSON-Daten werden nur im Arbeitsspeicher
ergänzt. Das Laden allein schreibt die JSON-Datei nicht um. Unbekannte Werte
aus bestehenden oder manuell veränderten JSON-Daten werden in der
Kategorieauswahl kontrolliert als "keine Kategorie" dargestellt.

Unbekannte oder mehrere Kategorien aus CSV- und vCard-Dateien dürfen den
Import eines ansonsten gültigen Kontakts nicht verhindern. Sie werden in
Sprint 3 als "keine Kategorie" behandelt. Bekannte Kategorien werden
unabhängig von ihrer Schreibweise auf den kanonischen Wert normalisiert.

### Konsequenzen
- Bestehende Kontakte bleiben ohne Migration kompatibel.
- Ein Kontakt kann höchstens eine Kategorie besitzen.
- Freie Tags und Mehrfachkategorien sind ausgeschlossen.
- Unbekannte Importwerte gehen nicht in das interne Kontaktmodell ein.
- GUI, Import und Validierung verwenden dieselbe zentrale Kategorienliste.
