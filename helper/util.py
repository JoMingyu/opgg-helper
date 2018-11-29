from typing import List, Tuple

from helper.metadata import CHAMPION_KOREAN_NAME_ENGLISH_NAME_MAPPING, POSITION_KOREAN_NAME_ENGLISH_NAME_MAPPING

CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
JONGSUNG_LIST = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']


def _split_korean(korean_word: str) -> List[str]:
    r_lst = []
    for w in list(korean_word.strip()):
        if '가' <= w <= '힣':
            ch1 = (ord(w) - ord('가'))//588
            ch2 = ((ord(w) - ord('가')) - (588*ch1)) // 28
            ch3 = (ord(w) - ord('가')) - (588*ch1) - 28*ch2
            r_lst += [CHOSUNG_LIST[ch1], JUNGSUNG_LIST[ch2]]
            if JONGSUNG_LIST[ch3]:
                r_lst.append(JONGSUNG_LIST[ch3])
        else:
            r_lst.append(w)

    return r_lst


def _get_similarity(typo: List[str], word: List[str]) -> int:
    similarity = 0
    for i in range(len(typo)):
        for j in range(len(word)-1, -1, -1):
            if typo[i] == word[j]:
                similarity += 1
                del word[j]
                break

    return similarity


def fix_typo(typo: str) -> str:
    typo = _split_korean(typo)

    expect_word = ''
    expect_length = 0
    for word in list(CHAMPION_KOREAN_NAME_ENGLISH_NAME_MAPPING) + list(POSITION_KOREAN_NAME_ENGLISH_NAME_MAPPING):
        similarity = _get_similarity(typo, _split_korean(word))
        if similarity > expect_length:
            expect_word = word
            expect_length = similarity
    print(expect_word)

    return expect_word
