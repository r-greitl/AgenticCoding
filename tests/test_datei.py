"""Tests fuer die JSON-Kompatibilitaet des Kategorienfelds."""

import json
import tempfile
import unittest
from pathlib import Path

import datei
from kontaktfelder import kontakt_vervollstaendigen


class KategorieDateiTests(unittest.TestCase):
    def setUp(self):
        self.verzeichnis = tempfile.TemporaryDirectory()
        self.alter_dateipfad = datei.DATEIPFAD
        self.alter_sicherungspfad = datei.SICHERUNGSPFAD
        datei.DATEIPFAD = Path(self.verzeichnis.name) / "kontakte.json"
        datei.SICHERUNGSPFAD = (
            Path(self.verzeichnis.name) / "kontakte_backup.json"
        )

    def tearDown(self):
        datei.DATEIPFAD = self.alter_dateipfad
        datei.SICHERUNGSPFAD = self.alter_sicherungspfad
        self.verzeichnis.cleanup()

    def test_alte_datei_wird_beim_laden_nicht_umgeschrieben(self):
        urspruengliche_daten = [{"name": "Alter Kontakt"}]
        datei.DATEIPFAD.write_text(
            json.dumps(urspruengliche_daten),
            encoding="utf-8",
        )
        inhalt_vorher = datei.DATEIPFAD.read_bytes()

        geladene_kontakte = datei.kontakte_laden()
        vollstaendige_kontakte = [
            kontakt_vervollstaendigen(kontakt)
            for kontakt in geladene_kontakte
        ]

        self.assertEqual(vollstaendige_kontakte[0]["kategorie"], "")
        self.assertEqual(datei.DATEIPFAD.read_bytes(), inhalt_vorher)

    def test_kategorie_bleibt_beim_speichern_erhalten(self):
        kontakte = [{"name": "Testkontakt", "kategorie": "Arbeit"}]

        self.assertTrue(datei.kontakte_speichern(kontakte))

        self.assertEqual(datei.kontakte_laden(), kontakte)


if __name__ == "__main__":
    unittest.main()
