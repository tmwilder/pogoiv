import unittest

from pogoiv.iv_calculator import IvCalculator


class TestIv(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.slowbro_data_t1 = [
            {'level': 21.0, 'atk_iv': 13, 'def_iv': 11, 'stam_iv': 15, 'perfection': 86.7},
            {'level': 21.0, 'atk_iv': 14, 'def_iv': 9, 'stam_iv': 15, 'perfection': 84.4},
            {'level': 21.0, 'atk_iv': 15, 'def_iv': 7, 'stam_iv': 15, 'perfection': 82.2},
            {'level': 21.5, 'atk_iv': 9, 'def_iv': 13, 'stam_iv': 12, 'perfection': 75.6},
            {'level': 21.5, 'atk_iv': 8, 'def_iv': 14, 'stam_iv': 13, 'perfection': 77.8},
            {'level': 21.5, 'atk_iv': 9, 'def_iv': 12, 'stam_iv': 13, 'perfection': 75.6},
            {'level': 22.0, 'atk_iv': 6, 'def_iv': 12, 'stam_iv': 10, 'perfection': 62.2},
            {'level': 22.0, 'atk_iv': 5, 'def_iv': 13, 'stam_iv': 11, 'perfection': 64.4},
            {'level': 22.0, 'atk_iv': 6, 'def_iv': 11, 'stam_iv': 11, 'perfection': 62.2},
            {'level': 22.5, 'atk_iv': 4, 'def_iv': 9, 'stam_iv': 8, 'perfection': 46.7},
            {'level': 22.5, 'atk_iv': 5, 'def_iv': 7, 'stam_iv': 8, 'perfection': 44.4}
        ]

        cls.slowbro_data_t2 = [
            {'level': 21.5, 'atk_iv': 13, 'def_iv': 11, 'stam_iv': 15, 'perfection': 86.7},
            {'level': 21.5, 'atk_iv': 14, 'def_iv': 9, 'stam_iv': 15, 'perfection': 84.4},
            {'level': 22.0, 'atk_iv': 9, 'def_iv': 13, 'stam_iv': 12, 'perfection': 75.6}
        ]

        cls.bulba_data_t1 = [{'atk_iv': 15, 'def_iv': 15, 'stam_iv': 15, 'perfection': 100.0, 'level': 10.5}]

    def test_calculate_iv_eevee(self):
        calculator = IvCalculator()
        result = calculator.get_ivs(
            pokemon_name='Eevee',
            current_cp=320,
            current_health=49,
            dust_to_upgrade=1300,
            powered=False
        )
        self.assertEquals([{'atk_iv': 15, 'def_iv': 15, 'stam_iv': 2, 'level': 11.0, 'perfection': 71.1}], result)

    def test_get_ivs_slowbro(self):
        calculator = IvCalculator()
        actual = calculator.get_ivs(
            pokemon_name='Slowbro',
            current_cp=1528,
            current_health=125,
            dust_to_upgrade=3000,
            powered=True
        )
        self._compare_result_lists(self.slowbro_data_t1, actual)

    def test_get_ivs_bulbasaur_edge_case(self):
        calculator = IvCalculator()
        actual = calculator.get_ivs(
            pokemon_name='Bulbasaur',
            current_cp=321,
            current_health=45,
            dust_to_upgrade=1000,
            powered=True
        )
        self._compare_result_lists(self.bulba_data_t1, actual)

    def test_get_ivs_slowbro_across_powerups(self):
        calculator = IvCalculator()
        actual = calculator.get_ivs_across_powerups(
            pokemon_name='Slowbro',
            powerup_stats=[(1528, 125, 3000, True), (1564, 126, 3000, True)]
        )
        self._compare_result_lists(self.slowbro_data_t2, actual)

    def _compare_result_lists(self, expected, actual):
        self.assertEquals(self._tupleify(expected), self._tupleify(actual))

    def _tupleify(self, result_list):
        return sorted([tuple(sorted(poke_dict.items())) for poke_dict in result_list])
