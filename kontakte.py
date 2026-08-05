import validierung
def test():
    print("kontakte.py wurde erfolgreich geladen")

def name_eingeben():
    while True:
        name = input("Name: ").strip()

        if name:
            return name

        print("Der Name darf nicht leer sein.")
def kontakt_eingeben():
    kontakt = {
    "name": name_eingeben(),
    "wohnort": input("Wohnort: ").strip(),
        "alter": input("Alter: ").strip(),
        "beruf": input("Beruf: ").strip(),
        "telefon": input("Telefonnummer: ").strip(),
        "email": input("E-Mail: ").strip(),
        "geburtstag": input("Geburtstag: ").strip()
}
    return kontakt

def kontakt_anzeigen(kontakt):
    print(f"Name: {kontakt['name']}")
    print(f"Wohnort: {kontakt['wohnort']}")
    print(f"Alter: {kontakt['alter']}")
    print(f"Beruf: {kontakt['beruf']}")
    print(f"Telefonnummer: {kontakt['telefon']}")
    print(f"E-Mail: {kontakt['email']}")
    print(f"Geburtstag: {kontakt['geburtstag']}")




def kontakt_loeschen(kontaktliste):
    kontakt = kontakt_auswaehlen(kontaktliste)

    if kontakt is None:
        return

    print()
    kontakt_anzeigen(kontakt)

    antwort = input("Diesen Kontakt wirklich löschen? (j/n): ").lower()

    if antwort == "j":
        kontaktliste.remove(kontakt)
        print("Kontakt wurde gelöscht.")
    else:
        print("Löschen wurde abgebrochen.")

def kontakt_bearbeiten(kontaktliste):
    kontakt = kontakt_auswaehlen(kontaktliste)

    if kontakt is None:
        return

    print("Kontakt gefunden.")
    kontakt_anzeigen(kontakt)

    print()
    print("Welches Feld möchtest du ändern?")
    print("1. Name")
    print("2. Wohnort")
    print("3. Alter")
    print("4. Beruf")
    print("5. Telefonnummer")
    print("6. E-Mail")
    print("7. Geburtstag")

    auswahl = input("Bitte wählen: ")

    felder = {
        "1": "name",
        "2": "wohnort",
        "3": "alter",
        "4": "beruf",
        "5": "telefon",
        "6": "email",
        "7": "geburtstag"
    }

    if auswahl in felder:
        feldname = felder[auswahl]
        print(f"Aktueller Wert: {kontakt[feldname]}")
        neuer_wert = input("Neuer Wert: ")
        kontakt[feldname] = neuer_wert
        print("Kontakt wurde aktualisiert.")
    else:
        print("Ungültige Auswahl.")

def kontakte_auflisten(kontaktliste):
    if not kontaktliste:
        print("Es wurden noch keine Kontakte erfasst.")
        return

    print("=========================")
    print("Ihre Kontakte")
    print("=========================")

    for nummer, kontakt in enumerate(kontaktliste, start=1):
        print(f"{nummer}. {kontakt['name']}")    

def kontakt_auswaehlen(kontaktliste):
    if not kontaktliste:
        print("Es wurden noch keine Kontakte erfasst.")
        return None

    kontakte_auflisten(kontaktliste)

    auswahl = validierung.nummer_auswaehlen(
        "Nummer des Kontakts: ",
        1,
        len(kontaktliste)
    )

    return kontaktliste[auswahl - 1]

def kontakt_verwalten(kontaktliste):
    kontakt = kontakt_auswaehlen(kontaktliste)

    if kontakt is None:
        return

    print()
    kontakt_anzeigen(kontakt)

    print()
    print("Was möchtest du mit diesem Kontakt machen?")
    print("1. Kontakt bearbeiten")
    print("2. Kontakt löschen")
    print("3. Zurück")

    auswahl = input("Bitte wählen: ")

    if auswahl == "1":
        kontakt_bearbeiten_auswahl(kontakt)

    elif auswahl == "2":
        kontakt_loeschen_auswahl(kontaktliste, kontakt)

    elif auswahl == "3":
        return

    else:
        print("Ungültige Auswahl.")


def kontakt_bearbeiten_auswahl(kontakt):
    print()
    print("Welches Feld möchtest du ändern?")
    print("1. Name")
    print("2. Wohnort")
    print("3. Alter")
    print("4. Beruf")
    print("5. Telefonnummer")
    print("6. E-Mail")
    print("7. Geburtstag")

    felder = {
        "1": "name",
        "2": "wohnort",
        "3": "alter",
        "4": "beruf",
        "5": "telefon",
        "6": "email",
        "7": "geburtstag"
    }

    while True:
        auswahl = input("Bitte wählen: ")

        if auswahl in felder:
            feldname = felder[auswahl]
            print(f"Aktueller Wert: {kontakt[feldname]}")

            neuer_wert = input("Neuer Wert: ").strip()

            if neuer_wert:
                kontakt[feldname] = neuer_wert
                print("Kontakt wurde aktualisiert.")
            else:
                print("Der neue Wert darf nicht leer sein.")

            return

        print("Bitte wählen Sie eine Zahl zwischen 1 und 7.")  

def kontakt_loeschen_auswahl(kontaktliste, kontakt):
    antwort = input("Diesen Kontakt wirklich löschen? (j/n): ").lower()

    if antwort == "j":
        kontaktliste.remove(kontakt)
        print("Kontakt wurde gelöscht.")
    else:
        print("Löschen wurde abgebrochen.")      