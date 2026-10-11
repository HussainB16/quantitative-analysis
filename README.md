# EduMetrics — Quantitative Analysis Dashboard

An interactive Streamlit application for exploring student performance data with descriptive statistics, sampling methods, visualizations, correlation, regression, hypothesis testing, and maximum likelihood estimation (MLE).

## Features

- Upload a CSV or use the built-in synthetic student dataset
- Review data quality and descriptive statistics
- Explore multiple sampling techniques
- Visualize distributions and relationships
- Analyze feature correlations
- Fit and evaluate regression models
- Run statistical tests and explore MLE

## Tech stack

Python · Streamlit · Pandas · NumPy · Matplotlib · Seaborn · SciPy · scikit-learn

## Project structure

```text
Quantitative-Analysis/
├── app.py                      # Streamlit shell, styling, navigation and page routing
├── experiments/
│   ├── data.py                 # Data upload, preview and descriptive statistics
│   ├── sampling.py             # Sampling techniques
│   ├── visualization.py        # Charts and visual exploration
│   ├── correlation.py          # Correlation analysis
│   ├── regression.py           # Regression modelling
│   └── hypothesis_testing.py   # Hypothesis tests and MLE
├── utils/
│   └── common.py               # Shared theme, chart styles and UI helpers
├── requirements.txt
├── .gitignore
└── README.md
```

## Run locally

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
```

Activate the environment, then install dependencies:

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

**macOS / Linux**
```bash
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The application opens in your browser at the local Streamlit URL.

## Notes

- The existing Streamlit interface and experiment logic have been separated into modules; the project does not require a separate API server.
- Upload your own CSV from the Data tab or use the included synthetic sample data.
- Do not commit private datasets, credentials, or Streamlit secrets.
