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
