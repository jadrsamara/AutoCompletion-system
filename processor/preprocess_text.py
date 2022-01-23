import csv
import re
from nltk.corpus import stopwords

stop_words = []
punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''
arabic_diacritics = re.compile("""
                             ّ    | # Shadda
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)


def load_stopwords_from_files_and_library():
    global stop_words
    stop_words = stopwords.words('arabic')
    with open('C:\\Users\\jadsa\\Documents\\Birzeit\\other\\Python-Workspace\\NLP\\stopwords\\stopwordsallforms.txt',
              newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter="	")
        for row in reader:
            stop_words.append(row[0])


def preprocess(text):
    # remove punctuations
    translator = str.maketrans('', '', punctuations)
    text = text.translate(translator)

    # remove Tashkeel
    text = re.sub(arabic_diacritics, '', text)

    # remove longation
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("گ", "ك", text)

    text = ' '.join(word for word in text.split() if word not in stop_words)

    return text


def test_func():
    text = 'مرحبا يا صديقي، كيف الحال؟'
    print(preprocess(text))


if __name__ == "__main__":
    load_stopwords_from_files_and_library()
