import unittest

from pogoiv.iv_calculator import IvCalculator


class TestAppraisal(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.slowbro_data_t1 = [
            {'atk_iv': 9, 'def_iv': 13, 'stam_iv': 12, 'perfection': 75.6, 'level': 22.0}
        ]

        cls.slowbro_data_t2 = [
            {'atk_iv': 14, 'def_iv': 9, 'stam_iv': 15, 'perfection': 84.4, 'level': 21.5},
            {'atk_iv': 13, 'def_iv': 11, 'stam_iv': 15, 'perfection': 86.7, 'level': 21.5},
        ]

        cls.vaporeon_data_t1 = [
            {'atk_iv': 15, 'def_iv': 15, 'stam_iv': 15, 'perfection': 100.0, 'level': 23.0}
        ]

        cls.vaporeon_data_t2 = [
            {'atk_iv': 13, 'def_iv': 14, 'stam_iv': 12, 'perfection': 86.7, 'level': 28.0}
        ]

    # def test_appraisal_filter_slowbro_low(self):
    #     calculator = IvCalculator()
    #     result = calculator.get_ivs_across_powerups(
    #         pokemon_name = 'Slowbro',
    #         powerup_stats = [(580, 75, 1000, False), (1564, 126, 3000, True)],
    #         appraisal = [2, 2, False, True, False]
    #     )
    #     self.assertEquals(self.slowbro_data_t1, result)

    # def test_appraisal_filter_slowbro_high(self):
    #     calculator = IvCalculator()
    #     result = calculator.get_ivs_across_powerups(
    #         pokemon_name = 'Slowbro',
    #         powerup_stats = [(1528, 125, 3000, True), (1564, 126, 3000, True)],
    #         appraisal = [3, 3, False, False, True]
    #     )
    #     self._compare_result_lists(self.slowbro_data_t2, result)

    def test_appraisal_filter_vaporeon_max(self):
        calculator = IvCalculator()
        result = calculator.get_ivs_across_powerups(
            pokemon_name = 'Vaporeon',
            powerup_stats = [(2074, 176, 3500, True)],
            appraisal = [3, 3, True, True, True]
        )
        self._compare_result_lists(self.vaporeon_data_t1, result)

    # def test_appraisal_filter_vaporeon_low(self):
    #     calculator = IvCalculator()
    #     result = calculator.get_ivs_across_powerups(
    #         pokemon_name = 'Vaporeon',
    #         powerup_stats = [(2212, 192, 4500, True)],
    #         appraisal = [3, 2, False, True, False]
    #     )
    #     self._compare_result_lists(self.vaporeon_data_t2, result)

    def test_appraisal_filter_vaporeon_none(self):
        calculator = IvCalculator()
        result = calculator.get_ivs_across_powerups(
            pokemon_name = 'Vaporeon',
            powerup_stats = [(2212, 192, 4500, True)],
            appraisal = [3, 3, False, True, False]
        )
        self._compare_result_lists([], result)


    def _compare_result_lists(self, expected, actual):
        self.assertEquals(self._tupleify(expected), self._tupleify(actual))

    def _tupleify(self, result_list):
        return sorted([tuple(sorted(poke_dict.items())) for poke_dict in result_list])
