import os
from setuptools import setup, find_packages

setup(
    name="fewshot_enrichment",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "biopython==1.83",
        "sentence-transformers==2.2.2",
        "transformers==4.30.2",
        "huggingface_hub==0.14.1",
        "scikit-learn==1.3.0",
        "numpy==1.24.4",
        "scipy==1.11.4",
        "python-dotenv==1.0.1",
        "matplotlib==3.8.2",
        "umap-learn==0.5.5",
        "keybert==0.7.0",
        "wordcloud==1.9.3"
    ],
    entry_points={
        "console_scripts": [
            "fewshot-enrich=fewshot_enrichment.main:main"
        ]
    },
    author="Mahati Munikoti",
    description="Few-shot semantic enrichment using language models.",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/mahati-munikoti/fewshot-enrichment",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.8, <3.12'
)
