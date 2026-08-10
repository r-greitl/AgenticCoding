import tkinter as tk
from tkinter import filedialog

import dialoge
import datei
import kontaktexport
import kontaktimport
import kontaktlogik

from kontaktfelder import (
    FELDER,
    kontakt_aus_eingabefeldern,
    kontakt_vervollstaendigen,
)

from validierung import kontakt_validieren
from styles import (
    FARBE_HINTERGRUND,
    FARBE_KARTE,
    FARBE_PRIMAER,
    FARBE_PRIMAER_AKTIV,
    FARBE_ERFOLG,
    FARBE_ERFOLG_AKTIV,
    FARBE_WARNUNG,
    FARBE_WARNUNG_AKTIV,
    FARBE_GEFAHR,
    FARBE_GEFAHR_AKTIV,
    FARBE_TEXT,
    FARBE_TEXT_HELL,
    FARBE_RAND,
    FARBE_AUSWAHL,
    SCHRIFT_TITEL,
    SCHRIFT_UNTERTITEL,
    SCHRIFT_NORMAL,
    SCHRIFT_KLEIN,
    SCHRIFT_BUTTON,
    ABSTAND_KLEIN,
    ABSTAND_NORMAL,
    ABSTAND_GROSS,
    FENSTER_TITEL,
    FENSTER_BREITE,
    FENSTER_HOEHE,
    FENSTER_MIN_BREITE,
    FENSTER_MIN_HOEHE,
)

geladene_kontakte = datei.kontakte_laden()

kontaktliste = [
    kontakt_vervollstaendigen(kontakt)
    for kontakt in geladene_kontakte
]

kontaktliste = kontaktlogik.kontakte_sortieren(
    kontaktliste
)
angezeigte_kontakte = kontaktliste.copy()


fenster = tk.Tk()
fenster.title(FENSTER_TITEL)
fenster.geometry(f"{FENSTER_BREITE}x{FENSTER_HOEHE}")
fenster.minsize(
    FENSTER_MIN_BREITE,
    FENSTER_MIN_HOEHE,
)
fenster.configure(
    bg=FARBE_HINTERGRUND,
)



ueberschrift = tk.Label(
    fenster,
    text="Mein Kontaktbuch",
    font=SCHRIFT_TITEL
    
)
ueberschrift.pack(pady=(20, 15))


suchbereich = tk.Frame(fenster)
suchbereich.pack(fill="x", padx=30, pady=(0, 15))

such_label = tk.Label(
    suchbereich,
    text="Suche:",
    
)
such_label.pack(side="left", padx=(0, 10))

suchtext = tk.StringVar()

suchfeld = tk.Entry(
    suchbereich,
    textvariable=suchtext,
    font=SCHRIFT_UNTERTITEL,
    
    relief="solid",
    bd=1,
)
suchfeld.pack(side="left", fill="x", expand=True, ipady=6)


hauptbereich = tk.Frame(fenster)
hauptbereich.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=(0, 20),
)


listenbereich = tk.Frame(
    hauptbereich,
        highlightthickness=1,
)
listenbereich.pack(
    side="left",
    fill="both",
    padx=(0, 12),
)

listen_ueberschrift = tk.Label(
    listenbereich,
    text="Kontakte",
    font=SCHRIFT_UNTERTITEL
    )
listen_ueberschrift.pack(
    anchor="w",
    padx=15,
    pady=(15, 10),
)

listeninhalt = tk.Frame(
    listenbereich,
   
)
listeninhalt.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=(0, 10),
)

scrollbar = tk.Scrollbar(listeninhalt)
scrollbar.pack(side="right", fill="y")

liste = tk.Listbox(
    listeninhalt,
    width=28,
    font=SCHRIFT_UNTERTITEL,
    
    selectforeground="white",
    relief="flat",
    bd=0,
    highlightthickness=0,
    yscrollcommand=scrollbar.set,
)
liste.pack(
    side="left",
    fill="both",
    expand=True,
)

scrollbar.config(command=liste.yview)


detailbereich = tk.Frame(
    hauptbereich,
       highlightthickness=1,
    padx=25,
    pady=20,
)
detailbereich.pack(
    side="left",
    fill="both",
    expand=True,
)


status_text = tk.StringVar()

statusleiste = tk.Label(
    fenster,
    textvariable=status_text,
    anchor="w",
    font=SCHRIFT_KLEIN,
    bg=FARBE_PRIMAER,
    fg="white",
    padx=12,
    pady=6,
)

statusleiste.pack(
    side="bottom",
    fill="x",
)


