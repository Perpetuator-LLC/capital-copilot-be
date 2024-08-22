"""
Copyright (c) 2024 Perpetuator LLC

This file is part of Capital Copilot by Perpetuator LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

import csv
import os

import graphene
import pandas as pd
import requests
from openbb import obb
from pandas.core.frame import DataFrame


class OHLCData(graphene.ObjectType):
    x = graphene.DateTime()
    y = graphene.List(graphene.Float)


class VolumeData(graphene.ObjectType):
    x = graphene.DateTime()
    y = graphene.Float()


class SqueezeData(graphene.ObjectType):
    x = graphene.DateTime()
    y = graphene.List(graphene.Float)


class KcData(graphene.ObjectType):
    x = graphene.DateTime()
    y = graphene.List(graphene.Float)


class EarningsData(graphene.ObjectType):
    symbol = graphene.String()
    name = graphene.String()
    reportDate = graphene.DateTime()
    fiscalDateEnding = graphene.DateTime()
    estimate = graphene.Float()
    currency = graphene.String()


class GraphQLData(graphene.ObjectType):
    success = graphene.Boolean()
    message = graphene.String()


class ChartData(GraphQLData):
    ohlc = graphene.List(OHLCData)
    volume = graphene.List(VolumeData)
    squeeze = graphene.List(SqueezeData)
    kc = graphene.List(KcData)
    earnings = graphene.List(EarningsData)
    ticker = graphene.String()


class TickerData(graphene.ObjectType):
    symbol = graphene.String()
    name = graphene.String()
    cik = graphene.String()


class Autocomplete(GraphQLData):
    results = graphene.List(TickerData)


def resolve_get_autocomplete(self, info, query) -> Autocomplete:
    user = info.context.user
    if not user or not user.is_authenticated:
        raise Exception("Authentication credentials were not provided or are invalid")

    query = query.upper()

    if query:
        try:
            response = obb.equity.search(query)  # type: ignore

            return Autocomplete(success=True, results=response.results)

        except Exception as e:
            return Autocomplete(success=False, message=f"Failed to load data for '{query}': {e}")

    else:
        return Autocomplete(success=False, message="No query provided")


def resolve_get_chart_data(self, info, ticker):
    user = info.context.user
    if not user or not user.is_authenticated:
        raise Exception("Authentication credentials were not provided or are invalid")

    ticker = ticker.upper()

    if ticker:
        try:
            # Assuming 'obb' is defined and setup elsewhere to use Alpha Vantage API
            alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
            obb.user.credentials.alpha_vantage_api_key = alpha_vantage_api_key
            historical_data = obb.equity.price.historical(symbol=ticker, provider="alpha_vantage")
            df = historical_data.to_df()

            # Prepare OHLC, Volume, and Squeeze data
            ohlc_data = []
            volume_data = []
            squeeze_data = []
            kc_data = []

            earnings_df = get_earnings_dates(ticker, alpha_vantage_api_key)
            earnings_data = parse_earnings_data(earnings_df)

            df.ta.kc(append=True, scalar=1)
            df.ta.kc(append=True, scalar=2)
            df.ta.kc(append=True, scalar=3)

            # Assuming squeeze function is correctly imported and used
            df.ta.squeeze(append=True)
            df.fillna(0, inplace=True)  # Replace NaN with 0
            for timestamp, row in df.iterrows():
                ohlc_data.append(OHLCData(x=timestamp, y=[row["open"], row["high"], row["low"], row["close"]]))
                volume_data.append(VolumeData(x=timestamp, y=row["volume"]))
                squeeze_data.append(
                    SqueezeData(
                        x=timestamp,
                        y=[row["SQZ_ON"], row["SQZ_20_2.0_20_1.5"]],
                    )
                )
                kc_data.append(
                    KcData(
                        x=timestamp,
                        y=[
                            row["KCLe_20_1.0"],
                            row["KCBe_20_1.0"],
                            row["KCUe_20_1.0"],
                            row["KCLe_20_2.0"],
                            row["KCBe_20_2.0"],
                            row["KCUe_20_2.0"],
                            row["KCLe_20_3.0"],
                            row["KCBe_20_3.0"],
                            row["KCUe_20_3.0"],
                        ],
                    )
                )

            return ChartData(
                success=True,
                ohlc=ohlc_data,
                volume=volume_data,
                squeeze=squeeze_data,
                kc=kc_data,
                ticker=ticker,
                earnings=earnings_data,
            )

        except Exception as e:
            return ChartData(success=False, message=f"Failed to load data for '{ticker}': {e}")

    else:
        return ChartData(success=False, message="No ticker provided")


def parse_earnings_data(earnings_df: DataFrame) -> list[EarningsData]:
    earnings_data: list[EarningsData] = []
    for index, row in earnings_df.iterrows():
        data = EarningsData(
            symbol=row["symbol"],
            name=row["name"],
            reportDate=pd.to_datetime(row["reportDate"]),
            fiscalDateEnding=pd.to_datetime(row["fiscalDateEnding"]),
            estimate=float(row["estimate"]) if row["estimate"] else None,
            currency=row["currency"],
        )
        earnings_data.append(data)
    return earnings_data


def get_earnings_dates(symbol, api_key):
    try:
        # Cannot use the obb.equity.calendar.earnings function because it only supports the "fmp" provider
        # See: .venv/lib/python3.11/site-packages/openbb/package/equity.py
        # NOTE: This API seems to work with the API key: "fake_api_key"
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
        return earnings_df
    except Exception as e:
        print(f"Error fetching earnings dates: {e}")
        return None


class Query(graphene.ObjectType):
    get_chart_data = graphene.Field(
        ChartData,
        ticker=graphene.String(required=True),
        resolver=resolve_get_chart_data,  # Connect the resolver to the field
    )
    get_autocomplete = graphene.Field(
        Autocomplete,
        query=graphene.String(required=True),
        resolver=resolve_get_autocomplete,  # Connect the resolver to the field
    )


schema = graphene.Schema(query=Query)
