"""Tests fuer den Kontaktimport mit Kategorien."""

import tempfile
import unittest
from pathlib import Path
from unittest import mock

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

    def test_outlook_csv_nutzt_komma_fallback(self):
        inhalt = (
            "First Name,Last Name,E-mail Address,Business Phone\n"
            "Max,Mustermann,max@example.org,+49 123 456\n"
        )
        urspruengliches_trennzeichen = kontaktimport.csv.excel.delimiter

        with mock.patch.object(
            kontaktimport.csv.Sniffer,
            "sniff",
            side_effect=kontaktimport.csv.Error,
        ):
            kontakte, fehler = self._csv_importieren(inhalt)

        self.assertEqual(fehler, [])
        self.assertEqual(len(kontakte), 1)
        self.assertEqual(kontakte[0]["name"], "Max Mustermann")
        self.assertEqual(kontakte[0]["email"], "max@example.org")
        self.assertEqual(kontakte[0]["telefon"], "+49 123 456")
        self.assertEqual(
            kontaktimport.csv.excel.delimiter,
            urspruengliches_trennzeichen,
        )

    def test_csv_fallback_ueberspringt_fuehrende_leerzeilen(self):
        inhalt = (
            "\n"
            "\n"
            "First Name,Last Name,E-mail Address\n"
            "Max,Mustermann,max@example.org\n"
        )

        with mock.patch.object(
            kontaktimport.csv.Sniffer,
            "sniff",
            side_effect=kontaktimport.csv.Error,
        ):
            kontakte, fehler = self._csv_importieren(inhalt)

        self.assertEqual(fehler, [])
        self.assertEqual(len(kontakte), 1)
        self.assertEqual(kontakte[0]["name"], "Max Mustermann")
        self.assertEqual(kontakte[0]["email"], "max@example.org")

    def test_semikolon_csv_nutzt_semikolon_fallback(self):
        inhalt = (
            "Name;E-Mail;Telefon\n"
            "Testkontakt;test@example.org;+49 123\n"
        )

        with mock.patch.object(
            kontaktimport.csv.Sniffer,
            "sniff",
            side_effect=kontaktimport.csv.Error,
        ):
            kontakte, fehler = self._csv_importieren(inhalt)

        self.assertEqual(fehler, [])
        self.assertEqual(len(kontakte), 1)
        self.assertEqual(kontakte[0]["name"], "Testkontakt")
        self.assertEqual(kontakte[0]["email"], "test@example.org")
        self.assertEqual(kontakte[0]["telefon"], "+49 123")

    def test_csv_trennzeichen_fallback(self):
        faelle = (
            ("Name,E-Mail", ","),
            ("Name;E-Mail", ";"),
            ("Name\tE-Mail", "\t"),
            ("Name|E-Mail", "|"),
            ("Name", ";"),
        )

        for kopfzeile, erwartet in faelle:
            with self.subTest(kopfzeile=kopfzeile):
                self.assertEqual(
                    kontaktimport._csv_trennzeichen_fallback(kopfzeile),
                    erwartet,
                )

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

    def test_csv_fotospalte_wird_ignoriert(self):
        kontakte, fehler = self._csv_importieren(
            "Name;Foto\nTestkontakt;bilder/falsch.png\n"
        )

        self.assertEqual(fehler, [])
        self.assertEqual(kontakte[0]["foto"], "")

    def test_vcard_photo_wird_ignoriert(self):
        kontakte, fehler = self._vcard_importieren(
            "PHOTO;ENCODING=b;TYPE=PNG:iVBORw0KGgo=\r\n"
        )

        self.assertEqual(fehler, [])
        self.assertEqual(kontakte[0]["foto"], "")


if __name__ == "__main__":
    unittest.main()
