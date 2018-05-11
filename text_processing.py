import nltk

from nltk.tokenize.moses import MosesDetokenizer


def split_into_sentences(text):
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = sent_detector.tokenize(text)

    return sentences


def split_into_words(text):
    return nltk.word_tokenize(text)


def untokenize_text(words):
    detokenizer = MosesDetokenizer()

    return detokenizer.detokenize(words, return_str=True)


def lemmatize_text(text):
    words = split_into_words(text)
    lemmatized_words = [lemmatize_word(word) for word in words]

    return untokenize_text(lemmatized_words)


def lemmatize_words(words):
    return [lemmatize_word(word) for word in words]


def lemmatize_word(word):
    word_lemmatizer = nltk.WordNetLemmatizer()
    return word_lemmatizer.lemmatize(word_lemmatizer.lemmatize(word_lemmatizer.lemmatize(word, 'v'), 'n'), 'a')


def lemmatize_sentences(sentences):
    lemmatized_sentences = []
    for sentence in sentences:
        lemmatized_sentences.append(lemmatize_text(sentence))

    return lemmatized_sentences
