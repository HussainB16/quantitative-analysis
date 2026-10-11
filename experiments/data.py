from utils.common import *


def render():
    st.markdown(section_header("Data Collection & Preview", "STEP 01"), unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Drop your CSV file here", type=["csv"],
                                      help="Upload any CSV with numeric columns for analysis.")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Loaded **{uploaded_file.name}** — {len(df):,} rows, {len(df.columns)} columns")
    else:
        st.markdown(f"""
        <div class="info-banner">
          ℹ️ No file uploaded — using a synthetic student dataset (n=80) with StudyHours, Sleep, Attendance, ScreenTime, and Marks.
        </div>
        """, unsafe_allow_html=True)
        np.random.seed(42)
        n = 80
        study = np.random.randint(1, 10, n)
        sleep = np.random.randint(4, 10, n)
        attend = np.random.randint(50, 100, n)
        screen = np.random.randint(1, 8, n)
        df = pd.DataFrame({
            "StudyHours": study,
            "Sleep":      sleep,
            "Attendance": attend,
            "ScreenTime": screen,
            "Marks":      np.clip(study * 5 + attend * 0.2 + np.random.randint(20, 40, n), 40, 100).astype(int),
        })

    df = pd.get_dummies(df, drop_first=True)
    numeric_df = df.select_dtypes(include=np.number)
    st.session_state["df"] = df
    st.session_state["numeric_df"] = numeric_df

    # KPI cards
    color_cycle = ["blue", "pink", "green", "yellow", "purple"]
    icons = ["📚", "😴", "🏫", "📱", "🎯"]
    cols_stat = numeric_df.columns.tolist()[:5]

    cards_html = '<div class="kpi-grid">'
    for i, c in enumerate(cols_stat):
        col_data = numeric_df[c]
        pct_change = f"σ = {col_data.std():.1f}"
        cards_html += kpi_card(
            f"{col_data.mean():.1f}",
            f"avg {c}",
            icon=icons[i] if i < len(icons) else "📊",
            sub=pct_change,
            color=color_cycle[i % len(color_cycle)]
        )
    cards_html += "</div>"
    st.markdown(cards_html, unsafe_allow_html=True)

    # Quick stats row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Records", f"{len(numeric_df):,}")
    col2.metric("Features", f"{len(numeric_df.columns)}")
    col3.metric("Missing Values", f"{numeric_df.isnull().sum().sum()}")
    col4.metric("Data Quality", "100%" if numeric_df.isnull().sum().sum() == 0 else f"{(1 - numeric_df.isnull().mean().mean()):.0%}")

    st.markdown(section_header("Preview"), unsafe_allow_html=True)
    st.dataframe(numeric_df.head(10), use_container_width=True)

    st.markdown(section_header("Descriptive Statistics"), unsafe_allow_html=True)
    desc = numeric_df.describe().T
    desc.columns = [c.title() for c in desc.columns]
    st.dataframe(desc.style.background_gradient(cmap="Blues", subset=["Mean", "Std"]).format("{:.2f}"),
                 use_container_width=True)

    # Insight
    top_col = numeric_df.mean().idxmax()
    st.markdown(insight(
        f"The dataset contains <strong>{len(numeric_df):,} student records</strong> with "
        f"<strong>{len(numeric_df.columns)} numeric features</strong>. "
        f"<strong>{top_col}</strong> has the highest average value ({numeric_df[top_col].mean():.1f}). "
        f"All features are complete with no missing values."
    ), unsafe_allow_html=True)

