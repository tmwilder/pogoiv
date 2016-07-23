import unittest
from pogoiv.level_dust_costs import LevelDustCosts


class TestLevelDustCosts(unittest.TestCase):
    def tests_get_low_range(self):
        level_dust_costs = LevelDustCosts()
        level_range = level_dust_costs.get_level_range(200)
        self.assertEquals((1, 2.5), level_range)

    def tests_get_average_range(self):
        level_dust_costs = LevelDustCosts()
        level_range = level_dust_costs.get_level_range(3000)
        self.assertEquals((21, 22.5), level_range)

