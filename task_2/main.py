import os
from typing import List, Dict, Set

import pymorphy2


def pos(word: str, morth=pymorphy2.MorphAnalyzer()) -> str:
    # функция возвращает часть речи слова
    return morth.parse(word)[0].tag.POS


def text_preprocessing(input_text: str) -> str:
    # убираем знаки пунктуации и числа; приводим к нижнему регистру
    punctuation = """!"#$%&\'()*+,.:;<=>?@[\\]^_`{|}~"""
    tt = str.maketrans(dict.fromkeys(f"{punctuation}“”«»"))
    return input_text.lower().translate(tt).replace("/", " ")


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


def write_tokens_to_file(tokens: Set[str]) -> None:
    """Метод для записи токенов в файл"""
    with open("tokens.txt", "w", encoding="utf-8") as f:
        for token in tokens:
            f.write(f"{token}\n")


def get_lemmas_from_token(tokens: Set[str]) -> Dict[str, List[str]]:
    """Метод для получения словаря лемм из списка токенов"""
    lemmas = {}
    morph = pymorphy2.MorphAnalyzer()
    for token in tokens:
        p = morph.parse(token)[0]
        if p.normal_form not in lemmas:
            lemmas[p.normal_form] = [token, ]
        else:
            lemmas[p.normal_form].append(token)
    return lemmas


def write_lemmas_to_file(lemmas: Dict[str, List[str]]) -> None:
    """Метод для записи лемм в файл"""
    with open("lemmas.txt", "w", encoding="utf-8") as f:
        for lemma in lemmas:
            f.write(f"{lemma}: {' '.join(lemmas[lemma])}\n")


def main():
    tokens = set()
    for root, dirs, files in os.walk("../task_1/sites"):
        for filename in files:
            file = f"{root}/{filename}"
            print(f"Open {file}...")
            with open(file, "r", encoding="utf-8") as f:
                print(f"Preprocessing {file}...")
                text = text_preprocessing(f.read())
                print(f"Tokenize {file}...")
                words = get_words_from_text(text)
                tokens.update(set(words))
    print("Writing tokens to file")
    write_tokens_to_file(tokens)
    print("Lemmatize tokens")
    lemmas = get_lemmas_from_token(tokens)
    print("Writing lemmas to file")
    write_lemmas_to_file(lemmas)


main()
