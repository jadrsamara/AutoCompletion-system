import csv

words = []
word_list = []

with open('datasets\\n_grams.txt', newline='', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=";")
    for row in reader:
        words.append(row[0])

with open('word_list_dir\\word_list_counted.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=",")
    for row in reader:
        word_list.append(row)

# with open('orange_input.txt', 'w', newline='', encoding='utf-8') as the_file:
#     for line in words:
#         line = line.split(' ')
#         if len(line) > 1:
#             the_file.write(line[0])
#             for i in range(1, len(line) - 1):
#                 the_file.write(' ' + line[i])
#             the_file.write(',' + line[len(line) - 1])
#             the_file.write('\n')

with open('orange_input.txt', 'w', newline='', encoding='utf-8') as the_file:
    for line in words:
        line = line.split(' ')
        if len(line) > 1:
            prob = 0
            for word in word_list:
                if word[1] == line[1]:
                    prob = word[0]
                    break
                # break
            n_line = ''
            for i in range(len(line)-1):
                n_line += line[i] + ' '
            n_line += line[len(line)-1]
            the_file.write(n_line+','+str(prob)+'\n')
