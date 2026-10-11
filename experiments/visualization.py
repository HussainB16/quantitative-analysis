from utils.common import *


def render():
    st.markdown(section_header("Data Visualization", "STEP 03"), unsafe_allow_html=True)

    if "numeric_df" not in st.session_state:
        st.warning("⚠️ Please load data first in the **📥 Data** tab.")
        st.stop()

    numeric_df = st.session_state["numeric_df"]
    sample_df  = st.session_state.get("sample_df", numeric_df)

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Histogram", "🔵 Scatter", "📦 Box Plot", "📉 Pair Plot"])

    with tab1:
        c1, c2, c3 = st.columns([2, 1, 1])
        col1 = c1.selectbox("Column", numeric_df.columns, key="hist_col")
        bins = c2.slider("Bins", 5, 50, 15)
        show_kde = c3.checkbox("Show KDE", value=True)

        fig, ax = plt.subplots(figsize=(10, 4.5))
        n_vals, bin_edges, patches = ax.hist(
            sample_df[col1], bins=bins,
            color=PALETTE["accent"], edgecolor=PALETTE["bg"], alpha=0.8, rwidth=0.88
        )
        # Color gradient on bars
        norm = plt.Normalize(n_vals.min(), n_vals.max())
        for patch, val in zip(patches, n_vals):
            patch.set_facecolor(plt.cm.Blues(0.3 + 0.6 * norm(val)))

        if show_kde:
            kde_xs = np.linspace(sample_df[col1].min(), sample_df[col1].max(), 300)
            kde = stats.gaussian_kde(sample_df[col1].dropna())
            ax2_twin = ax.twinx()
            ax2_twin.plot(kde_xs, kde(kde_xs), color=PALETTE["accent2"], linewidth=2.5, label="KDE")
            ax2_twin.set_facecolor("none")
            ax2_twin.tick_params(colors=PALETTE["muted"], labelsize=8)
            ax2_twin.yaxis.label.set_color(PALETTE["muted"])
            ax2_twin.set_ylabel("Density", fontsize=9)
            for spine in ax2_twin.spines.values():
                spine.set_color(PALETTE["border2"])

        ax.axvline(sample_df[col1].mean(), color=PALETTE["accent3"], linewidth=2,
                   linestyle="--", label=f"Mean: {sample_df[col1].mean():.2f}")
        ax.axvline(sample_df[col1].median(), color=PALETTE["accent4"], linewidth=2,
                   linestyle=":", label=f"Median: {sample_df[col1].median():.2f}")
        ax.set_xlabel(col1); ax.set_ylabel("Frequency")
        ax.set_title(f"Distribution of {col1}")
        ax.legend(facecolor=PALETTE["card"], edgecolor=PALETTE["border"],
                  labelcolor=PALETTE["text"], fontsize=8)
        apply_chart_style(ax, fig)
        st.pyplot(fig, use_container_width=True)

        # Stats summary
        col_data = sample_df[col1]
        sk, ku = stats.skew(col_data.dropna()), stats.kurtosis(col_data.dropna())
        st.markdown(f"""
        <div class="result-box">
          <div class="result-grid">
            <div class="result-item"><div class="result-key">Mean</div><div class="result-val blue">{col_data.mean():.3f}</div></div>
            <div class="result-item"><div class="result-key">Median</div><div class="result-val blue">{col_data.median():.3f}</div></div>
            <div class="result-item"><div class="result-key">Std Dev</div><div class="result-val">{col_data.std():.3f}</div></div>
            <div class="result-item"><div class="result-key">Skewness</div><div class="result-val {'green' if abs(sk)<0.5 else ''}">{sk:.3f}</div></div>
            <div class="result-item"><div class="result-key">Kurtosis</div><div class="result-val">{ku:.3f}</div></div>
            <div class="result-item"><div class="result-key">Range</div><div class="result-val">{col_data.max()-col_data.min():.2f}</div></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        c1, c2, c3 = st.columns(3)
        x_col = c1.selectbox("X-axis", numeric_df.columns, key="sc_x")
        y_col = c2.selectbox("Y-axis", numeric_df.columns, key="sc_y",
                              index=min(1, len(numeric_df.columns) - 1))
        color_col = c3.selectbox("Color by", ["None"] + numeric_df.columns.tolist(), key="sc_c")

        fig2, ax2 = plt.subplots(figsize=(10, 5))
        c_data = sample_df[color_col] if color_col != "None" else sample_df[y_col]
        sc = ax2.scatter(sample_df[x_col], sample_df[y_col],
                         c=c_data, cmap="plasma",
                         edgecolors=PALETTE["border2"], s=65, alpha=0.8, linewidths=0.5)
        cbar = plt.colorbar(sc, ax=ax2)
        cbar.ax.tick_params(colors=PALETTE["muted"], labelsize=8)
        cbar.set_label(color_col if color_col != "None" else y_col,
                       color=PALETTE["muted"], fontsize=9)

        # Trend line
        from numpy.polynomial import polynomial as P
        mask = sample_df[[x_col, y_col]].dropna().index
        xs_t = sample_df.loc[mask, x_col].values
        ys_t = sample_df.loc[mask, y_col].values
        if len(xs_t) > 2:
            z = np.polyfit(xs_t, ys_t, 1)
            p = np.poly1d(z)
            xs_line = np.linspace(xs_t.min(), xs_t.max(), 100)
            ax2.plot(xs_line, p(xs_line), color=PALETTE["accent2"], linewidth=2,
                     linestyle="--", alpha=0.8, label="Trend")
            ax2.legend(facecolor=PALETTE["card"], edgecolor=PALETTE["border"],
                       labelcolor=PALETTE["text"], fontsize=8)

        ax2.set_xlabel(x_col); ax2.set_ylabel(y_col)
        ax2.set_title(f"{x_col} vs {y_col}")
        apply_chart_style_clean(ax2, fig2)
        st.pyplot(fig2, use_container_width=True)

        # Correlation info
        r, p_val = stats.pearsonr(
            sample_df[[x_col, y_col]].dropna()[x_col],
            sample_df[[x_col, y_col]].dropna()[y_col]
        )
        st.markdown(f"""
        <div class="result-box">
          <div class="result-grid">
            <div class="result-item"><div class="result-key">Pearson r</div><div class="result-val {'green' if abs(r)>0.5 else 'blue'}">{r:.4f}</div></div>
            <div class="result-item"><div class="result-key">p-value</div><div class="result-val {'green' if p_val<0.05 else ''}">{p_val:.4f}</div></div>
            <div class="result-item"><div class="result-key">R² (linear)</div><div class="result-val">{r**2:.4f}</div></div>
            <div class="result-item"><div class="result-key">Strength</div><div class="result-val">{'Strong' if abs(r)>0.7 else 'Moderate' if abs(r)>0.4 else 'Weak'}</div></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        cols_bp = st.multiselect("Select columns to compare",
                                  numeric_df.columns.tolist(),
                                  default=numeric_df.columns.tolist()[:4])
        if cols_bp:
            fig3, ax3 = plt.subplots(figsize=(10, 4.5))
            bp = ax3.boxplot(
                [sample_df[c].dropna() for c in cols_bp],
                labels=cols_bp,
                patch_artist=True,
                notch=False,
                medianprops=dict(color=PALETTE["text"], linewidth=2.5),
                whiskerprops=dict(color=PALETTE["muted"], linewidth=1.2),
                capprops=dict(color=PALETTE["muted"], linewidth=1.5),
                flierprops=dict(markerfacecolor=PALETTE["accent2"], marker="o",
                                alpha=0.5, markersize=5, markeredgecolor="none"),
                boxprops=dict(linewidth=1.5),
            )
            for i, (patch, color) in enumerate(zip(bp["boxes"], CHART_COLORS * 10)):
                patch.set_facecolor(color + "33")
                patch.set_edgecolor(color)

            ax3.set_title("Box Plot Comparison")
            apply_chart_style(ax3, fig3)
            ax3.tick_params(axis="x", labelsize=9)
            st.pyplot(fig3, use_container_width=True)

            # IQR table
            iqr_data = {c: {
                "Q1": sample_df[c].quantile(0.25),
                "Median": sample_df[c].median(),
                "Q3": sample_df[c].quantile(0.75),
                "IQR": sample_df[c].quantile(0.75) - sample_df[c].quantile(0.25),
                "Outliers": len(sample_df[c][
                    (sample_df[c] < sample_df[c].quantile(0.25) - 1.5*(sample_df[c].quantile(0.75)-sample_df[c].quantile(0.25))) |
                    (sample_df[c] > sample_df[c].quantile(0.75) + 1.5*(sample_df[c].quantile(0.75)-sample_df[c].quantile(0.25)))
                ])
            } for c in cols_bp}
            st.dataframe(pd.DataFrame(iqr_data).T.style.format("{:.2f}"), use_container_width=True)

    with tab4:
        st.markdown(f'<div class="info-banner">ℹ️ Pair plot shows pairwise relationships across all selected features.</div>', unsafe_allow_html=True)
        pp_cols = st.multiselect("Features for pair plot", numeric_df.columns.tolist(),
                                  default=numeric_df.columns.tolist()[:4], key="pp_cols")
        if len(pp_cols) >= 2:
            n = len(pp_cols)
            fig_pp, axes = plt.subplots(n, n, figsize=(min(12, n * 3), min(12, n * 3)))
            fig_pp.patch.set_facecolor(PALETTE["card"])

            for i, col_i in enumerate(pp_cols):
                for j, col_j in enumerate(pp_cols):
                    ax_pp = axes[i][j] if n > 1 else axes
                    ax_pp.set_facecolor(PALETTE["surface"])
                    for spine in ax_pp.spines.values():
                        spine.set_color(PALETTE["border"])
                    ax_pp.tick_params(colors=PALETTE["muted"], labelsize=7)

                    if i == j:
                        ax_pp.hist(sample_df[col_i].dropna(), bins=12,
                                   color=PALETTE["accent"] + "88", edgecolor="none")
                    else:
                        ax_pp.scatter(sample_df[col_j], sample_df[col_i],
                                      color=PALETTE["accent2"], alpha=0.45, s=12, edgecolors="none")

                    if i == n - 1: ax_pp.set_xlabel(col_j, color=PALETTE["muted"], fontsize=8)
                    if j == 0:     ax_pp.set_ylabel(col_i, color=PALETTE["muted"], fontsize=8)

            fig_pp.suptitle("Pair Plot Matrix", color=PALETTE["text"], fontsize=11, fontweight="semibold", y=1.01)
            fig_pp.tight_layout(pad=0.5)
            st.pyplot(fig_pp, use_container_width=True)
        else:
            st.info("Select at least 2 features.")

