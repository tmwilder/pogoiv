import json


class IvCalculator():
    def __init__(self):
        # TODO, add path to poke tsv resource
        self.poke_data = json.loads('')

    def calculate_iv(self, pokemon_name, current_cp, current_health, dust_to_upgrade, powered=False):
        self._validate_inputs(pokemon_name, current_cp, current_health, dust_to_upgrade, powered)
        base_atk, base_def, base_stam = self.get_base_stats(pokemon_name)


    def get_base_stats(self, pokemon_name):
        # TODO, return self.poke_data.get(pokemon_name)
        return (10, 10, 10)

    def _validate_inputs(self, pokemon_name, current_cp, current_health, dust_to_upgrade, powered):
        # TODO, add validations such as ensuring name in self.poke_data
        pass

    # HP = (Base Stam + Stam IV) *Lvl(CPScalar)
    # CP = (Base Atk + Atk IV) *(Base Def + Def IV) ^ 0.5 * (Base Stam + Stam IV) ^ 0.5 * Lvl(CPScalar) ^ 2 / 10

    # Free variables, batk, bdef, bstam, level