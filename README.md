# Money Laundering Detection using Machine Learning

A modern, production-ready Anti-Money Laundering (AML) compliance monitoring dashboard and detection engine built with Streamlit and Scikit-Learn.

This application provides a professional fintech UI, interactive visual analytics with Plotly, and a machine learning pipeline for real-time transaction risk scoring.

## Features

- **Overview Dashboard**: High-level KPIs, anomaly detection graphs, and real-time transaction volume monitoring.
- **Transaction Monitor**: Interactive data tables with sorting, conditional formatting, and advanced filtering to identify high-risk accounts quickly.
- **ML Detection Engine**: Drag-and-drop CSV upload utility that processes bulk transactions through a Random Forest Classifier to detect structuring, smurfing, and anomalous movements.
- **Risk Intelligence**: Deep-dive clustering analysis and entity profiling.
- **Compliance Insights**: Executive-level reporting, Value at Risk (VaR) calculations, and macro-level risk segmentation.

## Architecture

```text
money-laundering-detection/
├── app.py                         # Main Streamlit app and routing
├── model.pkl                      # Pre-trained ML artifact (Random Forest)
├── README.md                      # Project documentation
├── requirements.txt               # Python dependencies
├── sample_transactions.csv        # Dummy dataset for upload testing
├── train_model.py                 # Pipeline to generate data and train ML
├── pages/                         # Streamlit multipage directory
│   ├── 1_Overview_Dashboard.py    # Main KPIs and charts
│   ├── 2_Transaction_Monitor.py   # Data grid and filtering
│   ├── 3_Detection_Engine.py      # ML Inference UI
│   ├── 4_Risk_Intelligence.py     # Advanced Analytics Center
│   └── 5_Compliance_Insights.py   # Executive Reporting
└── utils/                         # Helper modules
    ├── __init__.py
    ├── data_generator.py          # Synthetic financial data modeling
    ├── helpers.py                 # Formatting and UI utilities
    └── styles.py                  # Professional CSS injection
```

## Installation & Setup

1. **Clone the repository** (or download the source code).
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Train the ML model** (Generates `model.pkl` and sample data):
   ```bash
   python train_model.py
   ```
4. **Launch the Web Dashboard**:
   ```bash
   streamlit run app.py
   ```
5. **Open in Browser**: The application will be running at `http://localhost:8501`.

## Usage

- Upon launching, use the **Sidebar Navigation** to traverse the core modules.
- In the **Detection Engine** page, upload the generated `sample_transactions.csv` file (or any formatted CSV matching the schema) to view real-time model inference.
- The UI features a dynamic custom CSS mapping, operating best in Streamlit's Dark Mode for a sleek "fintech terminal" aesthetic.

## Built With

- **[Streamlit](https://streamlit.io/)** - Frontend Framework
- **[Scikit-Learn](https://scikit-learn.org/)** - Machine Learning Modeling
- **[Plotly](https://plotly.com/)** - Interactive Visualizations
- **[Pandas](https://pandas.pydata.org/)** - Data Manipulation
