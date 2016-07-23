import unittest
from pogoiv.level_dust_costs import LevelDustCosts


class TestLevelDustCosts(unittest.TestCase):
    def tests_get_level_range(self):
        base_stats = LevelDustCosts()
        min_level, max_level = base_stats.get_level_range(3000)
        self.assertEquals((19, 21), (min_level, max_level))
