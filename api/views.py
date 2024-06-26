"""
Copyright (c) 2024 eContriver LLC

This file is part of Capital Copilot by eContriver LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

import os

from django.http import JsonResponse
from openbb import obb
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api(request):
    """
    Return chart data as JSON instead of rendering HTML.
    """
    response_data = {}
    ticker = request.data.get("ticker").upper() if request.method == "POST" else "TSLA"

    if ticker:
        try:
            obb.user.credentials.alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
            historical_data = obb.equity.price.historical(symbol=ticker, provider="alpha_vantage")
            df = historical_data.to_df()

            df["BB_upper"], df["BB_middle"], df["BB_lower"] = obb.ta.bbands(df["close"], length=20, std=2)
            # Prepare OHLC and Volume data
            ohlc_data = []
            volume_data = []

            for timestamp, row in df.iterrows():
                date = timestamp
                ohlc_data.append({"x": date, "y": [row["open"], row["high"], row["low"], row["close"]]})
                volume_data.append({"x": date, "y": row["volume"]})

            response_data = {
                "success": True,
                "ohlc": ohlc_data,
                "volume": volume_data,
                "ticker": ticker,
            }

        except Exception as e:
            response_data = {"success": False, "message": f"Failed to load data for '{ticker}': {e}"}

    else:
        response_data = {"success": False, "message": "No ticker provided"}

    return JsonResponse(response_data)
