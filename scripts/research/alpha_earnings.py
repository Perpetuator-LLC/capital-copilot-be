"""
Copyright (c) 2024 Perpetuator LLC

This file is part of Capital Copilot by Perpetuator LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

import csv
import logging
import os
import sys

import pandas as pd
import requests

from copilot.copilot_shared import process_env


def main():
    process_env()
    logging.getLogger().setLevel(logging.DEBUG)
    symbol = sys.argv[1] if len(sys.argv) > 1 else "MSFT"
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    CSV_URL = (
        f"https://www.alphavantage.co/query"
        f"?function=EARNINGS_CALENDAR"
        f"&horizon=12month"
        f"&symbol={symbol}"
        f"&apikey={api_key}"
    )

    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode("utf-8")
        cr = csv.reader(decoded_content.splitlines(), delimiter=",")
        my_list = list(cr)

    # Convert list to DataFrame
    columns = my_list[0]
    data = my_list[1:]
    earnings_df = pd.DataFrame(data, columns=columns)
    logging.info(earnings_df)


if __name__ == "__main__":
    try:
        print("starting main")
        main()
        # time.sleep(10)
    except Exception as e:
        logging.exception(f"main caught exception: {e}", exc_info=e)
        sys.exit(1)
