from nltk import ngrams

sentence = ''
tmp = []


def load_articles(input_name):
    global sentence
    with open(input_name, encoding='utf8') as f:
        for line in f:
            sentence += line.strip()


def make_n_grams(output_name):
    with open(output_name, 'w', newline='', encoding='utf-8') as the_file:
        for i in range(1, 6):
            n = i
            n_grams = ngrams(sentence.split(), n)
            for gram in n_grams:
                if gram not in tmp:
                    tmp.append(gram)
                    the_file.write(gram[0])
                    for j in range(1, i):
                        the_file.write(' ' + gram[j])
                    # the_file.write(' ' + gram[len(gram)-1])
                    the_file.write('\n')
