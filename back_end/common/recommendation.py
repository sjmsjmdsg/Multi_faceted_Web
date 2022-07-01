from TextPreprocess import *
import tqdm
import time


def recommend_related_info_expv1():
    new_type2th = PostLoader().load_pickle('./type_thesaurus_new.pkl')
    new_type = PostLoader().load_pickle('./word_type_new.pkl')
    new_phrase = PostLoader().load_pickle('./phrase2cve_new.pkl')
    new_w2cve = PostLoader().load_pickle('./word2cve_new.pkl')
    new_cve2w = PostLoader().load_pickle('./cve2word_new.pkl')
    new_th2type = PostLoader().load_pickle('./thesaurus_type_new.pkl')

    tp = TextPreprocess()

    keywords = input("keywords: ")
    phraseslist = [tp.clean_so_data_nopos(one_word.strip()) for one_word in keywords.split(',') if
                   len(one_word) > 0]
    wordslist = []
    for one_phrase in phraseslist:
        wordslist += one_phrase.split()
    wordslist = set([one_word for one_word in wordslist if len(one_word) > 0])
    phraseslist = set([one_phrase for one_phrase in phraseslist if len(one_phrase.split()) > 1])

    priority = ['name', 'component', 'type', 'impact', 'vector', 'root']
    type_dict = {one_ele: set() for one_ele in priority}
    for one_word in wordslist:
        if new_type.get(one_word) is None:
            continue
        word_types = new_type[one_word]
        for one_type in word_types:
            type_dict[one_type].add(one_word)


    candidate_words = set()
    for one_priority in priority:
        if len(type_dict[one_priority]) > 0:
            candidate_words = type_dict[one_priority]
            break

    candidate_cves = set()
    for one_word in candidate_words:
        if new_w2cve.get(one_word) is None:
            continue
        candidate_cves = candidate_cves.union(set(new_w2cve[one_word]))

    cve_scores = {}
    time_count = [0, 0, 0, 0, 0, 0]
    for one_cve in tqdm.tqdm(candidate_cves):
        cve_scores[one_cve] = 0
        cve_words = set()
        time1 = time.time()
        if not new_cve2w.get(one_cve) is None:
            cve_words = set(new_cve2w[one_cve])
        time_count[0] += time.time() - time1
        time1 = time.time()

        cve_phrases = set()
        if not new_phrase.get(one_cve) is None:
            cve_phrases = set(new_phrase[one_cve])
        time_count[1] += time.time() - time1
        time1 = time.time()

        thesaurus = set()
        for one_word in wordslist:
            if new_th2type.get(one_word) is None:
                continue
            thesaurus = thesaurus.union(set(new_th2type[one_word]))
        time_count[2] += time.time() - time1
        time1 = time.time()

        thesaurus_words = set()
        for one_thesa in thesaurus:
            if new_type2th.get(one_thesa) is None or one_thesa in ['impact:3', 'root:1', 'impact:4', 'impact:6']:
                continue
            thesaurus_words = thesaurus_words.union(set(new_type2th[one_thesa]))
        time_count[3] += time.time() - time1
        time1 = time.time()

        for one_word in wordslist:
            if one_word in cve_words:
                cve_scores[one_cve] += 1
        time_count[4] += time.time() - time1
        time1 = time.time()

        for one_phrase in phraseslist:
            if one_phrase in cve_phrases:
                cve_scores[one_cve] += 1
            elif one_phrase in thesaurus_words:
                cve_scores[one_cve] += 1
        time_count[5] += time.time() - time1
        time1 = time.time()

    cve_scores = sorted(cve_scores.items(), key=lambda x: x[1], reverse=True)
    print(cve_scores)
    print(time_count)

if __name__ == "__main__":
    recommend_related_info_expv1()