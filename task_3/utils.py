import pymorphy2


def pos(word: str, morth=pymorphy2.MorphAnalyzer()) -> str:
    # функция возвращает часть речи слова
    return morth.parse(word)[0].tag.POS


def text_preprocessing(input_text: str) -> str:
    # убираем знаки пунктуации и числа; приводим к нижнему регистру
    punctuation = """!"#$%&\'()*+,.:;<=>?@[\\]^_`{|}~"""
    tt = str.maketrans(dict.fromkeys(f"{punctuation}“”«»"))
    functors_pos = {'CONJ', 'PREP', 'PRCL', 'INTJ'}
    output = input_text.lower().translate(tt).replace("/", " ")
    output_splitted = output.split()
    for word in output_splitted:
        if pos(word) in functors_pos or word in ["–", "", " "] or is_digit(word):
            output = output.replace(word, "")
    return output


def is_digit(str_input: str) -> bool:
    # проверяем есть ли в слове цифра
    for el in str_input:
        try:
            float(el)
            return True
        except ValueError:
            pass
    return False


def get_words_from_text(input_text: str) -> list[str]:
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


def lemmatize_word(word: str) -> str:
    """
    Метод для получения леммы
    """
    morph = pymorphy2.MorphAnalyzer()
    p = morph.parse(word)[0]
    return p.normal_form


def restruct(input_text: str) -> str:
    """
    Метод, который убирает из текста пунктуацию, служебные части речи,
    И приводит каждое слово к нижнему регистру, и заменяет на лемму
    """
    operators = ["AND", "OR", "NOT"]
    split_text = input_text.split()
    punctuation = """!"#$%&\'*+,.:;<=>?@[\\]^_`{|}~"""
    tt = str.maketrans(dict.fromkeys(f"{punctuation}“”«»"))
    functors_pos = {'CONJ', 'PREP', 'PRCL', 'INTJ'}
    text = []
    for el in split_text:
        if el in operators:
            text.append(el)
        elif pos(el) not in functors_pos or el in ["–", "", " "] or is_digit(el):
            if el.startswith("("):
                text.append("(" + lemmatize_word(el[1:].lower().translate(tt).replace("/", " ")))
            elif el[-1] == ")":
                text.append(lemmatize_word(el[:-1].lower().translate(tt).replace("/", " ")) + ")")
            else:
                text.append(lemmatize_word(el.lower().translate(tt).replace("/", " ")))
    return " ".join(text)
