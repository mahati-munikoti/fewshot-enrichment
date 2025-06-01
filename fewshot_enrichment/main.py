# main.py

import json
import argparse
import os
from fewshot_enrichment.embed_gene_set import embed_gene_set
from fewshot_enrichment.match_signatures import match_signatures
from fewshot_enrichment.visualize_embeddings import plot_embedding_map
from fewshot_enrichment.fetch_ncbi import fetch_gene_summaries
from fewshot_enrichment.analyze_results import generate_wordcloud, extract_key_phrases

def main():
    parser = argparse.ArgumentParser(description="Few-shot enrichment analysis using gene summaries")
    parser.add_argument("--genes", nargs="*", help="List of gene symbols")
    parser.add_argument("--file", type=str, help="Path to file containing gene symbols (one per line)")
    parser.add_argument("--model", type=str, default="all-MiniLM-L6-v2", help="Sentence-transformer model name")
    parser.add_argument("--top-n-phrases", type=int, default=20, help="Number of top key phrases to extract")
    parser.add_argument("--list-models", action="store_true", help="List supported transformer models and exit")
    args = parser.parse_args()

    if args.list_models:
        with open("data/models.json") as f:
            model_info = json.load(f)
        print("\n Supported Sentence-Transformer Models:\n")
        for name, meta in model_info.items():
            print(f"- {name}")
            print(f"  → {meta['description']} (Domain: {meta['domain']})\n")
        exit(0)

    # Load gene list
    gene_set = []
    if args.genes:
        gene_set = args.genes
    elif args.file:
        with open(args.file, "r") as f:
            gene_set = [line.strip() for line in f if line.strip()]
    else:
        raise ValueError("Please provide a list of genes using --genes or a file using --file")

    print(f"Fetching NCBI summaries for {len(gene_set)} genes...")
    gene_summaries = {gene: fetch_gene_summaries([gene]) for gene in gene_set}
    gene_text = " ".join(gene_summaries.values())

    os.makedirs("results", exist_ok=True)
    with open("results/gene_summaries.json", "w") as f:
        json.dump(gene_summaries, f, indent=2)
    print("Gene summaries saved to results/gene_summaries.json")

    print("Generating word cloud...")
    generate_wordcloud(gene_text, output_path="results/wordcloud.png")

    print("Extracting key biological phrases...")
    phrases = extract_key_phrases(gene_text, model_name=args.model, top_n=args.top_n_phrases)
    print(f"\nTop {args.top_n_phrases} Key Biological Phrases:")
    for p, score in phrases:
        print(f" - {p} ({score:.2f})")

    with open("results/key_phrases.txt", "w") as f:
        for p, score in phrases:
            f.write(f"{p}\t{score:.4f}\n")
    print("Key phrases saved to results/key_phrases.txt")

    print("Embedding gene text...")
    query_embedding = embed_gene_set(gene_text)

    print("Loading known signatures...")
    with open("data/known_signatures.json", "r") as f:
        known_signatures = json.load(f)

    print("Matching signatures...")
    top_matches, known_signature_embeddings = match_signatures(
        query_embedding, known_signatures, model_name=args.model
    )

    print("Top enriched labels:")
    for label, score in top_matches[:5]:
        print(f"{label} (score: {score:.4f})")

    top_matches_output = [{"label": label, "score": score} for label, score in top_matches[:5]]
    with open("results/top_matches.json", "w") as f:
        json.dump(top_matches_output, f, indent=2)
    print("Top matches saved to results/top_matches.json")

    # Per-gene signature matches and phrases
    print("\n Computing per-gene signature enrichment and key phrases...")
    per_gene_scores = {}
    per_gene_phrases = {}

    for gene, summary in gene_summaries.items():
        if summary.strip():
            emb = embed_gene_set(summary)
            matches, _ = match_signatures(emb, known_signatures, model_name=args.model)
            per_gene_scores[gene] = matches[:5]

            key_phrases = extract_key_phrases(summary, model_name=args.model, top_n=args.top_n_phrases)
            per_gene_phrases[gene] = key_phrases
        else:
            per_gene_scores[gene] = []
            per_gene_phrases[gene] = []

    with open("results/per_gene_top_matches.json", "w") as f:
        json.dump(per_gene_scores, f, indent=2)
    print("Per-gene signature scores saved to results/per_gene_top_matches.json")

    with open("results/per_gene_key_phrases.json", "w") as f:
        json.dump(per_gene_phrases, f, indent=2)
    print("Per-gene key phrases saved to results/per_gene_key_phrases.json")

    print("Visualizing embedding map...")
    top_signatures_dict = {
        label: {
            "embedding": known_signature_embeddings[label],
            "score": score
        }
        for label, score in top_matches[:5]
    }
    plot_embedding_map(query_embedding, top_signatures_dict, save_path="results/embedding_plot.png")

if __name__ == "__main__":
    main()
