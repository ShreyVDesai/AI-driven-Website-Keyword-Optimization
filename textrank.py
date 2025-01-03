# import spacy

# def preprocess_for_textrank(text):
#     nlp = spacy.load("en_core_web_sm")
#     doc = nlp(text.lower())
#     # Lemmatize and remove stopwords
#     tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
#     return ' '.join(tokens)


# def extract_keywords_textrank(text, num_keywords=10):
#     text = preprocess_for_textrank(text)
#     nlp = spacy.load("en_core_web_sm")
#     nlp.add_pipe("textrank")
#     doc = nlp(text)
#     return [phrase.text for phrase in doc._.phrases[:num_keywords]]
import spacy
import textacy
import subprocess

def preprocess_for_textrank(text):
    model_name = "en_core_web_sm"  # Replace with the desired model name if needed
    try:
        
        nlp = spacy.load(model_name)
    except (ImportError, OSError):
        subprocess.run(["python", "-m", "spacy", "download", model_name])
        # os.system('python -m spacy download en_core_web_sm')
        nlp = spacy.load(model_name)
    doc = nlp(text.lower())
    # Lemmatize and remove stopwords
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return ' '.join(tokens)

def extract_keywords_textrank(text, num_keywords=10):
    text = preprocess_for_textrank(text)
    model_name = "en_core_web_sm"  # Replace with the desired model name if needed
    try:
        nlp = spacy.load(model_name)
    except (ImportError, OSError):
        subprocess.run(["python", "-m", "spacy", "download", model_name])
        # os.system('python -m spacy download en_core_web_sm')
        nlp = spacy.load(model_name)
    
    # Process the text through spaCy and textacy
    doc = nlp(text)
    # Extract top keywords using TextRank
    keywords = textacy.extract.keyterms.textrank(doc, topn=num_keywords)
    
    # Return the extracted keywords
    return [keyword[0] for keyword in keywords]

# Example usage
text = "SpaCy is an open-source library for advanced natural language processing in Python."
keywords = extract_keywords_textrank(text)
print(keywords)

