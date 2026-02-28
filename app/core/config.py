# app/core/config.py

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Settings:
    # ==============================
    # Groww Base URLs
    # ==============================

    GROWW_SEARCH_BASE_URL: str = os.getenv(
        "GROWW_SEARCH_BASE_URL"
    )

    GROWW_DERIVATIVE_BASE_URL: str = os.getenv(
        "GROWW_DERIVATIVE_BASE_URL"
    )

    GROWW_AGGREGATED_BASE_URL: str = os.getenv(
        "GROWW_AGGREGATED_BASE_URL"
    )

    # ==============================
    # System Config
    # ==============================

    POLL_INTERVAL: int = int(os.getenv("POLL_INTERVAL", 3))
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", 10))

    # ==============================
    # CORS
    # ==============================

    CORS_ORIGINS: list[str] = os.getenv(
        "CORS_ORIGINS",
        ""
    ).split(",")


settings = Settings()