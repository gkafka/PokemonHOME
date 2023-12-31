import json

import serebii_reader

DEFAULT_DATA_PATH = 'data_moves.json'
FULL_COUNT = 'full count'
MAIN_COUNT = 'main count'


class ManageMoves(object):
    def __init__(self):
        self._default_path = DEFAULT_DATA_PATH
        self._data = []

        self.loadData()

    def analyzeMoveset(self, pokemon, gen, alt='', tm=False, egg=False, tutor=False):
        moveset = []

        sr = serebii_reader.SerebiiReader()
        moves = sr.getMoveset(pokemon, gen, alt)

        for move, level in moves.items():
            moveset.append(
                (
                    self._data[move][MAIN_COUNT],
                    self._data[move][FULL_COUNT],
                    move,
                    'Level {0}'.format(level),
                )
            )

        extras = {}
        if any([tm, egg, tutor]):
            extras = sr.getMovesetExtras(pokemon, gen, alt, tm, egg, tutor)

        for move, label in extras.items():
            moveset.append(
                (
                    self._data[move][MAIN_COUNT],
                    self._data[move][FULL_COUNT],
                    move,
                    label,
                )
            )

        moveset = sorted(moveset, key=lambda t: (t[0], t[1]))

        return moveset

    def depositPokemon(self, moveset, is_main=True):
        for move in moveset:
            self._data[move][FULL_COUNT] += 1

            if is_main:
                self._data[move][MAIN_COUNT] += 1

        return

    def depositPokemonList(self, movesets, is_mains=None):
        mains = is_mains if isinstance(is_mains, list) else [True] * len(movesets)

        if is_mains is False:
            mains = [False] * len(movesets)

        for moveset, is_main in zip(movesets, mains):
            self.depositPokemon(moveset, is_main)               

        return

    def loadData(self, data_path=None):
        path = self._default_path if data_path is None else data_path

        with open(path) as f:
            self._data = json.load(f)

    def withdrawPokemon(self, moveset, is_main):
        for move in moveset:
            self._data[move][FULL_COUNT] -= 1

            if is_main:
                self._data[move][MAIN_COUNT] -= 1

        return

    def withdrawPokemonList(self, movesets, is_mains=None):
        mains = is_mains if isinstance(is_mains, list) else [True] * len(movesets)

        if is_mains is False:
            mains = [False] * len(movesets)

        for moveset, is_main in zip(movesets, mains):
            self.withdrawPokemon(moveset, is_main)               

        return

    def writeData(self, data_path=None):
        path = self._default_path if data_path is None else data_path

        with open(path, 'w+') as f:
            json.dump(self._data, f, indent=4)
