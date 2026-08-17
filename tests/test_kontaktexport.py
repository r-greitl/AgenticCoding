"""Tests fuer den vCard-Export."""

import tempfile
import unittest
from pathlib import Path

import kontaktexport
import kontaktimport


class VCardExportTests(unittest.TestCase):
    def test_kontakt_als_vcard_exportiert_alle_felder(self):
        kontakt = {
            "name": "Ada Lovelace",
            "telefon": "+44 123",
            "email": "ada@example.org",
            "wohnort": "London",
            "beruf": "Mathematikerin",
            "geburtstag": "1815-12-10",
            "alter": "36",
        }

        vcard = kontaktexport.kontakt_als_vcard(kontakt)

        self.assertIn("VERSION:3.0\r\n", vcard)
        self.assertIn("FN:Ada Lovelace\r\n", vcard)
        self.assertIn("TEL:+44 123\r\n", vcard)
        self.assertIn("EMAIL:ada@example.org\r\n", vcard)
        self.assertIn("ADR:;;;London;;;\r\n", vcard)
        self.assertIn("TITLE:Mathematikerin\r\n", vcard)
        self.assertIn("BDAY:1815-12-10\r\n", vcard)
        self.assertNotIn("ALTER", vcard)

    def test_kategorie_wird_exportiert(self):
        vcard = kontaktexport.kontakt_als_vcard({
            "name": "Testkontakt",
            "kategorie": "Familie",
        })

        self.assertIn("CATEGORIES:Familie\r\n", vcard)

    def test_leere_oder_unbekannte_kategorie_wird_ausgelassen(self):
        for kategorie in ("", "Sport"):
            with self.subTest(kategorie=kategorie):
                vcard = kontaktexport.kontakt_als_vcard({
                    "name": "Testkontakt",
                    "kategorie": kategorie,
                })
                self.assertNotIn("CATEGORIES:", vcard)

    def test_mehrere_kontakte_werden_exportiert(self):
        kontakte = [
            {"name": "Erster"},
            {"name": "Zweiter"},
        ]

        vcard = kontaktexport.kontakte_als_vcard(kontakte)

        self.assertEqual(vcard.count("BEGIN:VCARD"), 2)
        self.assertLess(vcard.index("FN:Erster"), vcard.index("FN:Zweiter"))

    def test_leere_optionale_felder_werden_ausgelassen(self):
        kontakt = {
            "name": "Testkontakt",
            "telefon": " ",
            "email": "",
            "wohnort": "",
            "beruf": "",
            "geburtstag": "",
        }

        vcard = kontaktexport.kontakt_als_vcard(kontakt)

        for eigenschaft in ("TEL:", "EMAIL:", "ADR:", "TITLE:", "BDAY:"):
            self.assertNotIn(eigenschaft, vcard)

    def test_sonderzeichen_und_zeilenumbrueche_werden_escaped(self):
        wert = "A\\B,C;D\r\nE\nF\rG"

        ergebnis = kontaktexport.vcard_wert_escapen(wert)

        self.assertEqual(ergebnis, r"A\\B\,C\;D\nE\nF\nG")

    def test_fehlende_felder_verursachen_keinen_fehler(self):
        vcard = kontaktexport.kontakt_als_vcard({"name": "Nur Name"})

        self.assertIn("FN:Nur Name", vcard)
        self.assertTrue(vcard.endswith("END:VCARD\r\n"))

    def test_quelldaten_werden_nicht_veraendert(self):
        kontakt = {"name": "A, B", "wohnort": "Ort;Teil"}
        kontakte = [kontakt]
        erwartet = kontakt.copy()

        kontaktexport.kontakte_als_vcard(kontakte)

        self.assertEqual(kontakt, erwartet)
        self.assertEqual(kontakte, [erwartet])

    def test_datei_wird_utf8_mit_crlf_geschrieben(self):
        with tempfile.TemporaryDirectory() as verzeichnis:
            dateipfad = Path(verzeichnis) / "kontakte.vcf"

            erfolgreich, fehlermeldung = (
                kontaktexport.kontakte_als_vcard_exportieren(
                    [{"name": "Jörg Weiß"}],
                    dateipfad,
                )
            )

            self.assertTrue(erfolgreich, fehlermeldung)
            daten = dateipfad.read_bytes()
            self.assertIn("Jörg Weiß".encode("utf-8"), daten)
            self.assertIn(b"VERSION:3.0\r\n", daten)
            self.assertNotIn(b"\r\r\n", daten)
            assert b"\n" not in daten.replace(b"\r\n", b"")

    def test_schreibfehler_wird_zurueckgegeben(self):
        with tempfile.TemporaryDirectory() as verzeichnis:
            erfolgreich, fehlermeldung = (
                kontaktexport.kontakte_als_vcard_exportieren(
                    [{"name": "Test"}],
                    Path(verzeichnis),
                )
            )

            self.assertFalse(erfolgreich)
            self.assertTrue(fehlermeldung)

    def test_exportierte_vcard_kann_importiert_werden(self):
        kontakt = {
            "name": "Jörg Weiß",
            "telefon": "+49 123",
            "email": "joerg@example.org",
            "wohnort": "Köln",
            "beruf": "Entwickler",
            "geburtstag": "1990-01-02",
            "kategorie": "Arbeit",
        }

        with tempfile.TemporaryDirectory() as verzeichnis:
            dateipfad = Path(verzeichnis) / "kontakt.vcf"
            erfolgreich, fehlermeldung = (
                kontaktexport.kontakte_als_vcard_exportieren(
                    [kontakt],
                    dateipfad,
                )
            )
            importierte_kontakte, fehlerliste = (
                kontaktimport.kontakte_importieren(dateipfad)
            )

        self.assertTrue(erfolgreich, fehlermeldung)
        self.assertEqual(fehlerliste, [])
        self.assertEqual(len(importierte_kontakte), 1)
        for feldname, wert in kontakt.items():
            self.assertEqual(importierte_kontakte[0][feldname], wert)

    def test_fehlender_name_schluessel_verhindert_export(self):
        with tempfile.TemporaryDirectory() as verzeichnis:
            dateipfad = Path(verzeichnis) / "kontakte.vcf"

            erfolgreich, fehlermeldung = (
                kontaktexport.kontakte_als_vcard_exportieren(
                    [{}],
                    dateipfad,
                )
            )

            self.assertFalse(erfolgreich)
            self.assertEqual(
                fehlermeldung,
                "Kontakt 1 kann nicht exportiert werden, "
                "weil der Name fehlt.",
            )
            self.assertFalse(dateipfad.exists())

    def test_leerer_name_verhindert_export(self):
        with tempfile.TemporaryDirectory() as verzeichnis:
            dateipfad = Path(verzeichnis) / "kontakte.vcf"

            erfolgreich, fehlermeldung = (
                kontaktexport.kontakte_als_vcard_exportieren(
                    [{"name": ""}],
                    dateipfad,
                )
            )

            self.assertFalse(erfolgreich)
            self.assertIn("Kontakt 1", fehlermeldung)
            self.assertFalse(dateipfad.exists())

    def test_name_aus_leerzeichen_verhindert_export(self):
        with tempfile.TemporaryDirectory() as verzeichnis:
            dateipfad = Path(verzeichnis) / "kontakte.vcf"

            erfolgreich, fehlermeldung = (
                kontaktexport.kontakte_als_vcard_exportieren(
                    [{"name": "   "}],
                    dateipfad,
                )
            )

            self.assertFalse(erfolgreich)
            self.assertIn("Kontakt 1", fehlermeldung)
            self.assertFalse(dateipfad.exists())

    def test_spaeterer_ungueltiger_kontakt_bricht_export_ab(self):
        kontakte = [
            {"name": "Erster Kontakt"},
            {"name": "Zweiter Kontakt"},
            {"name": "   "},
        ]

        with tempfile.TemporaryDirectory() as verzeichnis:
            dateipfad = Path(verzeichnis) / "kontakte.vcf"

            erfolgreich, fehlermeldung = (
                kontaktexport.kontakte_als_vcard_exportieren(
                    kontakte,
                    dateipfad,
                )
            )

            self.assertFalse(erfolgreich)
            self.assertEqual(
                fehlermeldung,
                "Kontakt 3 kann nicht exportiert werden, "
                "weil der Name fehlt.",
            )
            self.assertFalse(dateipfad.exists())

    def test_fehlgeschlagener_export_ueberschreibt_keine_datei(self):
        vorhandener_inhalt = b"bestehender Inhalt"

        with tempfile.TemporaryDirectory() as verzeichnis:
            dateipfad = Path(verzeichnis) / "kontakte.vcf"
            dateipfad.write_bytes(vorhandener_inhalt)

            erfolgreich, _ = (
                kontaktexport.kontakte_als_vcard_exportieren(
                    [
                        {"name": "Gueltiger Kontakt"},
                        {"name": ""},
                    ],
                    dateipfad,
                )
            )

            self.assertFalse(erfolgreich)
            self.assertEqual(
                dateipfad.read_bytes(),
                vorhandener_inhalt,
            )

    def test_foto_wird_nicht_exportiert_und_kategorie_bleibt(self):
        kontakt = {
            "name": "Testkontakt",
            "kategorie": "Familie",
            "foto": "bilder/vertraulich.png",
        }
        erwartet = kontakt.copy()

        vcard = kontaktexport.kontakt_als_vcard(kontakt)

        self.assertIn("CATEGORIES:Familie\r\n", vcard)
        self.assertNotIn("PHOTO", vcard)
        self.assertNotIn("vertraulich", vcard)
        self.assertEqual(kontakt, erwartet)


if __name__ == "__main__":
    unittest.main()
