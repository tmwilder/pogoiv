# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import unittest
from pogoiv.base_stats import BaseStats


class TestBaseStates(unittest.TestCase):
    def test_base_stats(self):
        base_stats = BaseStats()
        values = base_stats.get_base_stats('Charmander')
        self.assertEquals(values[BaseStats.BASE_ATTACK], 116)
        self.assertEquals(values[BaseStats.BASE_STAMINA], 78)
        self.assertEquals(values[BaseStats.BASE_DEFENSE], 96)

    def test_base_stats_nidorans(self):
        base_stats = BaseStats()
        female_values = base_stats.get_base_stats('Nidoran♀')
        male_values = base_stats.get_base_stats('Nidoran♂')

        self.assertEquals(female_values[BaseStats.BASE_ATTACK], 86)
        self.assertEquals(female_values[BaseStats.BASE_STAMINA], 110)
        self.assertEquals(female_values[BaseStats.BASE_DEFENSE], 94)

        self.assertEquals(male_values[BaseStats.BASE_ATTACK], 105)
        self.assertEquals(male_values[BaseStats.BASE_STAMINA], 92)
        self.assertEquals(male_values[BaseStats.BASE_DEFENSE], 76)
