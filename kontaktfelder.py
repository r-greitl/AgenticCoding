"""Felddefinitionen und Hilfsfunktionen für Kontakte."""


FELDER = [
    ("Name", "name"),
    ("Wohnort", "wohnort"),
    ("Alter", "alter"),
    ("Beruf", "beruf"),
    ("Telefonnummer", "telefon"),
    ("E-Mail", "email"),
    ("Geburtstag", "geburtstag"),
]


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
