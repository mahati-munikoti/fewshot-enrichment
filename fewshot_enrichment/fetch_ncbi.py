# src/fetch_ncbi.py

from Bio import Entrez
import time
import os
from dotenv import load_dotenv

load_dotenv()
Entrez.email = os.getenv("NCBI_EMAIL", "anonymous@example.com")

def fetch_gene_summaries(gene_symbols, organism="Homo sapiens", delay=0.4):
    summaries = []

    for gene in gene_symbols:
        try:
            search_handle = Entrez.esearch(
                db="gene", term=f"{gene}[sym] AND {organism}[orgn]", retmax=1
            )
            search_results = Entrez.read(search_handle)
            search_handle.close()

            ids = search_results.get("IdList", [])
            if not ids:
                continue

            fetch_handle = Entrez.efetch(db="gene", id=ids[0], retmode="xml")
            records = Entrez.read(fetch_handle)
            fetch_handle.close()

            summary = records[0].get("Entrezgene_summary", "")
            if summary:
                summaries.append(summary)

            time.sleep(delay)  # Be respectful to NCBI servers
        except Exception as e:
            print(f"Error fetching {gene}: {e}")
            continue

    return " ".join(summaries)
