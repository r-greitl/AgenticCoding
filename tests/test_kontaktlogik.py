"""Tests fuer die Kontaktsuche nach Kategorien."""

import unittest

import kontaktlogik


class KontaktlogikTests(unittest.TestCase):
    def setUp(self):
        self.kontakte = [
            {"name": "Zora", "kategorie": "Familie"},
            {"name": "Anna", "kategorie": "Arbeit"},
            {"name": "Berta", "kategorie": "Familie"},
            {"name": "Clara", "kategorie": ""},
        ]

    def test_suche_findet_kontakte_ueber_kategorie(self):
        ergebnis = kontaktlogik.kontakte_suchen(
            self.kontakte,
            "Familie",
        )

        self.assertEqual(
            [kontakt["name"] for kontakt in ergebnis],
            ["Berta", "Zora"],
        )

    def test_kategoriesuche_ignoriert_grossschreibung(self):
        ergebnis = kontaktlogik.kontakte_suchen(
            self.kontakte,
            "arbeit",
        )

        self.assertEqual([kontakt["name"] for kontakt in ergebnis], ["Anna"])

    def test_kategoriesuche_veraendert_quelldaten_nicht(self):
        erwartet = [kontakt.copy() for kontakt in self.kontakte]

        kontaktlogik.kontakte_suchen(self.kontakte, "Familie")

        self.assertEqual(self.kontakte, erwartet)


if __name__ == "__main__":
    unittest.main()
