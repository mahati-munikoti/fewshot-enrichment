# Few-Shot Enrichment

**Few-Shot Enrichment** is an AI-powered semantic enrichment analysis tool that matches input gene sets to biological processes using transformer-based language models (e.g., BioBERT, MiniLM, Specter). It allows insights even from small or poorly annotated gene sets.

---

## Features

* Fetches gene summaries from NCBI
* Embeds gene text using transformer models (BioBERT, MiniLM, T5, etc.)
* Matches to biological signatures using cosine similarity
* UMAP visualization of enrichment space
* Generates word clouds and extracts top biological key phrases
* CLI interface and text file support

---

## Installation

```bash
git clone https://github.com/yourusername/fewshot-enrichment.git
cd fewshot-enrichment
pip install -e .
```

> You can now run it via `fewshot-enrich` on the command line.

---

## Usage

### Analyze a gene list:

```bash
fewshot-enrich --genes IL6 TNF CXCL8 TP53
```

### Or use a text file:

```bash
fewshot-enrich --file data/sample_genes.txt
```

### List supported transformer models:

```bash
fewshot-enrich --list-models
```

---

## Project Structure

```
fewshot-enrichment/

├── setup.py                    ← Packaging script
├── requirements.txt            ← Dependencies
├── data/
│   ├── known_signatures.json   ← Biological label descriptions
│   ├── models.json             ← Transformer model options
│   └── sample_genes.txt        ← Sample gene list
├── results/                    ← Output directory
│   ├── top_matches.json
│   ├── key_phrases.txt
|   ├── gene_summaries.json
|   ├── per_gene_top_matches.json
│   ├── wordcloud.png
│   └── embedding_plot.png
├── fewshot_enrichment/             ← Core modules
|   |── main.py                     ← CLI script entry point                       
│   ├── __init__.py
│   ├── fetch_ncbi.py
│   ├── embed_gene_set.py
│   ├── match_signatures.py
│   ├── analyze_results.py
│   └── visualize_embeddings.py
```

---

## Output Files (in `results/`)

| File                             | Description                                                  |
|----------------------------------|--------------------------------------------------------------|
| `top_matches.json`               | Top enriched biological signatures based on full gene set    |
| `key_phrases.txt`                | Top biological phrases extracted from all gene summaries     |
| `gene_summaries.json`            | Raw NCBI summary for each gene used in the input             |
| `per_gene_top_matches.json`      | Top enriched signatures for each individual gene             |
| `per_gene_key_phrases.json`      | Top key phrases per gene, using transformer-based extraction |
| `wordcloud.png`                  | Visual word cloud generated from all gene summaries          |
| `embedding_plot.png`             | UMAP plot of query vs. known signature embeddings            |


---

## Sample Gene File

You can test with this list saved as `data/sample_genes.txt`:

```
TP53
BRCA1
EGFR
PTEN
IL6
CXCL8
TNF
```

---

## Supported Models

```bash
fewshot-enrich --list-models
```

| Model Name                               | Description                    |
| ---------------------------------------- | ------------------------------ |
| `all-MiniLM-L6-v2`                       | Fast general-purpose (default) |
| `pritamdeka/BioBERT-...`                 | Biomedical (PubMed/NLI)        |
| `sentence-transformers/sentence-t5-base` | Fluent text-based              |
| `allenai/specter`                        | Scientific paper embeddings    |

---

## Contributing

Pull requests welcome!
Open an issue for suggestions, bugs, or feature requests.

---

## License

MIT License © 2024 mahati-munikoti

---

##  Credits

Built using:

* [sentence-transformers](https://www.sbert.net/)
* [Biopython](https://biopython.org/)
* [KeyBERT](https://github.com/MaartenGr/KeyBERT)
* [UMAP-learn](https://github.com/lmcinnes/umap)
