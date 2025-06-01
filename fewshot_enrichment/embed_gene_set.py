# src/embed_gene_set.py

from sentence_transformers import SentenceTransformer

# Load a general-purpose or bio-specific embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")  # Replace with BioBERT variant if desired

def embed_gene_set(text):
    """
    Embed concatenated gene summaries using a transformer model.

    Args:
        text (str): Combined gene summaries as a single string.

    Returns:
        np.array: Sentence embedding of the gene text.
    """
    return model.encode(text)
