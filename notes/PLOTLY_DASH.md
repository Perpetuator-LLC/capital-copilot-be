# Add Dash Apps

## Add the Instance

Open the admin panel:

- http://127.0.0.1:8000/admin

Add the Stateless App and then the Dash App Instance.

For instance, using slug `simpexam` will be rendered when visiting:

- http://127.0.0.1:8000/dash/instance/simpexam/

From here, the app file must also be loaded into the `views.py` for the plugin. For instance, with the
`capital-copilot-dashboard` plugin, the `views.py` file must include the following import:

```python
from . import plotly_app
```

That file is expected to contain the Dash app instance. For instance:

```python
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import os
from openbb import obb

from django_plotly_dash import DjangoDash

# Create a DjangoDash instance
app = DjangoDash("SimpleExample")

# Define the layout of the app
app.layout = html.Div(
    [
        dcc.Input(id="ticker-input", type="text", value="TSLA", debounce=True),
        dcc.Graph(id="stock-chart"),
    ]
)


# Define the callback to update the chart
@app.callback(Output("stock-chart", "figure"), [Input("ticker-input", "value")])
def update_graph(ticker):
    obb.user.credentials.alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    historical_data = obb.equity.price.historical(
        symbol=ticker, provider="alpha_vantage"
    )
    fig = go.Figure()
    indicators = dict(
        bbands=dict(length=20, std=2),
        kc=dict(length=20),
    )
    historical_data.charting.to_chart(**{"indicators": indicators}, render=False)
    return historical_data.chart.fig
```

## Configure Formatting

Here is the configuration tools on-line to change chart settings:

- https://chart-studio.plotly.com/create/

# Install

```shell
poetry add django_plotly_dash
```

## Configure Django to Use django_plotly_dash

Add django_plotly_dash to your installed apps in your Django settings file:

```python
INSTALLED_APPS = [..., "django_plotly_dash.apps.DjangoPlotlyDashConfig", ...]
```

Also, add the following middleware:

```python
MIDDLEWARE = [..., "django_plotly_dash.middleware.BaseMiddleware", ...]
```
