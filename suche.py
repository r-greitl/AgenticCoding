import validierung
def kontakt_suchen(kontaktliste, kontakt_anzeigen):
    suchbegriff = input("Welchen Kontakt suchst du? ").strip().lower()

    if not suchbegriff:
        print("Bitte geben Sie einen Suchbegriff ein.")
        return

    trefferliste = []

    for kontakt in kontaktliste:
        name = kontakt["name"].lower()

        if suchbegriff in name:
            trefferliste.append(kontakt)

    if not trefferliste:
        print("Kein Kontakt gefunden.")
        return

    print()
    print("Gefundene Kontakte:")
    print()

    for nummer, kontakt in enumerate(trefferliste, start=1):
        print(f"{nummer}. {kontakt['name']}")

    auswahl = validierung.nummer_auswaehlen(
        "Nummer des Kontakts: ",
        1,
        len(trefferliste)
    )

    kontakt = trefferliste[auswahl - 1]

    print()
    kontakt_anzeigen(kontakt)
