"""
Copyright (c) 2024 Perpetuator LLC

This file is part of Capital Copilot by Perpetuator LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

import json
from datetime import date
from unittest.mock import MagicMock, Mock, patch

from django.contrib.auth.models import User
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from api.schema import schema
from api.serializers import RegisterSerializer


class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("graphql")  # Use the correct URL name configured in urls.py
        self.valid_ticker = "AAPL"
        self.invalid_ticker = ""

        self.user = User.objects.create_user(username="testuser")
        self.user.set_password("securepassword")
        self.user.save()
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

    @patch("os.getenv")
    @patch("openbb.package.equity_price.ROUTER_equity_price.historical")
    def test_successful_data_retrieval(self, mock_historical, mock_getenv):
        # Setup Mocks
        mock_getenv.return_value = "fake_api_key"

        # Mock OpenBB response

        mock_df = Mock()
        mock_df.iterrows.return_value = [
            (
                date(2023, 1, 1),
                {
                    "open": 100,
                    "high": 110,
                    "low": 90,
                    "close": 105,
                    "volume": 1000,
                    "SQZ_ON": 1,
                    "SQZ_20_2.0_20_1.5": 0,
                    "KCLe_20_1.0": 85,
                    "KCBe_20_1.0": 102,
                    "KCUe_20_1.0": 120,
                    "KCLe_20_2.0": 80,
                    "KCBe_20_2.0": 102,
                    "KCUe_20_2.0": 125,
                    "KCLe_20_3.0": 75,
                    "KCBe_20_3.0": 102,
                    "KCUe_20_3.0": 130,
                },
            ),
            (
                date(2023, 1, 2),
                {
                    "open": 106,
                    "high": 115,
                    "low": 95,
                    "close": 110,
                    "volume": 1500,
                    "SQZ_ON": 1,
                    "SQZ_20_2.0_20_1.5": 0,
                    "KCLe_20_1.0": 85,
                    "KCBe_20_1.0": 102,
                    "KCUe_20_1.0": 120,
                    "KCLe_20_2.0": 80,
                    "KCBe_20_2.0": 102,
                    "KCUe_20_2.0": 125,
                    "KCLe_20_3.0": 75,
                    "KCBe_20_3.0": 102,
                    "KCUe_20_3.0": 130,
                },
            ),
        ]

        mock_ta = Mock()
        mock_df.ta = mock_ta

        mock_squeeze_result = MagicMock()
        mock_ta.squeeze.return_value = mock_squeeze_result

        mock_squeeze_series = MagicMock()

        def mock_at(index):
            if index[1] == "SQZ_ON":
                return 1
            else:
                return 0

        mock_squeeze_series.at.side_effect = mock_at
        mock_squeeze_result.__getitem__.side_effect = lambda key: (
            mock_squeeze_series if key in ["SQZ_ON"] else MagicMock()
        )

        mock_historical_data = MagicMock()
        mock_historical_data.to_df.return_value = mock_df
        mock_historical.return_value = mock_historical_data

        # Simulate authenticated request
        mock_user = Mock()
        mock_user.is_authenticated = True
        self.client.force_authenticate(user=mock_user, token=self.token)

        query = """
        {
            getChartData(ticker: "AAPL") {
                success
                message
            }
        }
        """
        response = self.client.post(self.url, data={"query": query}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(json.loads(response.content)["data"]["getChartData"]["success"])


class TestAutocomplete(TestCase):

    def setUp(self):
        self.client = Client(schema)
        self.factory = RequestFactory()

    @patch("openbb.package.equity.ROUTER_equity.search")
    def test_successful_autocomplete_retrieval(self, mock_search):
        mock_user = Mock()
        mock_user.is_authenticated = True

        mock_results = Mock()
        mock_results.results = [
            {"symbol": "AAPL", "name": "Apple Inc.", "cik": "320193"},
            {"symbol": "CART", "name": "Maplebear Inc.", "cik": "1579091"},
            {"symbol": "APLS", "name": "Apellis Pharmaceuticals, Inc.", "cik": "1492422"},
            {"symbol": "APLE", "name": "Apple Hospitality REIT, Inc.", "cik": "1418121"},
            {"symbol": "OLPX", "name": "OLAPLEX HOLDINGS, INC.", "cik": "1868726"},
            {"symbol": "APLD", "name": "Applied Digital Corp.", "cik": "1144879"},
            {"symbol": "CAPL", "name": "CrossAmerica Partners LP", "cik": "1538849"},
            {"symbol": "APLT", "name": "Applied Therapeutics, Inc.", "cik": "1697532"},
            {"symbol": "APLM", "name": "Apollomics Inc.", "cik": "1944885"},
            {"symbol": "PAPL", "name": "Pineapple Financial Inc.", "cik": "1938109"},
            {"symbol": "APLMW", "name": "Apollomics Inc.", "cik": "1944885"},
        ]

        # Mocking the return value of the autocomplete function
        mock_search.return_value = mock_results

        query = """
        {
            getAutocomplete(query: "APL") {
                success
                message
                results {
                    symbol
                    name
                    cik
                }
            }
        }
        """
        request = self.factory.get("/")
        request.user = mock_user
        executed = schema.execute(query, context_value=request)
        self.maxDiff = None
        self.assertDictEqual(
            executed.data,
            {
                "getAutocomplete": {
                    "success": True,
                    "message": None,
                    "results": [
                        {"symbol": "AAPL", "name": "Apple Inc.", "cik": "320193"},
                        {"symbol": "CART", "name": "Maplebear Inc.", "cik": "1579091"},
                        {"symbol": "APLS", "name": "Apellis Pharmaceuticals, Inc.", "cik": "1492422"},
                        {"symbol": "APLE", "name": "Apple Hospitality REIT, Inc.", "cik": "1418121"},
                        {"symbol": "OLPX", "name": "OLAPLEX HOLDINGS, INC.", "cik": "1868726"},
                        {"symbol": "APLD", "name": "Applied Digital Corp.", "cik": "1144879"},
                        {"symbol": "CAPL", "name": "CrossAmerica Partners LP", "cik": "1538849"},
                        {"symbol": "APLT", "name": "Applied Therapeutics, Inc.", "cik": "1697532"},
                        {"symbol": "APLM", "name": "Apollomics Inc.", "cik": "1944885"},
                        {"symbol": "PAPL", "name": "Pineapple Financial Inc.", "cik": "1938109"},
                        {"symbol": "APLMW", "name": "Apollomics Inc.", "cik": "1944885"},
                    ],
                }
            },
        )


class ChartDataTests(TestCase):
    def setUp(self):
        self.client = Client(schema)
        self.factory = RequestFactory()

    def test_authentication(self):
        query = """
        {
            getChartData(ticker: "AAPL") {
                success
                message
            }
        }
        """
        request = self.factory.get("/")
        request.user = None
        executed = schema.execute(query, context_value=request)
        self.assertDictEqual(
            executed.formatted,
            {
                "data": {"getChartData": None},
                "errors": [
                    {
                        "message": "Authentication credentials were not provided or are invalid",
                        "locations": [{"line": 3, "column": 13}],
                        "path": ["getChartData"],
                    }
                ],
            },
        )

    def test_invalid_ticker(self):
        mock_user = Mock()
        mock_user.is_authenticated = True
        query = """
        {
            getChartData(ticker: "") {
                success
                message
            }
        }
        """
        request = self.factory.get("/")
        request.user = mock_user
        executed = schema.execute(query, context_value=request)
        self.assertDictEqual(
            executed.formatted, {"data": {"getChartData": {"success": False, "message": "No ticker provided"}}}
        )

    @patch("openbb.package.equity_price.ROUTER_equity_price.historical")
    def test_successful_data_retrieval(self, mock_historical):
        mock_user = Mock()
        mock_user.is_authenticated = True

        mock_df = Mock()
        mock_df.iterrows.return_value = [
            (
                date(2023, 1, 1),
                {
                    "open": 100,
                    "high": 110,
                    "low": 90,
                    "close": 105,
                    "volume": 1000,
                    "SQZ_ON": 1,
                    "SQZ_20_2.0_20_1.5": 12,
                    "KCLe_20_1.0": 85,
                    "KCBe_20_1.0": 102,
                    "KCUe_20_1.0": 120,
                    "KCLe_20_2.0": 80,
                    "KCBe_20_2.0": 102,
                    "KCUe_20_2.0": 125,
                    "KCLe_20_3.0": 75,
                    "KCBe_20_3.0": 102,
                    "KCUe_20_3.0": 130,
                },
            ),
            (
                date(2023, 1, 2),
                {
                    "open": 106,
                    "high": 115,
                    "low": 95,
                    "close": 110,
                    "volume": 1500,
                    "SQZ_ON": 0,
                    "SQZ_20_2.0_20_1.5": 13,
                    "KCLe_20_1.0": 85,
                    "KCBe_20_1.0": 102,
                    "KCUe_20_1.0": 120,
                    "KCLe_20_2.0": 80,
                    "KCBe_20_2.0": 102,
                    "KCUe_20_2.0": 125,
                    "KCLe_20_3.0": 75,
                    "KCBe_20_3.0": 102,
                    "KCUe_20_3.0": 130,
                },
            ),
        ]

        mock_ta = Mock()
        mock_df.ta = mock_ta

        mock_squeeze_result = MagicMock()
        mock_ta.squeeze.return_value = mock_squeeze_result

        mock_historical_data = MagicMock()

        mock_historical_data.to_df.return_value = mock_df
        mock_historical.return_value = mock_historical_data

        query = """
        {
            getChartData(ticker: "AAPL") {
                success
                message
                squeeze {
                    x
                    y
                }
                ohlc {
                    x
                    y
                }
                volume {
                    x
                    y
                }
                ticker
            }
        }
        """
        request = self.factory.get("/")
        request.user = mock_user
        executed = schema.execute(query, context_value=request)
        self.maxDiff = None
        self.assertDictEqual(
            executed.formatted,
            {
                "data": {
                    "getChartData": {
                        "success": True,
                        "message": None,
                        "squeeze": [
                            {"x": "2023-01-01", "y": [1.0, 12.0]},
                            {"x": "2023-01-02", "y": [0.0, 13.0]},
                        ],
                        "ohlc": [
                            {"x": "2023-01-01", "y": [100.0, 110.0, 90.0, 105.0]},
                            {"x": "2023-01-02", "y": [106.0, 115.0, 95.0, 110.0]},
                        ],
                        "volume": [{"x": "2023-01-01", "y": 1000.0}, {"x": "2023-01-02", "y": 1500.0}],
                        "ticker": "AAPL",
                    }
                }
            },
        )

    @patch("openbb.package.equity_price.ROUTER_equity_price.historical")
    def test_failed_data_retrieval(self, mock_historical):
        mock_user = Mock()
        mock_user.is_authenticated = True

        # Mock OpenBB response to raise an exception
        mock_historical.side_effect = Exception("Data retrieval error")

        query = """
        {
            getChartData(ticker: "AAPL") {
                success
                message
            }
        }
        """
        request = self.factory.get("/")
        request.user = mock_user
        executed = schema.execute(query, context_value=request)
        self.assertEqual(
            executed.formatted,
            {
                "data": {
                    "getChartData": {
                        "success": False,
                        "message": "Failed to load data for 'AAPL': Data retrieval error",
                    }
                }
            },
        )


class RegisterSerializerTests(TestCase):

    def test_valid_data_creates_user(self):
        data = {"username": "testuser", "email": "testuser@example.com", "password": "Testpassword123"}
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertEqual(user.username, data["username"])
        self.assertEqual(user.email, data["email"])
        self.assertTrue(user.check_password(data["password"]))

    def test_missing_username(self):
        data = {"email": "testuser@example.com", "password": "Testpassword123"}
        serializer = RegisterSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_password(self):
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "123",  # Assuming validate_password enforces stronger passwords
        }
        serializer = RegisterSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class RegisterViewTests(APITestCase):

    def test_register_user(self):
        url = reverse("auth_register")
        data = {"username": "newuser", "email": "newuser@example.com", "password": "Newuserpassword123"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        user = User.objects.get(username=data["username"])
        self.assertEqual(user.email, data["email"])
        self.assertTrue(user.check_password(data["password"]))

    def test_register_with_invalid_data(self):
        url = reverse("auth_register")
        data = {"username": "", "email": "invalidemail", "password": "123"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)
        self.assertIn("password", response.data)