def status_aktualisieren():
    anzahl_gesamt = len(kontaktliste)
    anzahl_sichtbar = len(angezeigte_kontakte)
    suchbegriff = suchtext.get().strip()

    if suchbegriff:
        status_text.set(
            f"{anzahl_sichtbar} Treffer | "
            f"{anzahl_gesamt} Kontakte insgesamt"
        )
    else:
        wort = "Kontakt" if anzahl_gesamt == 1 else "Kontakte"
        status_text.set(f"{anzahl_gesamt} {wort} geladen")


def detailbereich_leeren():
    for element in detailbereich.winfo_children():
        element.destroy()

def button_erstellen(
    elternelement,
    text,
    command,
    hintergrundfarbe,
    aktive_farbe=None,
    breite=None,
):
    if aktive_farbe is None:
        aktive_farbe = hintergrundfarbe

    einstellungen = {
        "text": text,
        "command": command,
        "font": SCHRIFT_BUTTON,
        "bg": hintergrundfarbe,
        "fg": "white",
        "activebackground": aktive_farbe,
        "activeforeground": "white",
        "relief": "flat",
        "bd": 0,
        "padx": 14,
        "pady": 8,
        "cursor": "hand2",
    }

    if breite is not None:
        einstellungen["width"] = breite

    return tk.Button(
        elternelement,
        **einstellungen,
    )


def formular_erstellen(titel, kontakt=None):
    detailbereich_leeren()

    tk.Label(
        detailbereich,
        text=titel,
        font=("Arial", 16, "bold"),
        
    ).pack(pady=(0, 15))

    eingabefelder = {}

    for beschriftung, feldname in FELDER:
        zeile = tk.Frame(
            detailbereich,
            
        )
        zeile.pack(fill="x", pady=4)

        tk.Label(
            zeile,
            text=f"{beschriftung}:",
            width=15,
            anchor="w",
            
        ).pack(side="left")

        eingabe = tk.Entry(
            zeile,
            
            relief="solid",
            bd=1,
        )
        eingabe.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=4,
        )

        if kontakt is not None:
            eingabe.insert(0, kontakt.get(feldname, ""))

        eingabefelder[feldname] = eingabe

    eingabefelder["name"].focus_set()
    return eingabefelder

def kontakt_anzeigetext(kontakt):
    """Erstellt den Text für einen Eintrag in der Kontaktliste."""

    name = kontakt.get("name", "").strip()
    wohnort = kontakt.get("wohnort", "").strip()

    if wohnort:
        return f"{name} – {wohnort}"

    return name

def kontaktliste_aktualisieren():
    """Aktualisiert die sichtbaren Einträge und die Statusleiste."""

    liste.delete(0, tk.END)

    for kontakt in angezeigte_kontakte:
        liste.insert(
            tk.END,
            kontakt_anzeigetext(kontakt),
        )

    status_aktualisieren()


def kontakte_filtern(*_):
    global angezeigte_kontakte

    suchtext = suchfeld.get()

    angezeigte_kontakte = kontaktlogik.kontakte_suchen(
        kontaktliste,
        suchtext,
    )

    kontaktliste_aktualisieren() 

def kontakt_auswahl_anzeigen(event=None):
    auswahl = liste.curselection()

    if not auswahl:
        return

    index = auswahl[0]

    if index >= len(angezeigte_kontakte):
        return

    kontakt = angezeigte_kontakte[index]
    detailbereich_leeren()

    tk.Label(
        detailbereich,
        text="Kontaktdetails",
        
    ).pack(anchor="w", pady=(0, 20))

    for beschriftung, feldname in FELDER:
        zeile = tk.Frame(detailbereich,)
        zeile.pack(fill="x", pady=4)

        tk.Label(
            zeile,
            text=f"{beschriftung}:",
            width=15,
            anchor="w",
        
        ).pack(side="left")

        tk.Label(
            zeile,
            text=kontakt.get(feldname, ""),
            anchor="w",
            
        ).pack(side="left", fill="x", expand=True)

    buttonbereich_erstellen()

def kontaktliste_sortieren():
    """Sortiert die globale Kontaktliste nach Namen."""

    sortierte_kontakte = kontaktlogik.kontakte_sortieren(
        kontaktliste
    )

    kontaktliste.clear()
    kontaktliste.extend(sortierte_kontakte)

