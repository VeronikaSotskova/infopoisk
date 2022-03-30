import math
import pickle

import pymorphy2

site_db_filename = "../task_3/sites_db.pickle"
lemma_base_vector_db_name = "lemma_base_vector_db.pickle"
idf_global_lemmas_db_name = "idf_global_lemmas.pickle"
vectors_by_doc_db_name = "vectors_by_doc_db.pickle"


def get_lemma_from_token(token: str) -> str:
    morph = pymorphy2.MorphAnalyzer()
    p = morph.parse(token)[0]
    return p.normal_form


def text_preprocessing(input_text: str) -> str:
    # убираем знаки пунктуации и числа; приводим к нижнему регистру
    punctuation = """!"#$%&\'()*+,.:;<=>?@[\\]^_`{|}~"""
    tt = str.maketrans(dict.fromkeys(f"{punctuation}“”«»"))
    return input_text.lower().translate(tt).replace("/", " ")


def get_sites() -> dict[int, str]:
    """
    Получение списка сайтов с их номером
    """
    with open(site_db_filename, 'rb') as sites_db:
        sites = pickle.load(sites_db)
    return sites


def get_base_vector() -> dict[str, float]:
    """
    Получение базового вектора
    """
    with open(lemma_base_vector_db_name, 'rb') as vector:
        base_vector = pickle.load(vector)
    return base_vector


def get_global_idf_lemmas() -> dict[str, float]:
    """
    Получение словаря с idf лемм
    """
    with open(idf_global_lemmas_db_name, 'rb') as f:
        idf_lemmas = pickle.load(f)
    return idf_lemmas


def get_vectors_by_doc() -> dict[int, list[float]]:
    """
    Получение словаря с tfidf по документу и лемме
    """
    with open(vectors_by_doc_db_name, 'rb') as f:
        vectors = pickle.load(f)
    return vectors


def cos(v1: list[float], v2: list[float]) -> float:
    """
    :param v1: вектор 1
    :param v2: вектор 2
    :return: косинусная мера между векторами
    """
    sum_numerator = sum(list(map(lambda el: el[0] * el[1], zip(v1, v2))))

    len_v1 = math.sqrt(sum(map(lambda x: x * x, v1)))
    len_v2 = math.sqrt(sum(map(lambda x: x * x, v2)))
    denominator = len_v1 * len_v2
    if denominator == 0:
        return 0
    return sum_numerator / denominator
