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

# Logging in OpenBB

This library uses `posthog` for logging. The logging is done in the following way:

```python
from openbb import obb
```

Inside of this import the following stack will be called:

```
__init__, posthog_handler.py:31
_add_posthog_handler, handlers_manager.py:37
__init__, handlers_manager.py:32
_setup_handlers, logging_service.py:128
__init__, logging_service.py:80
__call__, singleton.py:12
init_logging_service, command_runner.py:420
__init__, app_factory.py:28
create_app, app_factory.py:66
<module>, __init__.py:44
<frame not available>
<frame not available>
<frame not available>
<frame not available>
<frame not available>
<module>, openbb_chart.py:19 <- our code
<frame not available>
<frame not available>
```

The logs are sent to the following directory:

```
/Users/user/OpenBBUserData
```

From this file:

- .venv/lib/python3.11/site-packages/openbb_core/app/logs/logging_service.py

The logging is setup when this object is initialized.

Here is the stack at initialization:

```
__init__, logging_service.py:76
__call__, singleton.py:12
init_logging_service, command_runner.py:420
__init__, app_factory.py:28
create_app, app_factory.py:66
<module>, __init__.py:44
<frame not available>
<frame not available>
<frame not available>
<frame not available>
<frame not available>
<module>, openbb_chart.py:19
<frame not available>
<frame not available>
```

The logging_handlers are passed in as `['file', 'posthog']` in the `settings.py` file.

The system settings come from this file:

- /Users/user/.openbb_platform/system_settings.json

The 'posthog' logging handler is added in the following way:

- .venv/lib/python3.11/site-packages/openbb_core/app/model/system_settings.py

```python
@model_validator(mode="after")  # type: ignore
@classmethod
def validate_posthog_handler(cls, values: "SystemSettings") -> "SystemSettings":
    """If the user has enabled log collection, then we need to add the Posthog."""
    if (
        not any([values.test_mode, values.debug_mode, values.logging_suppress])
        and values.log_collect
        and "posthog" not in values.logging_handlers
    ):
        values.logging_handlers.append("posthog")

    return values
```

To disable add the following to the `system_settings.json` file:

```json
{
  "debug_mode": true,
  "log_collect": false
}
```

# Run-time with OpenBB

There is a significant run-time cost to using OpenBB. See this example:

```shell
$ poetry add "openbb[charting,alpha_vantage]"
$ time ./.venv/bin/python -m scripts.research.openbb_chart
...
./.venv/bin/python -m   6.60s user 2.30s system 119% cpu 7.458 total
```

Versus this example:

```shell
$ poetry add "openbb[all]"
$ time ./.venv/bin/python -m scripts.research.openbb_chart
...
./.venv/bin/python -m   16.03s user 12.30s system 169% cpu 17.042 total
```

# Indicators in OpenBB

The indicators in OpenBB are calculated using the `plotly_ta` library. This library is a wrapper around the `ta`
library.

Here is a stack when indicators are applied:

```
to_dataframe, data_classes.py:201
calculate_indicators, ta_class.py:299
plot_fig, ta_class.py:457
__plot__, ta_class.py:204
plot, ta_class.py:250
to_chart, to_chart.py:52
to_chart, __init__.py:192
update_graph, plotly_app.py:35
add_context, _callback.py:82
dispatch_with_args, dash_wrapper.py:705
_update, views.py:95
update, views.py:75
_view_wrapper, csrf.py:65
_get_response, base.py:197
inner, exception.py:55
__call__, middleware.py:34
inner, exception.py:55
__call__, middleware.py:99
inner, exception.py:55
middleware, middleware.py:29
inner, exception.py:55
__call__, deprecation.py:134
inner, exception.py:55
__call__, deprecation.py:134
inner, exception.py:55
__call__, deprecation.py:134
inner, exception.py:55
__call__, deprecation.py:134
inner, exception.py:55
__call__, deprecation.py:134
inner, exception.py:55
__call__, deprecation.py:134
inner, exception.py:55
__call__, deprecation.py:134
inner, exception.py:55
__call__, deprecation.py:134
inner, exception.py:55
get_response, base.py:140
__call__, wsgi.py:124
__call__, handlers.py:80
run, handlers.py:137
handle_one_request, basehttp.py:252
handle, basehttp.py:229
__init__, socketserver.py:755
finish_request, socketserver.py:361
process_request_thread, socketserver.py:691
run, threading.py:982
_bootstrap_inner, threading.py:1045
_bootstrap, threading.py:1002
```

Here is an example of how to use the `plotly_ta` library:

```python
from openbb import obb
from charting.core.plotly_ta.ta_class import PlotlyTA

df = obb.equity.price.historical("SPY")
indicators = dict(
    sma=dict(length=[20, 50, 100]),
    adx=dict(length=14),
    macd=dict(fast=12, slow=26, signal=9),
    rsi=dict(length=14),
)
fig = PlotlyTA.plot(df, indicators=indicators)
fig.show()

# If you want to plot the chart with the same indicators, you can
# reuse the same instance of the class as follows:

ta = PlotlyTA()
fig = ta.plot(df, indicators=indicators)
df2 = obb.equity.price.historical("AAPL")
fig2 = ta.plot(df2)
fig.show()
fig2.show()
```
