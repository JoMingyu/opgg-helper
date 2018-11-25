import re
import webbrowser
from typing import Tuple

import click

from metadata import *

HOST_FORMAT = 'http://www.op.gg/champion/{champion_name}/statistics/{position}'
ENGLISH_REGEX = re.compile('^[A-z]+$')


@click.group()
def cli():
    pass


def _map_korean_champion_name_to_english(champion_name: str) -> str:
    if champion_name not in CHAMPION_KOREAN_NAME_ENGLISH_NAME_MAPPING:
        raise ValueError()

    return CHAMPION_KOREAN_NAME_ENGLISH_NAME_MAPPING[champion_name]


def _map_korean_position_name_to_english(position_name: str) -> str:
    return POSITION_KOREAN_NAME_ENGLISH_NAME_MAPPING.get(position_name, '')
    # position이 전달되지 않거나, 전달된 position이 invalid 하다면
    # op.gg에서 가장 점유율 높은 포지션으로 리다이렉트 시켜주므로 key exist check하지 않음


def _map_korean_arguments_to_english(champion_name: str, position_name: str) -> Tuple[str, str]:
    return (
        champion_name if ENGLISH_REGEX.match(champion_name) else _map_korean_champion_name_to_english(champion_name),
        position_name if ENGLISH_REGEX.match(position_name) else _map_korean_position_name_to_english(position_name)
    )


def _extract_retrieve_target_info_from_arguments(arg1: str, arg2: str) -> Tuple[str, str]:
    """
    This function makes user can change the order of the arguments without any problems.
    ex) lulu support, support lulu

    returns tuple represents - (champion name, position name)
    """

    if arg1 in VALID_POSITION_NAMES:
        return arg2, arg1
    elif arg2 in VALID_POSITION_NAMES:
        return arg1, arg2
    elif arg1 in VALID_CHAMPION_NAMES:
        return arg1, arg2
    elif arg2 in VALID_CHAMPION_NAMES:
        return arg2, arg1
    else:
        # 아 못찾겠당
        raise ValueError()


@click.command()
@click.argument('arg1')
@click.argument('arg2')
def browser(arg1: str, arg2: str):
    champion_name, position_name = _extract_retrieve_target_info_from_arguments(arg1, arg2)
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
