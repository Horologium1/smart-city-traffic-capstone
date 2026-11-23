# Smart City Mobility Analytics - Part 3: Machine Learning

## Project Overview

Part 3 of the Smart City Mobility Analytics Capstone applies machine learning, deep learning, recommendation systems, experiment tracking, deployment and monitoring techniques to the Metro Interstate Traffic Volume dataset.

The dataset contains hourly traffic observations from westbound I-94 near Minneapolis–St Paul, together with weather and time-related features. This part of the capstone explores traffic patterns, predicts traffic conditions and volume, generates travel-window recommendations, and demonstrates deployment and monitoring workflows.

## Objectives

- Develop supervised models for traffic classification and traffic-volume prediction.
- Explore traffic behaviour using unsupervised learning.
- Forecast traffic volume using a time-series deep learning model.
- Develop a historical-data-based travel recommendation system.
- Track and compare experiments using MLflow.
- Demonstrate prediction API deployment and model monitoring.

## Project Structure

```text
part3_machine_learning/
├── create_part3_dataset.py
├── README.md
├── data/
│   └── processed/
│       └── metro_traffic_part3.csv
├── task1_supervised_learning/
│   ├── scripts/
│   ├── results/
│   └── figures/
├── task2_unsupervised/
│   ├── association_rules.py
│   ├── kmeans_clustering.py
│   └── results/
├── task3_deep_learning/
│   ├── lstm_traffic_prediction.py
│   ├── lstm_permutation_importance.py
│   ├── shap_traffic_explainability.py
│   ├── lime_traffic_explainability.py
│   └── results/
├── task4_mlflow/
│   ├── mlflow_tracking.py
│   ├── mlflow_comparison.py
│   ├── mlflow.db
│   └── mlruns/
├── task5_recommendation_system/
│   └── traffic_recommender.py
└── task6_mlops_deployment/
    ├── api.py
    ├── create_lstm_scaler.py
    ├── export_deployment_model.py
    ├── mlflow_task6.py
    ├── monitoring.py
    ├── models/
    ├── monitoring_results/
    ├── mlruns/
    └── model_versions.csv
```

## Dataset Preparation

The processed Part 3 dataset was generated using `create_part3_dataset.py` and saved to:

`data/processed/metro_traffic_part3.csv`

Feature preparation includes temporal and weather-related features and traffic-related target/category information used across the subsequent tasks.

## Task 1 — Supervised Machine Learning

Classification and regression models were developed and evaluated.

### Classification

Models:
- Logistic Regression
- Random Forest Classifier

Metrics:

| Model | Accuracy | Precision | Recall | F1-score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.9472 | 0.8043 | 0.9886 | 0.8870 | 0.9875 |
| Random Forest | 0.9713 | 0.9208 | 0.9441 | 0.9323 | 0.9909 |

Random Forest achieved stronger overall classification performance across accuracy, precision, F1-score and ROC-AUC in the recorded evaluation.

### Regression

Models:
- Linear Regression
- Random Forest Regression

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Linear Regression | 822.12 | 1,047.70 | 0.7165 |
| Random Forest Regression | 296.03 | 527.69 | 0.9281 |

Random Forest Regression produced lower error and a higher R² than Linear Regression in the recorded evaluation.

### Visualisations

The saved Task 1 figures include classification confusion matrices and ROC curves, regression actual-versus-predicted plots, residual analysis and model comparison plots.

## Task 2 — Unsupervised Learning

### K-Means Clustering

K-Means clustering was used to explore traffic behaviour. Four cluster profiles were interpreted as:

- Cluster 0: Weekend daytime and moderate traffic behaviour.
- Cluster 1: Weekday, dry-weather and high traffic behaviour.
- Cluster 2: Weekday, adverse-weather and high traffic behaviour.
- Cluster 3: Weekday overnight and low traffic behaviour.

Cluster assignments and cluster profiles were saved as CSV outputs.

### Association Rule Mining

Association rule mining was used to investigate relationships among temporal, weather and traffic conditions. Recorded outputs included:

- 76 frequent itemsets
- 138 generated rules
- 52 filtered rules

Examples of patterns identified included weekday-afternoon conditions associated with severe traffic and night-time conditions associated with low traffic. Rules involving weekday nights and night-time cloudy conditions were also among the identified patterns.

## Task 3 — Deep Learning: LSTM Traffic Prediction

An LSTM model was developed for time-series traffic-volume prediction.

### Evaluation

| Metric | Result |
|---|---:|
| MAE | 238.62 |
| RMSE | 354.46 |
| R² | 0.9675 |

### Feature Importance

Permutation importance was used to assess the effect of input features on model performance. Traffic volume and hour-related features were among the most influential features, followed by weekend and day-of-week features.

Saved core artifacts include the LSTM model, evaluation results, prediction results, training history and permutation-importance outputs.

SHAP and LIME explainability scripts were also included as supplementary analyses. Their execution encountered environment-related limitations, and corresponding complete outputs were not verified as part of the final file audit.

## Task 4 — MLflow Experiment Tracking

MLflow was used to demonstrate experiment tracking and model comparison. The task included experiment tracking scripts, a model-comparison visualisation, an MLflow database and an artifact directory.

The project files for this task are retained in `task4_mlflow/`.

## Task 5 — Traffic Travel Recommendation System

A console-based recommendation system was developed to identify historical travel windows based on selected day and weather conditions.

The script:
- Identifies suitable historical travel windows for selected conditions.
- Handles invalid inputs and combinations with no available historical data.
- Produces travel-window and plain-language recommendations.
- Uses logging to record its execution.

One recorded recommendation identified a weekday evening window from 8 PM to 10 PM, with an average traffic volume of approximately 2,758 vehicles per hour.

## Task 6 — MLOps and Deployment

### Prediction API

A FastAPI prediction API was developed. The API loads the saved LSTM model from the Task 3 results directory and deployment scaler metadata from Task 6.

The API was demonstrated locally and exposes a Swagger interface for testing.

### Monitoring

A monitoring workflow was implemented to compare prediction error against a baseline.

| Monitoring metric | Value |
|---|---:|
| Baseline MAE | 238.62 |
| Alert threshold (1.5 × baseline MAE) | 357.93 |
| Synthetic monitoring MAE | 635.29 |
| Monitoring result | Alert triggered |

The synthetic monitoring scenario demonstrated that the alert mechanism responds when error exceeds the threshold.

### Model Version Tracking and Artifacts

Task 6 includes model-version tracking files and MLflow-related artifacts. The verified project structure also contains the scaler JSON, monitoring report CSV and monitoring dashboard image.

The separate Random Forest deployment export script is present. Its generated `.joblib` model file was not verified in the final directory audit; the audited API prediction path uses the LSTM model.

## Limitations and Environment Notes

- A later K-Means execution attempt encountered a Windows Application Control DLL or dependency-related issue. Previously saved clustering outputs were retained; the final audit did not rerun clustering.
- SHAP and LIME execution encountered environment-related limitations. These supplementary analyses were not treated as blockers for the core saved LSTM prediction artifacts.
- The final audit was intentionally read-only and did not rerun models, create new MLflow runs or modify existing outputs.

