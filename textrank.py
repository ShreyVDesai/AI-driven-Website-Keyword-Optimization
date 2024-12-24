import spacy

def preprocess_for_textrank(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text.lower())
    # Lemmatize and remove stopwords
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return ' '.join(tokens)


def extract_keywords_textrank(text, num_keywords=10):
    text = preprocess_for_textrank(text)
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("textrank")
    doc = nlp(text)
    return [phrase.text for phrase in doc._.phrases[:num_keywords]]
