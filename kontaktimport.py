"""Importfunktionen für Kontakte aus CSV- und vCard-Dateien."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from kontaktfelder import leerer_kontakt
from validierung import kontakt_validieren


SPALTEN_ALIASE = {
    "name": {"name", "vollständiger name", "vollstaendiger name", "display name", "full name", "formatted name"},
    "vorname": {"vorname", "first name", "given name"},
    "nachname": {"nachname", "last name", "family name", "surname"},
    "wohnort": {"wohnort", "ort", "stadt", "city", "home city", "address city"},
    "alter": {"alter", "age"},
    "beruf": {"beruf", "job title", "occupation", "title", "position"},
    "telefon": {"telefon", "telefonnummer", "phone", "phone number", "mobile phone", "mobile", "home phone", "business phone", "primary phone"},
    "email": {"email", "e-mail", "e-mail address", "email address", "primary email"},
    "geburtstag": {"geburtstag", "birthday", "birth date", "date of birth"},
}


def _normalisieren(text: Any) -> str:
    return str(text or "").strip().casefold()


def _wert_aus_zeile(zeile: dict[str, Any], feldgruppe: str) -> str:
    aliase = SPALTEN_ALIASE[feldgruppe]
    for spaltenname, wert in zeile.items():
        if _normalisieren(spaltenname) in aliase:
            return str(wert or "").strip()
    return ""


def _kontakt_aus_csv_zeile(zeile: dict[str, Any]) -> dict[str, str]:
    kontakt = leerer_kontakt()
    name = _wert_aus_zeile(zeile, "name")
    if not name:
        vorname = _wert_aus_zeile(zeile, "vorname")
        nachname = _wert_aus_zeile(zeile, "nachname")
        name = " ".join(teil for teil in (vorname, nachname) if teil).strip()

    kontakt.update({
        "name": name,
        "wohnort": _wert_aus_zeile(zeile, "wohnort"),
        "alter": _wert_aus_zeile(zeile, "alter"),
        "beruf": _wert_aus_zeile(zeile, "beruf"),
        "telefon": _wert_aus_zeile(zeile, "telefon"),
        "email": _wert_aus_zeile(zeile, "email"),
        "geburtstag": _wert_aus_zeile(zeile, "geburtstag"),
    })
    return kontakt


def _csv_lesen(dateipfad: Path) -> list[dict[str, str]]:
    letzte_exception: Exception | None = None
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            with dateipfad.open("r", encoding=encoding, newline="") as datei:
                probe = datei.read(4096)
                datei.seek(0)
                try:
                    dialekt = csv.Sniffer().sniff(probe, delimiters=",;\t|")
                except csv.Error:
                    dialekt = csv.excel
                    dialekt.delimiter = ";"
                leser = csv.DictReader(datei, dialect=dialekt)
                return [_kontakt_aus_csv_zeile(zeile) for zeile in leser if zeile]
        except (UnicodeDecodeError, OSError) as fehler:
            letzte_exception = fehler

    if letzte_exception is not None:
        raise letzte_exception
    return []


def _vcard_zeilen_verbinden(text: str) -> list[str]:
    ergebnis: list[str] = []
    for zeile in text.splitlines():
        if zeile.startswith((" ", "\t")) and ergebnis:
            ergebnis[-1] += zeile[1:]
        else:
            ergebnis.append(zeile)
    return ergebnis


def _vcard_wert_bereinigen(wert: str) -> str:
    return (wert.replace(r"\n", " ")
                .replace(r"\N", " ")
                .replace(r"\,", ",")
                .replace(r"\;", ";")
                .replace(r"\\", "\\")
                .strip())


def _vcard_eintraege(text: str) -> list[list[str]]:
    zeilen = _vcard_zeilen_verbinden(text)
    eintraege: list[list[str]] = []
    aktueller_eintrag: list[str] | None = None

    for zeile in zeilen:
        if zeile.upper() == "BEGIN:VCARD":
            aktueller_eintrag = []
        elif zeile.upper() == "END:VCARD":
            if aktueller_eintrag is not None:
                eintraege.append(aktueller_eintrag)
            aktueller_eintrag = None
        elif aktueller_eintrag is not None:
            aktueller_eintrag.append(zeile)
    return eintraege


def _kontakt_aus_vcard(zeilen: list[str]) -> dict[str, str]:
    kontakt = leerer_kontakt()
    namensbestandteile: list[str] = []

    for zeile in zeilen:
        if ":" not in zeile:
            continue
        kopf, roher_wert = zeile.split(":", 1)
        eigenschaft = kopf.split(";", 1)[0].upper()
        wert = _vcard_wert_bereinigen(roher_wert)

        if eigenschaft == "FN" and wert:
            kontakt["name"] = wert
        elif eigenschaft == "N" and wert:
            bestandteile = [_vcard_wert_bereinigen(teil) for teil in wert.split(";")]
            nachname = bestandteile[0] if len(bestandteile) > 0 else ""
            vorname = bestandteile[1] if len(bestandteile) > 1 else ""
            weitere = bestandteile[2] if len(bestandteile) > 2 else ""
            namensbestandteile = [teil for teil in (vorname, weitere, nachname) if teil]
        elif eigenschaft == "EMAIL" and not kontakt["email"]:
            kontakt["email"] = wert
        elif eigenschaft == "TEL" and not kontakt["telefon"]:
            kontakt["telefon"] = wert
        elif eigenschaft == "TITLE" and not kontakt["beruf"]:
            kontakt["beruf"] = wert
        elif eigenschaft == "ORG" and not kontakt["beruf"]:
            kontakt["beruf"] = wert.replace(";", " – ")
        elif eigenschaft == "BDAY" and not kontakt["geburtstag"]:
            kontakt["geburtstag"] = wert
        elif eigenschaft == "ADR" and not kontakt["wohnort"]:
            bestandteile = wert.split(";")
            kontakt["wohnort"] = bestandteile[3].strip() if len(bestandteile) > 3 else ""

    if not kontakt["name"] and namensbestandteile:
        kontakt["name"] = " ".join(namensbestandteile)
    return kontakt


def _vcard_lesen(dateipfad: Path) -> list[dict[str, str]]:
    letzte_exception: Exception | None = None
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            text = dateipfad.read_text(encoding=encoding)
            return [_kontakt_aus_vcard(eintrag) for eintrag in _vcard_eintraege(text)]
        except (UnicodeDecodeError, OSError) as fehler:
            letzte_exception = fehler

    if letzte_exception is not None:
        raise letzte_exception
    return []


def kontakte_importieren(dateiname: str | Path) -> tuple[list[dict[str, str]], list[str]]:
    """Importiert Kontakte aus CSV oder VCF und validiert sie."""

    dateipfad = Path(dateiname)
    if not dateipfad.exists():
        return [], ["Die ausgewählte Datei wurde nicht gefunden."]

    endung = dateipfad.suffix.casefold()
    try:
        if endung == ".csv":
            rohe_kontakte = _csv_lesen(dateipfad)
        elif endung in {".vcf", ".vcard"}:
            rohe_kontakte = _vcard_lesen(dateipfad)
        else:
            return [], ["Dieses Dateiformat wird nicht unterstützt. Erlaubt sind CSV und VCF."]
    except (OSError, UnicodeError, csv.Error) as fehler:
        return [], [f"Die Datei konnte nicht gelesen werden: {fehler}"]

    gueltige_kontakte: list[dict[str, str]] = []
    fehlerliste: list[str] = []

    for nummer, kontakt in enumerate(rohe_kontakte, start=1):
        ist_gueltig, fehlermeldung = kontakt_validieren(kontakt)
        if ist_gueltig:
            gueltige_kontakte.append(kontakt)
        else:
            name = kontakt.get("name", "").strip() or f"Eintrag {nummer}"
            fehlerliste.append(f"{name}: {fehlermeldung}")

    return gueltige_kontakte, fehlerliste