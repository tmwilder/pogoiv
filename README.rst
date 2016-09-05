pogoiv: Calculate possible IVs for your Pokemon
===============================================

In the augmented reality mobile game, Pokemon Go, you adventure around the physical world capturing Pokemon and
exploring new places.

When a Pokemon is caught, it has a number of hidden statistics that the more hardcore players of the game are interested
in uncovering.

This project implements a simple, reusable library that supports enumerating possible combinations of these hidden stats
for a given Pokemon's public information.

It is intended for use in other applications and includes a reference CLI that leverages the package's functionality.

We take a brute force approach to the problem in the main entry point module: pogoiv.iv_calculator

Features
--------

- Calculate possible IVs and levels for a Pokemon given the appropriate public stats.
- Calculate the above for multiple point in time snapshots of that Pokemon to narrow down possibilities.

Installation
------------

.. code-block:: bash

    $ pip install pogoiv

Example Usage
-------------
Library:

.. code-block:: python

    >>> from pogoiv.iv_calculator import IvCalculator
    >>> calculator = IvCalculator()
    >>> calculator.get_ivs_across_powerups(pokemon_name='Slowbro', powerup_stats=[(1528, 125, 3000, True), (1564, 126, 3000, True)])
    [{'level': 21.5, 'atk_iv': 13, 'def_iv': 11, 'stam_iv': 15, 'perfection': 86.7}, {'level': 21.5, 'atk_iv': 14, 'def_iv': 9, 'stam_iv': 15, 'perfection': 84.4}, {'level': 22.0, 'atk_iv': 9, 'def_iv': 13, 'stam_iv': 12, 'perfection': 75.6}]

CLI:

.. code-block:: bash

    $ pogoiv --dust-cost 3000 3000 --combat-power 1528 1564 --hp 125 126 --powered True True --pokemon Slowbro
    +-------+--------+--------+---------+--------------+
    | Level | Atk IV | Def IV | Stam IV | Perfection % |
    +-------+--------+--------+---------+--------------+
    |  22.0 |   9    |   13   |    12   |     75.6     |
    |  21.5 |   14   |   9    |    15   |     84.4     |
    |  21.5 |   13   |   11   |    15   |     86.7     |
    +-------+--------+--------+---------+--------------+

Library with appraisal feature:

.. code-block:: python

    >>> from pogoiv.iv_calculator import IvCalculator
    >>> calculator = IvCalculator()
    >>> calculator.get_ivs_across_powerups(pokemon_name='Horsea', powerup_stats=[(10, 10, 200, False), (20, 10, 200, True), (30, 10, 200, True)], appraisal = (1, 3, True, False, False))
    [{'atk_iv': 9, 'def_iv': 13, 'stam_iv': 12, 'perfection': 75.6, 'level': 22.0}]

Appraisal values:

Mystic first value
0. Overall, your Pokemon is not likely to make much headway in battle.
1. Overall, your Pokemon is above average.
2. Overall, your Pokemon has certainly caught my attention.
3. Overall, your Pokemon is a wonder! What a breathtaking Pokemon!

Mystic second value
0. Its stats are not out of the norm, in my opinion.
1. Its stats are noticeably trending to the positive.
2. I am certainly impressed by its stats, I must say.
3. Its stats exceed my calculations. It's incredible!

Valor first value
0. Overall, your Pokemon may not be great in battle, but I still like it!
1. Overall, your Pokemon is a decent Pokemon.
2. Overall, your Pokemon is a strong Pokemon. You should be proud!
3. Overall, your Pokemon simply amazes me. It can accomplish anything!

Valor second value
0. Its stats don't point to greatness in battle.
1. Its stats indicate that in battle, it'll get the job done.
2. It's got excellent stats! How exciting!
3. I'm blown away by its stats. WOW!

Instinct first value
0. Overall, your Pokemon has room for improvement as far as battling goes.
1. Overall, your Pokemon is pretty decent!
2. Overall, your Pokemon is really strong!
3. Overall, your Pokemon looks like it can really battle with the best of them!

Instinct second value
0. Its stats are all right, but kinda basic, as far as I can see.
1. It's definitely got some good stats. Definitely!
2. Its stats are really strong! Impressive.
3. Its stats are the best I've ever seen! No doubt about it!

Third, Fourth and Fifth boolean values indicate whether or not the stat (Attack, Defense or Stamina respectively) are the highest of the three. (Several True values mean that several stats have the same highest values).


How To Contribute
-----------------
Check out, make changes, install, ensure tests are passing, open pr.

To run tests:

.. code-block:: bash

    nosetests -s
