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
