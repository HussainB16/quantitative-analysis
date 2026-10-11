from utils.common import *


def render():
    st.markdown(section_header("Regression Modelling", "STEP 05"), unsafe_allow_html=True)

    if "numeric_df" not in st.session_state:
        st.warning("⚠️ Please load data first in the **📥 Data** tab.")
        st.stop()

    numeric_df = st.session_state["numeric_df"]
    sample_df  = st.session_state.get("sample_df", numeric_df)

    tab_s, tab_m, tab_r = st.tabs(["📉 Simple Linear", "📐 Multiple Linear", "📊 Residual Analysis"])

    with tab_s:
        c1, c2 = st.columns(2)
        x_col = c1.selectbox("X — Predictor", numeric_df.columns, key="slr_x")
        y_col = c2.selectbox("Y — Target", numeric_df.columns,
                              key="slr_y", index=len(numeric_df.columns) - 1)

        X_slr = sample_df[[x_col]].dropna()
        y_slr = sample_df[y_col].loc[X_slr.index]

        model_slr = LinearRegression().fit(X_slr, y_slr)
        y_pred_slr = model_slr.predict(X_slr)
        r2_slr = model_slr.score(X_slr, y_slr)
        rmse_slr = np.sqrt(mean_squared_error(y_slr, y_pred_slr))
        mae_slr = mean_absolute_error(y_slr, y_pred_slr)

        c1m, c2m, c3m, c4m, c5m = st.columns(5)
        c1m.metric("Coefficient (β₁)", f"{model_slr.coef_[0]:.4f}")
        c2m.metric("Intercept (β₀)", f"{model_slr.intercept_:.4f}")
        c3m.metric("R² Score", f"{r2_slr:.4f}")
        c4m.metric("RMSE", f"{rmse_slr:.4f}")
        c5m.metric("MAE", f"{mae_slr:.4f}")

        fig5, ax5 = plt.subplots(figsize=(10, 5))
        ax5.scatter(X_slr, y_slr, color=PALETTE["accent"], alpha=0.7, s=55,
                    edgecolors=PALETTE["border2"], linewidths=0.5, label="Data", zorder=3)

        xs_reg = np.linspace(X_slr.values.min(), X_slr.values.max(), 200).reshape(-1, 1)
        ys_reg = model_slr.predict(xs_reg)
        ax5.plot(xs_reg, ys_reg, color=PALETTE["accent2"], linewidth=2.5,
                 label=f"ŷ = {model_slr.coef_[0]:.3f}x + {model_slr.intercept_:.3f}", zorder=4)

        # Confidence band (approximate)
        n_pts = len(y_slr)
        se = np.sqrt(((y_slr - y_pred_slr)**2).sum() / (n_pts - 2))
        x_mean = X_slr.values.mean()
        x_range = ((xs_reg - x_mean)**2).sum()**0.5 / n_pts
        ci = 1.96 * se * np.sqrt(1/n_pts + (xs_reg - x_mean)**2 / ((X_slr.values - x_mean)**2).sum())
        ax5.fill_between(xs_reg.flatten(), ys_reg - ci.flatten(), ys_reg + ci.flatten(),
                         alpha=0.15, color=PALETTE["accent2"], label="95% CI")

        ax5.set_xlabel(x_col); ax5.set_ylabel(y_col)
        ax5.set_title(f"Simple Linear Regression: {y_col} ~ {x_col}  (R² = {r2_slr:.3f})")
        ax5.legend(facecolor=PALETTE["card"], edgecolor=PALETTE["border"],
                   labelcolor=PALETTE["text"], fontsize=8.5)
        apply_chart_style_clean(ax5, fig5)
        fig5.tight_layout()
        st.pyplot(fig5, use_container_width=True)

        st.markdown(insight(
            f"For every unit increase in <strong>{x_col}</strong>, <strong>{y_col}</strong> changes by "
            f"<strong>{model_slr.coef_[0]:.3f}</strong> units. The model explains "
            f"<strong>{r2_slr*100:.1f}%</strong> of variance in {y_col} "
            f"(R² = {r2_slr:.4f}). RMSE of {rmse_slr:.2f} indicates average prediction error."
        ), unsafe_allow_html=True)

    with tab_m:
        features = st.multiselect("Feature Columns (X)", numeric_df.columns.tolist(),
                                   default=numeric_df.columns.tolist()[:-1])
        target = st.selectbox("Target Column (Y)", numeric_df.columns,
                               index=len(numeric_df.columns) - 1, key="mlr_target")

        if len(features) > 0:
            Xm = sample_df[features].dropna()
            ym = sample_df[target].loc[Xm.index]
            mm = LinearRegression().fit(Xm, ym)
            ym_pred = mm.predict(Xm)
            r2m = mm.score(Xm, ym)
            rmse_m = np.sqrt(mean_squared_error(ym, ym_pred))
            mae_m = mean_absolute_error(ym, ym_pred)

            c1m, c2m, c3m, c4m = st.columns(4)
            c1m.metric("R² Score", f"{r2m:.4f}")
            c2m.metric("Adj. R²", f"{1-(1-r2m)*(len(ym)-1)/(len(ym)-len(features)-1):.4f}")
            c3m.metric("RMSE", f"{rmse_m:.4f}")
            c4m.metric("MAE", f"{mae_m:.4f}")

            coef_df = pd.DataFrame({"Feature": features, "Coefficient": mm.coef_}) \
                .sort_values("Coefficient", key=abs, ascending=True)

            fig6, ax6 = plt.subplots(figsize=(10, max(3.5, len(features) * 0.7)))
            colors_coef = [PALETTE["accent3"] if v >= 0 else PALETTE["danger"]
                           for v in coef_df["Coefficient"]]
            bars = ax6.barh(coef_df["Feature"], coef_df["Coefficient"],
                            color=colors_coef, edgecolor=PALETTE["border"],
                            height=0.6, alpha=0.85)
            ax6.axvline(0, color=PALETTE["muted"], linewidth=1, linestyle="--")

            # Value labels
            for bar, val in zip(bars, coef_df["Coefficient"]):
                ax6.text(val + (0.01 * abs(coef_df["Coefficient"]).max()),
                         bar.get_y() + bar.get_height() / 2,
                         f"{val:.3f}", va="center", ha="left" if val >= 0 else "right",
                         color=PALETTE["text2"], fontsize=8,
                         fontfamily="JetBrains Mono")

            ax6.set_title(f"Feature Coefficients — Predicting {target}")
            apply_chart_style(ax6, fig6)
            fig6.tight_layout()
            st.pyplot(fig6, use_container_width=True)

            # Coefficient table
            coef_table = pd.DataFrame({
                "Feature": features,
                "Coefficient": mm.coef_,
                "Abs Importance": np.abs(mm.coef_)
            }).sort_values("Abs Importance", ascending=False)
            st.dataframe(coef_table.style.format({"Coefficient": "{:.4f}", "Abs Importance": "{:.4f}"}),
                         use_container_width=True)
        else:
            st.info("Select at least one feature column.")

    with tab_r:
        st.markdown(f'<div class="info-banner">ℹ️ Residual analysis for the Simple Linear Regression model from the previous tab.</div>',
                    unsafe_allow_html=True)

        if "x_col" not in dir() or "y_col" not in dir():
            x_col = numeric_df.columns[0]
            y_col = numeric_df.columns[-1]

        # Re-run SLR with whatever's in session
        X_r = sample_df[[numeric_df.columns[0]]].dropna()
        y_r = sample_df[numeric_df.columns[-1]].loc[X_r.index]
        m_r = LinearRegression().fit(X_r, y_r)
        resid = y_r - m_r.predict(X_r)
        fitted = m_r.predict(X_r)

        fig_res, axes_res = plt.subplots(1, 3, figsize=(14, 4))
        fig_res.patch.set_facecolor(PALETTE["card"])

        # Residuals vs Fitted
        axes_res[0].scatter(fitted, resid, color=PALETTE["accent"], alpha=0.65, s=45,
                            edgecolors=PALETTE["border2"], linewidths=0.4)
        axes_res[0].axhline(0, color=PALETTE["accent2"], linewidth=1.5, linestyle="--")
        axes_res[0].set_xlabel("Fitted Values"); axes_res[0].set_ylabel("Residuals")
        axes_res[0].set_title("Residuals vs Fitted")

        # Histogram of residuals
        axes_res[1].hist(resid, bins=15, color=PALETTE["accent5"], alpha=0.8,
                         edgecolor=PALETTE["bg"], rwidth=0.88)
        axes_res[1].set_xlabel("Residual"); axes_res[1].set_ylabel("Count")
        axes_res[1].set_title("Residual Distribution")

        # Q-Q plot
        (osm, osr), (slope, intercept, r) = stats.probplot(resid)
        axes_res[2].scatter(osm, osr, color=PALETTE["accent3"], alpha=0.7, s=40)
        axes_res[2].plot(osm, slope * np.array(osm) + intercept,
                         color=PALETTE["accent2"], linewidth=2)
        axes_res[2].set_xlabel("Theoretical Quantiles"); axes_res[2].set_ylabel("Sample Quantiles")
        axes_res[2].set_title("Q-Q Plot")

        for ax_r in axes_res:
            apply_chart_style(ax_r, fig_res)

        fig_res.tight_layout(pad=2)
        st.pyplot(fig_res, use_container_width=True)

        # Normality test
        stat_sw, p_sw = stats.shapiro(resid)
        st.markdown(f"""
        <div class="result-box">
          <div class="result-grid">
            <div class="result-item"><div class="result-key">Shapiro-Wilk Stat</div><div class="result-val blue">{stat_sw:.4f}</div></div>
            <div class="result-item"><div class="result-key">p-value</div><div class="result-val {'green' if p_sw>0.05 else ''}">{p_sw:.4f}</div></div>
            <div class="result-item"><div class="result-key">Normality</div><div class="result-val {'green' if p_sw>0.05 else ''}">{('✓ Normal' if p_sw>0.05 else '✗ Non-normal')} (α=0.05)</div></div>
            <div class="result-item"><div class="result-key">Mean Residual</div><div class="result-val">{resid.mean():.4f}</div></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

