# Market-Analysis-Housing-Casablanca-Morocco


**Predicting property prices in Casablanca, Morocco using advanced regression models**

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
Accurately estimating property prices is crucial for both sellers and buyers. This project combines web scraping, data cleaning, exploratory analysis, and state-of-the-art regression techniques to provide reliable price recommendations for Casablanca’s dynamic real estate market.

## Features
- **Automated Data Acquisition:** Scrape 3000+ listings from Mubawab.ma using Selenium.
- **Robust Data Cleaning:** Extract and structure embedded tags, handle missing values, and remove duplicates.
- **Outlier Management:** Apply rational thresholds and iterative z‑score filtering to ensure data integrity.
- **In-depth EDA:** Visualize price distributions, neighborhood trends, and feature correlations.
- **Comprehensive Model Suite:** Train and optimize Linear, Ridge, Lasso, Random Forest, and Gradient Boosting regressors with GridSearchCV.
- **Clear Performance Metrics:** Evaluate models with MAPE for interpretability and R² for variance explanation.

## Data Collection
The Selenium-driven scraper captures:
- Property type, title, neighborhood, latitude/longitude
- Tags: area, rooms, bedrooms, bathrooms, floor, building age, condition, price

## Data Processing
1. Parse numeric values (price, area, etc.)
2. Expand tag lists into individual columns
3. Handle missing entries and drop incomplete rows
4. Compute price per m²
5. Merge underrepresented categories (e.g., Villas + Maisons)
6. Remove outliers below 3,000 MAD/m² and refine with iterative z‑score filtering

## Exploratory Data Analysis
- Distribution of listings by type and neighborhood
- Boxplots of price per m² to detect anomalies
- Correlation heatmaps to inform feature selection

## Modeling & Evaluation
```python
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV

params = {'alpha': [0.01, 0.1, 1, 10]}
model = GridSearchCV(Ridge(), params, cv=5, scoring='neg_mean_absolute_percentage_error')
```  
**Model Performance:**
| Model                        | Test MAPE | Test R² |
| ---------------------------- | --------- | ------- |
| Linear Regression            | 23.9%     | 0.90    |
| Ridge (α=0.1)                | 23.9%     | 0.90    |
| Polynomial (degree=2)        | 25.5%     | 0.92    |
| Random Forest (depth=10)     | 18.8%     | 0.94    |
| Gradient Boosting (lr=0.1)   | 17.1%     | 0.94    |

## Tech Stack
- **Python 3.8**
- Libraries: pandas, numpy, scikit-learn, matplotlib, seaborn, selenium, pickle

## Getting Started
1. **Clone the repo**
   ```bash
   git clone https://github.com/username/Casablanca-House-Prices.git
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the scraper**
   ```bash
   python scraper.py
   ```
4. **Explore notebooks** for EDA and model training

## Future Improvements
- Integrate actual transaction data for enhanced accuracy
- Add interactive geospatial visualizations
- Deploy as a web service for real-time price estimates

## License
Distributed under the MIT License. Feel free to contribute and share!
