import os

import sentry_sdk
from dotenv import load_dotenv

load_dotenv()


sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    send_default_pii=True,
    max_request_body_size="always",
    traces_sample_rate=1.0,
)


# --- Test Error ---
def trigger_test_error():
    try:
        # This will fail on purpose
        1 / 0  # type: ignore
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print("Test error sent to Sentry.")


if __name__ == "__main__":
    dsn = os.getenv("SENTRY_DSN")
    if not dsn:
        print("SENTRY_DSN not found in env!")
    trigger_test_error()
