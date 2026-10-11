from utils.common import *


def render():
    st.markdown(section_header("Correlation Analysis", "STEP 04"), unsafe_allow_html=True)

    if "numeric_df" not in st.session_state:
        st.warning("⚠️ Please load data first in the **📥 Data** tab.")
        st.stop()

    numeric_df = st.session_state["numeric_df"]
    sample_df  = st.session_state.get("sample_df", numeric_df)

    corr_method = st.radio("Correlation Method", ["Pearson", "Spearman", "Kendall"],
                            horizontal=True)
    corr = sample_df.corr(method=corr_method.lower())

    tab_a, tab_b, tab_c = st.tabs(["🌡 Heatmap", "📋 Table & Partial Corr", "🏆 Top Correlations"])

    with tab_a:
        fig4, ax4 = plt.subplots(figsize=(9, 6.5))
        mask = np.triu(np.ones_like(corr, dtype=bool))
        cmap = sns.diverging_palette(220, 10, as_cmap=True)
        sns.heatmap(
            corr, mask=mask, annot=True, fmt=".2f", cmap=cmap,
            ax=ax4, linewidths=0.6, linecolor=PALETTE["border"],
            annot_kws={"size": 9, "color": PALETTE["text"], "weight": "500"},
            cbar_kws={"shrink": 0.75, "pad": 0.02},
            vmin=-1, vmax=1, center=0,
            square=True
        )
        ax4.set_title(f"{corr_method} Correlation Heatmap", pad=14)
        apply_chart_style(ax4, fig4)
        ax4.tick_params(axis="x", rotation=35, labelsize=8)
        ax4.tick_params(axis="y", rotation=0, labelsize=8)
        fig4.tight_layout()
        st.pyplot(fig4, use_container_width=True)

    with tab_b:
        st.dataframe(
            corr.style
            .background_gradient(cmap="RdBu_r", vmin=-1, vmax=1)
            .format("{:.3f}")
            .highlight_between(left=-1, right=-0.5, color="#f8717140")
            .highlight_between(left=0.5, right=1, color="#34d39940"),
            use_container_width=True
        )

        if len(sample_df.columns) >= 3:
            st.markdown(section_header("Partial Correlation"), unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            col_x = c1.selectbox("Variable X", numeric_df.columns, key="pc_x")
            col_y = c2.selectbox("Variable Y", numeric_df.columns,
                                  index=min(1, len(numeric_df.columns)-1), key="pc_y")
            col_z = c3.selectbox("Control for Z", numeric_df.columns,
                                  index=min(2, len(numeric_df.columns)-1), key="pc_z")

            x_s, y_s, z_s = sample_df[col_x], sample_df[col_y], sample_df[col_z]
            r_xy = np.corrcoef(x_s, y_s)[0, 1]
            r_xz = np.corrcoef(x_s, z_s)[0, 1]
            r_yz = np.corrcoef(y_s, z_s)[0, 1]
            denom = np.sqrt((1 - r_xz**2) * (1 - r_yz**2))
            partial = (r_xy - r_xz * r_yz) / denom if denom != 0 else np.nan

            st.markdown(f"""
            <div class="result-box">
              <div class="result-grid">
                <div class="result-item">
                  <div class="result-key">Raw Corr ({col_x} & {col_y})</div>
                  <div class="result-val blue">{r_xy:.4f}</div>
                </div>
                <div class="result-item">
                  <div class="result-key">Partial Corr | controlling {col_z}</div>
                  <div class="result-val {'green' if abs(partial) < abs(r_xy) else ''}">{partial:.4f}</div>
                </div>
                <div class="result-item">
                  <div class="result-key">Change</div>
                  <div class="result-val">{partial - r_xy:+.4f}</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(insight(
                f"Controlling for <strong>{col_z}</strong>, the correlation between "
                f"<strong>{col_x}</strong> and <strong>{col_y}</strong> changes from "
                f"<strong>{r_xy:.3f}</strong> to <strong>{partial:.3f}</strong> "
                f"({'decreases' if abs(partial) < abs(r_xy) else 'increases'}), suggesting "
                f"that {col_z} {'partially explains' if abs(partial) < abs(r_xy) else 'does not explain'} "
                f"the relationship."
            ), unsafe_allow_html=True)

    with tab_c:
        # Top correlations table
        corr_pairs = []
        for i in range(len(corr.columns)):
            for j in range(i + 1, len(corr.columns)):
                corr_pairs.append({
                    "Feature A": corr.columns[i],
                    "Feature B": corr.columns[j],
                    "Correlation": corr.iloc[i, j],
                    "Abs": abs(corr.iloc[i, j])
                })
        corr_pairs_df = pd.DataFrame(corr_pairs).sort_values("Abs", ascending=False).drop("Abs", axis=1)
        st.dataframe(
            corr_pairs_df.style
            .bar(subset=["Correlation"], color=[PALETTE["danger"] + "80", PALETTE["accent3"] + "80"])
            .format({"Correlation": "{:.4f}"}),
            use_container_width=True
        )

        # Bar chart of top 10
        top10 = corr_pairs_df.head(10).copy()
        top10["pair"] = top10["Feature A"] + " — " + top10["Feature B"]
        colors_bar = [PALETTE["accent3"] if v > 0 else PALETTE["danger"] for v in top10["Correlation"]]

        fig_tc, ax_tc = plt.subplots(figsize=(10, 4))
        bars = ax_tc.barh(top10["pair"], top10["Correlation"], color=colors_bar,
                           edgecolor=PALETTE["border"], height=0.6, alpha=0.85)
        ax_tc.axvline(0, color=PALETTE["muted"], linewidth=1, linestyle="--")
        ax_tc.set_xlabel("Correlation Coefficient")
        ax_tc.set_title("Top Feature Pair Correlations")
        apply_chart_style(ax_tc, fig_tc)
        fig_tc.tight_layout()
        st.pyplot(fig_tc, use_container_width=True)

