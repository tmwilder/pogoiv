import unittest
from pogoiv.base_stats import BaseStats


class TestBaseStates(unittest.TestCase):
    def test_base_stats(self):
        base_stats = BaseStats()
        values = base_stats.get_base_stats('Charmander')
        self.assertEquals(values[BaseStats.BASE_ATTACK], 128)
        self.assertEquals(values[BaseStats.BASE_STAMINA], 78)
        self.assertEquals(values[BaseStats.BASE_DEFENSE], 108)
