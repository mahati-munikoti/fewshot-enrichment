# src/visualize_embeddings.py

import umap
import umap.umap_ as umap
import numpy as np
import matplotlib.pyplot as plt
import os

def plot_embedding_map(query_embedding, known_signatures, save_path="results/embedding_plot.png"):
    # Create results directory if it doesn't exist
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Combine query + known embeddings
    labels = ["Query"] + list(known_signatures.keys())
    embeddings = [query_embedding] + [sig["embedding"] for sig in known_signatures.values()]
    
    embeddings_np = np.array(embeddings)

    # UMAP dimensionality reduction
    reducer = umap.UMAP(n_neighbors=5, min_dist=0.3, metric="cosine", random_state=42)
    reduced = reducer.fit_transform(embeddings_np)

    # Plot
    plt.figure(figsize=(8, 6))
    for i, label in enumerate(labels):
        x, y = reduced[i]
        plt.scatter(x, y, s=100 if label == "Query" else 60)
        plt.text(x + 0.01, y + 0.01, label, fontsize=10)

    plt.title("UMAP Embedding of Gene Signature Similarities")
    plt.xlabel("UMAP-1")
    plt.ylabel("UMAP-2")
    plt.tight_layout()

    # Save to file
    plt.savefig(save_path)
    plt.close()
    print(f"UMAP plot saved to: {save_path}")
