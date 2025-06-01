from wordcloud import WordCloud
import matplotlib.pyplot as plt
from keybert import KeyBERT

def generate_wordcloud(text, output_path="results/wordcloud.png"):
    """
    Generate and save a word cloud image from the provided text.

    Args:
        text (str): 
            A string of text (e.g., NCBI gene summaries) to generate the word cloud from.
        output_path (str): 
            File path to save the resulting word cloud image. Default is "results/wordcloud.png".

    Returns:
        None. Saves the word cloud image to the specified output path.
    """
    wc = WordCloud(width=800, height=400, background_color="white").generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Wordcloud saved to {output_path}")

def extract_key_phrases(text, model_name="all-MiniLM-L6-v2", top_n=10):
    """
    Extract key phrases from a text using KeyBERT and a specified sentence-transformer model.

    Args:
        text (str): 
            The input text (e.g., gene function summaries) to analyze.
        model_name (str): 
            The sentence-transformer model to use for embedding phrases. Default is "all-MiniLM-L6-v2".
        top_n (int): 
            The number of top key phrases to return. Default is 10.

    Returns:
        List[Tuple[str, float]]: 
            A list of (key phrase, relevance score) tuples, sorted by descending score.
    """
    kw_model = KeyBERT(model=model_name)
    return kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 3), stop_words="english", top_n=top_n)
