"""Verhaltenstests fuer den nebenwirkungsfreien GUI-Import."""

import importlib
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tkinter.ttk
import unittest
from unittest import mock

import datei


REPOSITORY = Path(__file__).resolve().parents[1]


def gui_neu_importieren():
    sys.modules.pop("kontaktbuch_gui", None)
    return importlib.import_module("kontaktbuch_gui")


class KontaktbuchGuiStartupTests(unittest.TestCase):
    def tearDown(self):
        sys.modules.pop("kontaktbuch_gui", None)

    def test_import_erzeugt_weder_tk_noch_widgets_oder_mainloop(self):
        with (
            mock.patch("tkinter.Tk") as tk_erzeugen,
            mock.patch("tkinter.Label") as label_erzeugen,
        ):
            modul = gui_neu_importieren()

        tk_erzeugen.assert_not_called()
        label_erzeugen.assert_not_called()
        self.assertIsNone(modul.fenster)

    def test_import_laed_keine_kontakte(self):
        with mock.patch.object(datei, "kontakte_laden") as laden:
            gui_neu_importieren()

        laden.assert_not_called()

    def test_import_veraendert_kontaktdatei_nicht(self):
        vorher_vorhanden = datei.DATEIPFAD.exists()
        vorher = datei.DATEIPFAD.read_bytes() if vorher_vorhanden else None

        gui_neu_importieren()

        self.assertEqual(datei.DATEIPFAD.exists(), vorher_vorhanden)
        if vorher_vorhanden:
            self.assertEqual(datei.DATEIPFAD.read_bytes(), vorher)

    def test_import_funktioniert_headless(self):
        code = (
            "import tkinter as tk; "
            "tk.Tk=lambda: (_ for _ in ()).throw("
            "RuntimeError('Tk darf nicht starten')); "
            "import kontaktbuch_gui"
        )
        umgebung = os.environ.copy()
        umgebung.pop("DISPLAY", None)

        ergebnis = subprocess.run(
            [sys.executable, "-c", code],
            cwd=REPOSITORY,
            env=umgebung,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

        self.assertEqual(ergebnis.returncode, 0, ergebnis.stderr)

    def test_main_startet_ablauf_in_vorgesehener_reihenfolge(self):
        modul = gui_neu_importieren()
        aufrufe = []
        fenster = mock.Mock()
        suchfeld = mock.Mock()

        def oberflaeche_initialisieren():
            aufrufe.append("oberflaeche")
            modul.fenster = fenster
            modul.suchfeld = suchfeld

        with (
            mock.patch.object(
                modul,
                "laufzeitdaten_initialisieren",
                side_effect=lambda: aufrufe.append("laufzeitdaten"),
            ),
            mock.patch.object(
                modul,
                "oberflaeche_initialisieren",
                side_effect=oberflaeche_initialisieren,
            ),
            mock.patch.object(
                modul,
                "kontaktliste_aktualisieren",
                side_effect=lambda: aufrufe.append("kontaktliste"),
            ),
            mock.patch.object(
                modul,
                "startansicht_anzeigen",
                side_effect=lambda: aufrufe.append("startansicht"),
            ),
            mock.patch.object(
                modul,
                "menueleiste_erstellen",
                side_effect=lambda: aufrufe.append("menue"),
            ),
            mock.patch.object(
                modul,
                "ereignisse_binden",
                side_effect=lambda: aufrufe.append("ereignisse"),
            ),
        ):
            suchfeld.focus_set.side_effect = lambda: aufrufe.append("fokus")
            fenster.mainloop.side_effect = lambda: aufrufe.append("mainloop")
            modul.main()

        self.assertEqual(
            aufrufe,
            [
                "laufzeitdaten",
                "oberflaeche",
                "kontaktliste",
                "startansicht",
                "menue",
                "ereignisse",
                "fokus",
                "mainloop",
            ],
        )

    def test_direkter_skriptstart_erreicht_mainloop(self):
        fenster = mock.MagicMock()
        widget = mock.MagicMock()

        with (
            mock.patch.object(datei, "kontakte_laden", return_value=[]),
            mock.patch("tkinter.Tk", return_value=fenster),
            mock.patch("tkinter.Label", return_value=widget),
            mock.patch("tkinter.Frame", return_value=widget),
            mock.patch("tkinter.Entry", return_value=widget),
            mock.patch("tkinter.Scrollbar", return_value=widget),
            mock.patch("tkinter.Listbox", return_value=widget),
            mock.patch("tkinter.StringVar", return_value=widget),
            mock.patch("tkinter.Menu", return_value=widget),
        ):
            runpy.run_module("kontaktbuch_gui", run_name="__main__")

        fenster.mainloop.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
