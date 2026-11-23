
import pandas as pd
import logging
import argparse
from datetime import datetime
from pathlib import Path
import sys

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "processed" / "metro_traffic_features.csv"


def load_data():
    try:
        df = pd.read_csv(DATA_FILE)
        df["date_time"] = pd.to_datetime(df["date_time"])
        logger.info("Processed traffic dataset loaded successfully.")
        return df

    except Exception as e:
        logger.error("Failed to load traffic dataset: %s", e, exc_info=True)
        raise


def query_date(df, date, hour):
    try:
        datetime.strptime(date, "%Y-%m-%d")

        if hour < 0 or hour > 23:
            raise ValueError("Hour must be between 0 and 23.")

        logger.info(
            "Command invoked: date | arguments: date=%s, hour=%s",
            date, hour
        )

        result = df[
            (df["date_time"].dt.strftime("%Y-%m-%d") == date) &
            (df["hour"] == hour)
        ]

        if result.empty:
            print("No traffic data found for the specified date and hour.")
        else:
            print(
                result[[
                    "date_time",
                    "traffic_volume",
                    "weather_main",
                    "weather_description"
                ]].to_string(index=False)
            )

    except ValueError as e:
        logger.error("Invalid date or hour input: %s", e)


def query_peak(df):
    logger.info("Command invoked: peak")

    result = (
        df.groupby("hour")["traffic_volume"]
        .mean()
        .sort_values(ascending=False)
        .head(5)
    )

    print("\nTop 5 busiest hours (average traffic):")
    print(result.round(2))


def compare_weekday_weekend(df):
    logger.info("Command invoked: compare")

    result = df.groupby("is_weekend")["traffic_volume"].mean()

    print("\nAverage traffic comparison:")
    print("Weekday:", round(result.get(0, 0), 2))
    print("Weekend:", round(result.get(1, 0), 2))


def query_weather(df, weather):
    logger.info(
        "Command invoked: weather | arguments: weather=%s",
        weather
    )

    result = df[
        df["weather_main"].str.lower() == weather.lower()
    ]

    if result.empty:
        print("No records found for this weather condition.")
    else:
        print("\nAverage traffic under", weather, "weather:")
        print(round(result["traffic_volume"].mean(), 2))
        print("Number of records:", len(result))


def main():

    # Reuse centralized logging configuration
    from main import configure_logging
    configure_logging()

    logger.info("Traffic analytics application started.")

    parser = argparse.ArgumentParser(
        description="Mini Traffic Analytics Application"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    # Date query
    date_parser = subparsers.add_parser("date")
    date_parser.add_argument("--date", required=True)
    date_parser.add_argument("--hour", type=int, required=True)

    # Peak traffic query
    subparsers.add_parser("peak")

    # Weekday/weekend comparison
    subparsers.add_parser("compare")

    # Weather query
    weather_parser = subparsers.add_parser("weather")
    weather_parser.add_argument("--condition", required=True)

    args = parser.parse_args()

    try:
        df = load_data()

        if args.command == "date":
            query_date(df, args.date, args.hour)

        elif args.command == "peak":
            query_peak(df)

        elif args.command == "compare":
            compare_weekday_weekend(df)

        elif args.command == "weather":
            query_weather(df, args.condition)

        return 0

    except Exception as e:
        logger.error("Traffic analytics application failed: %s", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
