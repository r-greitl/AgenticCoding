"""GUI-unabhaengige Verwaltung der Kontaktfotos."""

from pathlib import Path
import shutil
import uuid


ANWENDUNGSORDNER = Path(__file__).parent
BILDERORDNER = ANWENDUNGSORDNER / "bilder"
UNTERSTUETZTE_ENDUNGEN = {".png", ".gif"}


def verwalteten_pfad_aufloesen(fotopfad):
    """Loest einen sicheren relativen Fotopfad auf oder gibt None zurueck."""

    if not isinstance(fotopfad, str) or not fotopfad:
        return None
    if any(
        segment in {".", ".."}
        for segment in fotopfad.replace("\\", "/").split("/")
    ):
        return None

    relativer_pfad = Path(fotopfad)
    if relativer_pfad.is_absolute() or relativer_pfad.drive:
        return None

    basis = BILDERORDNER.resolve()
    ziel = (ANWENDUNGSORDNER / relativer_pfad).resolve()

    try:
        ziel.relative_to(basis)
    except ValueError:
        return None

    if ziel.parent != basis or ziel.suffix.casefold() not in UNTERSTUETZTE_ENDUNGEN:
        return None

    return ziel


def foto_kopieren(quelldatei):
    """Kopiert ein PNG/GIF in den Bilderordner und liefert den relativen Pfad."""

    quelle = Path(quelldatei)
    endung = quelle.suffix.casefold()
    if endung not in UNTERSTUETZTE_ENDUNGEN:
        raise ValueError("Unterstuetzt werden nur PNG- und GIF-Dateien.")
    if not quelle.is_file():
        raise FileNotFoundError("Die ausgewaehlte Bilddatei wurde nicht gefunden.")

    BILDERORDNER.mkdir(parents=True, exist_ok=True)
    ziel = BILDERORDNER / f"{uuid.uuid4().hex}{endung}"
    try:
        shutil.copy2(quelle, ziel)
    except OSError:
        try:
            ziel.unlink(missing_ok=True)
        except OSError:
            pass
        raise
    return ziel.relative_to(ANWENDUNGSORDNER).as_posix()


def kontaktfoto_speichern(
    kontakt,
    neue_daten,
    speichern,
    quelldatei=None,
    entfernen=False,
):
    """Speichert eine Kontaktaenderung mit transaktionaler Fotoverwaltung."""

    alter_zustand = kontakt.copy()
    aktualisierte_daten = neue_daten.copy()
    alter_fotopfad = alter_zustand.get("foto", "")
    neuer_fotopfad = alter_fotopfad

    if quelldatei:
        neuer_fotopfad = foto_kopieren(quelldatei)
    elif entfernen:
        neuer_fotopfad = ""

    kontakt.clear()
    kontakt.update(aktualisierte_daten)
    kontakt["foto"] = neuer_fotopfad

    speicherfehler = None
    try:
        erfolgreich = speichern()
    except Exception as fehler:
        erfolgreich = False
        speicherfehler = fehler

    if erfolgreich:
        if alter_fotopfad != neuer_fotopfad:
            foto_loeschen(alter_fotopfad)
        return True

    if neuer_fotopfad != alter_fotopfad:
        foto_loeschen(neuer_fotopfad)
    kontakt.clear()
    kontakt.update(alter_zustand)

    if speicherfehler is not None:
        raise speicherfehler
    return False


def foto_loeschen(fotopfad):
    """Loescht ausschliesslich eine Datei direkt im verwalteten Bilderordner."""

    ziel = verwalteten_pfad_aufloesen(fotopfad)
    if ziel is None:
        return False

    try:
        ziel.unlink(missing_ok=True)
        return True
    except OSError:
        return False
