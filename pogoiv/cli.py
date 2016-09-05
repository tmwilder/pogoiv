from argparse import ArgumentParser
from os import linesep

from prettytable import PrettyTable

from pogoiv.iv_calculator import IvCalculator, IvStats
from pogoiv.poke_data_error import PokeDataError


def collate_args(combat_powers, hitpoints, dust_costs, powered):
    if powered is None:
        powered = [True for _ in dust_costs]
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
    rows = sorted(rows, key=lambda x: x[4])

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

    parser.add_argument(
        '--a1', '--appraisal1',
        type=int,
        required=False,
        help='Integer from 0 to 3 indicating the global appraisal phrase. 0 the lowest, 3 the highest.'
    )
    parser.add_argument(
        '--a2', '--appraisal2',
        type=int,
        required=False,
        help='Integer from 0 to 3 indicating the best stat appraisal phrase. 0 the lowest, 3 the highest.'
    )
    parser.add_argument('--at', choices=["True", "False"], required=False, help='Is attack the best stat?')
    parser.add_argument('--de', choices=["True", "False"], required=False, help='Is defense the best stat?')
    parser.add_argument('--st', choices=["True", "False"], required=False, help='Is stamina the best stat?')

    args = parser.parse_args()

    appraisal = []
    if not (args.a1 == None or args.a2 == None or args.at == None or args.de == None or args.st == None):
        appraisal.append(args.a1)
        appraisal.append(args.a2)
        appraisal.append(str2bool(args.at))
        appraisal.append(str2bool(args.de))
        appraisal.append(str2bool(args.st))
    print appraisal

    calculator = IvCalculator()
    try:
        possible_ivs = calculator.get_ivs_across_powerups(
            args.pokemon,
            collate_args(args.cp, args.hp, args.d, [str2bool(bool_str) for bool_str in args.powered]),
            appraisal
        )
        pretty_possible_ivs = get_pretty_table(possible_ivs)
        print(pretty_possible_ivs)
    except PokeDataError as pde:
        print(pde)
