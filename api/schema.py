"""
Copyright (c) 2024 eContriver LLC

This file is part of Capital Copilot by eContriver LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

import os

import graphene
import openbb


class OHLCData(graphene.ObjectType):
    x = graphene.DateTime()
    y = graphene.List(graphene.Float)


class VolumeData(graphene.ObjectType):
    x = graphene.DateTime()
    y = graphene.Float()


class ChartData(graphene.ObjectType):
    success = graphene.Boolean()
    message = graphene.String()
    ohlc = graphene.List(OHLCData)
    volume = graphene.List(VolumeData)
    ticker = graphene.String()


def resolve_get_chart_data(self, info, ticker):
    user = info.context.user
    if not user or not user.is_authenticated:
        raise Exception("Authentication credentials were not provided or are invalid")

    ticker = ticker.upper()

    if ticker:
        try:
            openbb.obb.user.credentials.alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
            historical_data = openbb.obb.equity.price.historical(symbol=ticker, provider="alpha_vantage")
            df = historical_data.to_df()

            # Prepare OHLC and Volume data
            ohlc_data = []
            volume_data = []

            for timestamp, row in df.iterrows():
                date = timestamp
                ohlc_data.append(OHLCData(x=date, y=[row["open"], row["high"], row["low"], row["close"]]))
                volume_data.append(VolumeData(x=date, y=row["volume"]))

            return ChartData(success=True, ohlc=ohlc_data, volume=volume_data, ticker=ticker)

        except Exception as e:
            return ChartData(success=False, message=f"Failed to load data for '{ticker}': {e}")

    else:
        return ChartData(success=False, message="No ticker provided")


class Query(graphene.ObjectType):
    get_chart_data = graphene.Field(
        ChartData,
        ticker=graphene.String(required=True),
        resolver=resolve_get_chart_data,  # Connect the resolver to the field
    )


schema = graphene.Schema(query=Query)
