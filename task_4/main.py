import math
import os
import pickle

from task_4.utils import text_preprocessing, get_words_from_text, get_lemma_from_token, write_counter_to_file

tokens_db_name = "tokens_db.pickle"
lemmas_db_name = "lemmas_db.pickle"

tfidf_tokens_db_name = "tfidf_tokens_db.pickle"
tfidf_lemmas_db_name = "tfidf_lemmas_db.pickle"


def get_lemmas_tokens_by_site():
    """
    разбивает леммы и токены по каждому документы с кол-вом
    """
    global_tokens = {}
    global_lemmas = {}
    for root, dirs, files in os.walk("../task_1/sites"):
        for filename in files:
            file = f"{root}/{filename}"
            file_num = int(filename.split(".")[0])
            print(f"Open {file}...")
            with open(file, "r", encoding="utf-8") as f:
                print(f"Preprocessing {file}...")
                text = text_preprocessing(f.read())
                print(f"Tokenize {file}...")
                words = get_words_from_text(text)
                tokens = {}
                lemmas = {}
                for word in words:
                    if word not in tokens:
                        tokens[word] = 1
                    else:
                        tokens[word] += 1
                    word_lemma = get_lemma_from_token(word)
                    if word_lemma not in lemmas:
                        lemmas[word_lemma] = 1
                    else:
                        lemmas[word_lemma] += 1
                global_tokens[file_num] = tokens
                global_lemmas[file_num] = lemmas
                write_counter_to_file(words=tokens, filename=f"tokens/{str(file_num)}.txt")
                write_counter_to_file(words=lemmas, filename=f"lemmas/{str(file_num)}.txt")
                print(f"Writing {filename} finished")
    with open(lemmas_db_name, 'wb') as f:
        pickle.dump(global_lemmas, f)
    with open(tokens_db_name, 'wb') as f:
        pickle.dump(global_tokens, f)


def write_tf_idf():
    """
    считает tf-idf по каждому документу для каждой леммы и токена; записывает в pickle файл
    """
    global_tokens = {}
    global_lemmas = {}
    with open(tokens_db_name, 'rb') as tokens:
        global_tokens = pickle.load(tokens)
    with open(lemmas_db_name, 'rb') as lemmas:
        global_lemmas = pickle.load(lemmas)

    count_of_tokens = len(global_tokens.keys())
    count_of_lemmas = len(global_tokens.keys())
    global_tfidf_tokens = {}
    global_tfidf_lemmas = {}

    for site_id in range(1, 101):
        print(f"Go parse {site_id}.txt")
        keys_tokens = list(global_tokens.get(site_id).keys())
        keys_lemmas = list(global_lemmas.get(site_id).keys())
        sum_of_tokens_in_doc = sum(global_tokens.get(site_id).values())
        sum_of_lemmas_in_doc = sum(global_lemmas.get(site_id).values())
        global_tfidf_tokens[site_id] = {}
        global_tfidf_lemmas[site_id] = {}
        print(f"Parsing tokens {site_id}...")
        for key_token in keys_tokens:
            token_count = global_tokens.get(site_id)[key_token]
            tf_token = token_count / sum_of_tokens_in_doc
            count_of_docs_with_token = 0
            for k in global_tokens.keys():
                if global_tokens[k].get(key_token):
                    count_of_docs_with_token += 1
            idf_token = math.log10(count_of_tokens / count_of_docs_with_token)
            global_tfidf_tokens[site_id][key_token] = {"tf": tf_token, "idf": idf_token, "tfidf": tf_token * idf_token}
        print(f"Parsing lemmas {site_id}...")
        for key_lemma in keys_lemmas:
            lemma_count = global_lemmas.get(site_id)[key_lemma]
            tf_lemma = lemma_count / sum_of_lemmas_in_doc
            count_of_docs_with_lemma = 0
            for k in global_lemmas.keys():
                if global_lemmas[k].get(key_lemma):
                    count_of_docs_with_lemma += 1
            idf_lemma = math.log10(count_of_lemmas / count_of_docs_with_lemma)
            global_tfidf_lemmas[site_id][key_lemma] = {"tf": tf_lemma, "idf": idf_lemma, "tfidf": tf_lemma * idf_lemma}

    with open(tfidf_tokens_db_name, 'wb') as f:
        pickle.dump(global_tfidf_tokens, f)
    with open(tfidf_lemmas_db_name, 'wb') as f:
        pickle.dump(global_tfidf_lemmas, f)


def main():
    """
    записывает из pickle файла tf-idf для каждого документа в отдельный txt файл
    """
    with open(tfidf_tokens_db_name, 'rb') as tokens:
        tfidf_tokens = pickle.load(tokens)
        for site_id in tfidf_tokens.keys():
            with open(f"tfidf_tokens/{str(site_id)}.txt", "w", encoding="utf-8") as f:
                for key_word in tfidf_tokens[site_id].keys():
                    idf = tfidf_tokens[site_id][key_word]["idf"]
                    tfidf = tfidf_tokens[site_id][key_word]["tfidf"]
                    f.write(f"{key_word} {idf} {tfidf}\n")

    with open(tfidf_lemmas_db_name, 'rb') as lemmas:
        tfidf_lemmas = pickle.load(lemmas)
        for site_id in tfidf_lemmas.keys():
            with open(f"tfidf_lemmas/{str(site_id)}.txt", "w", encoding="utf-8") as f:
                for key_word in tfidf_lemmas[site_id].keys():
                    idf = tfidf_lemmas[site_id][key_word]["idf"]
                    tfidf = tfidf_lemmas[site_id][key_word]["tfidf"]
                    f.write(f"{key_word} {idf} {tfidf}\n")


# get_lemmas_tokens_by_site()
# write_tf_idf()

main()
