"""Tests fuer zentrale Kontaktfelder und Kategorien."""

import unittest

from kontaktfelder import (
    KATEGORIEN,
    kategorie_normalisieren,
    kontakt_vervollstaendigen,
    leerer_kontakt,
)


class KontaktfelderTests(unittest.TestCase):
    def test_leerer_kontakt_enthaelt_leere_kategorie(self):
        self.assertEqual(leerer_kontakt()["kategorie"], "")

    def test_alter_kontakt_wird_um_leere_kategorie_ergaenzt(self):
        alter_kontakt = {"name": "Alter Kontakt"}

        vollstaendig = kontakt_vervollstaendigen(alter_kontakt)

        self.assertEqual(vollstaendig["kategorie"], "")
        self.assertNotIn("kategorie", alter_kontakt)

    def test_vorhandene_kategorie_bleibt_erhalten(self):
        kontakt = {
            "name": "Kontakt",
            "kategorie": "Familie",
        }

        vollstaendig = kontakt_vervollstaendigen(kontakt)

        self.assertEqual(vollstaendig["kategorie"], "Familie")

    def test_kategorien_sind_eindeutig(self):
        self.assertEqual(
            KATEGORIEN,
            (
                "Familie",
                "Freunde",
                "Arbeit",
                "Verein",
                "Sonstiges",
            ),
        )
        self.assertEqual(len(KATEGORIEN), len(set(KATEGORIEN)))

    def test_kategorie_wird_kanonisch_normalisiert(self):
        self.assertEqual(
            kategorie_normalisieren("  fReUnDe  "),
            "Freunde",
        )

    def test_unbekannte_kategorie_wird_leer_normalisiert(self):
        self.assertEqual(kategorie_normalisieren("Sport"), "")


if __name__ == "__main__":
    unittest.main()
