from sentence_transformers import SentenceTransformer, util

def match_signatures(query_embedding, known_signatures, model_name="all-MiniLM-L6-v2"):
    """
    Compute semantic similarity between a gene set embedding and known biological signatures.

    Args:
        query_embedding (np.array): 
            The embedding vector representing the gene set's textual summary.
        known_signatures (dict): 
            A dictionary where keys are signature labels and values are natural language descriptions.
            Example:
                {
                    "Apoptosis": "Programmed cell death...",
                    "Immune Response": "Activation of T-cells..."
                }
        model_name (str): 
            Name or path of a sentence-transformers model to use for encoding signature descriptions.
            Default is "all-MiniLM-L6-v2".

    Returns:
        results (list of tuples): 
            List of (label, similarity_score) tuples sorted in descending order of similarity.
        embeddings_dict (dict): 
            Dictionary mapping each label to its computed embedding (used for UMAP or further analysis).
    """
    model = SentenceTransformer(model_name)
    labels = list(known_signatures.keys())
    descriptions = list(known_signatures.values())

    signature_embeddings = model.encode(descriptions)
    scores = util.cos_sim(query_embedding, signature_embeddings)[0]

    results = [(label, float(score)) for label, score in zip(labels, scores)]
    results.sort(key=lambda x: x[1], reverse=True)

    embeddings_dict = {
        label: embedding for label, embedding in zip(labels, signature_embeddings)
    }

    return results, embeddings_dict
