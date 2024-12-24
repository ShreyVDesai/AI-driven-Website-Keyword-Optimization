from rake_nltk import Rake
import re

def preprocess_for_rake(text):
    # Remove special characters and lowercase the text
    cleaned_text = re.sub(r'[^\w\s]', '', text.lower())
    return cleaned_text

def extract_keywords_rake(text, num_keywords=10):
    rake = Rake()
    text = preprocess_for_rake(text)
    rake.extract_keywords_from_text(text)
    return rake.get_ranked_phrases()[:num_keywords]
