from .constants import *
from collections import Counter
from math import log
import snowballstemmer
from nltk.corpus import stopwords


def start_srt_a(s):
    stemmerE = snowballstemmer.stemmer('english')
    stemmerR = snowballstemmer.stemmer('russian')
    stopE = set(stemmerE.stemWords(stopwords.words('english')))
    stopR = set(stemmerR.stemWords(stopwords.words('russian')))
    PUNCTUATION_MARKS_END = ['!', '?', '.']
    PUNCTUATION_MARKS = [',', '"', '"', ':', ';', '(', ')', '-', '«', '»', '—']
    for c in PUNCTUATION_MARKS_END:
        s = s.replace(c, '')
    for c in PUNCTUATION_MARKS:
        s = s.replace(c, '')
    s = s.lower()
    words = list(s.split())
    words1 = []
    spot_word = []
    for w in words:
        if w[0] in 'abcdefghijklmnopqrstuvwxyz':
            p = stemmerE.stemWords([w])[0]
            if not (p in stopE):
                words1.append(p)
            else:
                spot_word.append(p)
        if w[0] in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
            p = stemmerR.stemWords([w])[0]
            if not (p in stopR):
                words1.append(p)
            else:
                spot_word.append(p)
    return words1, spot_word


def counting_characters(sl, arr):
    count = 0
    for ch in arr:
        count += sl[ch]
    return count


def delete_char(st, arr):
    sc = set(arr)
    f = ''.join([c for c in st if c not in sc]).split()
    return f


def tag_process(df, column):
    for tag in ALL_TAGS:
        df[column + '_is_' + tag] = df[column].apply(lambda t: t == tag)
        df = df.copy()
    df[column + '_is_HYPERLINK'] = df[column].apply(lambda t: t in HYPERLINK)
    df[column + '_is_ADDRESS'] = df[column].apply(lambda t: t in ADDRESS)
    df[column + '_is_INDIRECT_INFORMATION'] = df[column].apply(lambda t: t in INDIRECT_INFORMATION)
    df[column + '_is_SOURCE'] = df[column].apply(lambda t: t in SOURCE)
    df[column + '_is_FOOTER'] = df[column].apply(lambda t: t in FOOTER)
    df[column + '_is_HEADING'] = df[column].apply(lambda t: t in HEADING)
    df[column + '_is_ANNOTATION'] = df[column].apply(lambda t: t in ANNOTATION)
    df[column + '_is_IGNORED'] = df[column].apply(lambda t: t in IGNORED)
    df.drop(columns=[column], inplace=True)
    return df


