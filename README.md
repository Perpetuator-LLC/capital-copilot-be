# Capital Copilot

A tool to help aggregate market data, setup alerts, automate trading, and provide AI insights.

# Development

To start see: [Initial Config](notes/INITIAL_CONFIG.md)

After that, see: [Development](notes/DEVELOPMENT.md)

# Production

To understand the network setup see: [WAF](notes/WAF.md)

# Django

To start see: [Django Setup](notes/DJANGO_SETUP.md)

After that, see: [Django Management](notes/DJANGO_MGMT.md)

# Architecture

Front-end UI (Angular) will have a console tray This tray will accept commands that will come to cc-be (Django) cc-be
will have a command processor that will process the command and return the result all command parsing is done in the
cc-be and then delegated to the appropriate plugins for processing

ideally we can find a way to support thinkscript and more so pine script for filters, scans, alerts, and indicators

data from commands can be formatted in several ways:

- table (csv, etc. can come later)
- chart (open ui element, default?)
- json

## UI Elements

- Console Tray
  - Command History
- Grid
  - Heat Map
  - Sectors
  - Indices
  - ETFs
  - Stocks
  - Adjacent Stocks
  - Correlated Stocks
  - Inversely Correlated Stocks
- Chart
  - Candlestick
  - Indicators (BB, KC, Squeeze)
- Table
- Report / Markdown Rendering and for blog posts
  - Can all people post?

## Commands

```
price -t TSLA -i 1d -s 2021-01-01 -e 2021-12-31 -c close -f csv
set c1 [p -t TSLA -i 1d -s 2021-01-01 -e 2021-12-31 -c close -f graph]
p -t TSLA -i 1d -s 2021-01-01 -e 2021-12-31 -c close -f graph -n c1

balancesheet -t TSLA -s 2021-01-01 -e 2021-12-31 -f csv
cashflow -t TSLA -s 2021-01-01 -e 2021-12-31 -f csv
income -t TSLA -s 2021-01-01 -e 2021-12-31 -f csv

indicators -t TSLA -i 1d -s 2021-01-01 -e 2021-12-31 -f csv -i bbands -i kc -i squeeze -o c1
```

# TODO

- \[x\] Cookies Warning
- \[ \] Stripe
- \[x\] Terms and Conditions
- \[x\] Privacy Policy

## Features

- \[ \] Blog
- \[ \] Search History -> Auto Watchlist
  - \[ \] List of IN Watchlists on Dashboard
- \[ \] Stock to Indexes
  - \[ \] List of IN Indexes on Dashboard
- \[ \] Per Sector Heat Map
- \[ \] DCF
  - \[ \] DCF to Blog Posts
- \[ \] TTM Squeeze number triggering
  - \[ \] TTM Squeeze to Blog Posts
  - \[ \] TTM Squeeze to Watchlist
  - \[ \] TTM Squeeze to number uptrend + triggering per sector
  - \[ \] TTM Squeeze to number downtrend + triggering per sector
- \[ \] TTM Squeeze setting up with 5 dots
- \[ \] ML on TTM Squeeze for 90% of stocks and then check with remaining 10%
  - \[ \] Get Price data and calculate the TTM Squeeze, or get the TTM Squeeze data
- \[ \] Earnings + Economic Calendar
  - \[ \] Earnings Calendar
  - \[ \] Earnings History
  - \[ \] Earnings Blog
  - \[ \] Economic Calendar
  - \[ \] Economic History
  - \[ \] Economic Blog
  - \[ \] All showing on Dashboard Sidebar
- \[ \] M2V Velocity of Money
  - \[ \] Normally 1.5-2.5, current state
  - \[ \] M2V to Blog Posts based on current expectations

To build

- Up coming: earnings, CPI
- Time lapse
  - of the heat map
  - of Indicator signals, was setting up on 1h, 1d now also has 2d, 3d,
- Watchlist
  - History - auto adds but can be edited
  - Can add notes to stocks
- Individual Stock
  - Show 9 timeframes with squeeze
  - Show Indices, Sectors, ETFs under each of those that they belong to
  - Show list of Adjacent Stocks (NVDA -> SMCI), Correlated Stocks/Sectors/ETFs/Indices, Inversely Correlated
  - Make Earnings visible at the top
  - Income/Balance/Cash Flow
  - Stock detail (P/E, P/B, etc.)
  - Options !\[\[Pasted image 20240531062017.png\]\]
  - Option Equilibrium? !\[\[Pasted image 20240531062141.png\]\]
- Show Sectors and all stocks under them with Squeeze
- Show Call vs Put buying on price chart: HIRO from SpotGamma
- Multi-chart, one time frame
- Stop calculation: 2 x 14 ATR / 1.5 x 14 ATR (when to use what)
- Greed vs Fear Index
- Bond Auctions
- Futures Rotations/Trends: https://www.schwab.com/futures/futures-markets
- AI: numer.ai/mlst - train model on investing and if it works well, get paid for it
- Price & Volume: https://www.youtube.com/watch?v=19O_iWtiA18
- Filter

```
DMI("length" = 21, "average type" = "EXPONENTIAL")."DI+" is less than DMI("length" = 21, "average type" = "EXPONENTIAL")."DI-" and DMI("length" = 21, "average type" = "EXPONENTIAL")."ADX" is greater than 20 and MovAvgExponential("length" = 21)."AvgExp" is less than MovAvgExponential("length" = 34)."AvgExp" and MovAvgExponential("length" = 55)."AvgExp" is less than MovAvgExponential("length" = 89)."AvgExp" and TTM_Squeeze()."SqueezeAlert" is equal to 0 and close is less than MovAvgExponential("length" = 34)."AvgExp"
```
