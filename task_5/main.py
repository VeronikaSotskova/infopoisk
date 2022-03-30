import pickle

from task_5.utils import text_preprocessing, get_lemma_from_token, get_base_vector, get_global_idf_lemmas, \
    get_vectors_by_doc, cos, get_sites

tfidf_tokens_db_name = "../task_4/tfidf_tokens_db.pickle"
tfidf_lemmas_db_name = "../task_4/tfidf_lemmas_db.pickle"
lemma_base_vector_db_name = "lemma_base_vector_db.pickle"
vectors_by_doc_db_name = "vectors_by_doc_db.pickle"
idf_global_lemmas_db_name = "idf_global_lemmas.pickle"


def write_base_vector_lemma():
    """
    Ищем все леммы из всех документов, и создаем базовый вектор, с коэф-ом idf=0.0,
    Записываем в pickle файл
    """
    all_lemmas = set()
    with open(tfidf_lemmas_db_name, 'rb') as lemmas:
        tf_idf_lemmas = pickle.load(lemmas)
        for site_id in tf_idf_lemmas.keys():
            all_lemmas.update(list(tf_idf_lemmas[site_id].keys()))
        lemma_base_vector = {lemma: 0.0 for lemma in all_lemmas}

    with open(lemma_base_vector_db_name, 'wb') as f:
        pickle.dump(lemma_base_vector, f)


def write_tf_idf_by_doc():
    """
    Создаем словарь вида {doc_id: {lemma:tfidf, lemma2:tfidf}, doc_id2: {}}
    Записываем в pickle файл
    """
    with open(lemma_base_vector_db_name, 'rb') as vector:
        base_vector = pickle.load(vector)

    with open(tfidf_lemmas_db_name, 'rb') as lemmas:
        tf_idf_lemmas = pickle.load(lemmas)

    docs_vector = {}
    for site_id in tf_idf_lemmas.keys():
        vector_of_doc = base_vector.copy()
        for lemma in tf_idf_lemmas[site_id].keys():
            if lemma in vector_of_doc.keys():
                vector_of_doc[lemma] = tf_idf_lemmas[site_id][lemma]["tfidf"]
        docs_vector[site_id] = list(vector_of_doc.values())

    with open(vectors_by_doc_db_name, 'wb') as f:
        pickle.dump(docs_vector, f)


def write_all_idf_lemmas():
    """
    Создаем словарь idf всех лемм из всех документов
    Записываем в pickle файл
    """
    with open(tfidf_lemmas_db_name, 'rb') as lemmas:
        tf_idf_lemmas = pickle.load(lemmas)

    idf_of_all_lemmas = {}
    for site_id in tf_idf_lemmas.keys():
        for lemma in tf_idf_lemmas[site_id].keys():
            if lemma not in idf_of_all_lemmas.keys():
                idf_of_all_lemmas[lemma] = tf_idf_lemmas[site_id][lemma]["idf"]

    with open(idf_global_lemmas_db_name, 'wb') as f:
        pickle.dump(idf_of_all_lemmas, f)


def main(min_similarity: float = 0.0):
    """
    Векторный поиск
    """
    global_lemma_idf = get_global_idf_lemmas()
    base_vector = get_base_vector()
    docs_vectors = get_vectors_by_doc()
    sites = get_sites()

    input_query = input("Найти: ")
    clean_query = text_preprocessing(input_query)
    query_lemmas = list(map(lambda word: get_lemma_from_token(word), clean_query.split()))
    query_vector_dict = base_vector.copy()

    for lemma in query_lemmas:
        if lemma in query_vector_dict.keys():
            tf = query_lemmas.count(lemma) / len(query_lemmas)
            idf = global_lemma_idf[lemma]
            query_vector_dict[lemma] = tf * idf

    response = {"query": input_query}

    results = []
    query_vector = list(query_vector_dict.values())

    for site_id in docs_vectors.keys():
        doc_vector = docs_vectors[site_id]
        sim = cos(query_vector, doc_vector)
        if sim > min_similarity:
            results.append({
                "similarity": sim,
                "page": sites[site_id]
            })
    results = sorted(results, key=lambda x: x["similarity"], reverse=True)
    response["results"] = results
    for res in results:
        print(f"{res['page']}; sim: {res['similarity']}")


main()
