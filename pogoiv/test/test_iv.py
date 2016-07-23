import unittest

from pogoiv.iv import IvCalculator

class TestIv(unittest.TestCase):
    def test_hp_checks_out(self):
        pass

    def test_cp_checks_out(self):
        pass

    def test_calculate_iv(self):
        calculator = IvCalculator()
        result = calculator.calculate_iv(
            pokemon_name='Eevee',
            current_cp=320,
            current_health=49,
            dust_to_upgrade=1300,
            powered=True
        )
        self.assertEquals([{'atk_iv': 15, 'def_iv': 15, 'stam_iv': 2, 'level': 11.0}], result)