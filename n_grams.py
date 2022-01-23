# -*- coding: UTF-8 -*-
import csv
import tkinter

from nltk import ngrams

from processor import preprocess_text


def levenshtein_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]


def callback(text):
    global usr_input
    usr_input = text.get()
    if text == '':
        text_area.delete('1.0', tkinter.END)
        return

    query = usr_input.strip('\n')
    query = preprocess_text.preprocess(query)
    query = query.split()
    res = []
    entry2.delete(0, tkinter.END)
    for e in query:
        res.append([])
        entry2.insert(tkinter.END, e + ' ')


def callback_2():
    text = usr_input

    if text == '':
        text_area.delete('1.0', tkinter.END)
        return

    query = text.strip('\n')
    query = preprocess_text.preprocess(query)
    query = query.split()
    res = []
    entry2.delete(0, tkinter.END)
    for e in query:
        res.append([])
        entry2.insert(tkinter.END, e + ' ')

    res = []
    for i in range(len(query)):
        res.append([])

    if len(res) > 1:
        for word in word_list:
            for i in range(len(query) - 1):
                edit_distance = levenshtein_distance(query[i], word[1])
                if edit_distance <= 1:
                    res[i].append([edit_distance, float(word[0]), word[1]])
        query.reverse()
        res.reverse()
        for word in n_grams:
            word_ = word[0].split(' ')
            edit_distance = levenshtein_distance(query[0], word_[0])
            if edit_distance <= 1:
                res[0].append([edit_distance, float(word[1]) - len(word_), word[0]])
        res.reverse()
        query.reverse()
    elif len(res) == 1:
        for word in word_list:
            edit_distance = levenshtein_distance(query[0], word[1])
            if edit_distance <= 1:
                res[0].append([edit_distance, float(word[0]), word[1]])

    p = []
    for i in range(len(res)):
        p.append([])

    for r in range(len(res)):
        # print(sorted(sorted(res[r], key=lambda x: x[1]), key=lambda x: x[0], reverse=True))
        out = sorted(sorted(res[r], key=lambda x: x[1]), key=lambda x: x[0], reverse=True)
        out.reverse()
        for i in range(10):
            if i < len(out):
                p[r].append(out[i][2])

    for e in range(len(p)):
        if not p[e]:
            p[e] = [query[e]]
            adapt(query, p)

    sentence = ''
    for i in range(len(p)-1):
        sentence += p[i][0] + ' '

    res_list = []
    for n_gram in p[len(p)-1]:
        res_list.append(sentence+n_gram)

    text_area.delete('1.0', tkinter.END)

    for n_gram in res_list:
        print_me = n_gram.split(' ')
        print_me.reverse()
        print_me = ' '.join(print_me)

        text_area.insert(tkinter.END, print_me+'\n', 'tag-right')


def adapt(query, p):
    # add words to word list 'word_list'
    for e in query:
        flag = 0
        for word in word_list:
            if e == word[1]:
                flag = 1
                break
        if flag == 0:
            print('word \''+e+'\' added to words list.')
            word_list.append(['0.004', e])

    # make n-grams and add them to n-gram list 'n_grams'
    make_n_grams(' '.join(query))


def make_n_grams(sentence):
    tmp = []
    for i in range(2, 6):
        n = i
        n_grams_local = ngrams(sentence.split(), n)
        for gram in n_grams_local:
            if gram not in tmp:
                tmp.append(gram)
                new_gram = gram[0]
                for j in range(1, i):
                    new_gram += (' ' + gram[j])
                add_gram([new_gram, '0.005'])


def add_gram(gram):
    flag = 0
    for g in n_grams:
        if g[0] == gram[0]:
            flag = 1
            break
    if flag == 0:
        print('n-gram \'' + gram[0] + '\' added to n-grams list.')
        n_grams.append(gram)


if __name__ == '__main__':
    word_list = []
    n_grams = []
    usr_input = ''
    with open('word_list_dir\\word_list_counted.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            word_list.append(row)
    # with open('n_grams\\n_grams', newline='', encoding='utf-8') as f:
    with open('n_grams\\orange_input.txt', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            n_grams.append(row)
    preprocess_text.load_stopwords_from_files_and_library()

    root = tkinter.Tk()

    root.title('NLP')
    root.geometry("700x500")

    # creating a label
    label = tkinter.Label(root, text=":الاستفسار")
    label.place(x=620, y=50)

    entry2 = tkinter.Entry(root, width=37, font=('calibre', 10, 'normal'), justify=tkinter.RIGHT)
    entry2.place(x=350, y=100)

    # creating a label
    label = tkinter.Label(root, text=":النص معالج")
    label.place(x=610, y=100)

    # creating a label
    label = tkinter.Label(root, text=":التنبؤ")
    label.place(x=640, y=150)

    # creating a result text area
    text_area = tkinter.Text(root, font=('Consolas', 18), relief='flat', height=10, width=50)
    text_area.tag_configure('tag-right', justify='right')
    text_area.place(x=20, y=180)

    # button
    button = tkinter.Button(text="تنبأ", width=20, height=5, command=callback_2)
    button.place(x=100, y=50)

    # creating a entry
    sv = tkinter.StringVar()
    sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))
    entry = tkinter.Entry(root, textvariable=sv, width=37, font=('calibre', 10, 'normal'), justify=tkinter.RIGHT)
    # entry.insert(0, 'اللغة العربية هي')
    # entry.insert(0, 'اللغة العربية هي التي أدخلت في الغرب طريقة التعبير العلمي')
    # entry.insert(0, 'القرن الواحد والعشرين بكل إنجازاته الإنسانية')
    entry.insert(0, 'هذا النوع من الاستمرارية المتحوسبة')                           # not in the dataset
    entry.place(x=350, y=50)

    callback_2()

    root.mainloop()
