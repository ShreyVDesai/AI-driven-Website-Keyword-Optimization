from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


def extract_keywords_tfidf(texts, num_keywords=10):
    vectorizer = TfidfVectorizer(max_features=num_keywords, stop_words='english')
    texts = preprocess_for_tfidf(texts)
    tfidf_matrix = vectorizer.fit_transform([texts])
    return vectorizer.get_feature_names_out()

def preprocess_for_tfidf(text):
    # Lowercase and tokenize
    tokens = word_tokenize(text.lower())
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    cleaned_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    return ' '.join(cleaned_tokens)
