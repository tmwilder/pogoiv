from pogoiv.data import get_csv


class CpMultipliers:
    def __init__(self):
        self._stats = self._load_stats()

    def _load_stats(self):
        reader = get_csv('cp_multipliers.tsv')

        stats = {}
        for index, row in enumerate(reader):
            if index == 0:
                continue
            level, multiplier = row
            stats[float(level)] = float(multiplier)
        return stats

    def get_cp_multiplier(self, level):
        """
        :param level: Integer representing the level for which to get a pokemon's CP multipler.
        :return: float representing the coefficient for use in the CP equation appropriate to the pokemon's level.
        """
        return self._stats[level]