def neuer_kontakt_formular():
    eingabefelder = formular_erstellen(
        "Neuen Kontakt anlegen"
    )

    def kontakt_speichern():
        neuer_kontakt = kontakt_aus_eingabefeldern(
            eingabefelder
        )

        ist_gueltig, fehlermeldung = kontakt_validieren(
            neuer_kontakt
        )

        if not ist_gueltig:
           dialoge.ungueltige_eingabe(fehlermeldung)
           return

        if kontaktlogik.kontakt_bereits_vorhanden(
           kontaktliste,
            neuer_kontakt,
        ):
            if not dialoge.dublette_speichern_bestaetigen():
                return

        kontaktliste.append(neuer_kontakt)
        kontaktliste_sortieren()

        if datei.kontakte_speichern(kontaktliste):
            kontakte_filtern()
            startansicht_anzeigen()
            dialoge.kontakt_gespeichert()

        else:
            kontaktliste.remove(neuer_kontakt)
            dialoge.speicherfehler_neuer_kontakt()

    formular_buttons = tk.Frame(
        detailbereich,
        bg=FARBE_KARTE,
    )
    formular_buttons.pack(
        pady=20,
    )

    button_erstellen(
        formular_buttons,
        "Speichern",
        kontakt_speichern,
        FARBE_ERFOLG,
        FARBE_ERFOLG_AKTIV,
    ).pack(
        side="left",
        padx=5,
    )

    button_erstellen(
        formular_buttons,
        "Abbrechen",
        startansicht_anzeigen,
        FARBE_GEFAHR,
        FARBE_GEFAHR_AKTIV,
    ).pack(
        side="left",
        padx=5,
    )


def kontakt_bearbeiten_formular():
    auswahl = liste.curselection()

    if not auswahl:
        dialoge.keine_auswahl()
        return

    index = auswahl[0]
    kontakt = angezeigte_kontakte[index]

    eingabefelder = formular_erstellen(
        "Kontakt bearbeiten",
        kontakt,
    )

    def kontakt_aenderungen_speichern():
        geaenderter_kontakt = kontakt_aus_eingabefeldern(
            eingabefelder
        )

        ist_gueltig, fehlermeldung = kontakt_validieren(
            geaenderter_kontakt
        )

        if not ist_gueltig:
            dialoge.ungueltige_eingabe(fehlermeldung)
            return

        if kontaktlogik.kontakt_bereits_vorhanden(
            kontaktliste,
            geaenderter_kontakt,
           kontakt_ignorieren=kontakt,
        ):
            if not dialoge.dublette_bearbeiten_bestaetigen():
                return

        alter_kontakt = kontakt.copy()

        kontakt.clear()
        kontakt.update(geaenderter_kontakt)

        kontaktliste_sortieren()

        if datei.kontakte_speichern(kontaktliste):
            kontakte_filtern()
            startansicht_anzeigen()
            dialoge.kontakt_geaendert()

        else:
            kontakt.clear()
            kontakt.update(alter_kontakt)

            kontaktliste_sortieren()
            kontakte_filtern()

            dialoge.speicherfehler_bearbeiten()

    formular_buttons = tk.Frame(
        detailbereich,
        bg=FARBE_KARTE,
    )
    formular_buttons.pack(pady=20)

    button_erstellen(
        formular_buttons,
        "Änderungen speichern",
        kontakt_aenderungen_speichern,
        FARBE_ERFOLG,
        FARBE_ERFOLG_AKTIV,
        breite=20,
    ).pack(
        side="left",
        padx=5,
    )

    button_erstellen(
        formular_buttons,
        "Abbrechen",
        startansicht_anzeigen,
        FARBE_GEFAHR,
        FARBE_GEFAHR_AKTIV,
    ).pack(
        side="left",
        padx=5,
    )


def kontakt_loeschen():
    auswahl = liste.curselection()

    if not auswahl:
        dialoge.keine_auswahl()
        return

    index = auswahl[0]
    kontakt = angezeigte_kontakte[index]

    name = kontakt.get("name", "")

    if not dialoge.kontakt_loeschen_bestaetigen(name):
        return

    kontaktliste.remove(kontakt)

    if datei.kontakte_speichern(kontaktliste):
        kontakte_filtern()
        startansicht_anzeigen()
        dialoge.kontakt_geloescht()

    else:
        kontaktliste.append(kontakt)
        kontaktliste_sortieren()
        kontakte_filtern()

        dialoge.speicherfehler_loeschen()

    
def programm_beenden():
    if dialoge.programm_beenden_bestaetigen():
        fenster.destroy()


def suchfeld_fokussieren(event=None):
    suchfeld.focus_set()
    suchfeld.select_range(0, tk.END)

