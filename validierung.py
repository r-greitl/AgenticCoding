"""Prüffunktionen für Kontaktdaten."""

import re

from kontaktfelder import KATEGORIEN


def kontakt_validieren(kontakt):
    """
    Prüft die Daten eines Kontakts.

    Rückgabe:
        (True, "") bei gültigen Daten
        (False, "Fehlermeldung") bei ungültigen Daten
    """

    name = kontakt.get("name", "").strip()
    wohnort = kontakt.get("wohnort", "").strip()
    alter = kontakt.get("alter", "").strip()
    telefon = kontakt.get("telefon", "").strip()
    email = kontakt.get("email", "").strip()
    kategorie = kontakt.get("kategorie", "").strip()

    if not name:
        return False, "Bitte geben Sie einen Namen ein."

    if len(name) < 2:
        return False, "Der Name muss mindestens zwei Zeichen enthalten."

    if alter:
        if not alter.isdigit():
            return False, "Das Alter darf nur aus Ziffern bestehen."

        alter_zahl = int(alter)

        if alter_zahl < 0 or alter_zahl > 130:
            return False, "Bitte geben Sie ein Alter zwischen 0 und 130 ein."

    if email and not email_ist_gueltig(email):
        return False, "Bitte geben Sie eine gültige E-Mail-Adresse ein."

    if telefon and not telefon_ist_gueltig(telefon):
        return False, (
            "Die Telefonnummer enthält ungültige Zeichen. "
            "Erlaubt sind Ziffern, Leerzeichen, +, -, / und Klammern."
        )

    if len(wohnort) > 100:
        return False, "Der Wohnort darf höchstens 100 Zeichen enthalten."

    if kategorie and kategorie not in KATEGORIEN:
        return False, "Bitte wählen Sie eine gültige Kategorie aus."

    return True, ""


def email_ist_gueltig(email):
    """Prüft das grundlegende Format einer E-Mail-Adresse."""

    muster = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return re.fullmatch(
        muster,
        email,
    ) is not None


def telefon_ist_gueltig(telefon):
    """Prüft die erlaubten Zeichen einer Telefonnummer."""

    muster = r"^[0-9+\-()/\s]+$"

    return re.fullmatch(
        muster,
        telefon,
    ) is not None
