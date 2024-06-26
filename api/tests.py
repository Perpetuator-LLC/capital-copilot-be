"""
Copyright (c) 2024 eContriver LLC

This file is part of Capital Copilot by eContriver LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

import json
from datetime import date
from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from api.schema import schema

# from django.urls import reverse


# from rest_framework.test import APIClient
# from rest_framework_simplejwt.tokens import AccessToken


# class GraphQLViewTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(username="testuser")
#         self.user.set_password("securepassword")
#         self.user.save()
#         self.token = AccessToken.for_user(self.user)
#
#     def test_custom_graphql_view_with_authenticated_user(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.token)}')
#         response = self.client.get(reverse('graphql'))
#
#         # Directly print or inspect the user to see what's happening
#         print("Authenticated user:", response.wsgi_request.user)
#
#         self.assertTrue(response.wsgi_request.user.is_authenticated)
#         self.assertEqual(response.wsgi_request.user, self.user)
#
#     def test_custom_graphql_view_with_no_authentication(self):
#         response = self.client.get(reverse('graphql'))
#         self.assertFalse(response.wsgi_request.user.is_authenticated)


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
        mock_historical_data = Mock()
        mock_df = Mock()
        mock_df.iterrows.return_value = [
            (date(2023, 1, 1), {"open": 100, "high": 110, "low": 90, "close": 105, "volume": 1000}),
            (date(2023, 1, 2), {"open": 106, "high": 115, "low": 95, "close": 110, "volume": 1500}),
        ]
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

    # Additional tests...


# class APITests(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.url = reverse('graphql')
#         self.valid_ticker = "AAPL"
#         self.invalid_ticker = ""
#
#     def test_requires_authentication(self):
#         response = self.client.post(self.url, data={"ticker": self.valid_ticker})
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#     @patch('os.getenv')
#     @patch("openbb.package.equity_price.ROUTER_equity_price.historical")
#     def test_successful_data_retrieval(self, mock_historical, mock_getenv):
#         # Setup Mocks
#         mock_getenv.return_value = 'fake_api_key'
#         historical_data_mock = Mock()
#         historical_data_mock.to_df.return_value = ...
#         mock_historical.return_value = historical_data_mock
#
#         # Simulate authenticated request
#         self.client.force_authenticate(user=Mock(is_authenticated=True))
#         query = """
#         query {
#             getChartData(ticker: "AAPL") {
#                 success
#                 message
#             }
#         }
#         """
#         response = self.client.post(self.url, data=query)
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(json.loads(response.content)['success'])
#
#     @patch('os.getenv')
#     @patch("openbb.package.equity_price.ROUTER_equity_price.historical")
#     def test_failed_data_retrieval(self, mock_historical, mock_getenv):
#         mock_getenv.return_value = 'fake_api_key'
#         mock_historical.side_effect = Exception("Data retrieval error")
#
#         self.client.force_authenticate(user=Mock(is_authenticated=True))
#         response = self.client.post(self.url, data={"ticker": self.valid_ticker})
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertFalse(json.loads(response.content)['success'])
#         self.assertIn("Failed to load data for 'AAPL': Data retrieval error", str(response.content))
#
#     def test_invalid_ticker_provided(self):
#         self.client.force_authenticate(user=Mock(is_authenticated=True))
#         response = self.client.post(self.url, data={"ticker": self.invalid_ticker})
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertFalse(json.loads(response.content)['success'])
#         self.assertIn("No ticker provided", str(response.content))


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

        # Mock OpenBB response
        mock_historical_data = Mock()
        mock_df = Mock()
        mock_df.iterrows.return_value = [
            (date(2023, 1, 1), {"open": 100, "high": 110, "low": 90, "close": 105, "volume": 1000}),
            (date(2023, 1, 2), {"open": 106, "high": 115, "low": 95, "close": 110, "volume": 1500}),
        ]
        mock_historical_data.to_df.return_value = mock_df
        mock_historical.return_value = mock_historical_data

        query = """
        {
            getChartData(ticker: "AAPL") {
                success
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
        self.assertDictEqual(
            executed.formatted,
            {
                "data": {
                    "getChartData": {
                        "success": True,
                        "ohlc": [
                            {"x": "2023-01-01", "y": [100, 110, 90, 105]},
                            {"x": "2023-01-02", "y": [106, 115, 95, 110]},
                        ],
                        "volume": [{"x": "2023-01-01", "y": 1000}, {"x": "2023-01-02", "y": 1500}],
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
