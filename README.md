# Keyword Generation Project Report

This is a project that can extract keywords from a Wikipedia article using different extractors and optionally match them against a given list of words to see which are most similar.
Developed a system employing NLP techniques, including topical modelling and KeyBERT, to dynamically generate SEO-optimized keywords from web content using nltk.
Integrated a word2vec model to assess semantic alignment between generated & defined keywords for better relevance.
Compared multiple models, optimizing website keyword generation using diverse techniques.
We first use selenium to scrape a website. Then, the data is passed through the KeyBERT/Topical modelling module, which generates keywords. These keywords are ranked using a semantic similarity module, where we use cosine similarity as the similarity metric.



## Getting Started

- In order to run this program, you will need to:
  1. install all relevant python packages that that is required when attempting to run.
  2. Go to the Similarity module and run fast_text_downloader.py. This will download and save the fast text model as a file which is used in the program.

## Running

The main program is called keywordProgram.py. When running the program, you will encounter a few decision points:
1. You will enter the title of a wikipedia article you wish to be scraped
2. You will choose if you wish to see the keywords or match the article to a list of given keywords
      - if the latter is chosen, you will enter keywords that you wish to match against
3. You will choose whether you want to use the KeyBERT extractor or the LDA extractor for keyword extraction
4. If you chose to match the article to a keyword list, you will choose how many of the top similar keyword you wish to see

