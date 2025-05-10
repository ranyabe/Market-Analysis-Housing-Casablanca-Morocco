# Market Analysis: Housing in Casablanca, Morocco

**Accurate property price estimation using advanced regression models and automated workflows**

---

## Business Problem
Casablanca’s real estate market is highly fragmented and fast‑moving. Sellers struggle to price properties competitively and transparently across diverse neighborhoods—leading to overpricing, stale listings, or lost revenue. Buyers and investors lack reliable benchmarks to make informed decisions, increasing time on market and transactional friction.

## Solution Overview
This project delivers an end‑to‑end pipeline—from data acquisition to model deployment—that:
1. **Aggregates real‑time listings** via automated web scraping.  
2. **Standardizes and cleans** disparate data fields into actionable features.  
3. **Explores and visualizes** market dynamics across 27 key neighborhoods.  
4. **Trains and tunes** a suite of regression models to predict price per m² with 17% MAPE.  
5. **Provides actionable insights** and visual dashboards for stakeholders to optimize listing strategies.

---

## Table of Contents
- [Business Problem](#business-problem)
- [Solution Overview](#solution-overview)
- [Introduction](#introduction)
- [Features](#features)
- [Data Collection](#data-collection)
- [Data Processing](#data-processing)
- [Exploratory Data Analysis](#exploratory-data-analysis)
- [Modeling & Evaluation](#modeling--evaluation)
- [Results](#results)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)


## Introduction
Estimating property prices accurately is essential for sellers, buyers, and real estate professionals. This project leverages end-to-end data acquisition, cleaning, exploratory analysis, and cutting-edge regression techniques to deliver reliable price recommendations tailored to Casablanca’s diverse neighborhoods.

## Features
- **Automated Data Acquisition:** Scrape 3,000+ listings from Mubawab.ma with Selenium.
- **Comprehensive Cleaning:** Parse embedded tags, handle missing values, drop duplicates, and standardize formats.
- **Outlier Management:** Remove listings below 3,000 MAD/m² and apply iterative z-score filtering to detect anomalies.
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
6. Filter outliers (< 3,000 MAD/m²) and refine with two rounds of z-score filtering

## Exploratory Data Analysis
Below are key visualizations that reveal market insights.

### Price per m² by Neighborhood
![](images/output5.png)

### Boxplot & Mean Marker per Neighborhood
![](images/output6.png)

### Refined Distribution (Filtered Outliers)
![](images/output7.png)

### Overall Price per m² Distribution
![](images/output8.png)

### Price Distributions: Apartments vs. Villas
![](images/output10.png)

### Area Distributions: Villas vs. Apartments
![](images/output11.png)

### Average Price per m² by Neighborhood (Villas)
![](images/output12.png)

### Average Price per m² by Neighborhood (Apartments)
![](images/output13.png)

### Absolute Price Averages by Neighborhood
![](images/output14.png)

### Detailed Histograms by Top 27 Neighborhoods
![](images/output21.png)

> **Key Observations:**  
> - Luxury districts (e.g., Anfa, Ain Diab) command premium rates (20k–33k MAD/m²) with tight distributions.  
> - Emerging neighborhoods (e.g., CIL, Oasis) show wider variance—indicating opportunity for arbitrage.  
> - Villas exhibit greater price dispersion and larger areas; apartments cluster around 12k–18k MAD/m².

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
**Performance Metrics:**
| Model                        | Test MAPE | Test R² |
| ---------------------------- | --------- | ------- |
| Linear Regression            | 23.9%     | 0.90    |
| Ridge (α=0.1)                | 23.9%     | 0.90    |
| Polynomial (degree 2)        | 25.5%     | 0.92    |
| Random Forest (depth 10)     | 18.8%     | 0.94    |
| Gradient Boosting (lr 0.1)   | 17.1%     | 0.94    |

## Results
The Gradient Boosting model delivers the best balance of accuracy (17.1% MAPE) and generalization (R² 0.94), providing robust price estimates for stakeholders.


