# Delhi Air Quality Predictor

A machine learning system that predicts air quality index (AQI) in Delhi using real-time weather data from the World Air Quality Index (WAQI) API. The project includes automated data collection, feature engineering, and XGBoost-based predictions.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0+-green.svg)](https://xgboost.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Data Sources](#data-sources)
- [Installation](#installation)
- [Usage](#usage)
- [Model Details](#model-details)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Author](#author)
- [License](#license)

## Overview

Air quality in Delhi is a critical public health concern. This project builds a predictive model to forecast AQI levels based on meteorological and pollutant data, enabling proactive health advisories and pollution management.

### Key Objectives

- Collect real-time air quality data from WAQI API
- Build a feature store for continuous data ingestion
- Develop XGBoost regression model for AQI prediction
- Analyze pollutant patterns and weather correlations

## Features

- **Real-Time Data Collection**: Hourly data fetch from WAQI API
- **Automated Feature Store**: CSV-based storage with continuous updates
- **Comprehensive EDA**: Data analysis and visualization notebooks
- **XGBoost Prediction**: Gradient boosting model for accurate forecasting
- **Multiple Pollutant Tracking**: PM2.5, PM10, NO2, SO2, O3, CO monitoring

## Data Sources

### WAQI API Data

| Feature | Description | Unit |
|---------|-------------|------|
| **PM2.5** | Fine particulate matter | μg/m³ |
| **PM10** | Coarse particulate matter | μg/m³ |
| **NO2** | Nitrogen dioxide | ppb |
| **SO2** | Sulfur dioxide | ppb |
| **O3** | Ozone | ppb |
| **CO** | Carbon monoxide | ppm |
| **Temperature** | Ambient temperature | °C |
| **Humidity** | Relative humidity | % |
| **Pressure** | Atmospheric pressure | hPa |
| **Wind Speed** | Wind velocity | m/s |
| **Wind Direction** | Wind bearing | degrees |

### Data Collection

```python
# Data is fetched hourly from Delhi Mandir Marg monitoring station
API_URL = "https://api.waqi.info/feed/here/?token=YOUR_TOKEN"
```

## Installation

### Prerequisites

- Python 3.8 or higher
- WAQI API token (free at https://aqicn.org/data-platform/token/)

### Setup

```bash
# Clone the repository
git clone https://github.com/AbhinavSarkarr/delhi-aqi.git
cd delhi-aqi

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

```
pandas
numpy
requests
xgboost
scikit-learn
matplotlib
seaborn
jupyter
```

## Usage

### Start Data Collection

```bash
# Run continuous data collection (fetches hourly)
python data.py
```

### Run Data Analysis

```bash
jupyter notebook data_analysis.ipynb
```

### Train the Model

```bash
jupyter notebook feature_engineering_and_Model_Training.ipynb
```

### Make Predictions

```python
import pickle
import pandas as pd

# Load trained model
model = pickle.load(open('delhi_aqi_pred_xgboost.pkl', 'rb'))

# Prepare features
features = pd.DataFrame({
    'temperature': [25],
    'humidity': [60],
    'pressure': [1015],
    'wind_speed': [5],
    'pm10': [150],
    'no2': [30],
    'so2': [10],
    'o3': [40],
    'co': [1.5]
})

# Predict AQI
predicted_aqi = model.predict(features)
print(f"Predicted AQI: {predicted_aqi[0]:.2f}")
```

## Model Details

### XGBoost Configuration

| Parameter | Value |
|-----------|-------|
| **Objective** | reg:squarederror |
| **Learning Rate** | 0.1 |
| **Max Depth** | 6 |
| **N Estimators** | 100 |
| **Subsample** | 0.8 |

### Feature Importance

1. **PM2.5** - Primary predictor of overall AQI
2. **Temperature** - Affects pollutant dispersion
3. **Humidity** - Impacts particulate matter levels
4. **Wind Speed** - Crucial for pollutant dispersal
5. **PM10** - Secondary particulate indicator

### AQI Categories

| AQI Range | Category | Health Impact |
|-----------|----------|---------------|
| 0-50 | Good | Minimal |
| 51-100 | Satisfactory | Minor breathing discomfort |
| 101-200 | Moderate | Breathing discomfort |
| 201-300 | Poor | Breathing discomfort on prolonged exposure |
| 301-400 | Very Poor | Respiratory illness on prolonged exposure |
| 401-500 | Severe | Affects healthy people |

## Technologies

| Technology | Purpose |
|------------|---------|
| **XGBoost** | Gradient boosting prediction model |
| **pandas** | Data manipulation and analysis |
| **NumPy** | Numerical computations |
| **requests** | API data fetching |
| **Matplotlib/Seaborn** | Data visualization |
| **scikit-learn** | Model evaluation and preprocessing |

## Project Structure

```
delhi-aqi/
├── data.py                                    # Automated data collection script
├── dataset_creator.py                         # Dataset preparation utilities
├── data_analysis.ipynb                        # Exploratory data analysis
├── data_preprocessing.ipynb                   # Data cleaning and preparation
├── feature_engineering_and_Model_Training.ipynb  # Model training
├── delhi_aqi_pred_xgboost.pkl                # Trained XGBoost model
├── air_quality_feature_store.csv             # Feature store data
├── air_quality_feature_store[2-6].csv        # Historical data files
├── .gitignore
└── README.md                                  # This file
```

## Data Collection Pipeline

```
WAQI API → data.py (Hourly) → air_quality_feature_store.csv
                                        ↓
                              data_preprocessing.ipynb
                                        ↓
                              Feature Engineering
                                        ↓
                              XGBoost Training
                                        ↓
                              delhi_aqi_pred_xgboost.pkl
```

## Future Enhancements

- [ ] Add multi-location monitoring across Delhi NCR
- [ ] Implement LSTM for time-series forecasting
- [ ] Build real-time dashboard with Streamlit
- [ ] Add health advisory notifications
- [ ] Deploy prediction API

## Author

**Abhinav Sarkar**
- GitHub: [@AbhinavSarkarr](https://github.com/AbhinavSarkarr)
- LinkedIn: [abhinavsarkarrr](https://www.linkedin.com/in/abhinavsarkarrr)
- Portfolio: [abhinav-ai-portfolio.lovable.app](https://abhinav-ai-portfolio.lovable.app/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- World Air Quality Index Project (WAQI) for the API
- Delhi Pollution Control Committee for monitoring data
- XGBoost development team

---

<p align="center">
  <strong>Breathe better with data-driven air quality predictions</strong>
</p>
