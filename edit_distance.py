import csv
from tkinter import *
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


def search():
    slaves = root.pack_slaves()
    if len(slaves) > 4:
        for i in range(4, len(slaves)):
            slaves[i].destroy()
            # print(l[i])

    query = text_.get("1.0", END).strip('\n')
    query = preprocess_text.preprocess(query)
    query = query.split()
    res = []

    text_q.delete('1.0', END)
    for e in query:
        res.append([])
        text_q.insert(END, '  '+e, 'tag-right')

    for word in word_list:
        for i in range(0, len(query)):
            edit_distance = levenshtein_distance(query[i], word[0])
            if edit_distance <= 1:
                res[i].append([word, edit_distance])
    for i in range(0, len(res)):
        if len(res[i]) == 0:
            res[i].append([[query[i], '0'], -1])

    for e in res:
        # print(sorted(sorted(e, key=lambda x: x[0][1], reverse=True), key=lambda x: x[1]))
        text_res = Text(root, width=len(e[0][0][0]) + 2)
        text_res.pack(side=RIGHT)
        text_res.tag_configure('tag-right', justify='right')
        for i in sorted(sorted(e, key=lambda x: x[0][1], reverse=True), key=lambda x: x[1]):
            text_res.insert(END, i[0][0]+'\n', 'tag-right')


if __name__ == '__main__':
    word_list = []
    with open('word_list_dir\\word_list_counted.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            word_list.append([row[1], row[0]])
    preprocess_text.load_stopwords_from_files_and_library()

    root = Tk()
    root.title('Auto Complete System')
    root.geometry('700x500')

    label = Label(root, width=64)
    label['text'] = 'input:'
    label.pack(side=TOP)

    text_ = Text(root, width=100, height=1)
    text_.insert(END, "اللغة العربية هي التي أدخلت في الغرب طريقة التعبير العلمي", 'tag-right')
    # text_.insert(END, "سون", 'tag-right')
    text_.pack(side=TOP)
    text_.tag_configure('tag-right', justify='right')

    button = Button(text="Search", command=search)
    button.pack(side=TOP)

    text_q = Text(root, width=100, height=1)
    text_q.pack(side=TOP)
    text_q.tag_configure('tag-right', justify='right')

    root.mainloop()

