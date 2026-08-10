
"""Zentrale Dialogfenster für das Kontaktbuch."""

from tkinter import messagebox


def ungueltige_eingabe(fehlermeldung):
    """Zeigt eine Warnung bei ungültigen Eingaben."""

    messagebox.showwarning(
        "Ungültige Eingabe",
        fehlermeldung,
    )


def keine_auswahl():
    """Informiert darüber, dass kein Kontakt ausgewählt wurde."""

    messagebox.showwarning(
        "Keine Auswahl",
        "Bitte wählen Sie zuerst einen Kontakt aus.",
    )


def kontakt_gespeichert():
    """Bestätigt das Speichern eines neuen Kontakts."""

    messagebox.showinfo(
        "Kontakt gespeichert",
        "Der Kontakt wurde erfolgreich gespeichert.",
    )


def kontakt_geaendert():
    """Bestätigt das Speichern von Änderungen."""

    messagebox.showinfo(
        "Gespeichert",
        "Die Änderungen wurden gespeichert.",
    )


def kontakt_geloescht():
    """Bestätigt das Löschen eines Kontakts."""

    messagebox.showinfo(
        "Kontakt gelöscht",
        "Der Kontakt wurde erfolgreich gelöscht.",
    )


def speicherfehler_neuer_kontakt():
    """Zeigt einen Speicherfehler beim Erstellen an."""

    messagebox.showerror(
        "Speicherfehler",
        "Der Kontakt konnte nicht gespeichert werden.",
    )


def speicherfehler_bearbeiten():
    """Zeigt einen Speicherfehler beim Bearbeiten an."""

    messagebox.showerror(
        "Speicherfehler",
        "Die Änderungen konnten nicht gespeichert werden.",
    )


def speicherfehler_loeschen():
    """Zeigt einen Speicherfehler beim Löschen an."""

    messagebox.showerror(
        "Speicherfehler",
        "Der Kontakt konnte nicht gelöscht werden.",
    )


def kontakt_loeschen_bestaetigen(name):
    """Fragt nach, ob ein Kontakt gelöscht werden soll."""

    return messagebox.askyesno(
        "Kontakt löschen",
        f"Möchten Sie den Kontakt\n\n"
        f"{name}\n\n"
        f"wirklich löschen?",
    )


def dublette_speichern_bestaetigen():
    """Fragt, ob eine mögliche Dublette gespeichert werden soll."""

    return messagebox.askyesno(
        "Mögliche Dublette",
        "Ein Kontakt mit demselben Namen oder "
        "derselben E-Mail-Adresse existiert bereits.\n\n"
        "Möchten Sie den Kontakt trotzdem speichern?",
    )


def dublette_bearbeiten_bestaetigen():
    """Fragt, ob Änderungen trotz möglicher Dublette gespeichert werden."""

    return messagebox.askyesno(
        "Mögliche Dublette",
        "Ein anderer Kontakt mit demselben Namen oder "
        "derselben E-Mail-Adresse existiert bereits.\n\n"
        "Möchten Sie die Änderungen trotzdem speichern?",
    )


def programm_beenden_bestaetigen():
    """Fragt, ob das Programm beendet werden soll."""

    return messagebox.askyesno(
        "Programm beenden",
        "Möchten Sie das Kontaktbuch wirklich beenden?",
    )


def tastaturhilfe_anzeigen():
    """Zeigt die verfügbaren Tastenkürzel."""

    messagebox.showinfo(
        "Tastenkürzel",
        "Strg + N  – Neuer Kontakt\n"
        "Strg + F  – Suchfeld aktivieren\n"
        "Enter     – Kontakt bearbeiten\n"
        "Entf      – Kontakt löschen\n"
        "Escape    – Zur Startansicht\n"
        "Doppelklick – Kontakt bearbeiten",
    )


def programm_info_anzeigen():
    """Zeigt Informationen über das Kontaktbuch."""

    messagebox.showinfo(
        "Über Mein Kontaktbuch",
        "Mein Kontaktbuch\n\n"
        "Eine Kontaktverwaltung mit Python und Tkinter.\n\n"
        "Funktionen:\n"
        "• Kontakte anlegen\n"
        "• Kontakte bearbeiten\n"
        "• Kontakte löschen\n"
        "• Live-Suche\n"
        "• Speicherung als JSON",
    )

def import_fehler(meldung):
    messagebox.showerror(
        "Import fehlgeschlagen",
        meldung,
    )


def import_hinweis(meldung):
    messagebox.showinfo(
        "Kontaktimport",
        meldung,
    )


def import_dubletten_bestaetigen(
    anzahl_neu,
    anzahl_dubletten,
):
    return messagebox.askyesno(
        "Mögliche Dubletten",
        f"{anzahl_neu} neue Kontakte wurden gefunden.\n"
        f"{anzahl_dubletten} Kontakte scheinen bereits "
        f"vorhanden zu sein.\n\n"
        f"Sollen die möglichen Dubletten ebenfalls "
        f"importiert werden?",
    )


def import_erfolgreich(
    importiert,
    fehlerhaft=0,
    uebersprungen=0,
):
    text = (
        f"{importiert} Kontakte wurden importiert."
    )

    if uebersprungen:
        text += (
            f"\n{uebersprungen} mögliche Dubletten "
            f"wurden übersprungen."
        )

    if fehlerhaft:
        text += (
            f"\n{fehlerhaft} Einträge konnten nicht "
            f"übernommen werden."
        )

    messagebox.showinfo(
        "Import abgeschlossen",
        text,
    )


def speicherfehler_import():
    messagebox.showerror(
        "Speicherfehler",
        "Die importierten Kontakte konnten nicht "
        "gespeichert werden.",
    )


def export_hinweis(meldung):
    """Zeigt einen Hinweis zu einer leeren Exportauswahl."""

    messagebox.showinfo(
        "Kontaktexport",
        meldung,
    )


def export_erfolgreich(anzahl, exportformat):
    """Bestaetigt einen erfolgreichen Kontaktexport."""

    wort = "Kontakt wurde" if anzahl == 1 else "Kontakte wurden"
    messagebox.showinfo(
        "Export abgeschlossen",
        f"{anzahl} {wort} erfolgreich als "
        f"{exportformat} exportiert.",
    )


def export_fehler(meldung):
    """Zeigt einen Fehler beim Exportieren von Kontakten."""

    messagebox.showerror(
        "Export fehlgeschlagen",
        "Die Kontakte konnten nicht exportiert werden.\n\n"
        f"{meldung}",
    )
