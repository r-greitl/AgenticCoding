"""Tests fuer die Validierung von Kategorien."""

import unittest

from kontaktfelder import KATEGORIEN
from validierung import kontakt_validieren


class KategorieValidierungTests(unittest.TestCase):
    def test_leere_kategorie_ist_gueltig(self):
        self.assertEqual(
            kontakt_validieren({"name": "Test", "kategorie": ""}),
            (True, ""),
        )

    def test_alle_definierten_kategorien_sind_gueltig(self):
        for kategorie in KATEGORIEN:
            with self.subTest(kategorie=kategorie):
                self.assertEqual(
                    kontakt_validieren({
                        "name": "Test",
                        "kategorie": kategorie,
                    }),
                    (True, ""),
                )

    def test_unbekannte_kategorie_ist_ungueltig(self):
        gueltig, fehlermeldung = kontakt_validieren({
            "name": "Test",
            "kategorie": "Sport",
        })

        self.assertFalse(gueltig)
        self.assertEqual(
            fehlermeldung,
            "Bitte wählen Sie eine gültige Kategorie aus.",
        )


if __name__ == "__main__":
    unittest.main()
