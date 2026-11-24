# Metro Interstate Traffic Volume - Part 2: Python Data Pipeline

## Short Project Overview

This project develops a Python-based data pipeline to load, validate, clean, transform and prepare the Metro Interstate Traffic Volume dataset for further analysis.

Python, pandas and NumPy are used for data processing, feature engineering and analysis. Python's logging module is implemented through a central logging configuration to record processing activities, data-quality issues, execution status and errors across the project modules.

## Project / Repository Structure

```text
part2_python/
│
├── data/
│   ├── raw/
│   │   └── Metro_Interstate_Traffic_Volume.csv
│   └── processed/
│       ├── metro_traffic_cleaned.csv
│       └── metro_traffic_features.csv
│
├── figures/
│   ├── traffic_by_hour.png
│   ├── weekday_vs_weekend.png
│   └── temperature_vs_traffic.png
│
├── logs/
│   └── project.log
│
├── main.py
├── pipeline.py
├── feature_engineering.py
├── visualizations.py
├── traffic_analytics.py
├── requirements.txt
└── README.md
```

## Requirements & Tools Used

- Python 3.13.11
- pandas
- NumPy
- Matplotlib
- Logging
- argparse

## Instructions on How to Run

1. Place the original CSV dataset in `data/raw/`.
2. Open a terminal in the project folder.
3. Run the main project entry point:

```bash
python main.py
```

The main application sequentially executes the following processes:

1. Data cleaning and validation.
2. Feature engineering.
3. Visualisation generation.

The cleaned dataset will be saved in `data/processed/metro_traffic_cleaned.csv`.

The feature-engineered dataset will be saved in `data/processed/metro_traffic_features.csv`.

Visualisations will be saved in the `figures/` directory.

Project execution logs will be recorded in `logs/project.log`.

## Data Cleaning Process

The pipeline performs the following operations:

1. Loads the raw CSV file.
2. Validates the expected dataset columns.
3. Standardises categorical values by removing leading and trailing spaces.
4. Parses and validates date/time values.
5. Identifies and removes duplicate records.
6. Replaces impossible temperature readings of 0 Kelvin with missing values.
7. Replaces rainfall readings exceeding 9,000 mm with missing values.
8. Imputes missing temperature and rainfall values using monthly medians.
9. Saves the cleaned dataset.
10. Performs final data-quality validation.

## Logging Configuration

Python's logging module is used to monitor and record project execution activities.

### Centralised Logging

Logging configuration is centralised in `main.py`. The configuration defines the logging level, message format and output handlers.

Individual modules such as `pipeline.py`, `feature_engineering.py`, `visualisation.py` and `traffic_analytics.py` use module-level loggers through `logging.getLogger(__name__)` and reuse the central logging configuration.

### Logging Outputs

Log messages are displayed in the console and written to:

`logs/project.log`

### Logging Format

Each log message includes:

- Timestamp
- Logging level
- Module name
- Log message

### Logging Levels

- **DEBUG:** Detailed diagnostic information, such as feature scaling thresholds and congestion category thresholds.
- **INFO:** Successful loading, validation, processing, saving and execution events.
- **WARNING:** Data modifications, duplicate removal, invalid data handling and imputation.
- **ERROR:** Pipeline failures, exceptions and unsuccessful operations.

### Logging Implementation

The main entry point, `main.py`, initialises the logging configuration before executing the project modules.

The modules reuse the central logging setup rather than configuring independent logging handlers. This ensures consistent logging output across the project.

The `traffic_analytics.py` module also reuses the central logging configuration when executed directly through its command-line interface.

## Reproducing the Results

1. Install Python 3.13.11.
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Place the original CSV dataset in `data/raw/`.
4. Open a terminal in the project folder.
5. Run the complete pipeline:

```bash
python main.py
```

6. The cleaned dataset will be saved in `data/processed/`.
7. The feature-engineered dataset will be saved in `data/processed/metro_traffic_features.csv`.
8. Visualisation files will be generated in `figures/`.
9. Project execution logs will be recorded in `logs/project.log`.

