import logging
import os

import sentry_sdk
from dotenv import load_dotenv
from sentry_sdk.integrations.logging import EventHandler

load_dotenv()


sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    send_default_pii=True,
    max_request_body_size="always",
    traces_sample_rate=1.0,
)

# Create the Sentry logging handler
sentry_handler = EventHandler(level=logging.ERROR)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        sentry_handler,  # <--- sends errors from logger to Sentry
    ],
)
logger = logging.getLogger("main.py")


# --- Test Error ---
def trigger_test_error():
    try:
        # This will fail on purpose
        1 / 0  # type: ignore
    except Exception as e:
        logger.error(e)
        print("Test error sent to Sentry.")


if __name__ == "__main__":
    dsn = os.getenv("SENTRY_DSN")
    if not dsn:
        print("SENTRY_DSN not found in env!")
    trigger_test_error()
