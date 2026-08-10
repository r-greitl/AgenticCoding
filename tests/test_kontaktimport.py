"""Tests fuer den Kontaktimport mit Kategorien."""

import tempfile
import unittest
from pathlib import Path

import kontaktimport


class KategorieImportTests(unittest.TestCase):
    def _csv_importieren(self, inhalt):
        with tempfile.TemporaryDirectory() as verzeichnis:
            dateipfad = Path(verzeichnis) / "kontakte.csv"
            dateipfad.write_text(inhalt, encoding="utf-8")
            return kontaktimport.kontakte_importieren(dateipfad)

    def _vcard_importieren(self, zusaetzliche_zeilen=""):
        with tempfile.TemporaryDirectory() as verzeichnis:
            dateipfad = Path(verzeichnis) / "kontakt.vcf"
            dateipfad.write_text(
                "BEGIN:VCARD\r\n"
                "VERSION:3.0\r\n"
                "FN:Testkontakt\r\n"
                f"{zusaetzliche_zeilen}"
                "END:VCARD\r\n",
                encoding="utf-8",
                newline="",
            )
            return kontaktimport.kontakte_importieren(dateipfad)

    def test_csv_ohne_kategorie_bleibt_kompatibel(self):
        kontakte, fehler = self._csv_importieren(
            "Name;E-Mail\nTestkontakt;test@example.org\n"
        )

        self.assertEqual(fehler, [])
        self.assertEqual(kontakte[0]["kategorie"], "")

    def test_csv_kategorie_wird_kanonisch_importiert(self):
        kontakte, fehler = self._csv_importieren(
            "Name;Kategorie\nTestkontakt;freunde\n"
        )

        self.assertEqual(fehler, [])
        self.assertEqual(kontakte[0]["kategorie"], "Freunde")

    def test_unbekannte_csv_kategorie_verhindert_import_nicht(self):
        kontakte, fehler = self._csv_importieren(
            "Name;Kategorie\nTestkontakt;Sport\n"
        )

        self.assertEqual(fehler, [])
        self.assertEqual(len(kontakte), 1)
        self.assertEqual(kontakte[0]["kategorie"], "")

    def test_vcard_ohne_kategorie_bleibt_kompatibel(self):
        kontakte, fehler = self._vcard_importieren()

        self.assertEqual(fehler, [])
        self.assertEqual(kontakte[0]["kategorie"], "")

    def test_vcard_kategorie_wird_importiert(self):
        kontakte, fehler = self._vcard_importieren(
            "CATEGORIES:Verein\r\n"
        )

        self.assertEqual(fehler, [])
        self.assertEqual(kontakte[0]["kategorie"], "Verein")

    def test_unbekannte_vcard_kategorie_verhindert_import_nicht(self):
        kontakte, fehler = self._vcard_importieren(
            "CATEGORIES:Sport\r\n"
        )

        self.assertEqual(fehler, [])
        self.assertEqual(len(kontakte), 1)
        self.assertEqual(kontakte[0]["kategorie"], "")

    def test_mehrere_vcard_kategorien_werden_nicht_uebernommen(self):
        kontakte, fehler = self._vcard_importieren(
            "CATEGORIES:Familie,Freunde\r\n"
        )

        self.assertEqual(fehler, [])
        self.assertEqual(kontakte[0]["kategorie"], "")

    def test_zwei_bekannte_separate_kategorien_bleiben_leer(self):
        kontakte, fehler = self._vcard_importieren(
            "CATEGORIES:Familie\r\n"
            "CATEGORIES:Freunde\r\n"
        )

        self.assertEqual(fehler, [])
        self.assertEqual(kontakte[0]["kategorie"], "")

    def test_unbekannte_und_bekannte_separate_kategorien_bleiben_leer(self):
        kontakte, fehler = self._vcard_importieren(
            "CATEGORIES:Sport\r\n"
            "CATEGORIES:Arbeit\r\n"
        )

        self.assertEqual(fehler, [])
        self.assertEqual(kontakte[0]["kategorie"], "")

    def test_bekannte_und_unbekannte_separate_kategorien_bleiben_leer(self):
        kontakte, fehler = self._vcard_importieren(
            "CATEGORIES:Verein\r\n"
            "CATEGORIES:Hobby\r\n"
        )

        self.assertEqual(fehler, [])
        self.assertEqual(kontakte[0]["kategorie"], "")

    def test_zwei_unbekannte_separate_kategorien_bleiben_leer(self):
        kontakte, fehler = self._vcard_importieren(
            "CATEGORIES:Sport\r\n"
            "CATEGORIES:Hobby\r\n"
        )

        self.assertEqual(fehler, [])
        self.assertEqual(kontakte[0]["kategorie"], "")


if __name__ == "__main__":
    unittest.main()
