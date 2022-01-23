
grams = []
repeats = []

with open('n_grams.txt', encoding='utf8') as f:
    for line in f:
        if (line in grams) and (line not in repeats):
            repeats.append(line)
        elif line not in grams:
            grams.append(line)

with open('n_grams-repeated.txt', 'w', newline='', encoding='utf-8') as the_file:
    for gram in repeats:
        the_file.write(gram)

with open('n_grams-no-repeats.txt', 'w', newline='', encoding='utf-8') as the_file:
    for gram in grams:
        the_file.write(gram)
