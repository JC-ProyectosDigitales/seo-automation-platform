import os
from typing import Literal


PageSpeedStrategy = Literal["mobile", "desktop"]


def get_pagespeed_api_key() -> str | None:
    value = os.getenv(
        "PAGESPEED_API_KEY",
        "",
    ).strip()

    return value or None


def get_pagespeed_strategy() -> PageSpeedStrategy:
    value = os.getenv(
        "PAGESPEED_STRATEGY",
        "mobile",
    ).strip().lower()

    if value not in {
        "mobile",
        "desktop",
    }:
        return "mobile"

    return value  # type: ignore[return-value]


def get_pagespeed_timeout() -> float:
    raw_value = os.getenv(
        "PAGESPEED_TIMEOUT",
        "90",
    ).strip()

    try:
        timeout = float(raw_value)
    except ValueError:
        return 90.0

    return max(
        10.0,
        min(timeout, 180.0),
    )


PAGESPEED_API_URL = (
    "https://www.googleapis.com/"
    "pagespeedonline/v5/runPagespeed"
)

PAGESPEED_API_KEY = get_pagespeed_api_key()
PAGESPEED_STRATEGY = get_pagespeed_strategy()
PAGESPEED_TIMEOUT = get_pagespeed_timeout()