## Command-Line Traffic Analytics

The `traffic_analytics.py` module provides command-line queries using argparse.

Examples:

### Query Traffic Volume by Date and Hour

```bash
python traffic_analytics.py date --date 2018-09-30 --hour 16
```

### Query Peak Traffic Hours

```bash
python traffic_analytics.py peak
```

### Compare Weekday and Weekend Traffic

```bash
python traffic_analytics.py compare
```

### Query Traffic by Weather Condition

```bash
python traffic_analytics.py weather --condition Rain
```

The command-line interface supports input validation and logging of command execution and data loading activities.

## Data Cleaning Assumptions and Limitations

- Temperature readings of 0 Kelvin are treated as null/invalid sensor readings.
- Rainfall readings exceeding 9,000 mm are treated as physically unrealistic outliers.
- Missing temperature and rainfall values resulting from these checks are imputed using monthly median values.
- Duplicate records are identified based on identical values across all columns.
- Rows with invalid or missing `date_time` values are removed.
- The pipeline focuses on data preparation, feature engineering and descriptive analysis rather than predictive modelling.
- Monthly median imputation assumes that observations within the same calendar month provide a reasonable reference for replacing invalid readings.

## Final Cleaned Dataset

The cleaned dataset contains 48,187 records and 9 columns after removing 17 duplicate rows and handling identified invalid readings.

The original raw dataset is retained separately from the processed output.

---

## Task 2 - Feature Engineering (NumPy and Pandas)

The cleaned traffic dataset was used to create additional features for machine learning analysis.

### 1. Time Features

The following time-related features were created:

- `hour`: Hour of the day.
- `day_of_week`: Day of the week.
- `is_weekend`: Indicator for weekend observations.
- `hour_sin` and `hour_cos`: Cyclical encoding of the hour to represent the repeating 24-hour cycle.

### 2. Weather Features

- Weather categorical variables were converted into numerical features using one-hot encoding.
- An `is_adverse_weather` indicator was created to identify adverse weather conditions.

### 3. Numerical Features

Min-Max scaling was applied to:

- `temp`: Temperature.
- `rain_1h`: Rainfall in the previous hour.

The scaled variables are stored as `temp_scaled` and `rain_1h_scaled`.

### 4. Congestion Category

A data-driven `congestion_category` target was created using traffic volume percentiles:

- **Low:** Traffic volume at or below the 33rd percentile (2,157).
- **Medium:** Traffic volume above the 33rd percentile and at or below the 67th percentile (4,585.62).
- **High:** Traffic volume above the 67th percentile.

### 5. Output

The feature-engineered dataset is saved as:

`data/processed/metro_traffic_features.csv`

The final dataset contains 48,187 rows and 29 columns.

---

## Task 3 - Visualisation

Visualisations were generated using Matplotlib to explore traffic patterns and relationships within the dataset.

The following visualisations were produced:

1. Average traffic volume by hour.
2. Weekday versus weekend traffic patterns.
3. Temperature versus traffic volume.

The visualisation files are saved in the `figures/` directory.

---

## Task 5 - Logging Implementation

Centralised logging was implemented to monitor the execution of the data pipeline, feature engineering, visualisation and command-line analytics modules.

The logging configuration is defined in `main.py`, with individual modules using module-level loggers.

Log messages are written to both the console and `logs/project.log`.

The implementation supports:

- Centralised logging configuration.
- Consistent log formatting.
- Multiple logging levels.
- File and console logging.
- Logging of processing activities and data-quality issues.
- Exception and error logging.
- Logging across multiple modules.
- Logging of command-line analytics execution.

The logging implementation was tested through both the main project pipeline and the standalone traffic analytics app.

## Reports and Documentation

- [Smart City Mobility Analytics Report](Smart%20City%20Mobility%20Analytics%20Report.pdf) – Report covering SQL-based traffic analysis, trends, probability analysis and key findings.
