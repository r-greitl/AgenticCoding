"""Funktionen zum Laden und Speichern der Kontakte."""

import json
from pathlib import Path


DATEIPFAD = Path(__file__).with_name("kontakte.json")


def kontakte_laden():
    if not DATEIPFAD.exists():
        return []

    try:
        with open(
            DATEIPFAD,
            "r",
            encoding="utf-8",
        ) as datei:
            daten = json.load(datei)

        if isinstance(daten, list):
            return daten

        return []

    except (OSError, json.JSONDecodeError):
        return []


def kontakte_speichern(kontaktliste):
    try:
        with open(
            DATEIPFAD,
            "w",
            encoding="utf-8",
        ) as datei:
            json.dump(
                kontaktliste,
                datei,
                ensure_ascii=False,
                indent=4,
            )

        return True

    except (OSError, TypeError) as fehler:
        print(
            "Fehler beim Speichern:",
            fehler,
        )

        return False