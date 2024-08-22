"""
Copyright (c) 2024 Perpetuator LLC

This file is part of Capital Copilot by Perpetuator LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

import logging
import os
import sys

from openbb import obb

from copilot.copilot_shared import process_env


def main():
    process_env()
    logging.getLogger().setLevel(logging.DEBUG)
    logging.info("main")
    ticker = sys.argv[1] if len(sys.argv) > 1 else "MSFT"
    logging.debug(f"Loading ticker: {ticker}")

    obb.user.credentials.alpha_vantage_api_key = os.getenv("FMP_API_KEY")
    earnings_data = obb.equity.calendar.earnings(ticker, provider="fmp")
    # obb.user.credentials.alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    # earnings_data = obb.equity.calendar.earnings(ticker, provider="alpha_vantage")
    logging.debug(earnings_data)


if __name__ == "__main__":
    try:
        print("starting main")
        main()
        # time.sleep(10)
    except Exception as e:
        logging.exception(f"main caught exception: {e}", exc_info=e)
        sys.exit(1)
