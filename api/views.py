"""
Copyright (c) 2024 eContriver LLC

This file is part of Capital Copilot by eContriver LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

import json
import os

from django.http import JsonResponse
from openbb import obb
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(["GET", "POST"])
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
            df_json = json.loads(historical_data.to_df().to_json())
            response_data = {
                "success": True,
                "data": df_json,
                "ticker": ticker,
            }
        except Exception as e:
            response_data = {"success": False, "message": f"No matches found for: {ticker}: {e}"}

    else:
        response_data = {"success": False, "message": "No ticker provided"}

    return JsonResponse(response_data)
