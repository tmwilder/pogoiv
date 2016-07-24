import csv
from StringIO import StringIO
from pkg_resources import resource_string

from pogoiv.poke_data_error import PokeDataError

class BaseStats:
    BASE_ATTACK = 'base_attack'
    BASE_DEFENSE = 'base_defense'
    BASE_STAMINA = 'base_stamina'

    def __init__(self):
        self._stats = self._load_stats()

    def _load_stats(self):
        contents = resource_string('pogoiv', 'data/base_stats.tsv')
        f = StringIO(contents)
        reader = csv.reader(f, delimiter='\t')

        stats = {}
        for index, row in enumerate(reader):
            if index == 0:
                continue
            name, attack, defense, stamina = row
            stats[name.lower()] = {
                self.BASE_ATTACK: int(attack),
                self.BASE_DEFENSE: int(defense),
                self.BASE_STAMINA: int(stamina)
            }
        return stats

    def get_base_stats(self, pokemon_name):
        self.validate_pokemon(pokemon_name)
        return self._stats[pokemon_name.lower()]

    def validate_pokemon(self, pokemon_name):
        if pokemon_name.lower() not in self._stats:
            raise PokeDataError("Could not find Pokemon matching: {}".format(pokemon_name))
