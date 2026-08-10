"""Exportfunktionen fuer Kontakte."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping


def vcard_wert_escapen(wert: Any) -> str:
    """Escapet einen Textwert fuer vCard 3.0."""

    text = str(wert or "").strip()
    text = text.replace("\\", "\\\\")
    text = text.replace("\r\n", "\\n")
    text = text.replace("\r", "\\n")
    text = text.replace("\n", "\\n")
    text = text.replace(",", "\\,")
    return text.replace(";", "\\;")


def kontakt_als_vcard(kontakt: Mapping[str, Any]) -> str:
    """Erzeugt fuer einen Kontakt eine vCard im Format 3.0."""

    zeilen = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"FN:{vcard_wert_escapen(kontakt.get('name', ''))}",
    ]

    eigenschaften = (
        ("TEL", "telefon"),
        ("EMAIL", "email"),
        ("TITLE", "beruf"),
        ("BDAY", "geburtstag"),
    )

    for eigenschaft, feldname in eigenschaften:
        wert = str(kontakt.get(feldname, "") or "").strip()
        if wert:
            zeilen.append(
                f"{eigenschaft}:{vcard_wert_escapen(wert)}"
            )

    wohnort = str(kontakt.get("wohnort", "") or "").strip()
    if wohnort:
        zeilen.append(
            f"ADR:;;;{vcard_wert_escapen(wohnort)};;;"
        )

    zeilen.append("END:VCARD")
    return "\r\n".join(zeilen) + "\r\n"


def kontakte_als_vcard(
    kontakte: Iterable[Mapping[str, Any]],
) -> str:
    """Erzeugt eine vCard-Datei fuer mehrere Kontakte."""

    return "".join(
        kontakt_als_vcard(kontakt)
        for kontakt in kontakte
    )


def kontakte_als_vcard_exportieren(
    kontakte: Iterable[Mapping[str, Any]],
    dateiname: str | Path,
) -> tuple[bool, str]:
    """Schreibt Kontakte UTF-8-kodiert in eine vCard-Datei."""

    kontaktliste = list(kontakte)

    for position, kontakt in enumerate(kontaktliste, start=1):
        name = str(kontakt.get("name", "") or "").strip()
        if not name:
            return (
                False,
                f"Kontakt {position} kann nicht exportiert werden, "
                "weil der Name fehlt.",
            )

    try:
        dateipfad = Path(dateiname)
        dateipfad.write_text(
            kontakte_als_vcard(kontaktliste),
            encoding="utf-8",
            newline="",
        )
        return True, ""
    except (OSError, UnicodeError, TypeError) as fehler:
        return False, str(fehler)
