from typing import List

import pymorphy2


def text_preprocessing(input_text: str) -> str:
    # убираем знаки пунктуации и числа; приводим к нижнему регистру
    punctuation = """!"#$%&\'()*+,.:;<=>?@[\\]^_`{|}~"""
    tt = str.maketrans(dict.fromkeys(f"{punctuation}“”«»"))
    return input_text.lower().translate(tt).replace("/", " ")


def pos(word: str, morth=pymorphy2.MorphAnalyzer()) -> str:
    # функция возвращает часть речи слова
    return morth.parse(word)[0].tag.POS


def is_digit(str_input: str) -> bool:
    # проверяем есть ли в слове цифра
    for el in str_input:
        try:
            float(el)
            return True
        except ValueError:
            pass
    return False


def get_words_from_text(input_text: str) -> List[str]:
    """
    Разбиваем текст на слова; обрезаем пробелы вокруг слова
    убираем служебные части речи
    """
    # INTJ - междометие; PRCL - частица; CONJ - союз; PREP - предлог
    functors_pos = {'CONJ', 'PREP', 'PRCL', 'INTJ'}
    words = list(map(lambda word: word.strip(), input_text.split()))
    words = [word for word in words if
             pos(word) not in functors_pos and word not in ["–", "", " "] and not is_digit(word)]
    return words


def get_lemma_from_token(token: str) -> str:
    morph = pymorphy2.MorphAnalyzer()
    p = morph.parse(token)[0]
    return p.normal_form


def write_counter_to_file(words: dict, filename: str) -> None:
    """Метод для записи токенов в файл"""
    with open(filename, "w", encoding="utf-8") as f:
        for word in words.keys():
            f.write(f"{word} {words[word]}\n")
