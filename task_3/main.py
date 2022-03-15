import pickle

from utils import text_preprocessing, get_words_from_text, lemmatize_word, restruct

site_db_filename = "sites_db.pickle"
inverted_indexes_db_filename = "inverted_indexes_db.pickle"


def save_index_file_to_pickle():
    """
    Метод, который считывает index файл с нумерацией страниц и записывает словарь в pickle файл
    """
    site_index_dict = {}

    with open("../task_1/index.txt", "r", encoding="utf-8") as f:
        for line in f:
            info = line.split()
            site_index_dict[int(info[0])] = info[1]

    with open(site_db_filename, 'wb') as f:
        pickle.dump(site_index_dict, f)


def get_sites() -> dict[int, str]:
    """
    Получение списка сайтов с их номером
    """
    with open(site_db_filename, 'rb') as sites_db:
        sites = pickle.load(sites_db)
    return sites


def create_inverted_indexes_to_pickle():
    """
    Метод, который проходится по всем страницам, разделяет тексты по словам, лемматизирует
    Создает словарь (обратный индекс) в качестве ключа - лемма слова; в качестве значения - список номеров документов
    Далее сохраняет в pickle файл
    """
    inverted_indexes = {}
    sites = get_sites()
    for site_id in sites:
        print(f"Parse {site_id} file")
        with open(f"../task_1/sites/{str(site_id)}.txt", "r", encoding="utf-8") as f:
            text = text_preprocessing(f.read())
            words = get_words_from_text(text)
            for word in words:
                word_lemma = lemmatize_word(word)
                if word_lemma in inverted_indexes:
                    if site_id not in inverted_indexes[word_lemma]:
                        inverted_indexes[word_lemma].append(site_id)
                else:
                    inverted_indexes[word_lemma] = [site_id, ]

    with open(inverted_indexes_db_filename, 'wb') as f:
        pickle.dump(inverted_indexes, f)


def save_inverted_indexes_to_txt():
    """
    Метод, который считывает словарь обратного индекса из pickle файла и записывает в txt файл
    """
    inverted_indexes = get_inverted_indexes()
    with open("inverted_index.txt", "w", encoding="utf-8") as f:
        for index in inverted_indexes:
            indexes = " ".join(list(map(str, inverted_indexes[index])))
            f.write(f"{index}: {indexes}\n")


def get_inverted_indexes() -> dict[str, list[int]]:
    """
    Получение обратного индекса из pickle файла
    """
    with open(inverted_indexes_db_filename, 'rb') as inverted_indexes_db:
        inverted_indexes = pickle.load(inverted_indexes_db)
    return inverted_indexes


def not_operator(lemma: str, inverted_indexes: dict[str, list[int]]) -> set:
    """
    Оператор NOT
    :param lemma: лемма слова
    :param inverted_indexes: словарь обратного индекса
    :return: Возвращает множество id сайтов, в которых не встречается данное слово
    """
    sites_id = get_sites().keys()
    response = sites_id - set(inverted_indexes.get(lemma, []))
    return response


def bool_search(search: str) -> set[int]:
    operators = ["AND", "OR", "NOT"]
    search_new = restruct(search)
    split_search = search_new.split()

    res_q = []
    # Если между словами пробел, то вставляем AND между ними
    for i in range(len(split_search) - 1):
        if split_search[i] not in operators and (split_search[i + 1] not in operators or split_search[i + 1] == "NOT"):
            res_q.extend([split_search[i], "AND"])
            continue
        else:
            res_q.append(split_search[i])
    if split_search[-1] not in operators:
        res_q.append(split_search[-1])

    inverted_indexes = get_inverted_indexes()

    query = " ".join(res_q).replace("NOT ", "!").replace("OR", "|").replace("AND", "&")
    query_split = query.split()
    for word in query_split:
        if word not in ["&", "|"]:
            if word.startswith("!"):
                query = query.replace(word, str(set(not_operator(word[1:], inverted_indexes))))
            elif word.startswith("("):
                query = query.replace(word[1:], str(set(inverted_indexes.get(word[1:], []))))
            elif word[-1] == ")":
                query = query.replace(word[:-1], str(set(inverted_indexes.get(word[:-1], []))))
            else:
                query = query.replace(word, str(set(inverted_indexes.get(word, []))))
    try:
        result = eval(query)
    except Exception:
        result = set()
    return result


def main():
    # search_query = "(москва OR день) AND валентина"
    # search_query = "(социальные навыки) OR (доза государства)"
    search_query = input("Найти: ")
    sites = get_sites()
    idxs = bool_search(search_query)
    result_sites = [sites.get(idx) for idx in idxs]
    print(
        {
            "query": search_query,
            "results": result_sites
        }
    )


main()
