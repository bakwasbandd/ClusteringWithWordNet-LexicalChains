# ClusteringWithWordNet-LexicalChains

A research project and Streamlit dashboard for comparing document clustering approaches that use WordNet word-sense disambiguation and lexical-chain features.

The project experiments with 20 Newsgroups documents, builds semantic representations from nouns and WordNet synsets, clusters the documents with k-means, and compares the results against a TF-IDF baseline.

## Project Overview

This repository contains two main parts:

- `main.ipynb`: the full experiment notebook for loading data, preprocessing text, applying WordNet-based WSD, building lexical chains, clustering, evaluating, and generating plots.
- `app.py`: a Streamlit dashboard that displays the generated evaluation charts.

The experiment compares three systems:

| System | Description |
| --- | --- |
| Baseline | Standard TF-IDF features with k-means clustering. |
| DC | Disambiguated Concepts: WordNet sense-disambiguated concept features. |
| DCS | Disambiguated Core Semantics: lexical-chain-selected semantic features. |

## Dataset

The notebook uses a subset of the 20 Newsgroups dataset through `sklearn.datasets.fetch_20newsgroups`.

Selected categories:

- `rec.sport.hockey`
- `sci.space`
- `talk.politics.guns`
- `comp.graphics`
- `rec.autos`
- `sci.med`

The notebook samples up to 100 documents per category, giving 600 documents total for the reported run. The `dataset/` folder also contains text files and `list.csv` metadata for the broader 20 Newsgroups collection.

## Methodology

The experiment pipeline is:

1. Load selected 20 Newsgroups categories.
2. Clean and tokenize document text.
3. Extract nouns for semantic processing.
4. Use WordNet and Wu-Palmer similarity for word-sense disambiguation.
5. Build lexical chains from semantically related synsets.
6. Construct feature matrices for Baseline, DC, and DCS systems.
7. Cluster documents using k-means with six clusters.
8. Evaluate clusters using purity, F1, entropy, NMI, and ARI.
9. Generate visualization charts for analysis.

## Reported Results

Results from the saved notebook run:

| System | Purity | F1 | Entropy | NMI | ARI |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | 0.5167 | 0.5361 | 1.8278 | 0.3047 | 0.1923 |
| DC | 0.3050 | 0.2832 | 2.3576 | 0.0956 | 0.0404 |
| DCS | 0.3417 | 0.3515 | 2.2258 | 0.1630 | 0.0297 |

Feature matrix sizes from the same run:

| System | Matrix Shape |
| --- | --- |
| Baseline | `(600, 5000)` |
| DC | `(600, 3136)` |
| DCS | `(600, 2648)` |

## Dashboard

The Streamlit dashboard displays the generated charts:

- Clustering evaluation metrics
- Purity, F1, and entropy comparison
- NMI and ARI comparison
- Multi-metric radar chart
- Cluster size distribution
- PCA cluster visualization
- t-SNE visualization for DCS
- Feature dimensionality comparison
- Lexical chain statistics

## Repository Structure

```text
.
|-- app.py
|-- main.ipynb
|-- requirements.txt
|-- README.md
|-- Project Report.pdf
|-- wsd_docs.pkl
|-- chart_*.png
|-- dataset/
|   |-- list.csv
|   `-- *.txt
`-- paper/
    `-- DC with WordNet and Lexical Chain.pdf
```

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install the dashboard dependency:

```bash
pip install -r requirements.txt
```

To rerun the full notebook experiment, also install the research dependencies used in `main.ipynb`:

```bash
pip install numpy pandas matplotlib nltk scikit-learn scipy tqdm
```

The notebook uses NLTK resources such as WordNet, stopwords, tokenizers, and POS tagging data. If they are missing, download them inside Python or a notebook cell:

```python
import nltk

nltk.download("wordnet")
nltk.download("omw-1.4")
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
```

## Usage

Run the dashboard:

```bash
streamlit run app.py
```

Then open the local URL printed by Streamlit, usually:

```text
http://localhost:8501
```

To regenerate charts, open and run `main.ipynb`. The generated PNG files are saved in the repository root and loaded by `app.py`.

## Notes

- `wsd_docs.pkl` stores cached word-sense-disambiguated document data from the notebook run.
- Word-sense disambiguation and lexical-chain construction are computationally expensive, so the notebook limits the experiment to six categories and 600 documents.
- If a chart is missing, the dashboard will show a message asking you to rerun the visualization section of `main.ipynb`.

## References

The repository includes the source paper in `paper/DC with WordNet and Lexical Chain.pdf` and a project write-up in `Project Report.pdf`.
