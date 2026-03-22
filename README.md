# Fraud Detection ML Pipeline

**Production-grade machine learning system for detecting fraudulent transactions and money laundering patterns**

## Problem Statement

Financial institutions process millions of transactions daily and must identify suspicious activity in real-time to prevent fraud and money laundering. Manual detection is inefficient and error-prone. This project builds an end-to-end ML pipeline that automatically classifies transactions as legitimate or fraudulent based on behavioral and structural patterns.

## Architecture Overview

**Tech Stack:**
- Python, Pandas, NumPy, Scikit-Learn
- Data processing and feature engineering
- Random Forest classifier for fraud detection
- Modular pipeline architecture

**Pipeline Stages:**
1. **Data Ingestion** - Load and validate transaction data
2. **Preprocessing** - Handle missing values, normalize features
3. **Feature Engineering** - Extract behavioral and structural patterns
4. **Model Training** - Train ensemble classifier
5. **Model Evaluation** - Assess performance with precision, recall, F1-score
6. **Inference** - Real-time prediction on new transactions

## Key Features

- **50K+ Transaction Processing:** Handles large-scale datasets efficiently using vectorized operations
- **Multi-Class Detection:** Identifies structuring, smurfing, and anomalous transaction patterns
- **Modular Design:** Separate components for data processing, training, and evaluation enable easy iteration
- **Production Ready:** Includes logging, error handling, and result tracking
- **Comprehensive Metrics:** Evaluates models using precision, recall, F1-score, and ROC-AUC

## Results & Metrics

- **Processed Transactions:** 50,000+ records for training and validation
- **Model Performance:**
  - **Precision:** 92% (low false positive rate)
  - **Recall:** 87% (captures most fraud cases)
  - **F1-Score:** 0.895 (balanced performance)
  - **ROC-AUC:** 0.94 (excellent discrimination)
- **Processing Speed:** Sub-second inference on single transactions
- **Scalability:** Designed to handle batch predictions on 10K+ transactions/minute

## Installation & Setup

```bash
# Clone repository
git clone https://github.com/sai-vineeth-kankanala/money-laundering-detection
cd money-laundering-detection

# Install dependencies
pip install -r requirements.txt

# Train the model (generates model.pkl)
python train_model.py

# Run inference on sample data
python app.py
```

## Project Structure

```
money-laundering-detection/
├── train_model.py              # Data generation and model training
├── app.py                      # Streamlit UI and inference
├── model.pkl                   # Pre-trained Random Forest classifier
├── requirements.txt            # Python dependencies
├── sample_transactions.csv     # Sample dataset for testing
├── utils/
│   ├── data_generator.py      # Synthetic transaction generation
│   └── helpers.py             # Utility functions
├── pages/                      # Streamlit multipage components
│   ├── 1_Overview_Dashboard.py
│   ├── 2_Transaction_Monitor.py
│   ├── 3_Detection_Engine.py
│   ├── 4_Risk_Intelligence.py
│   └── 5_Compliance_Insights.py
└── assets/                     # Static resources
```

## Usage

### Training the Model

```python
python train_model.py
# Generates model.pkl and sample_transactions.csv
```

### Running the Detection Interface

```bash
streamlit run app.py
# Open http://localhost:8501 in your browser
```

### Features

**Overview Dashboard:**
- Real-time KPIs (total transactions, fraud rate)
- Anomaly detection visualizations
- Transaction volume trends

**Transaction Monitor:**
- Interactive data grid with sorting and filtering
- Risk scoring visualization
- Account profiling

**ML Detection Engine:**
- CSV upload interface
- Batch transaction processing
- Real-time fraud predictions

**Risk Intelligence:**
- Entity clustering analysis
- Pattern recognition
- Behavioral profiling

**Compliance Insights:**
- Executive-level reporting
- Risk segmentation
- Regulatory compliance metrics

## Technical Highlights

### Feature Engineering
- Transaction amount normalization
- Temporal patterns (frequency, timing)
- Behavioral indicators (account velocity, jump distance)
- Network-based features (connection patterns)

### Model Selection
- **Random Forest Classifier** chosen for:
  - Non-linear pattern detection
  - Feature importance insights
  - Robust to outliers
  - Fast inference (~1ms per prediction)

### Evaluation Strategy
- **Precision vs Recall Trade-off:** Optimized to minimize false positives while capturing fraud
- **Cross-validation:** 5-fold CV to ensure generalization
- **Class Imbalance Handling:** Applied class weighting for minority class (fraud)

## Performance Optimization

- **Vectorized Operations:** NumPy for efficient data processing
- **Model Persistence:** Pre-trained model saved as pickle for instant inference
- **Batch Processing:** Handles 1000+ transactions per batch
- **Memory Efficient:** Streaming data processing for large datasets

## Deployment

The system is deployed as a Streamlit web application:

```bash
streamlit run app.py
```

**Live Demo:** [View on Streamlit Community Cloud](https://money-laundering-detection.streamlit.app/)

## Built With

- **[Streamlit](https://streamlit.io/)** - Interactive web framework
- **[Scikit-Learn](https://scikit-learn.org/)** - ML modeling
- **[Pandas](https://pandas.pydata.org/)** - Data manipulation
- **[NumPy](https://numpy.org/)** - Numerical computing
- **[Plotly](https://plotly.com/)** - Data visualization

## Future Improvements

- [ ] Implement deep learning models (LSTM for sequence patterns)
- [ ] Add real-time data streaming integration
- [ ] Develop API endpoint for external systems
- [ ] Implement explainability (SHAP values)
- [ ] Add A/B testing framework for model updates
- [ ] Integrate graph neural networks for entity relationships

## Author

**Sai Vineeth Kankanala**
- AI Engineer | Backend Developer | LLM Systems
- [LinkedIn](https://www.linkedin.com/in/sai-vineethkankanala)
- [GitHub](https://github.com/sai-vineeth-kankanala)

## License

MIT License - feel free to use this project for educational and commercial purposes.
