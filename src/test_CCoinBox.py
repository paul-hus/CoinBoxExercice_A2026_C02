import io
import unittest
from contextlib import redirect_stdout
from CCoinBox import CCoinBox

class Test_CCoinBox(unittest.TestCase):

    def capturer_sortie(self, fonction):
        sortie = io.StringIO()
        with redirect_stdout(sortie):
            fonction()
        return sortie.getvalue()

    def test_pass(self):
        pass

    def test_monnaie(self):
        coinBox = CCoinBox()
        coinBox.ajouter_25c()
        coinBox.ajouter_25c()
        self.assertEqual(coinBox.get_vente_permise(), True)

    def test_retourne_monnaie(self):
        coinBox = CCoinBox()
        coinBox.ajouter_25c()
        piece = coinBox.retourne_monnaie()
        self.assertEqual(coinBox.get_vente_permise(), False)
        self.assertEqual(piece, 1)

    def test_retourne_monnaie_vide_le_solde(self):
        coinBox = CCoinBox()
        coinBox.ajouter_25c()
        coinBox.ajouter_25c()
        piece = coinBox.retourne_monnaie()
        self.assertEqual(piece, 2)
        self.assertEqual(coinBox.get_monnaie_courante(), 0)
        self.assertEqual(coinBox.get_vente_permise(), False)

    def test_permet_une_double_vente(self):
        coinBox = CCoinBox()
        coinBox.ajouter_25c()
        coinBox.ajouter_25c()
        coinBox.ajouter_25c()
        coinBox.ajouter_25c()
        coinBox.vente()
        self.assertEqual(coinBox.get_vente_permise(), True)

    def test_une_piece_ne_permet_pas_la_vente(self):
        coinBox = CCoinBox()
        coinBox.ajouter_25c()
        self.assertEqual(coinBox.get_monnaie_courante(), 1)
        self.assertEqual(coinBox.get_vente_permise(), False)

    def test_vente_consomme_deux_pieces(self):
        coinBox = CCoinBox()
        coinBox.ajouter_25c()
        coinBox.ajouter_25c()
        coinBox.vente()
        self.assertEqual(coinBox.get_monnaie_courante(), 0)
        self.assertEqual(coinBox.get_monnaie_totale(), 2)
        self.assertEqual(coinBox.get_vente_permise(), False)

    def test_reset_remet_tout_a_zero(self):
        coinBox = CCoinBox()
        coinBox.ajouter_25c()
        coinBox.ajouter_25c()
        coinBox.vente()
        coinBox.ajouter_25c()
        coinBox.reset()
        self.assertEqual(coinBox.get_monnaie_totale(), 0)
        self.assertEqual(coinBox.get_monnaie_courante(), 0)
        self.assertEqual(coinBox.get_vente_permise(), False)

    def test_message_ajout_piece(self):
        coinBox = CCoinBox()
        sortie = self.capturer_sortie(coinBox.ajouter_25c)
        self.assertEqual(sortie, "Une pièce a été ajoutée\n")

    def test_message_vente(self):
        coinBox = CCoinBox()
        coinBox.ajouter_25c()
        coinBox.ajouter_25c()
        sortie = self.capturer_sortie(coinBox.vente)
        self.assertEqual(sortie, "Vente! Voici votre article ...\n")

    def test_message_pas_assez_de_monnaie(self):
        coinBox = CCoinBox()
        sortie = self.capturer_sortie(coinBox.vente)
        self.assertEqual(sortie, "Pas assez de monnaie\n")

    def test_message_reset(self):
        coinBox = CCoinBox()
        sortie = self.capturer_sortie(coinBox.reset)
        self.assertEqual(sortie, "Réinitialisation\n")

    def test_message_retourne_monnaie(self):
        coinBox = CCoinBox()
        sortie = self.capturer_sortie(coinBox.retourne_monnaie)
        self.assertEqual(sortie, "Voici votre monnaie\n")
