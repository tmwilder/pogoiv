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


How To Contribute
-----------------
Check out, make changes, install, ensure tests are passing, open pr.

To run tests:

.. code-block:: bash

    nosetests -s
