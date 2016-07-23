import unittest

from pogoiv.iv import IvCalculator

class TestIv(unittest.TestCase):
    def test_hp_checks_out(self):
        pass

    def test_cp_checks_out(self):
        pass

    def test_calculate_iv_eevee(self):
        calculator = IvCalculator()
        result = calculator.calculate_iv(
            pokemon_name='Eevee',
            current_cp=320,
            current_health=49,
            dust_to_upgrade=1300,
            powered=False
        )
        self.assertEquals([{'atk_iv': 15, 'def_iv': 15, 'stam_iv': 2, 'level': 11.0, 'perfection': '71.1'}], result)

    def test_calculate_iv_slowbro(self):
        calculator = IvCalculator()
        actual = calculator.calculate_iv(
            pokemon_name='Slowbro',
            current_cp=1528,
            current_health=125,
            dust_to_upgrade=3000,
            powered=True
        )

        expected = [
            {'level': 21.0, 'atk_iv': 13, 'def_iv': 11, 'stam_iv': 15, 'perfection': '86.7'},
            {'level': 21.0, 'atk_iv': 14, 'def_iv': 9, 'stam_iv': 15, 'perfection': '84.4'},
            {'level': 21.0, 'atk_iv': 15, 'def_iv': 7, 'stam_iv': 15, 'perfection': '82.2'},
            {'level': 21.5, 'atk_iv': 9, 'def_iv': 13, 'stam_iv': 12, 'perfection': '75.6'},
            {'level': 21.5, 'atk_iv': 8, 'def_iv': 14, 'stam_iv': 13, 'perfection': '77.8'},
            {'level': 21.5, 'atk_iv': 9, 'def_iv': 12, 'stam_iv': 13, 'perfection': '75.6'},
            {'level': 22.0, 'atk_iv': 6, 'def_iv': 12, 'stam_iv': 10, 'perfection': '62.2'},
            {'level': 22.0, 'atk_iv': 5, 'def_iv': 13, 'stam_iv': 11, 'perfection': '64.4'},
            {'level': 22.0, 'atk_iv': 6, 'def_iv': 11, 'stam_iv': 11, 'perfection': '62.2'},
            {'level': 22.5, 'atk_iv': 4, 'def_iv': 9, 'stam_iv': 8, 'perfection': '46.7'},
            {'level': 22.5, 'atk_iv': 5, 'def_iv': 7, 'stam_iv': 8, 'perfection': '44.4'}
        ]
        self._compare_result_lists(expected, actual)

    def _compare_result_lists(self, expected, actual):
        self.assertEquals(self._tupleify(expected), self._tupleify(actual))

    def _tupleify(self, result_list):
        return sorted([sorted(poke_dict.items()) for poke_dict in result_list])
