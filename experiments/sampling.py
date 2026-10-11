from utils.common import *


def render():
    st.markdown(section_header("Sampling Techniques", "STEP 02"), unsafe_allow_html=True)

    if "numeric_df" not in st.session_state:
        st.warning("⚠️ Please load data first in the **📥 Data** tab.")
        st.stop()

    numeric_df = st.session_state["numeric_df"]

    # Method descriptions
    method_info = {
        "None (Full Dataset)": "Uses all available data with no sampling applied.",
        "Simple Random Sampling": "Each element has an equal probability of selection.",
        "Stratified Sampling": "Population divided into subgroups; samples taken from each.",
        "Cluster Sampling": "Population divided into clusters; entire clusters selected.",
        "Systematic Sampling": "Every k-th element selected from the population.",
        "Convenience Sampling": "Selects the most accessible elements (first N rows).",
        "Purposive Sampling": "Elements selected based on a specific criterion/threshold.",
        "Snowball Sampling": "Sequential chain sampling from a starting point.",
        "Quota Sampling": "Fixed quota of elements taken from each group.",
    }

    col_left, col_right = st.columns([2, 1])
    with col_left:
        method = st.selectbox("Sampling Method", list(method_info.keys()))
    with col_right:
        st.markdown(f"""
        <div style="background:{PALETTE['card2']};border:1px solid {PALETTE['border']};
                    border-radius:10px;padding:0.7rem 1rem;font-size:0.78rem;
                    color:{PALETTE['text2']};margin-top:1.6rem;line-height:1.5;">
          {method_info[method]}
        </div>
        """, unsafe_allow_html=True)

    sample_df = numeric_df.copy()

    if method == "Simple Random Sampling":
        frac = st.slider("Sample Fraction", 0.1, 1.0, 0.5, 0.05)
        sample_df = numeric_df.sample(frac=frac, random_state=42)

    elif method == "Stratified Sampling":
        col = st.selectbox("Stratify by", numeric_df.columns)
        frac_s = st.slider("Fraction per stratum", 0.1, 1.0, 0.5, 0.1)
        try:
            sample_df = numeric_df.groupby(col, group_keys=False).apply(
                lambda x: x.sample(frac=frac_s, random_state=42)
            )
        except Exception as e:
            st.warning(f"Column not suitable for stratified sampling: {e}")

    elif method == "Cluster Sampling":
        col = st.selectbox("Cluster Column", numeric_df.columns)
        val = st.selectbox("Select Cluster Value", sorted(numeric_df[col].unique()))
        sample_df = numeric_df[numeric_df[col] == val]

    elif method == "Systematic Sampling":
        step = st.slider("Step Size (k)", 2, 10, 3)
        sample_df = numeric_df.iloc[::step]

    elif method == "Convenience Sampling":
        n_conv = st.slider("Top-N Rows", 5, len(numeric_df), 20)
        sample_df = numeric_df.head(n_conv)

    elif method == "Purposive Sampling":
        col = st.selectbox("Filter Column", numeric_df.columns)
        threshold = st.slider(
            "Minimum Threshold",
            float(numeric_df[col].min()),
            float(numeric_df[col].max()),
            float(numeric_df[col].median())
        )
        sample_df = numeric_df[numeric_df[col] > threshold]

    elif method == "Snowball Sampling":
        start = st.slider("Start Index", 0, max(0, len(numeric_df) - 10), 0)
        size  = st.slider("Chain Size", 5, 30, 10)
        sample_df = numeric_df.iloc[start:start + size]

    elif method == "Quota Sampling":
        col   = st.selectbox("Group Column", numeric_df.columns)
        quota = st.slider("Rows per Group", 1, 10, 3)
        sample_df = numeric_df.groupby(col, group_keys=False).head(quota)

    st.session_state["sample_df"] = sample_df

    # Stats
    reduction = (1 - len(sample_df) / len(numeric_df)) * 100
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Original Rows", f"{len(numeric_df):,}")
    c2.metric("Sampled Rows", f"{len(sample_df):,}")
    c3.metric("Reduction", f"{reduction:.1f}%")
    c4.metric("Sample Ratio", f"{len(sample_df)/len(numeric_df):.1%}")

    st.markdown(section_header("Sampled Data Preview"), unsafe_allow_html=True)
    st.dataframe(sample_df.head(15), use_container_width=True)

    # Compare distributions
    if len(sample_df) > 0 and len(numeric_df.columns) > 0:
        st.markdown(section_header("Distribution Comparison"), unsafe_allow_html=True)
        compare_col = st.selectbox("Compare column", numeric_df.columns, key="samp_compare")
        fig_c, (ax_c1, ax_c2) = plt.subplots(1, 2, figsize=(12, 3.5))
        for ax_c, data, label, color in [
            (ax_c1, numeric_df[compare_col], "Full Dataset", PALETTE["accent"]),
            (ax_c2, sample_df[compare_col], f"Sample ({method.split()[0]})", PALETTE["accent3"])
        ]:
            ax_c.hist(data, bins=15, color=color, alpha=0.85, edgecolor=PALETTE["bg"], rwidth=0.9)
            ax_c.axvline(data.mean(), color=PALETTE["accent2"], linewidth=1.8, linestyle="--",
                         label=f"μ = {data.mean():.2f}")
            ax_c.set_title(label)
            ax_c.set_xlabel(compare_col)
            ax_c.legend(facecolor=PALETTE["card"], edgecolor=PALETTE["border"],
                        labelcolor=PALETTE["text"], fontsize=8)
            apply_chart_style(ax_c, fig_c)
        fig_c.tight_layout(pad=2)
        st.pyplot(fig_c, use_container_width=True)

