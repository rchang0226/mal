import json
import os
import string
import nltk
import numpy as np
from keras.saving.save import load_model
from keras_preprocessing.sequence import pad_sequences
from nltk import PorterStemmer
from keras.preprocessing.text import Tokenizer
from nltk.corpus import stopwords


def load_data(path):
    text = []
    files = [f for f in os.listdir(path) if f.endswith('.txt')]
    for filename in files:
        file = open(os.path.join(path, filename), 'rt', encoding='utf-8')
        doc = file.read()
        file.close()
        text.append(doc)
    return text


def tokenize_text(text):
    table = str.maketrans("," * len(string.punctuation), string.punctuation)
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words('english'))

    words = nltk.word_tokenize(text)
    words = [w.lower() for w in words]
    words = [w.translate(table) for w in words]
    words = [word for word in words if word.isalnum()]
    words = [stemmer.stem(word) for word in words if word not in stop_words]
    return words


def load_vocab(filename):
    words = []
    with open(filename, 'r') as fp:
        for line in fp:
            x = line[:-1]
            words.append(x)
    return words


if __name__ == '__main__':
    f = open('reviews.json')
    data = json.load(f)
    f.close()

    docs = [node["body"] for node in data]
    scores = [node["score"] for node in data]
    binary = [1 if score > 75 else -1 if score < 40 else 0 for score in scores]
    print(binary)
    print(scores)
    print(binary.count(-1))
    print(binary.count(1))

    filtered_docs = []
    filtered_scores = []
    for doc, score in zip(docs, binary):
        if score != 0:
            filtered_docs.append(doc)
            filtered_scores.append(score)

    # tokenize the text
    cleaned = [tokenize_text(doc) for doc in filtered_docs]

    # load vocab
    vocab = set(load_vocab('vocab.txt'))

    # filter out tokens not in vocab
    tokens = [[w for w in tokens if w in vocab] for tokens in cleaned]

    # Grab training data to fit tokenizer to
    pos_text = load_data('txt_sentoken/pos')
    pos_train = pos_text[:-100]
    neg_text = load_data('txt_sentoken/neg')
    neg_train = neg_text[:-100]
    all_train = pos_train + neg_train
    train_cleaned = [tokenize_text(text) for text in all_train]
    train = [[w for w in tokens if w in vocab] for tokens in train_cleaned]

    # set up tokenizer
    t = Tokenizer()
    t.fit_on_texts(train)
    vocab_size = len(t.word_index) + 1

    # encode
    encoded = t.texts_to_sequences(tokens)

    # pad sequences
    max_length = max([len(s) for s in train])
    X = pad_sequences(encoded, maxlen=max_length, padding='post')

    y = np.array([0 if x == -1 else x for x in filtered_scores])

    # load model
    model = load_model('model.h5')

    # evaluate the model
    score = model.evaluate(X, y, verbose=0)
    print("%s: %.2f%%" % (model.metrics_names[1], score[1] * 100))