def process(df):
    df = tag_process(df, 'tag')
    df = tag_process(df, 'parent_tag')
    df = tag_process(df, 'super_parent_tag')
    df['process_text'] = df['text'].apply(lambda t: t.strip().lower())
    all_lines = Counter(df['process_text'])
    df['has_duplicate'] = df['process_text'].apply(lambda t: all_lines[t] > 1)
    df['has_duplicate_fife'] = df['process_text'].apply(lambda t: all_lines[t] >= 5)
    quantity_char_all = [len(x) for x in df['process_text']]
    quantity_char_all1 = [len(x.replace(' ', '')) for x in df['process_text']]
    quantity_char = [Counter(x) for x in df['process_text']]
    df['quantity_offer'] = [counting_characters(x, PUNCTUATION_MARKS_END) for x in quantity_char]
    df['quantity_offer'] = df['quantity_offer'].apply(lambda t: log(t) if t > 0 else 0)
    words = [delete_char(s, PUNCTUATION_MARKS_END + PUNCTUATION_MARKS + OTHER_SIGNS) for s in df['process_text']]
    quantity_words = [len(x) for x in words]
    df['is_word'] = [x > 0 for x in quantity_words]
    df['log_words'] = [x for x in quantity_words]
    df['log_words'] = df['log_words'].apply(lambda t: log(t) if t > 0 else 0)
    frequency_punctuation = [counting_characters(x, PUNCTUATION_MARKS_END + PUNCTUATION_MARKS + OTHER_SIGNS) for x in
                             quantity_char]
    df['average_word'] = [
        (quantity_char_all1[i] - frequency_punctuation[i]) / quantity_words[i] if quantity_words[i] > 0 else 0 for i in
        range(len(quantity_words))]
    df['frequency_punctuation'] = [frequency_punctuation[i] / quantity_char_all[i] for i in
                                   range(len(quantity_char_all))]
    df['is_punctuation'] = [x > 0 for x in df['frequency_punctuation']]
    quantity_number = [counting_characters(x, NUMBERS) for x in quantity_char]
    df['is_number'] = [x > 0 for x in quantity_number]
    df['frequency_number'] = [quantity_number[i] / quantity_char_all[i] for i in range(len(quantity_number))]
    df['end_end_offer'] = [x[len(x) - 1] in PUNCTUATION_MARKS_END for x in df['process_text']]
    df['end_offer_?'] = [x[len(x) - 1] == '?' for x in df['process_text']]
    df['is_@'] = ['@' in x for x in df['process_text']]
    df['is_©'] = ['©' in x for x in df['process_text']]
    df['is_\n'] = ['\n' in x for x in df['process_text']]
    df['start_is_'] = [(x[0] in PUNCTUATION_MARKS_END) or (x[0] in PUNCTUATION_MARKS) for x in df['process_text']]
    is_math = []
    for x in df['process_text']:
        math = False
        for c in OTHER_SIGNS:
            if c in x:
                math = True
        is_math.append(math)
    df['is_math'] = is_math
    df['log_char'] = df['process_text'].apply(lambda t: log(len(t)) if len(t) > 0 else 0)
    frequency_capital_letters = []
    frequency_capital_letters_and = []
    k_all = 0
    k_all_N = 0
    for x in df['text']:
        k_one = 0
        k_one_N = 0
        n = len(x)
        for i in range(len(x) - 1):
            if x[i] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ':
                k_one += 1
                k_all += 1
                if x[i + 1] == '.':
                    k_one_N += 1
                    k_all_N += 1
        if x[n - 1] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ':
            k_one += 1
            k_all += 1
        frequency_capital_letters_and.append(k_one_N)
        frequency_capital_letters.append(k_one)
    df['frequency_capital_letters'] = [x / k_all if k_all > 0 else 0 for x in frequency_capital_letters]
    df['frequency_capital_letters_and'] = [x / k_all_N if k_all_N > 0 else 0 for x in frequency_capital_letters_and]
    year = []
    for x in df['text']:
        st = ' ' + x + ' '
        kol_year = 0
        n = len(st)
        num = '0123456789'
        if n >= 6:
            for c in range(1, n - 5):
                if (not st[c - 1] in num) and (st[c] in num) and (not st[c + 1] in num) and (not st[c + 2] in num) and (
                        not st[c + 3] in num) and (not st[c + 4] in num):
                    kol_year += 1
        year.append(kol_year)
    df['is_year'] = [x > 0 for x in year]
    stop_s = []
    k_all_s = 0
    words_all = []
    word_all = []
    for x in df['text']:
        word, stop = start_srt_a(x)
        stop_s.append(len(stop))
        k_all_s += len(stop)
        k_all_s += len(word)
        words_all += word
        word_all.append(word)
    all_words = Counter(words_all)
    popular_words = []
    not_popular_words = []
    popular = []
    for i in all_words:
        popular.append(all_words[i])
    popular.sort(reverse=True)
    kol_pop = 0
    if len(popular) < 10:
        for i in popular:
            if i > 1:
                kol_pop += 1
    else:
        n_pw = 0
        for i in popular:
            if i > 1:
                kol_pop += 1
            n_pw += 1
            if n_pw == 10:
                break
    for i in popular:
        kol_pop -= 1
        for j in all_words:
            if not (j in popular_words) and (all_words[j] == i):
                popular_words.append(j)
                break
        if kol_pop == 0:
            break
    is_popular_word = []
    for i in word_all:
        fl = False
        for j in popular_words:
            fl = j in i
            if fl:
                break
        is_popular_word.append(fl)
    for i in all_words:
        if all_words[i] == 1:
            not_popular_words.append(i)
    is_not_popular_word = []
    for i in word_all:
        fl = False
        for j in not_popular_words:
            fl = j in i
            if fl:
                break
        is_not_popular_word.append(fl)
    df['is_not_popular_word'] = is_not_popular_word
    df['is_popular_word'] = is_popular_word
    df['frequency_stop_word'] = [x / k_all_s if k_all_s > 0 else 0 for x in stop_s]
    df.drop(columns=['process_text'], inplace=True)
    return df
