\# Metro Interstate Traffic Volume - Python Data Pipeline



\## Short Project Overview



This project seeks to develop a Python-based data pipeline to load, validate, clean and prepare the Metro\_Interstate\_Traffic\_Volume dataset for further analysis.



Python and pandas with logging are used by the pipeline to record processing activities, data-quality issues and errors.





\## Project / Repository Structure



```text

part2\_python/

│

├── data/

│   ├── raw/

│   └── processed/

│       └── metro\_traffic\_cleaned.csv

│

├── logs/

│   └── pipeline.log

│

├── pipeline.py

├── requirements.txt

└── README.md

```





\## Requirements \& Tools used



\- Python 3.13.11

\- pandas





\## Instructions on how to run



Place the original CSV file in data/raw/.



Open a terminal in the project folder.



Run:



python pipeline.py



The cleaned dataset will be saved in data/processed/ and pipeline execution logs will be recorded in logs/pipeline.log.





\## Data Cleaning Process



The pipeline performs the following operations:

1\. Loads the raw CSV file.

2\. Validates the expected dataset columns.

3\. Standardises categorical values by removing leading and trailing spaces.

4\. Parses and validates date/time values.

5\. Identifies and removes duplicate records.

6\. Replaces impossible temperature readings of 0 Kelvin with missing values.

7\. Replaces rainfall readings exceeding 9,000 mm with missing values.

8\. Imputes missing temperature and rainfall values using monthly medians.

9\. Saves the cleaned dataset.

10\. Performs final data-quality validation.





\## Logging Configuration



Python's logging module is used to monitor pipeline execution and record:



Logging levels:

\- INFO: Successful loading, validation and processing events.

\- WARNING: Data modifications, duplicate removal and imputation.

\- ERROR: Pipeline failures and exceptions.



Log messages are displayed in the console and saved to:



logs/pipeline.log





\## Reproducing the results



1. Install Python 3.13.11.

2\. Install the required package:



```bash

pip install -r requirements.txt

```



3\. Place the original CSV file in `data/raw/`.

4\. Open a terminal in the project folder.

5\. Run:



```bash

python pipeline.py

```



6\. The cleaned dataset will be saved in `data/processed/`.

7\. The pipeline execution logs will be recorded in `logs/pipeline.log`.





\## Key Assumptions and Limitations



\- Temperature readings of 0 Kelvin are treated as null/invalid sensor readings.

\- Rainfall readings exceeding 9,000 mm are treated as physically unrealistic outliers.

\- Missing temperature and rainfall values resulting from these checks are imputed using monthly median values.

\- Duplicate records are identified based on identical values across all columns.

\- Rows with invalid or missing date\_time values are removed.

\- The pipeline focuses on data preparation and does not perform predictive modelling.

\- Monthly median imputation assumes that observations within the same calendar month provide a reasonable reference for replacing invalid readings.





\## Final Dataset



The cleaned dataset contains 48,187 records and 9 columns after removing 17 duplicate rows and handling identified invalid readings.



The original raw dataset is retained separately from the processed output.



