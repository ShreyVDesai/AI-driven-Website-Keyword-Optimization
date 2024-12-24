import streamlit as st
from similarity.Similarity import Similarity
from lda.LDAextractor import LDA_extractor
from KeyBert.keybert_extractor import KeyBertExtractor
from Scraper.Scraper import Scraper
import rake
import textrank
import tfidf


# Streamlit application
def main():
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
    extractor_type = st.radio("Select the extractor type:", ("KeyBERT", "RAKE", 'TFIDF', 'Text Rank'))

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
        document = scraper.scrape(topic)
        st.success("Scraping completed.")

        
        
        # Keyword extraction
        st.write("Extracting keywords...")
        if extractor_type == "KeyBERT":
            extractor = KeyBertExtractor()
            keywords = extractor.extract_keywords(document)
        elif extractor_type == 'RAKE':
            keywords = rake.extract_keywords_rake(document)
        elif extractor_type == 'TFIDF':
            keywords = tfidf.extract_keywords_tfidf(document)
        else:
            keywords = textrank.extract_keywords_textrank(document)
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