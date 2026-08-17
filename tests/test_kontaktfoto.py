"""Tests fuer die sichere, GUI-unabhaengige Kontaktfotoverwaltung."""

import tempfile
import unittest
from pathlib import Path
from unittest import mock

import kontaktfoto


class KontaktfotoTests(unittest.TestCase):
    def setUp(self):
        self.verzeichnis = tempfile.TemporaryDirectory()
        self.alter_anwendungsordner = kontaktfoto.ANWENDUNGSORDNER
        self.alter_bilderordner = kontaktfoto.BILDERORDNER
        kontaktfoto.ANWENDUNGSORDNER = Path(self.verzeichnis.name)
        kontaktfoto.BILDERORDNER = kontaktfoto.ANWENDUNGSORDNER / "bilder"

    def tearDown(self):
        kontaktfoto.ANWENDUNGSORDNER = self.alter_anwendungsordner
        kontaktfoto.BILDERORDNER = self.alter_bilderordner
        self.verzeichnis.cleanup()

    def _quelle(self, name, inhalt=b"bild"):
        pfad = Path(self.verzeichnis.name) / name
        pfad.write_bytes(inhalt)
        return pfad

    def test_png_und_gif_werden_mit_eindeutigen_namen_kopiert(self):
        for endung in (".png", ".gif"):
            with self.subTest(endung=endung):
                quelle = self._quelle(f"quelle{endung}")
                erster = kontaktfoto.foto_kopieren(quelle)
                zweiter = kontaktfoto.foto_kopieren(quelle)

                self.assertNotEqual(erster, zweiter)
                self.assertTrue(erster.startswith("bilder/"))
                self.assertFalse(Path(erster).is_absolute())
                self.assertTrue(kontaktfoto.verwalteten_pfad_aufloesen(erster).is_file())

    def test_fehlende_quelldatei_wird_abgelehnt(self):
        with self.assertRaises(FileNotFoundError):
            kontaktfoto.foto_kopieren(Path(self.verzeichnis.name) / "fehlt.png")

    def test_nicht_unterstuetzte_endung_wird_abgelehnt(self):
        with self.assertRaises(ValueError):
            kontaktfoto.foto_kopieren(self._quelle("foto.jpg"))

    def test_absolute_pfade_und_punktsegmente_werden_abgelehnt(self):
        for pfad in (
            str(Path(self.verzeichnis.name) / "bild.png"),
            "bilder/../bild.png",
            "bilder/unterordner/../foto.png",
            "bilder/./foto.png",
        ):
            with self.subTest(pfad=pfad):
                self.assertIsNone(kontaktfoto.verwalteten_pfad_aufloesen(pfad))
                self.assertFalse(kontaktfoto.foto_loeschen(pfad))

    def test_gueltiger_direkter_bilderpfad_wird_aufgeloest(self):
        erwartet = kontaktfoto.BILDERORDNER / "foto.png"

        self.assertEqual(
            kontaktfoto.verwalteten_pfad_aufloesen("bilder/foto.png"),
            erwartet,
        )

    def test_kopierfehler_entfernt_partielle_zieldatei(self):
        quelle = self._quelle("quelle.png", b"original")

        def teilweise_kopieren(_quelle, ziel):
            Path(ziel).write_bytes(b"teilweise")
            raise OSError("simulierter Kopierfehler")

        with mock.patch(
            "kontaktfoto.shutil.copy2",
            side_effect=teilweise_kopieren,
        ):
            with self.assertRaises(OSError):
                kontaktfoto.foto_kopieren(quelle)

        self.assertEqual(list(kontaktfoto.BILDERORDNER.iterdir()), [])
        self.assertEqual(quelle.read_bytes(), b"original")

    def test_nur_verwaltete_datei_wird_geloescht(self):
        quelle = self._quelle("quelle.png")
        relativer_pfad = kontaktfoto.foto_kopieren(quelle)
        verwaltete_datei = kontaktfoto.verwalteten_pfad_aufloesen(relativer_pfad)

        self.assertTrue(kontaktfoto.foto_loeschen(relativer_pfad))
        self.assertFalse(verwaltete_datei.exists())
        self.assertTrue(quelle.exists())

    def test_neue_kopie_wird_bei_speicherfehler_zurueckgerollt(self):
        quelle = self._quelle("neu.png")
        kontakt = {"name": "Alter Zustand", "foto": ""}
        erwartet = kontakt.copy()

        erfolgreich = kontaktfoto.kontaktfoto_speichern(
            kontakt,
            {"name": "Neuer Zustand"},
            lambda: False,
            quelldatei=quelle,
        )

        self.assertFalse(erfolgreich)
        self.assertEqual(kontakt, erwartet)
        self.assertEqual(list(kontaktfoto.BILDERORDNER.iterdir()), [])
        self.assertTrue(quelle.exists())

    def test_ersetzen_rollt_bei_speicherfehler_zurueck(self):
        altes_foto = kontaktfoto.BILDERORDNER / "alt.png"
        altes_foto.parent.mkdir()
        altes_foto.write_bytes(b"alt")
        quelle = self._quelle("neu.png", b"neu")
        kontakt = {"name": "Kontakt", "foto": "bilder/alt.png"}

        erfolgreich = kontaktfoto.kontaktfoto_speichern(
            kontakt,
            {"name": "Geaendert"},
            lambda: False,
            quelldatei=quelle,
        )

        self.assertFalse(erfolgreich)
        self.assertEqual(kontakt["foto"], "bilder/alt.png")
        self.assertTrue(altes_foto.exists())
        self.assertEqual(list(kontaktfoto.BILDERORDNER.iterdir()), [altes_foto])

    def test_entfernen_rollt_bei_speicherfehler_zurueck(self):
        altes_foto = kontaktfoto.BILDERORDNER / "alt.gif"
        altes_foto.parent.mkdir()
        altes_foto.write_bytes(b"alt")
        kontakt = {"name": "Kontakt", "foto": "bilder/alt.gif"}

        erfolgreich = kontaktfoto.kontaktfoto_speichern(
            kontakt,
            {"name": "Geaendert"},
            lambda: False,
            entfernen=True,
        )

        self.assertFalse(erfolgreich)
        self.assertEqual(kontakt["foto"], "bilder/alt.gif")
        self.assertTrue(altes_foto.exists())

    def test_erfolgreiches_ersetzen_loescht_alt_nach_speicherung(self):
        altes_foto = kontaktfoto.BILDERORDNER / "alt.png"
        altes_foto.parent.mkdir()
        altes_foto.write_bytes(b"alt")
        quelle = self._quelle("neu.png", b"neu")
        kontakt = {"name": "Kontakt", "foto": "bilder/alt.png"}

        def speichern():
            self.assertNotEqual(kontakt["foto"], "bilder/alt.png")
            self.assertTrue(
                kontaktfoto.verwalteten_pfad_aufloesen(
                    kontakt["foto"]
                ).exists()
            )
            self.assertTrue(altes_foto.exists())
            return True

        erfolgreich = kontaktfoto.kontaktfoto_speichern(
            kontakt,
            {"name": "Geaendert"},
            speichern,
            quelldatei=quelle,
        )

        self.assertTrue(erfolgreich)
        self.assertFalse(altes_foto.exists())
        self.assertTrue(
            kontaktfoto.verwalteten_pfad_aufloesen(kontakt["foto"]).exists()
        )


if __name__ == "__main__":
    unittest.main()
