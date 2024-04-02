# Using OpenBB

## API Key Management

Our .env is loaded in the `settings.py` file. This is done by the following code:

```python
from copilot.copilot_shared import process_env

...
process_env()
```

This makes the environment variables available to the Django application.

We then set API Keys in our plugins using code like:

```python
obb.user.credentials.alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
```

## Using the API

The API is used in the following way, for example get the historical data for a stock:

```python
from openbb import obb

historical_data = obb.equity.price.historical(symbol=ticker, provider="alpha_vantage")
```

## Can also search stocks using the API

```python
from openbb import obb

search_results = obb.equity.search(symbol=ticker, provider="alpha_vantage")
```
