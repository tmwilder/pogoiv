from math import floor

from pogoiv import cp_multipliers, base_stats, level_dust_costs, poke_data_error
from pogoiv.iv_stats import IvStats


class IvCalculator:
    def __init__(self):
        self.cp_multipliers = cp_multipliers.CpMultipliers()
        self.base_stats = base_stats.BaseStats()
        self.level_dust_costs = level_dust_costs.LevelDustCosts()

    def get_ivs(self, pokemon_name, current_cp, current_health, dust_to_upgrade, powered=False):
        """
        :param string pokemon_name: name of a Pokemon.
        :param integer current_cp: CP of Pokemon visible in game client.
        :param integer current_health: Health of Pokemon visible in game client.
        :param integer dust_to_upgrade: Amount of dust to buy the next powerup to the Pokemon visible in the game client.
        :param boolean powered: Whether or not the Pokemon has ever been powered up.
        :return: dict of the form:
                {
                    'atk_iv': integer - 0-15,
                    'def_iv': integer - 0-15,
                    'stam_iv': integer - 0-15,
                    'level': float - 1.0-40.5,
                    'perfection': float - 0.0 - 100.0
                }
        """
        self._validate_inputs(pokemon_name, current_cp, current_health, dust_to_upgrade, powered)
        base_stats = self.base_stats.get_base_stats(pokemon_name)
        base_atk = base_stats[self.base_stats.BASE_ATTACK]
        base_def = base_stats[self.base_stats.BASE_DEFENSE]
        base_stam = base_stats[self.base_stats.BASE_STAMINA]

        min_level, max_level = self.level_dust_costs.get_level_range(dust_to_upgrade)

        possible_stats = []

        # 16^3 * 80 = 327680 = fast enough for a single modern core, embrace the brute.
        for atk_iv in range(0, 16):
            for def_iv in range(0, 16):
                for stam_iv in range(0, 16):
                    for level_double in range(int(min_level*2), int(max_level*2 + 1)):
                        if powered is False and not self._legal_unpowered_level(level_double/2.0):
                            # Unpowered pokemon can only be odd leveled, skip.
                            continue

                        cp_multiplier = self.cp_multipliers.get_cp_multiplier(level_double/2.0)

                        hp_ok = self._hp_checks_out(
                            hp=current_health,
                            base_stam=base_stam,
                            stam_iv=stam_iv,
                            cp_multiplier=cp_multiplier
                        )

                        cp_ok = self._cp_checks_out(
                            cp=current_cp,
                            base_atk=base_atk,
                            atk_iv=atk_iv,
                            base_def=base_def,
                            def_iv=def_iv,
                            base_stam=base_stam,
                            stam_iv=stam_iv,
                            cp_multiplier=cp_multiplier
                        )

                        if hp_ok and cp_ok:
                            possible_stats.append({
                                IvStats.STAT_ATK_IV: atk_iv,
                                IvStats.STAT_STAM_IV: stam_iv,
                                IvStats.STAT_DEF_IV: def_iv,
                                IvStats.STAT_LEVEL: level_double/2.0,
                                IvStats.PERFECTION_PERCENTAGE:
                                    self._calculate_perfection_percentage(atk_iv=atk_iv, def_iv=def_iv, stam_iv=stam_iv)
                            })

        return possible_stats

    def get_ivs_across_powerups(self, pokemon_name, powerup_stats):
        """
        Returns all possible ivs for the given Pokemon and series of client facing stats for that Pokemon.
        :param string pokemon_name: name of a Pokemon.
        :param list<tuple> powerup_stats: List of tuples of the form:
                (integer current_cp, integer current_health, integer dust_to_upgrade, boolean powered)
                each representing the input stats for a pokemon at a given level.
        :return: list<dict> whose members are of the form:
                {
                    'atk_iv': integer - 0-15,
                    'def_iv': integer - 0-15,
                    'stam_iv': integer - 0-15,
                    'level': float - 1.0-40.5,
                    'perfection': float - 0.0 - 100.0
                }
        """
        answer_sets = []
        for stats in powerup_stats:
            current_cp, current_health, dust_to_upgrade, powered = stats
            ivs = self.get_ivs(
                pokemon_name=pokemon_name,
                current_cp=current_cp,
                current_health=current_health,
                dust_to_upgrade=dust_to_upgrade,
                powered=powered
            )
            answer_sets.append(ivs)

        if not answer_sets or not answer_sets[0]:
            return []
        else:
            setted_answer_sets = [set(self._make_hashable(answer_set)) for answer_set in answer_sets]
            remaining_options = setted_answer_sets[0]
            for possible_ivs in setted_answer_sets[1:]:
                remaining_options = remaining_options.intersection(possible_ivs)

            response = []
            for iv_stat_instance in remaining_options:
                response.append(iv_stat_instance.as_dict())
            return response

    def _legal_unpowered_level(self, level):
        """ Only whole number levels are legal for unpowered pokemon."""
        return level % 1 == 0

    def _hp_checks_out(self, hp, base_stam, stam_iv, cp_multiplier):
        derived_hp = floor((base_stam + stam_iv) * cp_multiplier)
        return max(10, derived_hp) == hp

    def _cp_checks_out(self, cp, base_atk, atk_iv, base_def, def_iv, base_stam, stam_iv, cp_multiplier):
        derived_cp = floor((
             (base_atk + atk_iv) *
             (base_def + def_iv) ** .5 *
             (base_stam + stam_iv) ** .5 *
             cp_multiplier ** 2
        )/ 10.0)
        return max(10, derived_cp) == cp

    def _calculate_perfection_percentage(self, atk_iv, def_iv, stam_iv):
        return float('%.1f' % ((atk_iv + def_iv + stam_iv) / 45.0 * 100))

    @classmethod
    def _make_hashable(cls, result_list):
        return [IvStats(
            level=poke_dict[IvStats.STAT_LEVEL],
            atk_iv=poke_dict[IvStats.STAT_ATK_IV],
            def_iv=poke_dict[IvStats.STAT_DEF_IV],
            stam_iv=poke_dict[IvStats.STAT_STAM_IV],
            perfection=poke_dict[IvStats.PERFECTION_PERCENTAGE]
        ) for poke_dict in result_list]

    def _validate_inputs(self, pokemon_name, current_cp, current_health, dust_to_upgrade, powered):
        self.base_stats.validate_pokemon(pokemon_name)
        self.level_dust_costs.validate_dust_cost(dust_to_upgrade)
        if not isinstance(current_cp, int):
            raise poke_data_error.PokeDataError("Input CP was not an integer: {}".format(current_cp))
        if not isinstance(current_health, int):
            raise poke_data_error.PokeDataError("Input health was not an integer: {}".format(current_cp))
        if not isinstance(dust_to_upgrade, int):
            raise poke_data_error.PokeDataError("Input upgrade cost was not an integer: {}".format(current_cp))
        if not isinstance(powered, bool):
            raise poke_data_error.PokeDataError("Input powered status was not a bool: {}".format(current_cp))