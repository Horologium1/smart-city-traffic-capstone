import logging
from pathlib import Path
import sys

# Create logs directory
BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "project.log"


# Central logging configuration
def configure_logging():

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(LOG_FILE, encoding="utf-8")
        ],
        force=True
    )


# Main project execution
def main():

    configure_logging()

    logger = logging.getLogger(__name__)

    logger.info("Traffic analytics project started.")
    logger.info("Central logging configuration initialized.")

    # --------------------------------------------------
    # Step 1: Data cleaning pipeline
    # --------------------------------------------------

    from pipeline import main as run_pipeline

    logger.info("Starting data cleaning pipeline.")

    result = run_pipeline()

    if result != 0:
        logger.error("Data cleaning pipeline failed.")
        return result

    logger.info("Data cleaning pipeline completed successfully.")

    # --------------------------------------------------
    # Step 2: Feature engineering
    # --------------------------------------------------

    from feature_engineering import main as run_feature_engineering

    logger.info("Starting feature engineering process.")

    result = run_feature_engineering()

    if result != 0:
        logger.error("Feature engineering process failed.")
        return result

    logger.info("Feature engineering process completed successfully.")

    # --------------------------------------------------
    # Step 3: Visualizations
    # --------------------------------------------------

    from visualizations import main as run_visualizations

    logger.info("Starting visualizations process.")

    result = run_visualizations()

    if result != 0:
        logger.error("Visualizations process failed.")
        return result

    logger.info("Visualizations process completed successfully.")

    # --------------------------------------------------
    # Project completion
    # --------------------------------------------------

    logger.info("All project processes completed successfully.")
    logger.info("Traffic analytics project completed.")

    return 0


if __name__ == "__main__":
    sys.exit(main())