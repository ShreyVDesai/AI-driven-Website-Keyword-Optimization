import streamlit as st
from similarity.Similarity import Similarity
from KeyBert.keybert_extractor import KeyBertExtractor
from Scraper.Scraper import Scraper
import rake
# import textrank
import tfidf
import subprocess
import os
import spacy

# Download SpaCy model if not already installed
# model_name = "en_core_web_sm"  # Replace with the desired model name if needed
# try:
#     import spacy
#     spacy.load(model_name)
# except (ImportError, OSError):
#     subprocess.run(["python", "-m", "spacy", "download", model_name])
#     # os.system('python -m spacy download en_core_web_sm')
#     import spacy
#     spacy.load(model_name)

 

# Streamlit application
def main():
    
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.core.os_manager import ChromeType

    # @st.cache_resource
    def get_driver():
        return webdriver.Chrome(
            service=Service(
                ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            ),
            options=options,
        )

    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    st.title("Keyword Generator")
    st.write("Welcome to the keyword generator. Use this tool to extract keywords and find similarities.")

    # Input: Topic
    topic = st.text_input("Enter the Wikipedia topic for which you want to generate keywords:")

    # Input: Mode selection
    mode = st.radio(
        "Select the mode:",
        ("See the keyword itself", "Match it with a list of keywords"),
        format_func=lambda x: "See generated keywords" if x == "See the keyword itself" else "Match it with a list of keywords",
    )

    # Extractor type selection
    extractor_type = st.radio("Select the extractor type:", ("KeyBERT", "RAKE", 'TFIDF'))

    # Input: List of topics (if mode is "Match it with a list of keywords")
    list_of_topics = []
    if mode == "Match it with a list of keywords":
        st.write("Enter keywords to include in the list (press Enter after each keyword):")
        topic_list = st.text_area("Enter keywords separated by commas (e.g., keyword1, keyword2):", "")
        list_of_topics = [keyword.strip() for keyword in topic_list.split(",") if keyword.strip()]
    else:
        list_of_topics.append(topic)

    # Scrape the webpage
    if st.button("Scrape and Generate Keywords"):
        st.write("Scraping the Wikipedia page...")
        scraper = Scraper()
        document = scraper.scrape(topic,driver=get_driver())
        st.success("Scraping completed.")

        # st.write(document)
        
        # Keyword extraction
        st.write("Extracting keywords...")
        if extractor_type == "KeyBERT":
            extractor = KeyBertExtractor()
            keywords = extractor.extract_keywords(document)
        elif extractor_type == 'RAKE':
            keywords = rake.extract_keywords_rake(document)
        elif extractor_type == 'TFIDF':
            keywords = tfidf.extract_keywords_tfidf(document)
        # else:
            # keywords = textrank.extract_keywords_textrank(document)
            
        st.success("Keyword extraction completed.")

        # Mode-based processing
        if mode == "Match it with a list of keywords":
            n = len(list_of_topics)
        
            st.write("Calculating similarities...")
            similarity = Similarity(n)
            max_sim = []
            similarity_dict = {}
            for kw in keywords:
                similar_words = similarity.top_n_similar_words(list_of_topics, kw)
                for word in similar_words:
                    similarity_dict[word] = similarity_dict.get(word, 0) + 1
            for _ in range(n):
                best_match = max(similarity_dict, key=similarity_dict.get)
                max_sim.append(best_match)
                similarity_dict[best_match] = 0
            st.write("Top similar keywords:")
            st.write(max_sim)
        else:
            st.write("Extracted Keywords:")
            st.write(keywords)


if __name__ == "__main__":
    main()

