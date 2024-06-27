"""
Copyright (c) 2024 eContriver LLC

This file is part of Capital Copilot by eContriver LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

import os

import graphene
from openbb import obb


class OHLCData(graphene.ObjectType):
    x = graphene.DateTime()
    y = graphene.List(graphene.Float)


class VolumeData(graphene.ObjectType):
    x = graphene.DateTime()
    y = graphene.Float()


class SqueezeData(graphene.ObjectType):
    x = graphene.DateTime()
    y = graphene.List(graphene.Float)


class ChartData(graphene.ObjectType):
    success = graphene.Boolean()
    message = graphene.String()
    ohlc = graphene.List(OHLCData)
    volume = graphene.List(VolumeData)
    squeeze = graphene.List(SqueezeData)
    ticker = graphene.String()


def resolve_get_chart_data(self, info, ticker):
    user = info.context.user
    if not user or not user.is_authenticated:
        raise Exception("Authentication credentials were not provided or are invalid")

    ticker = ticker.upper()

    if ticker:
        try:
            # Assuming 'obb' is defined and setup elsewhere to use Alpha Vantage API
            obb.user.credentials.alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
            historical_data = obb.equity.price.historical(symbol=ticker, provider="alpha_vantage")
            df = historical_data.to_df()

            # Prepare OHLC, Volume, and Squeeze data
            ohlc_data = []
            volume_data = []
            squeeze_data = []

            # Assuming squeeze function is correctly imported and used
            df.ta.squeeze(append=True)
            df.fillna(0, inplace=True)  # Replace NaN with 0
            # squeeze_result = df.ta.squeeze()
            # squeeze_result.fillna(0, inplace=True)  # Replace NaN with 0
            for timestamp, row in df.iterrows():
                ohlc_data.append(OHLCData(x=timestamp, y=[row["open"], row["high"], row["low"], row["close"]]))
                volume_data.append(VolumeData(x=timestamp, y=row["volume"]))
                squeeze_data.append(
                    SqueezeData(
                        x=timestamp,
                        y=[row["SQZ_ON"], row["SQZ_20_2.0_20_1.5"]],
                        # y=[squeeze_result.at[timestamp, "SQZ_ON"], squeeze_result.at[timestamp, "SQZ_20_2.0_20_1.5"]],
                    )
                )

            return ChartData(success=True, ohlc=ohlc_data, volume=volume_data, squeeze=squeeze_data, ticker=ticker)

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
