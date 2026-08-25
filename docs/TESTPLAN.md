## Sprint 2: vCard-Export

### Automatische Tests

- vCard-3.0-Grundstruktur und alle unterstuetzten Kontaktfelder
- Export mehrerer Kontakte in stabiler Reihenfolge
- Auslassen leerer optionaler Felder
- Escaping von Backslash, Komma, Semikolon und Zeilenumbruechen
- UTF-8-Ausgabe und CRLF-Zeilenenden
- fehlende Kontaktfelder und unveraenderte Quelldaten
- kontrollierte Behandlung von Schreibfehlern

Ausfuehrung:

```bash
python -m unittest discover -s tests
```

### Manuelle Regression

- Export aller Kontakte
- Export der sichtbaren Suchtreffer
- Abbruch des Speichern-Dialogs ohne Fehlermeldung
- verstaendlicher Hinweis bei leerer Exportmenge
- Programmstart, Anlegen, Bearbeiten und Loeschen
- Suche sowie CSV- und vCard-Import
- JSON-Speicherung und Datensicherung

## Sprint 3: Kontaktkategorien

### Automatische Tests

- zentrale und eindeutige Kategorienliste
- Vervollständigung alter Kontakte ohne Änderung der Quelldaten
- optionale Kategorie und Ablehnung unbekannter interner Werte
- Suche nach Kategorie einschließlich `casefold()`
- CSV- und vCard-Import mit fehlenden, bekannten und unbekannten Kategorien
- Behandlung mehrerer vCard-Kategorien als "keine Kategorie"
- vCard-Export mit und ohne Kategorie
- Export-/Import-Roundtrip der Kategorie
- JSON-Laden ohne automatisches Umschreiben
- JSON-Speicherung einer Kategorie

### Manuelle Regression

- Kategorie im Neu- und Bearbeiten-Formular auswählen und entfernen
- unbekannte JSON-Kategorie kontrolliert als leere Auswahl anzeigen
- Kategorie in der Detailansicht anzeigen
- Suche nach jeder Kategorie
- Programmstart, Anlegen, Bearbeiten und Löschen
- CSV- und vCard-Import bestehender Dateien
- vCard-Export aller und sichtbarer Kontakte
- JSON-Speicherung und Datensicherung

## Sprint 4: Kontaktfotos

### Automatische Tests

- Rueckwaertskompatibilitaet und `foto == ""` bei alten/leeren Kontakten
- Erhalt von Kategorie und relativem Fotopfad ohne Mutation der Quelldaten
- sichere Pfadauflösung nur innerhalb des verwalteten Bilderordners
- Ablehnung absoluter Pfade und von Pfad-Traversal
- Kopieren von PNG/GIF mit eindeutigen Namen
- fehlende Quelldatei und nicht unterstuetzte Dateiendung
- kontrolliertes Loeschen ausschliesslich verwalteter Dateien
- Kategorie bleibt durchsuchbar; Fotopfad ist nicht durchsuchbar
- CSV-/vCard-Import setzt `foto == ""` und ignoriert vCard-PHOTO
- vCard-Export enthaelt weder PHOTO noch Fotopfad; CATEGORIES bleibt erhalten

Ausfuehrung:

```bash
python -m unittest discover -s tests
```

### Manuelle Regression

- PNG und GIF beim neuen Kontakt auswaehlen, Vorschau pruefen und speichern
- vorhandenes Foto beim Bearbeiten ersetzen und entfernen
- Auswahl/Entfernung abbrechen und unveraenderte Daten/Dateien pruefen
- fehlende und beschaedigte verwaltete Bilddatei in Detail/Formular anzeigen
- simulierten JSON-Speicherfehler beim Anlegen und Ersetzen pruefen
- Programmstart, Anlegen, Bearbeiten, Loeschen, Suche, Import und Export

## Sprint 5: Nebenwirkungsfreier GUI-Import

### Automatische Tests

- Import erzeugt weder `tk.Tk()` noch Widgets oder einen Mainloop
- Import ruft `datei.kontakte_laden()` nicht auf
- Import erzeugt oder veraendert `kontakte.json` nicht
- Import funktioniert in einem headless Subprozess
- `main()` startet Daten, GUI, Darstellung, Menue, Ereignisse, Fokus und
  Mainloop in der festgelegten Reihenfolge

### Manuelle Regression

- normaler Programmstart mit `python kontaktbuch_gui.py`
- Laden und Anzeigen vorhandener Kontakte
- Anlegen, Bearbeiten und Loeschen einschliesslich Kontaktfotos
- Suche, Kategorien, Import und Export
- Tastaturbindungen, Menue, Fenster-Schliessen und Fokus im Suchfeld
