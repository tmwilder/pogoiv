from pogoiv.data import get_csv

from pogoiv.poke_data_error import PokeDataError


class LevelDustCosts:
    def __init__(self):
        self._stats = self._load_stats()

    def _load_stats(self):
        reader = get_csv('level_dust_costs.tsv')

        stats = {}
        for index, row in enumerate(reader):
            if index == 0:
                continue
            dust_cost, level = row
            stats[int(dust_cost)] = int(level)
        return stats

    def get_level_range(self, dust_cost):
        """
        :param dust_cost: Integer representing the upgrade cost in dust for the pokemon.
        :return: (integer, integer) representing the lowest and high possible levels for the pokemon.
        """
        self.validate_dust_cost(dust_cost)
        min_level = self._stats[dust_cost]
        return (float(min_level), min_level + 1.5)

    def validate_dust_cost(self, dust_cost):
        if dust_cost not in self._stats:
            raise PokeDataError("Could not find dust cost matching: {}".format(dust_cost))
