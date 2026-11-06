
import streamlit as st
import pandas as pd
import sqlite3
import json

from src.data_cleaning import extract_keywords


# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="TrendSphere AI | Intelligence",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# 2. PREMIUM CUSTOM CSS
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #080D1B;
    --surface: #111B30;
    --border: #253550;
    --text: #F1F5F9;
    --muted: #94A3B8;
    --cyan: #38BDF8;
    --purple: #A78BFA;
}

.stApp {
    background:
        radial-gradient(ellipse at 5% 0%, #172554 0%, transparent 35%),
        radial-gradient(ellipse at 95% 5%, #312E81 0%, transparent 30%),
        var(--bg);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: var(--text) !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px;
}

p, label {
    color: #CBD5E1;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111B30, #0B1120);
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: white !important;
}

[data-testid="stMetric"] {
    background: linear-gradient(
        140deg,
        rgba(30, 58, 138, 0.35),
        rgba(49, 46, 129, 0.20)
    );
    border: 1px solid rgba(96, 165, 250, 0.25);
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.20);
    transition: 0.25s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    border-color: var(--cyan);
}

[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
}

[data-testid="stMetricValue"] {
    color: var(--cyan) !important;
    font-weight: 800 !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(17, 27, 48, 0.75);
    border: 1px solid var(--border);
    border-radius: 15px;
}

.stTextInput input,
.stDateInput input {
    background: #111B30;
    color: white;
    border: 1px solid #334155;
    border-radius: 9px;
}

.stMultiSelect [data-baseweb="select"],
.stSelectbox [data-baseweb="select"] {
    background: #111B30;
    border-radius: 9px;
}

.stDownloadButton button,
.stButton button {
    background: linear-gradient(90deg, #2563EB, #7C3AED);
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: 700;
    transition: 0.25s ease;
}

.stDownloadButton button:hover,
.stButton button:hover {
    box-shadow: 0 5px 22px rgba(99,102,241,0.35);
    color: white;
    border: none;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 12px;
}

hr {
    border-color: var(--border) !important;
}

a {
    color: var(--cyan) !important;
    text-decoration: none;
}

a:hover {
    color: var(--purple) !important;
}

.hero {
    padding: 30px;
    border-radius: 20px;
    border: 1px solid rgba(96,165,250,0.30);
    background: linear-gradient(
        115deg,
        rgba(30,64,175,0.35),
        rgba(91,33,182,0.22),
        rgba(15,23,42,0.85)
    );
    margin-bottom: 25px;
}

.hero-tag {
    color: #38BDF8;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 3px;
}

.hero-title {
    color: #F8FAFC;
    font-size: 38px;
    font-weight: 800;
    margin: 12px 0;
}

.hero-description {
    color: #CBD5E1;
    font-size: 14px;
}

.news-card {
    padding: 18px;
    border-radius: 13px;
    border: 1px solid #263653;
    background: rgba(17,27,48,0.78);
    margin-bottom: 12px;
    transition: 0.2s ease;
}

.news-card:hover {
    border-color: #38BDF8;
    transform: translateY(-2px);
}

.news-title {
    color: #F8FAFC;
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 10px;
}

.news-meta {
    color: #94A3B8;
    font-size: 12px;
}

.section-label {
    color: #38BDF8;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
}

#MainMenu, footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. DATABASE LOADING
# =====================================================

@st.cache_data(ttl=60)
def load_data():

    connection = sqlite3.connect("database/news.db")

    try:
        data = pd.read_sql_query(
            "SELECT * FROM articles",
            connection
        )
    finally:
        connection.close()

    return data


try:
    df = load_data()

except Exception as error:

    st.error(f"Database loading failed: {error}")

    st.info(
        "Please run python app.py first to create and populate the database."
    )

    st.stop()


if df.empty:

    st.warning("No news articles found in the database.")

    st.stop()


# =====================================================
# 4. DATA PREPARATION
# =====================================================

required_columns = ["source", "title", "link", "published"]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:

    st.error(f"Missing database columns: {missing_columns}")

    st.stop()


df = df.dropna(
    subset=["source", "title", "link"]
).copy()

df["published_date"] = pd.to_datetime(
    df["published"],
    errors="coerce",
    utc=True
)

if "summary" not in df.columns:
    df["summary"] = ""

df["summary"] = df["summary"].fillna("")


# =====================================================
# 5. SIDEBAR NAVIGATION
# =====================================================

with st.sidebar:

    st.markdown("# ✧ TrendSphere AI")
    st.caption("TECHNOLOGY INTELLIGENCE")

    st.markdown("---")

    page = st.radio(
        "NAVIGATION",
        [
            "Executive Overview",
            "News Explorer",
            "Keyword Intelligence",
            "Data & Downloads"
        ],
        index=0
    )

    st.markdown("---")

    st.markdown("### DATA CONTROLS")

    search_text = st.text_input(
        "Search Articles",
        placeholder="Search AI, Python, Cloud..."
    )

    sources = sorted(
        df["source"].dropna().unique().tolist()
    )

    selected_sources = st.multiselect(
        "News Sources",
        options=sources,
        default=sources
    )

    st.markdown("---")

    if st.button("🔄 Refresh Database", use_container_width=True):

        load_data.clear()

        st.rerun()

    st.caption("Data sources: TechCrunch & The Verge RSS")

    st.caption("TrendSphere AI | Version 3.0")


# =====================================================
# 6. GLOBAL FILTERING
# =====================================================

filtered_df = df[
    df["source"].isin(selected_sources)
].copy()

if search_text:

    search_mask = (
        filtered_df["title"].str.contains(
            search_text,
            case=False,
            na=False
        )
        |
        filtered_df["summary"].str.contains(
            search_text,
            case=False,
            na=False
        )
    )

    filtered_df = filtered_df[search_mask].copy()



# =====================================================
# 7. PREMIUM ANIMATED HEADER
# =====================================================

st.html("""
<style>

.ts-hero {
    position: relative;
    overflow: hidden;
    padding: 38px;
    border-radius: 22px;
    border: 1px solid rgba(56,189,248,0.25);
    background: linear-gradient(
        120deg,
        #101D3A,
        #17183D,
        #10172B
    );
    margin-bottom: 30px;
}

.ts-orbit {
    position: absolute;
    right: 75px;
    top: 30px;
    width: 105px;
    height: 105px;
    border: 2px solid rgba(56,189,248,0.35);
    border-radius: 50%;
    animation: orbit 8s linear infinite;
}

.ts-orbit::before {
    content: "";
    position: absolute;
    inset: 13px;
    border: 2px solid rgba(167,139,250,0.6);
    border-radius: 50%;
}

.ts-orbit::after {
    content: "✦";
    position: absolute;
    top: -10px;
    right: 12px;
    color: #38BDF8;
    font-size: 25px;
    animation: sparkle 2s ease-in-out infinite;
}

.ts-logo {
    font-size: 44px;
    display: inline-block;
    color: #38BDF8;
    animation: float 3s ease-in-out infinite;
    text-shadow: 0 0 22px rgba(56,189,248,0.65);
}

.ts-tag {
    color: #38BDF8;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 3px;
    margin-top: 15px;
}

.ts-title {
    font-size: 39px;
    font-weight: 800;
    color: #F8FAFC;
    margin: 10px 0;
    letter-spacing: -1px;
}

.ts-subtitle {
    color: #C4B5FD;
    font-size: 17px;
    font-weight: 600;
}

.ts-description {
    color: #94A3B8;
    font-size: 14px;
    margin-top: 12px;
}

@keyframes orbit {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-9px); }
}

@keyframes sparkle {
    0%, 100% { opacity: 0.4; transform: scale(0.8); }
    50% { opacity: 1; transform: scale(1.3); }
}

</style>

<div class="ts-hero">

    <div class="ts-orbit"></div>

    <div class="ts-logo">✧</div>

    <div class="ts-tag">
        TECHNOLOGY • AI • INNOVATION
    </div>

    <div class="ts-title">
        TrendSphere AI
    </div>

    <div class="ts-subtitle">
        Technology & Innovation Intelligence Platform
    </div>

    <div class="ts-description">
        Discover emerging technologies, explore AI innovations,
        analyze industry signals and identify future opportunities.
    </div>

</div>
""")

# =====================================================
# 8. EXECUTIVE OVERVIEW
# =====================================================

if page == "Executive Overview":

    st.markdown(
        '<div class="section-label">OVERVIEW / ANALYTICS</div>',
        unsafe_allow_html=True
    )

    st.title("Executive Overview")

    st.caption(
        "A consolidated view of collected technology news."
    )

    total_articles = len(filtered_df)

    total_sources = filtered_df["source"].nunique()

    techcrunch_count = (
        filtered_df["source"] == "TechCrunch"
    ).sum()

    verge_count = (
        filtered_df["source"] == "The Verge"
    ).sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Articles",
        total_articles
    )

    col2.metric(
        "News Sources",
        total_sources
    )

    col3.metric(
        "TechCrunch",
        techcrunch_count
    )

    col4.metric(
        "The Verge",
        verge_count
    )

    st.markdown("---")

    # Analytics charts

    left_col, right_col = st.columns(2)

    with left_col:

        st.subheader("📰 Source Distribution")

        source_counts = (
            filtered_df["source"].value_counts()
        )

        if not source_counts.empty:

            st.bar_chart(source_counts)

        else:

            st.info("No source data available.")

    with right_col:

        st.subheader("🔥 Top Technology Keywords")

        if not filtered_df.empty:

            keywords = extract_keywords(filtered_df)

            keyword_df = pd.DataFrame(
                keywords,
                columns=["Keyword", "Frequency"]
            )

            if not keyword_df.empty:

                st.bar_chart(
                    keyword_df.set_index("Keyword")
                )

            else:

                st.info("No keywords found.")

        else:

            st.info("No data available.")

    st.markdown("---")

    st.subheader("🚀 Latest Technology Updates")

    latest_news = filtered_df.sort_values(
        "published_date",
        ascending=False,
        na_position="last"
    )

    for _, article in latest_news.head(5).iterrows():

        with st.container(border=True):

            st.markdown(
                f"**{article['title']}**"
            )

            st.caption(
                f"{article['source']} | {article['published']}"
            )

            st.markdown(
                f"[Read Full Article]({article['link']})"
            )


# =====================================================
# 9. NEWS EXPLORER
# =====================================================

elif page == "News Explorer":

    st.markdown(
        '<div class="section-label">INTELLIGENCE / NEWS</div>',
        unsafe_allow_html=True
    )

    st.title("News Explorer")

    st.caption(
        "Search, filter and explore collected technology articles."
    )

    st.metric(
        "Matching Articles",
        len(filtered_df)
    )

    if not filtered_df.empty:

        display_df = filtered_df.copy()

        display_df.insert(
            0,
            "Article No.",
            range(1, len(display_df) + 1)
        )

        display_columns = [
            "Article No.",
            "source",
            "title",
            "published",
            "link",
            "summary"
        ]

        display_df = display_df[
            [
                column for column in display_columns
                if column in display_df.columns
            ]
        ]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No articles match the selected filters.")


# =====================================================
# 10. KEYWORD INTELLIGENCE
# =====================================================

elif page == "Keyword Intelligence":

    st.markdown(
        '<div class="section-label">INTELLIGENCE / KEYWORDS</div>',
        unsafe_allow_html=True
    )

    st.title("Keyword Intelligence")

    st.caption(
        "Explore frequently mentioned terms in article titles."
    )

    if not filtered_df.empty:

        keywords = extract_keywords(filtered_df)

        keyword_df = pd.DataFrame(
            keywords,
            columns=["Keyword", "Frequency"]
        )

        if not keyword_df.empty:

            col1, col2 = st.columns(2)

            with col1:

                st.subheader("Top 10 Keywords")

                st.bar_chart(
                    keyword_df.set_index("Keyword")
                )

            with col2:

                st.subheader("Keyword Data")

                st.dataframe(
                    keyword_df,
                    use_container_width=True,
                    hide_index=True
                )

            st.info(
                "These values represent title keyword frequency, "
                "not verified market growth or time-based trends."
            )

        else:

            st.info("No keywords available.")

    else:

        st.warning("No matching articles available.")


# =====================================================
# 11. DATA & DOWNLOADS
# =====================================================

elif page == "Data & Downloads":

    st.markdown(
        '<div class="section-label">INTELLIGENCE / EXPORTS</div>',
        unsafe_allow_html=True
    )

    st.title("Data & Downloads")

    st.caption(
        "Export the currently filtered news dataset."
    )

    st.metric(
        "Records Available for Export",
        len(filtered_df)
    )

    if not filtered_df.empty:

        csv_data = filtered_df.to_csv(
            index=False
        ).encode("utf-8-sig")

        json_data = filtered_df.to_json(
            orient="records",
            indent=4,
            force_ascii=False,
            date_format="iso"
        ).encode("utf-8")

        col1, col2 = st.columns(2)

        with col1:

            st.download_button(
                label="⬇ Download CSV",
                data=csv_data,
                file_name="webtrend_atlas_news.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col2:

            st.download_button(
                label="⬇ Download JSON",
                data=json_data,
                file_name="webtrend_atlas_news.json",
                mime="application/json",
                use_container_width=True
            )

        st.markdown("---")

        st.subheader("Export Preview")

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "No records available to export."
        )


# =====================================================
# 12. FOOTER
# =====================================================

st.markdown("---")

st.markdown("""
<div style="
    text-align:center;
    padding:15px;
    color:#64748B;
    font-size:12px;
">
    WEBTREND ATLAS · AI & TECHNOLOGY INTELLIGENCE PLATFORM
    <br>
    Built with Python · Pandas · SQLite · Streamlit
</div>
""", unsafe_allow_html=True)
