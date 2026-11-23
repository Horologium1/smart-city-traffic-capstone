import pandas as pd
import numpy as np
import logging
from pathlib import Path
import sys

# Configure project paths
BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "metro_traffic_cleaned.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "metro_traffic_features.csv"

# Configure module logger
logger = logging.getLogger(__name__)


# Load cleaned dataset
def load_cleaned_data():

    try:
        df = pd.read_csv(INPUT_FILE)

        # Convert date_time to datetime
        df["date_time"] = pd.to_datetime(
            df["date_time"],
            errors="coerce"
        )

        logger.info(
            "Cleaned dataset loaded successfully: %d rows and %d columns.",
            df.shape[0],
            df.shape[1]
        )

        logger.info(
            "Dataset shape before feature engineering: %d rows and %d columns.",
            df.shape[0],
            df.shape[1]
        )

        return df

    except (FileNotFoundError, pd.errors.ParserError, OSError, ValueError):
        logger.error(
            "Unable to load or parse the cleaned dataset.",
            exc_info=True
        )
        raise


# Create time-based features
def create_time_features(df):

    # Extract hour of the day (0 to 23)
    df["hour"] = df["date_time"].dt.hour

    # Extract day of the week
    # Monday = 0, Sunday = 6
    df["day_of_week"] = df["date_time"].dt.dayofweek

    # Identify weekends
    # Saturday = 5, Sunday = 6
    df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

    # Cyclical encoding of hour
    df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)

    df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)

    logger.info(
        "Time features created: hour, day_of_week, is_weekend, "
        "hour_sin and hour_cos."
    )

    return df


# Create weather-based features
def create_weather_features(df):

    # One-hot encode weather conditions
    weather_encoded = pd.get_dummies(
        df["weather_main"],
        prefix="weather",
        dtype=int
    )

    # Add encoded columns to the dataset
    df = pd.concat([df, weather_encoded], axis=1)

    # Identify adverse weather conditions
    adverse_conditions = [
        "Rain",
        "Drizzle",
        "Snow",
        "Fog",
        "Mist",
        "Haze",
        "Thunderstorm",
        "Squall",
        "Smoke"
    ]

    df["is_adverse_weather"] = (
        df["weather_main"]
        .isin(adverse_conditions)
        .astype(int)
    )

    logger.info(
        "Weather features created: %d one-hot encoded columns "
        "and is_adverse_weather indicator.",
        len(weather_encoded.columns)
    )

    return df


# Scale numerical features using Min-Max scaling
def scale_numerical_features(df):

    numerical_columns = ["temp", "rain_1h"]

    for column in numerical_columns:

        minimum = df[column].min()
        maximum = df[column].max()

        # Log intermediate values at DEBUG level
        logger.debug(
            "%s scaling thresholds: minimum=%s, maximum=%s",
            column,
            minimum,
            maximum
        )

        # Apply Min-Max scaling
        if maximum != minimum:

            df[column + "_scaled"] = (
                (df[column] - minimum) / (maximum - minimum)
            )

        else:
            df[column + "_scaled"] = 0

        logger.info(
            "Min-Max scaling completed for '%s'.",
            column
        )

    logger.info("Numerical feature scaling completed.")

    return df


# Create data-driven congestion category
def create_congestion_category(df):

    # Calculate percentile thresholds
    lower_threshold = df["traffic_volume"].quantile(0.33)
    upper_threshold = df["traffic_volume"].quantile(0.67)

    # Log thresholds at DEBUG level
    logger.debug(
        "Congestion thresholds: 33rd percentile = %.2f, "
        "67th percentile = %.2f",
        lower_threshold,
        upper_threshold
    )

    # Assign congestion categories
    conditions = [
        df["traffic_volume"] <= lower_threshold,
        df["traffic_volume"] <= upper_threshold
    ]

    categories = ["Low", "Medium"]

    df["congestion_category"] = np.select(
        conditions,
        categories,
        default="High"
    )

    logger.info(
        "Congestion categories created using 33rd and 67th percentile thresholds."
    )

    logger.info(
        "Congestion category distribution: %s",
        df["congestion_category"].value_counts().to_dict()
    )

    return df


# Save feature-engineered dataset
def save_feature_engineered_data(df):

    try:
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(OUTPUT_FILE, index=False)

        logger.info(
            "Feature-engineered dataset saved successfully: "
            "%d rows and %d columns. File: %s",
            df.shape[0],
            df.shape[1],
            OUTPUT_FILE
        )

    except OSError:
        logger.error(
            "Unable to save feature-engineered dataset.",
            exc_info=True
        )
        raise


# Main feature engineering execution
def main():

    logger.info("Feature engineering process started.")

    try:

        df = load_cleaned_data()

        df = create_time_features(df)

        df = create_weather_features(df)

        df = scale_numerical_features(df)

        df = create_congestion_category(df)

        # Log final dataset shape
        logger.info(
            "Dataset shape after feature engineering: %d rows and %d columns.",
            df.shape[0],
            df.shape[1]
        )

        # Save feature-engineered dataset
        save_feature_engineered_data(df)

        logger.info(
            "All feature engineering steps completed successfully."
        )

        return 0

    except Exception:
        logger.error(
            "Feature engineering process failed.",
            exc_info=True
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())