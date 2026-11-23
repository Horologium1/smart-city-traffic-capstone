import pandas as pd
import matplotlib.pyplot as plt
import logging
from pathlib import Path
import sys

# Configure module logger
logger = logging.getLogger(__name__)

# File paths
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "processed" / "metro_traffic_features.csv"
FIGURE_DIR = BASE_DIR / "figures"


# Main visualisation execution
def main():

    logger.info("Visualisation process started.")

    try:

        # Create figures directory
        FIGURE_DIR.mkdir(parents=True, exist_ok=True)

        # Load feature-engineered dataset
        df = pd.read_csv(DATA_PATH)

        logger.info(
            "Feature-engineered dataset loaded successfully: "
            "%d rows and %d columns.",
            df.shape[0],
            df.shape[1]
        )

        # --------------------------------------------------
        # Visualisation 1: Average Traffic by Hour
        # --------------------------------------------------

        hourly_traffic = df.groupby("hour")["traffic_volume"].mean()

        plt.figure(figsize=(10, 6))
        plt.plot(hourly_traffic.index, hourly_traffic.values, marker="o")
        plt.title("Average Traffic Volume by Hour")
        plt.xlabel("Hour of Day")
        plt.ylabel("Average Traffic Volume")
        plt.xticks(range(0, 24))
        plt.grid(True)
        plt.tight_layout()

        file_path = FIGURE_DIR / "traffic_by_hour.png"
        plt.savefig(file_path)
        plt.close()

        logger.info("Figure saved successfully: %s", file_path)

        # --------------------------------------------------
        # Visualisation 2: Weekday vs Weekend Traffic
        # --------------------------------------------------

        weekend_traffic = df.groupby("is_weekend")["traffic_volume"].mean()

        labels = ["Weekday", "Weekend"]

        plt.figure(figsize=(8, 6))
        plt.bar(labels, weekend_traffic.values)
        plt.title("Average Traffic: Weekday vs Weekend")
        plt.xlabel("Day Type")
        plt.ylabel("Average Traffic Volume")
        plt.tight_layout()

        file_path = FIGURE_DIR / "weekday_vs_weekend.png"
        plt.savefig(file_path)
        plt.close()

        logger.info("Figure saved successfully: %s", file_path)

        # --------------------------------------------------
        # Visualisation 3: Temperature vs Traffic
        # --------------------------------------------------

        temperature_celsius = df["temp"] - 273.15

        plt.figure(figsize=(10, 6))
        plt.scatter(
            temperature_celsius,
            df["traffic_volume"],
            alpha=0.3
        )
        plt.title("Temperature vs Traffic Volume")
        plt.xlabel("Temperature (Celsius)")
        plt.ylabel("Traffic Volume")
        plt.tight_layout()

        file_path = FIGURE_DIR / "temperature_vs_traffic.png"
        plt.savefig(file_path)
        plt.close()

        logger.info("Figure saved successfully: %s", file_path)

        logger.info("All visualisations completed successfully.")

        return 0

    except (FileNotFoundError, pd.errors.ParserError, OSError, ValueError):
        logger.error(
            "Visualisation process failed.",
            exc_info=True
        )
        return 1

    except Exception:
        logger.error(
            "Unexpected error during visualisation.",
            exc_info=True
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())