def kontakte_aus_datei_importieren():
    dateiname = filedialog.askopenfilename(
        title="Kontakte importieren",
        filetypes=[
            (
                "Unterstützte Kontaktdateien",
                "*.csv *.vcf *.vcard",
            ),
            (
                "CSV-Dateien",
                "*.csv",
            ),
            (
                "vCard-Dateien",
                "*.vcf *.vcard",
            ),
            (
                "Alle Dateien",
                "*.*",
            ),
        ],
    )

    if not dateiname:
        return

    importierte_kontakte, fehlerliste = (
        kontaktimport.kontakte_importieren(
            dateiname
        )
    )

    if not importierte_kontakte:
        meldung = (
            "Es konnten keine gültigen Kontakte "
            "importiert werden."
        )

        if fehlerliste:
            meldung += "\n\n" + "\n".join(
                fehlerliste[:10]
            )

        dialoge.import_fehler(meldung)
        return

    neue_kontakte = []
    dubletten = []

    for kontakt in importierte_kontakte:
        if kontaktlogik.kontakt_bereits_vorhanden(
            kontaktliste,
            kontakt,
        ):
            dubletten.append(kontakt)
        else:
            neue_kontakte.append(kontakt)
    bestaetigung = False
    if dubletten:
        bestaetigung = (
            dialoge.import_dubletten_bestaetigen(
                anzahl_neu=len(neue_kontakte),
                anzahl_dubletten=len(dubletten),
            )
        )

        if bestaetigung:
            neue_kontakte.extend(dubletten)

    if not neue_kontakte:
        dialoge.import_hinweis(
            "Es wurden keine neuen Kontakte übernommen."
        )
        return

    kontaktliste.extend(neue_kontakte)
    kontaktliste_sortieren()

    if datei.kontakte_speichern(kontaktliste):
        kontakte_filtern()
        startansicht_anzeigen()

        dialoge.import_erfolgreich(
            importiert=len(neue_kontakte),
            fehlerhaft=len(fehlerliste),
            uebersprungen=(
                len(dubletten)
                if dubletten
                and not bestaetigung
                else 0
            ),
        )
    else:
        for kontakt in neue_kontakte:
            if kontakt in kontaktliste:
                kontaktliste.remove(kontakt)

        dialoge.speicherfehler_import()


def kontakte_exportieren(zu_exportierende_kontakte, exportformat):
    """Steuert den Export einer uebergebenen Kontaktliste."""

    if not zu_exportierende_kontakte:
        dialoge.export_hinweis(
            "Es sind keine Kontakte fuer den Export vorhanden."
        )
        return

    exportformat = exportformat.casefold()

    if exportformat != "vcard":
        dialoge.export_fehler(
            f"Das Exportformat {exportformat} wird nicht unterstuetzt."
        )
        return

    dateiname = filedialog.asksaveasfilename(
        title="Kontakte als vCard exportieren",
        defaultextension=".vcf",
        filetypes=[
            ("vCard-Dateien", "*.vcf"),
            ("Alle Dateien", "*.*"),
        ],
    )

    if not dateiname:
        return

    erfolgreich, fehlermeldung = (
        kontaktexport.kontakte_als_vcard_exportieren(
            zu_exportierende_kontakte,
            dateiname,
        )
    )

    if erfolgreich:
        dialoge.export_erfolgreich(
            len(zu_exportierende_kontakte),
            "vCard",
        )
    else:
        dialoge.export_fehler(fehlermeldung)


