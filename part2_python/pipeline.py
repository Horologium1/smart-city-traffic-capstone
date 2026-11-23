import pandas as pd
import logging
import sys
from pathlib import Path

# Configure project paths
BASE_DIR = Path(__file__).resolve().parent

RAW_FILE = BASE_DIR / "data" / "raw" / "Metro_Interstate_Traffic_Volume.csv"

# Define cleaned output file
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "metro_traffic_cleaned.csv"

# Obtain module logger
logger = logging.getLogger(__name__)

# Expected dataset columns
EXPECTED_COLUMNS = [
    "holiday",
    "temp",
    "rain_1h",
    "snow_1h",
    "clouds_all",
    "weather_main",
    "weather_description",
    "date_time",
    "traffic_volume"
]


# Load raw CSV file
def load_data(file_path):

    try:
        df = pd.read_csv(file_path)

        logger.info(
            "Raw CSV successfully loaded: %d rows and %d columns",
            df.shape[0],
            df.shape[1]
        )

        return df

    except FileNotFoundError:
        logger.error(
            "Raw CSV file not found: %s",
            file_path,
            exc_info=True
        )
        raise

    except pd.errors.ParserError:
        logger.error(
            "Unable to parse CSV file.",
            exc_info=True
        )
        raise

    except OSError:
        logger.error(
            "File I/O error while loading CSV.",
            exc_info=True
        )
        raise


# Validate dataset schema
def validate_schema(df):

    missing_columns = []

    for column in EXPECTED_COLUMNS:

        if column not in df.columns:
            missing_columns.append(column)

    if missing_columns:

        logger.error(
            "Schema validation failed. Missing columns: %s",
            missing_columns
        )

        raise ValueError(
            "Dataset schema does not match expected columns."
        )

    logger.info(
        "Schema validation successful. All %d expected columns are present.",
        len(EXPECTED_COLUMNS)
    )


# Standardise categorical values
def standardise_categories(df):

    categorical_columns = [
        "holiday",
        "weather_main",
        "weather_description"
    ]

    for column in categorical_columns:

        original_values = df[column].copy()

        df[column] = df[column].apply(
            lambda x: x.strip() if isinstance(x, str) else x
        )

        changed_rows = (original_values != df[column]).sum()

        if changed_rows > 0:
            logger.warning(
                "%d rows modified in column '%s' due to "
                "removal of leading/trailing spaces.",
                changed_rows,
                column
            )

    logger.info("Categorical standardisation completed.")

    return df


# Parse and validate date/time
def validate_datetime(df):

    original_count = len(df)

    df["date_time"] = pd.to_datetime(
        df["date_time"],
        errors="coerce"
    )

    invalid_count = df["date_time"].isna().sum()

    if invalid_count > 0:

        df = df.dropna(subset=["date_time"])

        logger.warning(
            "%d rows removed due to invalid or missing date_time values.",
            invalid_count
        )

    else:
        logger.info("All date_time values are valid.")

    logger.info(
        "Date/time validation completed. %d rows retained out of %d.",
        len(df),
        original_count
    )

    return df


# Identify and remove duplicate rows
def remove_duplicates(df):

    original_count = len(df)

    duplicate_count = df.duplicated().sum()

    if duplicate_count > 0:

        df = df.drop_duplicates()

        logger.warning(
            "%d duplicate rows removed from the dataset.",
            duplicate_count
        )

    else:

        logger.info("No duplicate rows found.")

    logger.info(
        "Duplicate removal completed. %d rows retained out of %d.",
        len(df),
        original_count
    )

    return df


# Detect impossible temperature readings
def clean_temperature(df):

    invalid_count = (df["temp"] == 0).sum()

    if invalid_count > 0:

        df.loc[df["temp"] == 0, "temp"] = float("nan")

        logger.warning(
            "%d rows modified because temperature was 0 Kelvin, "
            "which is physically impossible.",
            invalid_count
        )

    else:

        logger.info("No 0 Kelvin temperature readings found.")

    logger.info("Temperature validation completed.")

    return df


