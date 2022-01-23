from processor import preprocess_text
from n_grams import n_grams

preprocess_text.load_stopwords_from_files_and_library()
# preprocess_text.test_func()

n_grams.load_articles('datasets\\combined_articles.txt')
n_grams.sentence = preprocess_text.preprocess(n_grams.sentence)
n_grams.make_n_grams('datasets\\n_grams.txt')
