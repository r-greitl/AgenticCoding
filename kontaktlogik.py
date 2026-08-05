"""Allgemeine Funktionen zur Verarbeitung von Kontakten."""


def kontakte_sortieren(kontaktliste):
    """
    Sortiert Kontakte alphabetisch nach ihrem Namen.

    Es wird eine neue Liste zurückgegeben.
    Die übergebene Liste wird nicht verändert.
    """

    return sorted(
        kontaktliste,
        key=lambda kontakt: kontakt.get(
            "name",
            "",
        ).casefold(),
    )


def kontakte_suchen(kontaktliste, suchtext):
    """
    Durchsucht alle Felder eines Kontakts.

    Die Suche unterscheidet nicht zwischen
    Groß- und Kleinschreibung.
    """

    suchtext = suchtext.strip().casefold()

    if not suchtext:
        return kontakte_sortieren(kontaktliste)

    gefundene_kontakte = []

    for kontakt in kontaktliste:
        kontakt_gefunden = any(
            suchtext in str(wert).casefold()
            for wert in kontakt.values()
        )

        if kontakt_gefunden:
            gefundene_kontakte.append(kontakt)

    return kontakte_sortieren(
        gefundene_kontakte
    )


def kontakt_bereits_vorhanden(
    kontaktliste,
    neuer_kontakt,
    kontakt_ignorieren=None,
):
    """
    Prüft, ob ein Kontakt bereits vorhanden ist.

    Eine Dublette liegt vor, wenn:
    - der Name identisch ist oder
    - eine vorhandene E-Mail-Adresse identisch ist.
    """

    neuer_name = neuer_kontakt.get(
        "name",
        "",
    ).strip().casefold()

    neue_email = neuer_kontakt.get(
        "email",
        "",
    ).strip().casefold()

    for vorhandener_kontakt in kontaktliste:
        if vorhandener_kontakt is kontakt_ignorieren:
            continue

        vorhandener_name = vorhandener_kontakt.get(
            "name",
            "",
        ).strip().casefold()

        vorhandene_email = vorhandener_kontakt.get(
            "email",
            "",
        ).strip().casefold()

        gleicher_name = (
            neuer_name != ""
            and neuer_name == vorhandener_name
        )

        gleiche_email = (
            neue_email != ""
            and neue_email == vorhandene_email
        )

        if gleicher_name or gleiche_email:
            return True

    return False