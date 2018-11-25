import re
import requests
from bs4 import BeautifulSoup


def _get_perk_name(perk):
    perk_name_regex = re.compile(r'alt="[a-zA-Zㄱ-힇 ]*')
    perk_name_reqex2 = re.compile(r'[ㄱ-힇]{2}')

    perk_str = str(perk)
    perk_name = perk_name_regex.findall(perk_str)
    if 'perkStyle' in perk_str:
        perk_name = perk_name_reqex2.findall(perk_str)[0]
    else:
        perk_name = perk_name[0][5:]
    return perk_name


def _print_perk_row(perk_row):
    select_regex = re.compile(r'\/\/opgg-static\.akamaized\.net\/images\/lol.*png$')

    perk_name = ''
    perks = []
    for perk in perk_row.find_all('img'):
        if select_regex.match(perk['src']):
            perks.append('O')
            perk_name = _get_perk_name(perk)
        else:
            perks.append('X')

    print(f'{" ".join(perks)}\t\t{perk_name}')


def _print_perk(perk_pages):
    for perk_page in perk_pages[:2]:
        for perk_row in perk_page.find_all(class_='perk-page__row'):
            _print_perk_row(perk_row)
        print()


def _get_fragment_name(fragment):
    return str(fragment)[173:-16]


def _print_fragment_row(fragment_row):
    select_regex = re.compile(r'\/\/opgg-static\.akamaized\.net\/images\/lol.*png$')

    fragments = []
    fragment_name = ''
    for fragment in fragment_row.find_all('img'):
        if select_regex.match(fragment['src']):
            fragments.append('O')
            fragment_name = _get_fragment_name(fragment)
        else:
            fragments.append('X')

    print(f'{" ".join(fragments)}\t\t{fragment_name}')


def _print_fragment(fragment_page):
    for fragment_row in fragment_page.find_all(class_='fragment__row'):
        _print_fragment_row(fragment_row)


def console_print(opgg_url):
    html = requests.get(opgg_url).text
    soup = BeautifulSoup(html, 'html.parser')

    perk_pages = soup.find_all(class_='perk-page')
    fragment_page = soup.find(class_='fragment__detail')

    _print_perk(perk_pages[:2])
    _print_fragment(fragment_page)
