import re
import webbrowser

import click
from bs4 import BeautifulSoup
from requests import get

from metadata import _POSITION_KO_EN_MAPPING, _VALID_POSITION_NAMES, _CHAMPION_NAME_KO_EN_MAPPING

HOST_FORMAT = 'http://www.op.gg/champion/{champion_name}/statistics/{position}'
ENGLISH_REGEX = re.compile('^[A-z]+$')


@click.group()
def cli():
    pass


def _map_korean_champion_name_to_english(champion_name):
    if champion_name not in _CHAMPION_NAME_KO_EN_MAPPING:
        raise ValueError()

    return _CHAMPION_NAME_KO_EN_MAPPING[champion_name]


def _map_korean_position_name_to_english(position_name):
    return _POSITION_KO_EN_MAPPING.get(position_name, '')
    # position이 전달되지 않거나, 전달된 position이 invalid 하다면
    # op.gg에서 가장 점유율 높은 포지션으로 리다이렉트 시켜주므로 key in check하지 않음


def _map_korean_arguments_to_english(champion_name, position_name):
    return (
        champion_name if ENGLISH_REGEX.match(champion_name) else _map_korean_champion_name_to_english(champion_name),
        position_name if ENGLISH_REGEX.match(position_name) else _map_korean_position_name_to_english(position_name)
    )


def _extract_arguments(arg1, arg2):
    if arg1 in _VALID_POSITION_NAMES:
        return arg2, arg1
    elif arg2 in _VALID_POSITION_NAMES:
        return arg1, arg2
    else:
        # 어느 argument에도 position에 관련된 정보가 없는 경우
        raise ValueError()


@click.command()
@click.argument('arg1')
@click.argument('arg2')
def browser(arg1, arg2):
    champion_name, position_name = _extract_arguments(arg1, arg2)
    champion_name, position_name = _map_korean_arguments_to_english(champion_name, position_name)

    webbrowser.open(HOST_FORMAT.format(champion_name=champion_name, position=position_name))


# @click.command()
# @click.argument('champion_name')
# @click.argument('position')
# def stash(champion_name, position_name):
#     champion_name, position_name = _map_korean_arguments_to_english(champion_name, position_name)
#
#     return


cli.add_command(browser)
# cli.add_command(stash)

if __name__ == '__main__':
    cli()
