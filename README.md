# Market Analysis: Housing in Casablanca, Morocco

**Accurate property price estimation using advanced regression models and automated workflows**

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Data Collection](#data-collection)
- [Data Processing](#data-processing)
- [Exploratory Data Analysis](#exploratory-data-analysis)
- [Modeling & Evaluation](#modeling--evaluation)
- [Results](#results)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Future Improvements](#future-improvements)
- [License](#license)

## Introduction
Estimating property prices accurately is essential for sellers, buyers, and real estate professionals. This project leverages end-to-end data acquisition, cleaning, exploratory analysis, and cutting-edge regression techniques to deliver reliable price recommendations tailored to Casablanca’s diverse neighborhoods.

## Features
- **Automated Data Acquisition:** Scrape 3,000+ listings from Mubawab.ma with Selenium.
- **Comprehensive Cleaning:** Parse embedded tags, handle missing values, drop duplicates, and standardize formats.
- **Outlier Management:** Remove listings below 3,000 MAD/m² and apply iterative z-score filtering to detect anomalies.
- **Insightful EDA:** Visualize distribution of prices, neighborhood-specific trends, and feature correlations.
- **Full Modeling Suite:** Train and tune Linear, Ridge, Lasso, Random Forest, and Gradient Boosting regressors via GridSearchCV.
- **Clear Metrics:** Use MAPE for interpretability and R² for variance explanation.

## Data Collection
The Selenium scraper extracts:
- **Property metadata:** type, title, neighborhood, latitude/longitude
- **Listing tags:** area, rooms, bedrooms, bathrooms, floor, building age, condition, price

## Data Processing
1. Extract numeric values from strings (price, area, etc.)
2. Expand tag lists into separate columns
3. Impute or drop missing entries
4. Calculate price per m²
5. Merge low-frequency categories (e.g., Maisons + Riads → Villas)
6. Filter outliers (< 3,000 MAD/m²) and refine with two rounds of z-score filtering

## Exploratory Data Analysis
- Distribution of listings by property type and neighborhood
- Boxplots of price per m² to highlight anomalies
- Correlation heatmap to guide feature selection

## Modeling & Evaluation
```python
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV

params = {
    'learning_rate': [0.01, 0.1],
    'max_depth': [3, 5],
    'n_estimators': [100, 200]
}
gbr = GridSearchCV(
    GradientBoostingRegressor(),
    params,
    cv=5,
    scoring='neg_mean_absolute_percentage_error'
)
```  
**Model Performance:**
| Model                        | Test MAPE | Test R² |
| ---------------------------- | --------- | ------- |
| Linear Regression            | 23.9%     | 0.90    |
| Ridge (α=0.1)                | 23.9%     | 0.90    |
| Polynomial (degree 2)        | 25.5%     | 0.92    |
| Random Forest (depth 10)     | 18.8%     | 0.94    |
| Gradient Boosting (lr 0.1)   | 17.1%     | 0.94    |

## Results
The Gradient Boosting model achieved the lowest MAPE (~17.1%) and captured 94% of variance (R²) on the test set, offering robust performance across Casablanca’s varied markets.

## Tech Stack
- **Python 3.8**
- **Libraries:** pandas, numpy, scikit-learn, matplotlib, seaborn, selenium, pickle

## Getting Started
1. **Clone the repository**
   ```bash
   git clone https://github.com/username/Market-Analysis-Housing-Casablanca-Morocco.git
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the scraper**
   ```bash
   python scraper.py
   ```
4. **Launch Jupyter notebooks** for EDA and model training

## Future Improvements
- Integrate official transaction data for enhanced accuracy
- Deploy an interactive web API for real-time price estimates
- Add geospatial dashboards with Folium or Plotly
- Implement automated retraining on schedule to adapt to market shifts

## License
This project is licensed under the MIT License.