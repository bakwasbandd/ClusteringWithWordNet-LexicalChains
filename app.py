"""
streamlit dashboard for lexical-chain clustering visualizations.
run with: streamlit run app.py
"""

from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent

CHARTS = [
    {
        "id": "metrics_table",
        "file": "chart_metrics_table.png",
        "title": "clustering evaluation metrics",
        "section": "performance metrics",
        "description": (
            "summary table of purity, f1, entropy, nmi, and ari for baseline, "
            "dc (document chains), and dcs (document chains with selection). "
            "higher purity, f1, nmi, and ari indicate better alignment with true "
            "categories; lower entropy indicates more confident cluster assignments."
        ),
    },
    {
        "id": "purity_f1_entropy",
        "file": "chart_purity_f1_entropy.png",
        "title": "purity, f1, and entropy comparison",
        "section": "performance metrics",
        "description": (
            "side-by-side bar charts comparing the three systems on core clustering "
            "quality scores. purity measures dominant-class concentration per cluster, "
            "f1 balances precision and recall, and entropy captures assignment uncertainty."
        ),
    },
    {
        "id": "nmi_ari",
        "file": "chart_nmi_ari.png",
        "title": "nmi and ari comparison",
        "section": "performance metrics",
        "description": (
            "bar charts for normalized mutual information (nmi) and adjusted rand "
            "index (ari). both metrics compare predicted clusters against ground-truth "
            "labels and reward partitions that recover the true document groupings."
        ),
    },
    {
        "id": "radar",
        "file": "chart_radar.png",
        "title": "multi-metric radar chart",
        "section": "performance metrics",
        "description": (
            "radar plot overlaying all five evaluation metrics for each system on one "
            "view. entropy is inverted so every axis follows a higher-is-better scale, "
            "making it easy to compare overall clustering strength at a glance."
        ),
    },
    {
        "id": "cluster_sizes",
        "file": "chart_cluster_sizes.png",
        "title": "cluster size distribution",
        "section": "cluster structure",
        "description": (
            "document counts per cluster for baseline, dc, and dcs. the dashed red "
            "line marks the ideal balanced size if documents were evenly split across "
            "six clusters, helping spot over- or under-populated clusters."
        ),
    },
    {
        "id": "pca",
        "file": "chart_pca.png",
        "title": "pca cluster visualization",
        "section": "dimensionality projections",
        "description": (
            "two-dimensional pca projections of each system's feature space, with "
            "points colored by predicted cluster. shows how well-separated clusters "
            "appear in reduced space for baseline tf-idf, chain-based dc, and dcs features."
        ),
    },
    {
        "id": "tsne",
        "file": "chart_tsne_dcs.png",
        "title": "t-sne visualization (dcs)",
        "section": "dimensionality projections",
        "description": (
            "t-sne embedding of dcs features. the left panel colors documents by "
            "predicted cluster; the right panel colors them by true newsgroup category, "
            "revealing how closely unsupervised clusters match ground-truth topics."
        ),
    },
    {
        "id": "features",
        "file": "chart_features.png",
        "title": "feature dimensionality",
        "section": "feature analysis",
        "description": (
            "number of tf-idf features retained by each pipeline stage. lexical-chain "
            "filtering in dc and dcs reduces vocabulary size compared to the baseline, "
            "with percentage reductions annotated on the bars."
        ),
    },
    {
        "id": "chain_stats",
        "file": "chart_chain_stats.png",
        "title": "lexical chain statistics",
        "section": "feature analysis",
        "description": (
            "left: distribution of lexical chain lengths across all documents, with "
            "singleton chains highlighted. right: average number of chains extracted "
            "per document broken down by newsgroup category."
        ),
    },
]

