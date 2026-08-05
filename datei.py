import json
import shutil
from pathlib import Path


DATEIPFAD = Path(__file__).with_name("kontakte.json")
SICHERUNGSPFAD = Path(__file__).with_name("kontakte_backup.json")


def kontakte_laden():
    """Lädt die Kontakte aus der JSON-Datei."""

    kontakte = datei_laden(DATEIPFAD)

    if kontakte is not None:
        return kontakte

    print(
        "Die Hauptdatei konnte nicht geladen werden. "
        "Die Sicherung wird verwendet."
    )

    kontakte = datei_laden(SICHERUNGSPFAD)

    if kontakte is not None:
        return kontakte

    print("Es konnten keine gespeicherten Kontakte geladen werden.")
    return []


def datei_laden(pfad):
    """
    Lädt eine Kontaktliste aus einer JSON-Datei.

    Gibt None zurück, wenn die Datei nicht gelesen werden kann.
    """

    if not pfad.exists():
        return None

    try:
        with open(
            pfad,
            "r",
            encoding="utf-8",
        ) as datei:
            daten = json.load(datei)

        if not isinstance(daten, list):
            print(
                f"{pfad.name} enthält keine gültige Kontaktliste."
            )
            return None

        return daten

    except json.JSONDecodeError as fehler:
        print(
            f"{pfad.name} enthält ungültiges JSON:",
            fehler,
        )
        return None

    except OSError as fehler:
        print(
            f"{pfad.name} konnte nicht gelesen werden:",
            fehler,
        )
        return None


def kontakte_speichern(kontaktliste):
    """Speichert die Kontaktliste sicher in der JSON-Datei."""

    temporaerer_pfad = DATEIPFAD.with_suffix(".tmp")

    try:
        # Zuerst in eine temporäre Datei schreiben.
        with open(
            temporaerer_pfad,
            "w",
            encoding="utf-8",
        ) as datei:
            json.dump(
                kontaktliste,
                datei,
                ensure_ascii=False,
                indent=4,
            )

        # Vorhandene Hauptdatei als Sicherung kopieren.
        if DATEIPFAD.exists():
            shutil.copy2(
                DATEIPFAD,
                SICHERUNGSPFAD,
            )

        # Temporäre Datei wird zur neuen Hauptdatei.
        temporaerer_pfad.replace(DATEIPFAD)

        return True

    except (OSError, TypeError) as fehler:
        print(
            "Fehler beim Speichern der Kontakte:",
            fehler,
        )

        # Eine übrig gebliebene temporäre Datei entfernen.
        try:
            if temporaerer_pfad.exists():
                temporaerer_pfad.unlink()
        except OSError:
            pass

        return False