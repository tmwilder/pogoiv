from argparse import ArgumentParser
from os import linesep

from prettytable import PrettyTable

from pogoiv.iv_calculator import IvCalculator, IvStats
from pogoiv.poke_data_error import PokeDataError


def collate_args(combat_powers, hitpoints, dust_costs, powered):
    if powered is None:
        powered = [True for True in len(dust_costs)]
    return zip(combat_powers, hitpoints, dust_costs, powered)


def str2bool(bool_str):
    return bool_str == "True"


def get_pretty_table(possible_ivs):
    t = PrettyTable(["Level", "Atk IV", "Def IV", "Stam IV", "Perfection %"])
    rows = []
    for possible_iv in possible_ivs:
        rows.append([
             possible_iv[IvStats.STAT_LEVEL],
             possible_iv[IvStats.STAT_ATK_IV],
             possible_iv[IvStats.STAT_DEF_IV],
             possible_iv[IvStats.STAT_STAM_IV],
             possible_iv[IvStats.PERFECTION_PERCENTAGE]
        ])
    # Sort by completion %.
    rows = sorted(rows, lambda x, y: 0 if x[4] == y[4] else (-1 if x[4] < y[4] else 1))

    for row in rows:
        t.add_row(row)
    return t


def main():
    parser = ArgumentParser(description='Calculate possible IVs for your Pokemon.{line}Example Usage:{line}\t{cmd}'.format(
        line=linesep,
        cmd="pogoiv --dust-cost 3000 3000 --combat-power 1528 1564 --hp 125 126 --powered True True --pokemon Slowbro"
    ))
    parser.add_argument(
        '--d', '--dust-cost',
        type=int,
        nargs='+',
        required=True,
        help='Space delimited list of dust cost integers with one entry for each data point from the Pokemon\'s history.'
    )
    parser.add_argument(
        '--cp', '--combat-power',
        type=int,
        nargs='+',
        required=True,
        help='Space delimited list of combat power integers with one entry for each data point from the Pokemon\'s history.'
    )
    parser.add_argument(
        '--hp', '--hitpoints',
        type=int,
        nargs='+',
        required=True,
        help='Space delimited list of hit point integers with one entry for each data point from the Pokemon\'s history.'
    )
    parser.add_argument('--powered', nargs="+", choices=["True", "False"], required=True, help='For this data point, has the Pokemon ever been powered?')
    parser.add_argument('-p', '--pokemon', required=True, help='Name of the Pokemon')

    args = parser.parse_args()

    calculator = IvCalculator()
    try:
        possible_ivs = calculator.get_ivs_across_powerups(
            args.pokemon,
            collate_args(args.cp, args.hp, args.d, [str2bool(bool_str) for bool_str in args.powered])
        )
        pretty_possible_ivs = get_pretty_table(possible_ivs)
        print pretty_possible_ivs
    except PokeDataError as pde:
        print pde