SECTION_ORDER = [
    "performance metrics",
    "cluster structure",
    "dimensionality projections",
    "feature analysis",
]

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap');

    .stApp {
        background: linear-gradient(165deg, #0c1f1c 0%, #122a26 45%, #0f2420 100%);
        color: #e8f0ed;
        font-family: 'DM Sans', sans-serif;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1816 0%, #102420 100%);
        border-right: 1px solid #2a5c52;
    }

    [data-testid="stSidebar"] * {
        color: #d4e8e2 !important;
    }

    .title-block {
        background: linear-gradient(135deg, #152e29 0%, #1a3d36 100%);
        border: 1px solid #3d7a6d;
        border-left: 4px solid #e07a5f;
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin: 0 0 2.5rem 0;
        box-shadow: 0 6px 28px rgba(0, 0, 0, 0.22);
    }

    .app-title {
        font-size: 2.1rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
        line-height: 1.25;
    }

    .title-main {
        color: #f5faf8;
    }

    .title-accent {
        color: #7ec8b8;
    }

    .title-divider {
        width: 72px;
        height: 3px;
        background: linear-gradient(90deg, #e07a5f 0%, #7ec8b8 100%);
        border-radius: 2px;
        margin-top: 0.85rem;
    }

    .chart-spacer {
        height: 3rem;
        margin-bottom: 0.5rem;
        border-bottom: 1px solid #1f4a42;
    }

    div[data-testid="stImage"] {
        margin-top: 1.25rem;
        margin-bottom: 0.25rem;
        padding: 0.85rem;
        background: #0f2420;
        border: 1px solid #2a5c52;
        border-radius: 10px;
    }

    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e07a5f;
    }

    .section-header h2 {
        margin: 0;
        font-size: 1.35rem;
        font-weight: 700;
        color: #f0c9a8;
        text-transform: lowercase;
        letter-spacing: 0.01em;
    }

    .chart-card {
        background: #152e29;
        border: 1px solid #2f5f55;
        border-radius: 14px;
        padding: 1.25rem 1.5rem 1.5rem 1.5rem;
        margin-bottom: 0;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    }

    .chart-card h3 {
        margin: 0 0 0.65rem 0;
        font-size: 1.1rem;
        font-weight: 600;
        color: #7ec8b8;
    }

    .chart-card p {
        margin: 0 0 1rem 0;
        color: #a8c4bc;
        font-size: 0.95rem;
        line-height: 1.55;
    }

    .tag-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin-top: 0.75rem;
    }

    .tag {
        background: #1f4a42;
        color: #c5e8df;
        border: 1px solid #3d7a6d;
        border-radius: 999px;
        padding: 0.2rem 0.7rem;
        font-size: 0.78rem;
        font-family: 'JetBrains Mono', monospace;
    }

    .missing-banner {
        background: #3d2a1f;
        border: 1px solid #e07a5f;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        color: #f5d5c0;
        margin-bottom: 1rem;
    }

    .stButton > button {
        background: linear-gradient(135deg, #e07a5f 0%, #c96a52 100%);
        color: #1a120e;
        border: none;
        border-radius: 10px;
        font-weight: 600;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #eba88f 0%, #e07a5f 100%);
        color: #1a120e;
    }

    #MainMenu, footer, header { visibility: hidden; }
</style>
"""


def chart_path(filename: str) -> Path:
    return BASE_DIR / filename


def render_chart_card(chart: dict) -> None:
    path = chart_path(chart["file"])
    st.markdown(
        f"""
        <div class="chart-card">
            <h3>{chart["title"]}</h3>
            <p>{chart["description"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if path.exists():
        st.image(str(path), use_container_width=True)
    else:
        st.markdown(
            f"""
            <div class="missing-banner">
                chart not found: <code>{chart["file"]}</code>.
                run section 15 in <code>main.ipynb</code> to generate it.
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown('<div class="chart-spacer"></div>', unsafe_allow_html=True)


def main() -> None:
    st.set_page_config(
        page_title="ClusteringWithWordNet-LexicalChains",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="title-block">
            <h1 class="app-title">
                <span class="title-main">ClusteringWithWordNet</span><span class="title-accent">-LexicalChains</span>
            </h1>
            <div class="title-divider"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown("### navigation")
        view = st.radio(
            "show",
            ["all charts", "by section"],
            label_visibility="collapsed",
        )
        st.markdown("---")
        st.markdown("### systems compared")
        st.markdown(
            "- **baseline** — standard tf-idf + k-means\n"
            "- **dc** — document chains\n"
            "- **dcs** — document chains with selection"
        )
    if view == "all charts":
        for chart in CHARTS:
            render_chart_card(chart)
    else:
        for section in SECTION_ORDER:
            section_charts = [c for c in CHARTS if c["section"] == section]
            if not section_charts:
                continue
            st.markdown(
                f'<div class="section-header"><h2>{section}</h2></div>',
                unsafe_allow_html=True,
            )
            for chart in section_charts:
                render_chart_card(chart)

    st.markdown(
        """
        <div class="tag-row">
            <span class="tag">wordnet</span>
            <span class="tag">lexical chains</span>
            <span class="tag">k-means</span>
            <span class="tag">20 newsgroups</span>
            <span class="tag">tf-idf</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
