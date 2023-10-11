import json

import serebii_reader

DEFAULT_DATA_PATH = 'data_moves.json'

class ManageMoves(object):
    def __init__(self):
        self._default_path = DEFAULT_DATA_PATH
        self._data = []

        self.loadData()

    def analyzeMoveset(self, pokemon, gen, alt=''):
        moveset = []

        sr = serebii_reader.SerebiiReader()
        all_moves = sr.getMoveset(pokemon, gen, alt)

        for move in all_moves:
            moveset.append((move, self._data[move]['main count']))

        moveset = sorted(moveset, key=lambda t: t[1])

        return moveset

    def depositPokemon(self, moveset, is_main=True):
        for move in moveset:
            self._data[move]['full count'] += 1

            if is_main:
                self._data[move]['main count'] += 1

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
            self._data[move]['full count'] -= 1

            if is_main:
                self._data[move]['main count'] -= 1

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