def menueleiste_erstellen():
    menueleiste = tk.Menu(fenster)

    datei_menu = tk.Menu(
        menueleiste,
        tearoff=False
    )
    datei_menu.add_command(
        label="Neuer Kontakt",
        accelerator="Strg+N",
        command=neuer_kontakt_formular
    )
    datei_menu.add_command(
    label="Kontakte importieren …",
    accelerator="Strg+I",
    command=kontakte_aus_datei_importieren,
)
    datei_menu.add_separator()
    datei_menu.add_command(
        label="Alle Kontakte als vCard exportieren …",
        command=lambda: kontakte_exportieren(
            kontaktliste,
            "vCard",
        ),
    )
    datei_menu.add_command(
        label="Sichtbare Kontakte als vCard exportieren …",
        command=lambda: kontakte_exportieren(
            angezeigte_kontakte,
            "vCard",
        ),
    )
    datei_menu.add_separator()
    datei_menu.add_command(
        label="Beenden",
        command=programm_beenden
    )

    menueleiste.add_cascade(
        label="Datei",
        menu=datei_menu
    )

    bearbeiten_menu = tk.Menu(
        menueleiste,
        tearoff=False
    )
    bearbeiten_menu.add_command(
        label="Kontakt bearbeiten",
        accelerator="Enter",
        command=kontakt_bearbeiten_formular
    )
    bearbeiten_menu.add_command(
        label="Kontakt löschen",
        accelerator="Entf",
        command=kontakt_loeschen
    )
    bearbeiten_menu.add_separator()
    bearbeiten_menu.add_command(
        label="Suchen",
        accelerator="Strg+F",
        command=suchfeld_fokussieren
    )

    menueleiste.add_cascade(
        label="Bearbeiten",
        menu=bearbeiten_menu
    )

    hilfe_menu = tk.Menu(
        menueleiste,
        tearoff=False
    )
    hilfe_menu.add_command(
        label="Tastenkürzel",
        command=dialoge.tastaturhilfe_anzeigen
    )
    hilfe_menu.add_separator()
    hilfe_menu.add_command(
        label="Über Mein Kontaktbuch",
        command=dialoge.programm_info_anzeigen
    )

    menueleiste.add_cascade(
        label="Hilfe",
        menu=hilfe_menu
    )

    fenster.config(menu=menueleiste)

    
def buttonbereich_erstellen():
    buttonbereich = tk.Frame(
        detailbereich,
        bg=FARBE_KARTE,
    )
    buttonbereich.pack(
        pady=20,
    )

    button_erstellen(
        buttonbereich,
        "Neuer Kontakt",
        neuer_kontakt_formular,
        FARBE_PRIMAER,
        FARBE_PRIMAER_AKTIV,
    ).pack(
        side="left",
        padx=5,
    )

    button_erstellen(
        buttonbereich,
        "Kontakt bearbeiten",
        kontakt_bearbeiten_formular,
        FARBE_WARNUNG,
        FARBE_WARNUNG_AKTIV,
    ).pack(
        side="left",
        padx=5,
    )

    button_erstellen(
        buttonbereich,
        "Kontakt löschen",
        kontakt_loeschen,
        FARBE_GEFAHR,
        FARBE_GEFAHR_AKTIV,
    ).pack(
        side="left",
        padx=5,
    )


def startansicht_anzeigen():
    detailbereich_leeren()

    tk.Label(
        detailbereich,
        text="Kontaktdetails",
        
    ).pack(anchor="w", pady=(0, 15))

    tk.Label(
        detailbereich,
        text="Bitte wählen Sie links einen Kontakt aus.",
        justify="left",
        anchor="nw",
        
    ).pack(
        fill="both",
        expand=True,
    )

    buttonbereich_erstellen()


kontaktliste_aktualisieren()
startansicht_anzeigen()
menueleiste_erstellen()

def kontakt_mit_enter_bearbeiten(event=None):
    if liste.curselection():
        kontakt_bearbeiten_formular()


def kontakt_mit_entfernen_loeschen(event=None):
    if liste.curselection():
        kontakt_loeschen()


def neuen_kontakt_oeffnen(event=None):
    neuer_kontakt_formular()




liste.bind(
    "<<ListboxSelect>>",
    kontakt_auswahl_anzeigen,
)


def kontakt_doppelklick(event=None):
    if liste.curselection():
        kontakt_bearbeiten_formular()


liste.bind(
    "<Double-Button-1>",
    kontakt_doppelklick,
)

def zur_kontaktliste_wechseln(event=None):
    if liste.size() > 0:
        liste.focus_set()
        liste.selection_clear(0, tk.END)
        liste.selection_set(0)
        liste.activate(0)
        kontakt_auswahl_anzeigen()

suchfeld.bind(
    "<Down>",
    zur_kontaktliste_wechseln,
)

liste.bind(
    "<Return>",
    kontakt_mit_enter_bearbeiten,
)

liste.bind(
    "<Delete>",
    kontakt_mit_entfernen_loeschen,
)

fenster.bind(
    "<Control-n>",
    neuen_kontakt_oeffnen,
)

fenster.bind(
    "<Control-f>",
    suchfeld_fokussieren,
)

fenster.bind(
    "<Escape>",
    lambda event: startansicht_anzeigen(),
)
fenster.bind(
    "<Control-i>",
    lambda event: kontakte_aus_datei_importieren(),
)

suchtext.trace_add("write", kontakte_filtern)

suchfeld.focus_set()

fenster.protocol(
    "WM_DELETE_WINDOW",
    programm_beenden
)

fenster.mainloop()