# Detect unrealistic rainfall readings
def clean_rainfall(df):

    invalid_count = (df["rain_1h"] > 9000).sum()

    if invalid_count > 0:

        df.loc[df["rain_1h"] > 9000, "rain_1h"] = float("nan")

        logger.warning(
            "%d rows modified because rainfall exceeded "
            "9000 mm, which is physically unrealistic.",
            invalid_count
        )

    else:

        logger.info("No rainfall readings above 9000 mm found.")

    logger.info("Rainfall validation completed.")

    return df


# Impute missing values using monthly medians
def impute_monthly_median(df):

    # Extract month from date_time
    df["month"] = df["date_time"].dt.month

    columns_to_impute = ["temp", "rain_1h"]

    for column in columns_to_impute:

        missing_count = df[column].isna().sum()

        if missing_count > 0:

            # Calculate median for each month
            monthly_medians = df.groupby("month")[column].transform("median")

            # Replace missing values with monthly median
            df[column] = df[column].fillna(monthly_medians)

            logger.warning(
                "%d missing values in '%s' imputed using monthly medians.",
                missing_count,
                column
            )

        else:

            logger.info(
                "No missing values requiring imputation in '%s'.",
                column
            )

    # Remove temporary month column
    df = df.drop(columns=["month"])

    logger.info("Monthly median imputation completed.")

    return df


# Save cleaned dataset
def save_cleaned_data(df):

    try:
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(OUTPUT_FILE, index=False)

        logger.info(
            "Cleaned dataset successfully saved: %d rows and %d columns. File: %s",
            df.shape[0],
            df.shape[1],
            OUTPUT_FILE
        )

    except OSError:
        logger.error(
            "Unable to save cleaned dataset.",
            exc_info=True
        )
        raise


# Final data quality validation
def final_validation(df):

    missing_temp = df["temp"].isna().sum()
    missing_rain = df["rain_1h"].isna().sum()

    duplicate_count = df.duplicated().sum()

    zero_kelvin_count = (df["temp"] == 0).sum()
    rainfall_outlier_count = (df["rain_1h"] > 9000).sum()

    logger.info("Final data quality validation results:")
    logger.info("Remaining missing temperature values: %d", missing_temp)
    logger.info("Remaining missing rainfall values: %d", missing_rain)
    logger.info("Remaining duplicate rows: %d", duplicate_count)
    logger.info("Remaining zero Kelvin readings: %d", zero_kelvin_count)
    logger.info("Remaining rainfall outliers: %d", rainfall_outlier_count)

    if (
        missing_temp == 0
        and missing_rain == 0
        and duplicate_count == 0
        and zero_kelvin_count == 0
        and rainfall_outlier_count == 0
    ):
        logger.info("Final data quality validation passed.")

    else:
        logger.warning("Some data quality issues remain.")

    return df


# Main pipeline execution
def main():

    try:
        # Load raw data
        df = load_data(RAW_FILE)

        # Validate schema
        validate_schema(df)

        logger.info(
            "Initial loading and schema validation completed successfully."
        )

        # Standardise categorical values
        df = standardise_categories(df)

        # Validate date/time
        df = validate_datetime(df)

        # Remove duplicate records
        df = remove_duplicates(df)

        # Detect impossible temperature readings
        df = clean_temperature(df)

        # Detect unrealistic rainfall readings
        df = clean_rainfall(df)

        # Impute missing temperature and rainfall values
        df = impute_monthly_median(df)

        # Save cleaned dataset
        save_cleaned_data(df)

        # Perform final validation
        final_validation(df)

        logger.info("Pipeline execution completed successfully.")

    except Exception as error:

        logger.error(
            "Pipeline failed: %s",
            error,
            exc_info=True
        )

        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())