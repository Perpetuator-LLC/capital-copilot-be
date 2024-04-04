# ------------------------------------------------------------------------------
# Copyright (c) 2024 eContriver LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# ------------------------------------------------------------------------------

import logging
import os
import sys

from openbb import obb

from copilot.copilot_shared import process_env
from copilot.logging_service import LoggingService


def main():
    process_env()
    LoggingService.configure_logging({"stdout": logging.DEBUG})
    ticker = sys.argv[1] if len(sys.argv) > 1 else "MSFT"
    logging.debug(f"Loading ticker: {ticker}")

    obb.user.credentials.alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    historical_data = obb.equity.price.historical(symbol=ticker, provider="alpha_vantage")  # start_date="1990-01-01",
    indicators = dict(
        bbands=dict(length=20, std=2),
        kc=dict(length=20),
    )
    historical_data.charting.to_chart(**{"indicators": indicators}, render=True)
    historical_data.chart.fig.update_layout(
        height=600,
        template="plotly_dark",  # Start with a dark theme
        plot_bgcolor="rgba(0,0,0,0)",  # Transparent plot background
        paper_bgcolor="rgba(0,0,0,0)",  # Dark paper background
        # paper_bgcolor="#1e2124",  # Dark paper background
        font=dict(color="#d8d9da"),  # Light grey text
        # legend=dict(
        #     x=0,  # Aligns legend to the left
        #     y=1,  # Aligns legend to the top
        #     bgcolor="rgba(0,0,0,0)",  # Transparent background
        #     bordercolor="#d8d9da",  # Light grey border
        #     font=dict(
        #         color="#d8d9da"  # Light grey text
        #     )
        # ),
        # hovermode='x unified',
        # modebar_orientation='h',
        margin=dict(l=300, r=0, t=100, b=0),
    )
    historical_data.chart.fig.to_html(full_html=False)  # , include_plotlyjs='cdn')


if __name__ == "__main__":
    try:
        main()
        # time.sleep(10)
    except Exception as e:
        logging.error(f"main caught exception: {e}", exc_info=e)
        sys.exit(1)
