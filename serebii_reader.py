from bs4 import BeautifulSoup
import requests

SUFFIX = 'suffix'
TAG = 'tag'

URL_BASE = 'https://www.serebii.net/'
URL_POKEDEX = URL_BASE + 'pokedex{0}/{1}'

ARABIC_TO_STRINGS = {
    1: {TAG: '', SUFFIX: '{0}.shtml'},
    2: {TAG: '-gs', SUFFIX: '{0}.shtml'},
    3: {TAG: '-rs', SUFFIX: '{0}.shtml'},
    4: {TAG: '-dp', SUFFIX: '{0}.shtml'},
    5: {TAG: '-bw', SUFFIX: '{0}.shtml'},
    6: {TAG: '-xy', SUFFIX: '{0}.shtml'},
    7: {TAG: '-sm', SUFFIX: '{0}.shtml'},
    8: {TAG: '-swsh', SUFFIX: '{0}/'},
    9: {TAG: '-sv', SUFFIX: '{0}/'},
}

ROMAN_TO_ARABIC = {
    'I': 1,
    'II': 2,
    'III': 3,
    'IV': 4,
    'V': 5,
    'VI': 6,
    'VII': 7,
    'VIII': 8,
    'IX': 9,
}

MOVE_TABLE_TITLES = {
    1: 'Generation I Level Up',
    2: 'Generation II Level Up',
    3: 'Ruby/Sapphire/Emerald/Colosseum/XD Level Up',
    4: 'Diamond/Pearl/Platinum/HeartGold/SoulSilver Level Up',
    5: 'Black/White/Black 2/White 2 Level Up',
    6: 'Generation VI Level Up',
    7: 'Generation VII Level Up',
    8: 'Standard Level Up',
    9: 'Standard Level Up',
    'frlg': 'Fire Red/Leaf Green Level Up',
    'lgpe': 'Let\'s Go Level Up',
    'alola': 'Alola Form Level Up',
    'galar': 'Galarian Form Level Up',
    'hisui': 'Hisuian Form Level Up',
    'paldea': 'Paldean Form Level Up',
}

class SerebiiReader(object):
    def __init__(self):
        pass

    def getMoveset(self, pokemon, gen, alt=''):
        gen = self.standardizeGen(gen)

        moveset = {}

        url = self.getURLPokemon(pokemon, gen)

        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')

        tables = soup.find_all('table', class_='dextable')
        move_table = None

        for table in tables:
            first_row = table.find('tr')
            if first_row is None:
                continue

            header = first_row.find('h3')
            if header is None:
                continue

            title = MOVE_TABLE_TITLES[alt] if alt else MOVE_TABLE_TITLES[self.standardizeGen(gen)]
            if header.text == title:
                move_table = table
                break

        rows = move_table.find_all('tr')
        for row in rows[2::2]:
            cols = row.find_all('td')

            level = cols[0].text
            level = int(level) if level.isdigit() else 0

            moveset[cols[1].text] = level

        return moveset

    def getURLPokemon(self, pokemon, gen):
        strs = ARABIC_TO_STRINGS[self.standardizeGen(gen)]

        return URL_POKEDEX.format(strs[TAG], strs[SUFFIX].format(pokemon))

    def standardizeGen(self, gen):
        if isinstance(gen, int):
            return gen        
        if gen.isdigit():
            return int(gen)
        if gen.upper() in ROMAN_TO_ARABIC:
            return ROMAN_TO_ARABIC[gen.upper()]
        
        return ''
