from processor import preprocess_text

preprocess_text.load_stopwords_from_files_and_library()

with open("combined_articles.txt", "r", newline='', encoding='utf-8') as input:
    with open("combined_articlesREADY.txt", "w", newline='', encoding='utf-8') as output:
        for line in input:
            output.write(preprocess_text.preprocess(line) + '\n')
