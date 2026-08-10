"""Felddefinitionen und Hilfsfunktionen für Kontakte."""


KATEGORIEN = (
    "Familie",
    "Freunde",
    "Arbeit",
    "Verein",
    "Sonstiges",
)


FELDER = [
    ("Name", "name"),
    ("Wohnort", "wohnort"),
    ("Alter", "alter"),
    ("Beruf", "beruf"),
    ("Telefonnummer", "telefon"),
    ("E-Mail", "email"),
    ("Geburtstag", "geburtstag"),
    ("Kategorie", "kategorie"),
]


def kategorie_normalisieren(wert):
    """Gibt eine bekannte Kategorie in kanonischer Schreibweise zurück."""

    normalisierter_wert = str(wert or "").strip().casefold()

    for kategorie in KATEGORIEN:
        if normalisierter_wert == kategorie.casefold():
            return kategorie

    return ""


def kontakt_aus_eingabefeldern(eingabefelder):
    """Liest alle Werte aus den Tkinter-Eingabefeldern aus."""

    return {
        feldname: eingabe.get().strip()
        for feldname, eingabe in eingabefelder.items()
    }


def leerer_kontakt():
    """Erzeugt einen leeren Kontakt mit allen vorgesehenen Feldern."""

    return {
        feldname: ""
        for _, feldname in FELDER
    }


def kontakt_vervollstaendigen(kontakt):
    """Ergänzt fehlende Felder eines vorhandenen Kontakts."""

    vollstaendiger_kontakt = leerer_kontakt()
    vollstaendiger_kontakt.update(kontakt)

    return vollstaendiger_kontakt
