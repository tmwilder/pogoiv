from pogoiv import cp_multipliers, base_stats, level_dust_costs


class IvCalculator:
    STAT_ATK_IV = 'atk_iv'
    STAT_DEF_IV = 'def_iv'
    STAT_STAM_IV = 'stam_iv'
    STAT_LEVEL = 'level'


    def __init__(self):
        self.cp_multipliers = cp_multipliers.CpMultipliers()
        self.base_stats = base_stats.BaseStats()
        self.level_dust_costs = level_dust_costs.LevelDustCosts()

    def calculate_iv(self, pokemon_name, current_cp, current_health, dust_to_upgrade, powered=False):
        self._validate_inputs(pokemon_name, current_cp, current_health, dust_to_upgrade, powered)
        base_atk, base_def, base_stam = self.base_stats.get_base_stats(pokemon_name)

        min_level, max_level = self.level_dust_costs.get_level_range(dust_to_upgrade)

        possible_stats = []

        # 16^3 * 80 = 327680 = fast enough for a single modern core, embrace the brute.
        for atk_iv in range(0, 16):
            for def_iv in range(0, 16):
                for stam_iv in range(0, 16):
                    for level in (min_level, max_level + .5, .5):
                        cp_multiplier = self.cp_multipliers.get_cp_multiplier(level)

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
                                self.STAT_ATK_IV: atk_iv,
                                self.STAT_STAM_IV: stam_iv,
                                self.STAT_DEF_IV: def_iv,
                                self.STAT_LEVEL: level
                            })

        return possible_stats

    def _hp_checks_out(self, hp, base_stam, stam_iv, cp_multiplier):
        return hp == ((base_stam + stam_iv) * cp_multiplier)

    def _cp_checks_out(self, cp, base_atk, atk_iv, base_def, def_iv, base_stam, stam_iv, cp_multiplier):
        return cp == ((
             (base_atk + atk_iv) *
             (base_def + def_iv) ** .5 *
             (base_stam + stam_iv) ** .5 *
             cp_multiplier ** 2
        )/ 10)



    def _validate_inputs(self, pokemon_name, current_cp, current_health, dust_to_upgrade, powered):
        # TODO, add validations such as ensuring name in self.poke_data
        pass