from utils.common import *


def render():
    st.markdown(section_header("Statistical Testing & Estimation", "STEP 06"), unsafe_allow_html=True)

    if "numeric_df" not in st.session_state:
        st.warning("⚠️ Please load data first in the **📥 Data** tab.")
        st.stop()

    numeric_df = st.session_state["numeric_df"]
    sample_df  = st.session_state.get("sample_df", numeric_df)

    tab_h, tab_two, tab_mle = st.tabs(["🧪 One-Sample Test", "⚖️ Two-Sample Test", "📐 MLE"])

    with tab_h:
        c1, c2, c3 = st.columns(3)
        test_type = c1.selectbox("Test Type", ["One-Sample T-Test", "Z-Test"])
        col_test  = c2.selectbox("Column", numeric_df.columns, key="ht_col")
        mu0       = c3.number_input("Null Mean (μ₀)", value=float(round(numeric_df[col_test].mean(), 1)))
        alpha     = st.slider("Significance Level (α)", 0.01, 0.10, 0.05, 0.01)

        data_test = sample_df[col_test].dropna()

        if test_type == "One-Sample T-Test":
            t_stat, p_val = stats.ttest_1samp(data_test, mu0)
            reject = p_val < alpha
            ci_low, ci_high = stats.t.interval(1 - alpha, len(data_test) - 1,
                                                loc=data_test.mean(),
                                                scale=stats.sem(data_test))
        else:
            t_stat = (np.mean(data_test) - mu0) / (np.std(data_test) / np.sqrt(len(data_test)))
            p_val  = 2 * (1 - stats.norm.cdf(abs(t_stat)))
            reject = abs(t_stat) > stats.norm.ppf(1 - alpha / 2)
            ci_low  = data_test.mean() - 1.96 * stats.sem(data_test)
            ci_high = data_test.mean() + 1.96 * stats.sem(data_test)

        stat_label = "T" if "T-Test" in test_type else "Z"
        result_color = "green" if reject else ""
        decision = "Reject H₀ ✅" if reject else "Fail to Reject H₀ ❌"

        st.markdown(f"""
        <div class="result-box">
          <div class="result-grid">
            <div class="result-item"><div class="result-key">{stat_label}-Statistic</div><div class="result-val blue">{t_stat:.4f}</div></div>
            <div class="result-item"><div class="result-key">p-value</div><div class="result-val {'green' if p_val < alpha else ''}">{p_val:.4f}</div></div>
            <div class="result-item"><div class="result-key">Sample Mean (x̄)</div><div class="result-val">{data_test.mean():.4f}</div></div>
            <div class="result-item"><div class="result-key">{int((1-alpha)*100)}% CI</div><div class="result-val blue">[{ci_low:.3f}, {ci_high:.3f}]</div></div>
            <div class="result-item"><div class="result-key">Decision (α={alpha})</div><div class="result-val {result_color}">{decision}</div></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Distribution chart
        fig7, ax7 = plt.subplots(figsize=(10, 4))
        xs = np.linspace(data_test.min() - data_test.std(), data_test.max() + data_test.std(), 300)
        ax7.hist(data_test, bins=20, density=True,
                 color=PALETTE["accent"] + "44", edgecolor=PALETTE["border"], label="Data", rwidth=0.9)
        mu_hat, std_hat = data_test.mean(), data_test.std()
        ax7.plot(xs, stats.norm.pdf(xs, mu_hat, std_hat),
                 color=PALETTE["accent"], linewidth=2.5, label="Fitted Normal")
        ax7.axvline(mu0, color=PALETTE["accent2"], linewidth=2, linestyle="--",
                    label=f"H₀: μ₀ = {mu0}")
        ax7.axvline(mu_hat, color=PALETTE["accent3"], linewidth=2,
                    label=f"x̄ = {mu_hat:.2f}")
        ax7.axvspan(ci_low, ci_high, alpha=0.08, color=PALETTE["accent3"], label=f"{int((1-alpha)*100)}% CI")
        ax7.legend(facecolor=PALETTE["card"], edgecolor=PALETTE["border"],
                   labelcolor=PALETTE["text"], fontsize=8.5)
        ax7.set_title(f"Hypothesis Test — {col_test}")
        apply_chart_style_clean(ax7, fig7)
        fig7.tight_layout()
        st.pyplot(fig7, use_container_width=True)

        st.markdown(insight(
            f"With α = {alpha}, the {test_type} yields {stat_label} = {t_stat:.3f} and p = {p_val:.4f}. "
            f"We <strong>{'reject' if reject else 'fail to reject'}</strong> H₀ (μ = {mu0}). "
            f"The {int((1-alpha)*100)}% confidence interval [{ci_low:.2f}, {ci_high:.2f}] "
            f"{'does not contain' if reject else 'contains'} μ₀ = {mu0}."
        ), unsafe_allow_html=True)

    with tab_two:
        c1, c2 = st.columns(2)
        col_a = c1.selectbox("Group A Column", numeric_df.columns, key="tt_a")
        col_b = c2.selectbox("Group B Column", numeric_df.columns,
                              index=min(1, len(numeric_df.columns)-1), key="tt_b")
        equal_var = st.checkbox("Assume equal variances", value=False)
        alpha2 = st.slider("Significance Level (α)", 0.01, 0.10, 0.05, 0.01, key="alpha2")

        da, db = sample_df[col_a].dropna(), sample_df[col_b].dropna()
        t2, p2 = stats.ttest_ind(da, db, equal_var=equal_var)
        reject2 = p2 < alpha2

        c1r, c2r, c3r, c4r = st.columns(4)
        c1r.metric(f"Mean A ({col_a})", f"{da.mean():.3f}")
        c2r.metric(f"Mean B ({col_b})", f"{db.mean():.3f}")
        c3r.metric("T-Statistic", f"{t2:.4f}")
        c4r.metric("p-value", f"{p2:.4f}")

        st.markdown(f"""
        <div class="result-box">
          <div class="result-grid">
            <div class="result-item"><div class="result-key">Decision</div>
              <div class="result-val {'green' if reject2 else ''}">{('Reject H₀ ✅' if reject2 else 'Fail to Reject H₀ ❌')}</div>
            </div>
            <div class="result-item"><div class="result-key">Effect Size (Cohen's d)</div>
              <div class="result-val blue">{(da.mean()-db.mean())/np.sqrt((da.std()**2+db.std()**2)/2):.4f}</div>
            </div>
            <div class="result-item"><div class="result-key">Mean Difference</div>
              <div class="result-val">{da.mean()-db.mean():.4f}</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Comparison chart
        fig_tt, ax_tt = plt.subplots(figsize=(10, 4))
        ax_tt.hist(da, bins=15, alpha=0.7, color=PALETTE["accent"], label=col_a,
                   density=True, edgecolor=PALETTE["bg"], rwidth=0.9)
        ax_tt.hist(db, bins=15, alpha=0.7, color=PALETTE["accent2"], label=col_b,
                   density=True, edgecolor=PALETTE["bg"], rwidth=0.9)
        ax_tt.axvline(da.mean(), color=PALETTE["accent"], linewidth=2, linestyle="--")
        ax_tt.axvline(db.mean(), color=PALETTE["accent2"], linewidth=2, linestyle="--")
        ax_tt.legend(facecolor=PALETTE["card"], edgecolor=PALETTE["border"],
                     labelcolor=PALETTE["text"], fontsize=9)
        ax_tt.set_title(f"Distribution Comparison: {col_a} vs {col_b}")
        apply_chart_style(ax_tt, fig_tt)
        fig_tt.tight_layout()
        st.pyplot(fig_tt, use_container_width=True)

    with tab_mle:
        c1, c2 = st.columns(2)
        dist     = c1.selectbox("Distribution", ["Normal", "Poisson", "Exponential", "Gamma"])
        data_col = c2.selectbox("Column", numeric_df.columns, key="mle_col")
        data_mle = sample_df[data_col].dropna()

        params_html = ""
        if dist == "Normal":
            mu_e, sigma_e = np.mean(data_mle), np.std(data_mle)
            params_html = f"""
            <div class="result-item"><div class="result-key">MLE Mean (μ)</div><div class="result-val blue">{mu_e:.4f}</div></div>
            <div class="result-item"><div class="result-key">MLE Std Dev (σ)</div><div class="result-val">{sigma_e:.4f}</div></div>
            <div class="result-item"><div class="result-key">Variance (σ²)</div><div class="result-val">{sigma_e**2:.4f}</div></div>
            """
        elif dist == "Poisson":
            lam = np.mean(data_mle)
            params_html = f"""
            <div class="result-item"><div class="result-key">MLE Rate (λ)</div><div class="result-val blue">{lam:.4f}</div></div>
            <div class="result-item"><div class="result-key">Variance (=λ)</div><div class="result-val">{lam:.4f}</div></div>
            """
        elif dist == "Exponential":
            lam_e = 1 / np.mean(data_mle)
            params_html = f"""
            <div class="result-item"><div class="result-key">MLE Rate (λ)</div><div class="result-val blue">{lam_e:.4f}</div></div>
            <div class="result-item"><div class="result-key">MLE Mean (1/λ)</div><div class="result-val">{1/lam_e:.4f}</div></div>
            """
        elif dist == "Gamma":
            fit_alpha, fit_loc, fit_beta = stats.gamma.fit(data_mle, floc=0)
            params_html = f"""
            <div class="result-item"><div class="result-key">Shape (α)</div><div class="result-val blue">{fit_alpha:.4f}</div></div>
            <div class="result-item"><div class="result-key">Scale (β)</div><div class="result-val">{fit_beta:.4f}</div></div>
            <div class="result-item"><div class="result-key">Mean (αβ)</div><div class="result-val">{fit_alpha*fit_beta:.4f}</div></div>
            """

        st.markdown(f'<div class="result-box"><div class="result-grid">{params_html}</div></div>',
                    unsafe_allow_html=True)

        # Fitted distribution plot
        fig8, ax8 = plt.subplots(figsize=(10, 4.5))
        n_hist, bins_h, _ = ax8.hist(data_mle, bins=20, density=True,
                                      color=PALETTE["accent3"] + "44",
                                      edgecolor=PALETTE["border"], label="Data", rwidth=0.9)
        xs2 = np.linspace(max(0.001, data_mle.min()), data_mle.max(), 300)

        if dist == "Normal":
            ax8.plot(xs2, stats.norm.pdf(xs2, mu_e, sigma_e), color=PALETTE["accent3"],
                     lw=2.5, label="Fitted Normal")
        elif dist == "Poisson":
            k_vals = np.arange(0, int(data_mle.max()) + 1)
            ax8.vlines(k_vals, 0, stats.poisson.pmf(k_vals, lam),
                       color=PALETTE["accent3"], lw=3, label="Fitted Poisson", alpha=0.85)
        elif dist == "Exponential":
            ax8.plot(xs2, stats.expon.pdf(xs2, scale=1/lam_e),
                     color=PALETTE["accent3"], lw=2.5, label="Fitted Exponential")
        elif dist == "Gamma":
            ax8.plot(xs2, stats.gamma.pdf(xs2, fit_alpha, scale=fit_beta),
                     color=PALETTE["accent3"], lw=2.5, label="Fitted Gamma")

        ax8.legend(facecolor=PALETTE["card"], edgecolor=PALETTE["border"],
                   labelcolor=PALETTE["text"], fontsize=9)
        ax8.set_title(f"MLE Fit — {dist} Distribution on '{data_col}'")
        apply_chart_style_clean(ax8, fig8)
        fig8.tight_layout()
        st.pyplot(fig8, use_container_width=True)

        # GoF test
        if dist == "Normal":
            stat_ks, p_ks = stats.kstest(data_mle, "norm",
                                          args=(data_mle.mean(), data_mle.std()))
            st.markdown(f"""
            <div class="result-box">
              <div class="result-grid">
                <div class="result-item"><div class="result-key">KS Test Statistic</div><div class="result-val blue">{stat_ks:.4f}</div></div>
                <div class="result-item"><div class="result-key">KS p-value</div><div class="result-val {'green' if p_ks>0.05 else ''}">{p_ks:.4f}</div></div>
                <div class="result-item"><div class="result-key">Goodness of Fit</div><div class="result-val {'green' if p_ks>0.05 else ''}">{('Good fit ✅' if p_ks>0.05 else 'Poor fit ❌')} (α=0.05)</div></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

