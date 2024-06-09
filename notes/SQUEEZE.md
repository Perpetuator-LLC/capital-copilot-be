# The Squeeze Indicator

To get the data to calculate the squeeze indicator, we need to get the Bollinger Bands and Keltner Channels.

We can use the `plotly_ta` library to get the data for these indicators.

The indicators are calculated using the `plotly_ta` library. The `plotly_ta` library is a wrapper around the `ta`
library that provides the data in a format that can be used with Plotly.

See:

- .venv/lib/python3.11/site-packages/openbb_charting/core/plotly_ta/data_classes.py
- openbb_charting.core.plotly_ta.data_classes.ChartIndicators.to_dataframe

A ChartIndicators object is created from a DataFrame of OHLCV data. The ChartIndicators object contains the data for the
indicators that are calculated from the OHLCV data.

# Extracting the Bollinger Bands and Keltner Channels

The Bollinger Bands and Keltner Channels are extracted from the ChartIndicators object using the `get_bollinger_bands`
and `get_keltner_channels` methods.

```python
# Get the Bollinger Bands and Keltner Channels
# bb = chart_indicators.get_bollinger_bands()
# kc = chart_indicators.get_keltner_channels()
plotly_ta.df_ta
```

The column headers are:

BBL_20_2.0 - Lower Bollinger Band BBM_20_2.0 - Middle Bollinger Band BBU_20_2.0 - Upper Bollinger Band BBB_20_2.0 -
Bollinger Bands Width BBP_20_2.0 - Bollinger Bands Percentage KCLe_20_2 - Lower Keltner Channel KCBe_20_2 - Middle
Keltner Channel KCUe_20_2 - Upper Keltner Channel

# Calculating the Squeeze Indicator

To calculate the squeeze indicator, we need to get the Bollinger Bands and Keltner Channels and then calculate the
squeeze indicator from these indicators via the following formula:

```python
# Calculate the squeeze indicator
chart_data["squeeze"] = chart_data["bb_width"] - chart_data["kc_width"]
```

# Adding the Squeeze Indicator to the Chart

The squeeze indicator is added to the chart by creating a new trace for the squeeze indicator. The trace is added to the
chart using the `add_trace` method of the `plotly.graph_objects.Figure` object.

```python
import plotly.graph_objects as go

fig = go.Figure()

# Add the squeeze indicator trace to the chart
fig.add_trace(
    go.Scatter(
        x=chart_data.index,
        y=chart_data["squeeze"],
        mode="markers",
        marker=dict(color="red", size=10),
        name="Squeeze",
    )
)
```
