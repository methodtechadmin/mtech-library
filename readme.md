# mtech Library

Library for accessing market data, corporate actions, corporate financials, security information, universe management, return analytics, risk decomposition, and statistical utilities.

---

## Table of Contents

- [Installation](#installation)
- [Classes Overview](#classes-overview)
- [Quick Start](#quick-start)
- [DateTime](#datetime)
- [Region](#region)
- [DateUtils](#dateutils)
- [Universe](#universe)
- [MarketData](#marketdata)
- [CorporateActions](#corporateactions)
- [CorporateData](#corporatedata)
- [SecurityInfo](#securityinfo)
- [Returns](#returns)
- [RiskDecomposition](#riskdecomposition)
- [StatHelpers](#stathelpers)
- [Constants & Columns](#constants--columns)
- [Enums](#enums)

---

## Installation

Import the classes you need:

```python
from mtech import MarketData
from mtech import CorporateActions
from mtech import CorporateData
from mtech import SecurityInfo
from mtech import Universe
from mtech import DateTime
from mtech import DateUtils
from mtech import Region
from mtech import Returns
from mtech import RiskDecomposition
from mtech import StatHelpers
from mtech import constants as cns
from mtech import columns as col
from mtech.enums import VOLUME_TYPE
from mtech.enums import FinancialReportType
from mtech.enums import FinancialReportPeriod
from mtech.enums import FinancialReportMetric
from mtech.enums import FinancialType
from mtech.enums import UniverseType
```

---

## Classes Overview

| Class | Purpose |
|---|---|
| `DateTime` | Timezone-aware datetime object |
| `Region` | Exchange and timezone metadata for a region |
| `DateUtils` | Business date arithmetic and calendar utilities |
| `Universe` | Full, coverage, and estimation universes |
| `MarketData` | Prices, volumes, returns, market cap |
| `CorporateActions` | Splits, bonuses, dividends |
| `CorporateData` | Financial statements, shareholding |
| `SecurityInfo` | Security lookups, symbol/ISIN/ukey mapping |
| `Returns` | Forward, daily, cumulative, and category returns |
| `RiskDecomposition` | Risk-model data, portfolio risk, attribution, and event sensitivity |
| `StatHelpers` | Winsorization, standardization, correlation, and regression helpers |
| `constants` | Constant Variables |
| `columns` | Column Variables |

---

## Quick Start

Many security-level methods accept `ukeys` — unique integer keys that identify securities. The standard way to obtain them is to initialise a universe for a date and extract the keys from it. Everything else follows from there.

```python
from mtech import Universe
from mtech import DateTime
from mtech import Region
from mtech import columns as col
from mtech.enums import UniverseType

# 1. Define your date and region
sdate = DateTime("20240101")
region = Region("IN")

# 2. Get the universe and extract ukeys
univ  = Universe(region).get_universe(univ_type=UniverseType.NIFTY500, date=sdate)
ukeys = univ[col.MSYMBOL_UKEY].tolist()
```

`ukeys` is now a plain Python list of integers that can be passed to security-level methods in `MarketData`, `CorporateActions`, `CorporateData`, `SecurityInfo`, and `Returns`, or embedded in `RiskDecomposition` portfolio weight records.

---

## DateTime

A timezone-aware datetime object. Supports arithmetic, formatting, and epoch conversions. Defaults to `Asia/Kolkata`.

```python
from mtech import DateTime

sdate = DateTime("20240101")
edate = DateTime("20240630")
```

### Constructor

```python
DateTime(input: str, input_tz: str = "Asia/Kolkata", store_tz: str = "Asia/Kolkata")
```

| Parameter | Type | Description |
|---|---|---|
| `input` | `str` | Date/datetime string |
| `input_tz` | `str` | Timezone of the input string (default: `"Asia/Kolkata"`) |
| `store_tz` | `str` | Timezone to store internally (default: `"Asia/Kolkata"`) |

### Class Methods

#### `DateTime.from_epoch_days(epoch_days)`

| Parameter | Type | Description |
|---|---|---|
| `epoch_days` | `int` | Integer count of days since Unix epoch |

```python
dt = DateTime.from_epoch_days(19723)
```

### Properties

| Property | Type | Description |
|---|---|---|
| `year` | `int` | Year component |
| `month` | `int` | Month component |
| `day` | `int` | Day component |
| `hour` | `int` | Hour component |
| `minute` | `int` | Minute component |
| `second` | `int` | Second component |
| `native` | any | Native datetime object |

### Methods

| Method | Returns | Description |
|---|---|---|
| `to_epoch()` | `int` | Unix timestamp in seconds |
| `to_epoch_days()` | `int` | Days since Unix epoch |
| `datetime(tz)` | datetime | Native datetime in given timezone |
| `str_format(fmt, tz)` | `str` | Formatted string (e.g. `"%Y-%m-%d"`) |
| `input_tz()` | `str` | Input timezone string |
| `store_tz()` | `str` | Storage timezone string |

### Operators

`DateTime` supports `==`, `<`, `<=`, `hash()`, and `str()`.

```python
sdate = DateTime("20240101")
edate = DateTime("20240630")

sdate < edate        # True
str(sdate)           # "2024-01-01 ..."
sdate.to_epoch()     # 1704067200
```

---

## Region

Provides metadata about exchanges, countries, and timezones for a geographic/market region.

```python
from mtech import Region

region = Region("IN")
```

### Constructor

| Parameter | Type | Description |
|---|---|---|
| `region` | `str` | Region code e.g. `"IN"` |

### Properties

| Property | Type | Description |
|---|---|---|
| `name` | `str` | Region identifier |
| `countries` | `list` | Countries in the region |
| `exchanges` | `list` | All exchanges |
| `common_stock_exchanges` | `list` | Primary equity exchanges |
| `primary_exchange` | `str` | The main exchange |
| `timezone` | `str` | e.g. `"Asia/Kolkata"` |

```python
print(region.primary_exchange)   # "NSE"
print(region.timezone)           # "Asia/Kolkata"
```

---

## DateUtils

Business date arithmetic, calendar queries, and period boundary helpers.

```python
from mtech import DateUtils

du = DateUtils()
```

### Methods

#### Date Checking

| Method | Parameters | Returns | Description |
|---|---|---|---|
| `now(region)` | `region: Region` | `DateTime` | Current date and time |
| `is_busdate(date, region)` | `date: DateTime`, `region: Region` | `bool` | Check if date is a business day |
| `get_busdate(date, region, next)` | `date: DateTime`, `region: Region` | `DateTime` | Next or previous business date |
| `shift_busdate(date, region, n)` | `date: DateTime`, `region: Region`, `n: int` | `DateTime` | Shift by N business days |
| `get_busdate_range(start_date, end_date, region)` | `start_date: DateTime`, `end_date: DateTime`, `region: Region` | `List[DateTime]` | All business dates in range |
| `get_all_busdates(region)` | `region: Region` | `List[DateTime]` | All known business dates |

```python
region = Region("IN")
sdate  = DateTime("20240101")

du.now(region=region)                                                    # 20260328 11:52:02
du.is_busdate(sdate, region=region)                                      # True
du.get_busdate(sdate, region=region)
du.shift_busdate(sdate, region=region, n=-5)                             # 20231225
du.get_busdate_range(sdate, DateTime("20240105"), region=region)         # [20240101, ..., 20240105]
du.get_all_busdates(region=region)                                       # list of all business datetimes
```

---

#### Calendar Periods

All period methods return `(DateTime, DateTime)` tuples for start and end. The `n` parameter shifts by that many periods (e.g. `n=-1` for previous period, `n=1` for next).

| Method | Description |
|---|---|
| `get_week_start_end(date, region, n)` | Week boundaries |
| `get_month_start_end(date, region, n)` | Month boundaries |
| `get_quarter_start_end(date, region, n)` | Quarter boundaries |
| `get_semi_annual_start_end(date, region, n)` | Half-year boundaries |
| `get_financial_year_start_end(date, region, n)` | Financial year boundaries |
| `get_calendar_year_start_end(date, region, n)` | Calendar year boundaries |

| Parameter | Type | Description |
|---|---|---|
| `date` | `DateTime` | Reference date |
| `region` | `Region` | Region object (default: `Region("IN")`) |
| `n` | `int` | Period offset — `0` = current, `-1` = previous, `1` = next |

```python
region = Region("IN")
sdate  = DateTime("20240501")

start, end = du.get_quarter_start_end(sdate, region=region, n=0)         # 20240401, 20240630
start, end = du.get_financial_year_start_end(sdate, region=region, n=-1) # 20230401, 20240331
```

Each has a corresponding `get_all_*` variant that returns a list of `(start, end)` tuples across a date range:

| Method | Parameters |
|---|---|
| `get_all_week_start_end(start_date, end_date, region)` | `start_date: DateTime`, `end_date: DateTime`, `region: Region` |
| `get_all_month_start_end(start_date, end_date, region)` | `start_date: DateTime`, `end_date: DateTime`, `region: Region` |
| `get_all_quarter_start_end(start_date, end_date, region)` | `start_date: DateTime`, `end_date: DateTime`, `region: Region` |
| `get_all_semi_annual_start_end(start_date, end_date, region)` | `start_date: DateTime`, `end_date: DateTime`, `region: Region` |
| `get_all_financial_year_start_end(start_date, end_date, region)` | `start_date: DateTime`, `end_date: DateTime`, `region: Region` |
| `get_all_calendar_year_start_end(start_date, end_date, region)` | `start_date: DateTime`, `end_date: DateTime`, `region: Region` |

```python
quarters = du.get_all_quarter_start_end(DateTime("20230101"), DateTime("20241231"), region=Region("IN"))
# [(DateTime, DateTime), ...]
```

---

#### Other Utilities

| Method | Parameters | Returns | Description |
|---|---|---|---|
| `exchange_calendar(region, force_query)` | `region: Region`, `force_query: bool` | `pd.DataFrame` | Exchange holiday calendar |
| `epoch_to_datetime(epoch, tz)` | `epoch: int`, `tz: str` | `DateTime` | Convert Unix epoch to DateTime |
| `get_last_thurs_of_month(date, region)` | `date: DateTime`, `region: Region` | `DateTime` | Last Thursday of the month |
| `add_mins(date, mins)` | `date: DateTime`, `mins: int` | `DateTime` | Add minutes to a DateTime |
| `get_intervals(start_date, end_date, region, step_mins)` | `start_date: DateTime`, `end_date: DateTime`, `region: Region`, `step_mins: int` | `List[DateTime]` | Intraday intervals at fixed step |
| `get_quarter_index(date, region)` | `date: DateTime`, `region: Region` | `int` | Quarter number (1–4) |
| `get_dt_obj_with_filler(date_str, default_date)` | `date_str: str`, `default_date: str` | `DateTime` | Return default if date_str is blank |

```python
region = Region("IN")
sdate  = DateTime("20240115")

du.exchange_calendar(region=region)
du.epoch_to_datetime(1704067200, tz="Asia/Kolkata")
du.get_last_thurs_of_month(sdate, region=region)
du.add_mins(DateTime("20240115 09:30:00"), mins=30)
du.get_intervals(DateTime("20240115 09:15:00"), DateTime("20240115 15:30:00"), region=region, step_mins=5)
du.get_quarter_index(sdate, region=region)
du.get_dt_obj_with_filler("", default_date="20240101")
```

---

## Universe

Manage and retrieve security universes scoped to a `Region`.

```python
from mtech import Universe
from mtech import Region
from mtech import DateTime
from mtech import columns as col
from mtech.enums import UniverseType

region = Region("IN")
sdate  = DateTime("20240101")

univ  = Universe(region).get_universe(univ_type=UniverseType.NIFTY500, date=sdate)
ukeys = univ[col.MSYMBOL_UKEY].tolist()
```

### Methods

#### `get_universe(univ_type, date)`

| Parameter | Type | Description |
|---|---|---|
| `univ_type` | `UniverseType` | Universe type e.g. `UniverseType.NIFTY500, UniverseType.BSE500, UniverseType.NIFTY`  |
| `date` | `DateTime` | Reference date |

```python
univ  = Universe(region).get_universe(univ_type=UniverseType.NIFTY500, date=sdate)
ukeys = univ[col.MSYMBOL_UKEY].tolist()
```

---

#### `full_universe(date)`

| Parameter | Type | Description |
|---|---|---|
| `date` | `DateTime` | Reference date |

```python
df = Universe(region).full_universe(sdate)
```

---

#### `coverage_universe(date)`

| Parameter | Type | Description |
|---|---|---|
| `date` | `DateTime` | Reference date |

```python
df = Universe(region).coverage_universe(sdate)
```

---

#### `estimation_universe(date)`

| Parameter | Type | Description |
|---|---|---|
| `date` | `DateTime` | Reference date |

```python
df = Universe(region).estimation_universe(sdate)
```

---

#### `get_universe_map()`

Returns a dictionary mapping universe type names to their definitions. No parameters.

```python
universe_map = Universe(region).get_universe_map()
```

---

## MarketData

Fetch price, volume, return, and market cap data for securities.

```python
from mtech import MarketData
from mtech import Universe
from mtech import DateTime
from mtech import Region
from mtech import columns as col
from mtech.enums import UniverseType
from mtech.enums import VOLUME_TYPE

region = Region("IN")
sdate  = DateTime("20240101")
edate  = DateTime("20240630")

univ   = Universe(region).get_universe(univ_type=UniverseType.NIFTY500, date=sdate)
ukeys  = univ[col.MSYMBOL_UKEY].tolist()

md = MarketData()
```

### Methods

#### `get_unadjusted_price(date_times, ukeys)`

| Parameter | Type | Description |
|---|---|---|
| `date_times` | `List[DateTime]` | List of dates to query |
| `ukeys` | `List[int]` | List of security keys |

```python
df = md.get_unadjusted_price(
    date_times=[sdate],
    ukeys=ukeys
)
# returns pd.DataFrame -> [col.DATETIME, col.MSYMBOL_UKEY, col.HIGH_PRICE, col.LOW_PRICE, col.OPEN_PRICE, col.CLOSE_PRICE]
```

---

#### `get_adjusted_price(date_times, ukeys)`

| Parameter | Type | Description |
|---|---|---|
| `date_times` | `List[DateTime]` | List of dates to query |
| `ukeys` | `List[int]` | List of security keys |

```python
df = md.get_adjusted_price(
    date_times=[sdate],
    ukeys=ukeys
)
# returns pd.DataFrame -> [col.DATETIME, col.MSYMBOL_UKEY, col.HIGH_PRICE, col.LOW_PRICE, col.OPEN_PRICE, col.CLOSE_PRICE]
```

---

#### `get_daily_returns(date_times, ukeys)`

| Parameter | Type | Description |
|---|---|---|
| `date_times` | `List[DateTime]` | List of dates to query |
| `ukeys` | `List[int]` | List of security keys |

```python
df = md.get_daily_returns(
    date_times=[sdate],
    ukeys=ukeys
)
# returns pd.DataFrame -> [col.DATETIME, col.MSYMBOL_UKEY, col.RETURN, col.RETURN_CTO, col.RETURN_OTC]
```

---

#### `get_unadjusted_volume(date_times, ukeys, volume_type)`

| Parameter | Type | Description |
|---|---|---|
| `date_times` | `List[DateTime]` | List of dates to query |
| `ukeys` | `List[int]` | List of security keys |
| `volume_type` | `VOLUME_TYPE` | Volume aggregation type (default: `VOLUME_TYPE.MULTI_EXCHANGE_VOLUME`) |

```python
df = md.get_unadjusted_volume(
    date_times=[sdate],
    ukeys=ukeys,
    volume_type=VOLUME_TYPE.EXCHANGE_VOLUME,
)
# returns pd.DataFrame -> [col.DATETIME, col.MSYMBOL_UKEY, col.VOLUME_SHS, col.VOLUME_NTL]
```

---

#### `get_adjusted_volume(date_times, ukeys, volume_type)`

| Parameter | Type | Description |
|---|---|---|
| `date_times` | `List[DateTime]` | List of dates to query |
| `ukeys` | `List[int]` | List of security keys |
| `volume_type` | `VOLUME_TYPE` | Volume aggregation type (default: `VOLUME_TYPE.MULTI_EXCHANGE_VOLUME`) |

```python
df = md.get_adjusted_volume(
    date_times=[sdate],
    ukeys=ukeys,
    volume_type=VOLUME_TYPE.MULTI_EXCHANGE_VOLUME,
)
# returns pd.DataFrame -> [col.DATETIME, col.MSYMBOL_UKEY, col.VOLUME_SHS, col.VOLUME_NTL]
```

---

#### `get_adtv(date_times, ukeys, volume_type, lookback_days)`

Returns Average Daily Trading Volume (ADTV) over a lookback window. Default lookback is 63 days.

| Parameter | Type | Description |
|---|---|---|
| `date_times` | `List[DateTime]` | List of dates to query |
| `ukeys` | `List[int]` | List of security keys |
| `volume_type` | `VOLUME_TYPE` | Volume aggregation type (default: `VOLUME_TYPE.MULTI_EXCHANGE_VOLUME`) |
| `lookback_days` | `int` | Lookback window in trading days (default: `63`) |

```python
df = md.get_adtv(
    date_times=[sdate],
    ukeys=ukeys,
    volume_type=VOLUME_TYPE.MULTI_EXCHANGE_VOLUME,
    lookback_days=63
)
# returns pd.DataFrame -> [col.DATETIME, col.MSYMBOL_UKEY, col.ADTV]
```

---

#### `get_market_cap(date_times, ukeys)`

| Parameter | Type | Description |
|---|---|---|
| `date_times` | `List[DateTime]` | List of dates to query |
| `ukeys` | `List[int]` | List of security keys |

```python
df = md.get_market_cap(
    date_times=[sdate],
    ukeys=ukeys
)
# returns pd.DataFrame -> [col.DATETIME, col.MSYMBOL_UKEY, col.SHARES_OUTSTANDING, col.MARKET_CAP]
```

---

#### `get_cumulative_daily_returns(start_date, end_date, ukeys, daily_ret_winz_lb, daily_ret_winz_ub)`

Returns cumulative daily returns over a date range. Supports winsorization bounds (default: -10.0 to +10.0).

| Parameter | Type | Description |
|---|---|---|
| `start_date` | `DateTime` | Start of the date range |
| `end_date` | `DateTime` | End of the date range |
| `ukeys` | `List[int]` | List of security keys |
| `daily_ret_winz_lb` | `float` | Lower winsorization bound (default: `-10.0`) |
| `daily_ret_winz_ub` | `float` | Upper winsorization bound (default: `10.0`) |

```python
df = md.get_cumulative_daily_returns(
    start_date=sdate,
    end_date=edate,
    ukeys=ukeys,
    daily_ret_winz_lb=-10.0,
    daily_ret_winz_ub=10.0
)
# returns pd.DataFrame -> [col.MSYMBOL_UKEY, col.MISSING_DATA_PERCENTAGE, col.RETURN]
```

---

## CorporateActions

Fetch data on stock splits, bonuses, and dividends.

```python
from mtech import CorporateActions
from mtech import Universe
from mtech import DateTime
from mtech import Region
from mtech import columns as col
from mtech.enums import UniverseType

region = Region("IN")
sdate  = DateTime("20240101")
edate  = DateTime("20240630")

univ   = Universe(region).get_universe(univ_type=UniverseType.NIFTY500, date=sdate)
ukeys  = univ[col.MSYMBOL_UKEY].tolist()

ca = CorporateActions()
```

### Methods

#### `get_splits_bonuses_data(date_times, ukeys, filter_for_fin_types)`

| Parameter | Type | Description |
|---|---|---|
| `date_times` | `List[DateTime]` | List of dates to query |
| `ukeys` | `List[int]` | List of security keys |
| `filter_for_fin_types` | `bool` | Filter results by financial instrument type (optional) |

```python
df = ca.get_splits_bonuses_data(
    date_times=[sdate],
    ukeys=ukeys,
    filter_for_fin_types=True
)
# returns pd.DataFrame -> [col.DATETIME, col.MSYMBOL_UKEY, col.SPLIT_RATIO]
```

---

#### `get_cumulative_splits_bonuses_data(start_date, end_date, ukeys, filter_for_fin_types)`

| Parameter | Type | Description |
|---|---|---|
| `start_date` | `DateTime` | Start of the date range |
| `end_date` | `DateTime` | End of the date range |
| `ukeys` | `List[int]` | List of security keys |
| `filter_for_fin_types` | `bool` | Filter results by financial instrument type (optional) |

```python
df = ca.get_cumulative_splits_bonuses_data(
    start_date=sdate,
    end_date=edate,
    ukeys=ukeys
)
# returns pd.DataFrame -> [col.MSYMBOL_UKEY, col.SPLIT_RATIO]
```

---

#### `get_dividends_data(date_times, date_col)`

| Parameter | Type | Description |
|---|---|---|
| `date_times` | `List[DateTime]` | List of dates to query |
| `date_col` | `str` | col.EX_DIVIDEND_DATE, col.DIVIDEND_RECORD_DATE, col.DIVIDEND_PAY_DATE, col.DIVIDEND_DECLARATION_DATE |

```python
df = ca.get_dividends_data(
    date_times=[sdate],
    date_col=col.DIVIDEND_DECLARATION_DATE
)
# returns pd.DataFrame -> [col.MSYMBOL_UKEY, col.DATETIME, col.DIVIDEND_TYPE, col.DIVIDEND_PER_SHARE]
```

---

## CorporateData

Access financial statement metrics and shareholding data.

```python
from mtech import CorporateData
from mtech import Universe
from mtech import DateTime
from mtech import Region
from mtech import columns as col
from mtech.enums import UniverseType
from mtech.enums import FinancialReportType
from mtech.enums import FinancialReportPeriod
from mtech.enums import FinancialReportMetric

region = Region("IN")
sdate  = DateTime("20240101")

univ   = Universe(region).get_universe(univ_type=UniverseType.NIFTY500, date=sdate)
ukeys  = univ[col.MSYMBOL_UKEY].tolist()

cd = CorporateData()
```

### Methods

#### `get_financial_statement_metric_as_on_date(as_on_date, report_type, report_period, report_metric, ukeys, lookback_periods, fallback_to_annual)`

Fetches the most recent available value of a financial metric as of a given date.

| Parameter | Type | Description |
|---|---|---|
| `as_on_date` | `DateTime` | Reference date |
| `report_type` | `FinancialReportType` | e.g. `FinancialReportType.INCOME_STATEMENT`, `FinancialReportType.BALANCE_SHEET` |
| `report_period` | `FinancialReportPeriod` | e.g. `FinancialReportPeriod.QUARTERLY`, `FinancialReportPeriod.ANNUAL` |
| `report_metric` | `FinancialReportMetric` | e.g. `FinancialReportMetric.TOTAL_REVENUE`, `FinancialReportMetric.PROFIT_AFTER_TAX` |
| `ukeys` | `List[int]` | List of security keys |
| `lookback_periods` | `int` | How many periods to look back (default: `2`) |
| `fallback_to_annual` | `bool` | Fall back to annual if quarterly unavailable (default: `False`) |

```python
df = cd.get_financial_statement_metric_as_on_date(
    as_on_date=sdate,
    report_type=FinancialReportType.INCOME_STATEMENT,
    report_period=FinancialReportPeriod.QUARTERLY,
    report_metric=FinancialReportMetric.TOTAL_REVENUE,
    ukeys=ukeys,
    lookback_periods=2,
    fallback_to_annual=True
)
# returns pd.DataFrame -> [col.MSYMBOL_UKEY, col.PERIOD, col.METRIC, col.VALUE, col.SOURCE]
```

---

#### `get_financial_statement_raw_metric_for_periods(as_on_date, report_type, report_period, report_metric, ukeys, periods)`

Fetches raw metric values for specific reporting periods.

| Parameter | Type | Description |
|---|---|---|
| `as_on_date` | `DateTime` | Reference date |
| `report_type` | `FinancialReportType` | e.g. `FinancialReportType.INCOME_STATEMENT`, `FinancialReportType.BALANCE_SHEET` |
| `report_period` | `FinancialReportPeriod` | e.g. `FinancialReportPeriod.QUARTERLY`, `FinancialReportPeriod.ANNUAL` |
| `report_metric` | `FinancialReportMetric` | e.g. `FinancialReportMetric.TOTAL_REVENUE`, `FinancialReportMetric.PROFIT_AFTER_TAX` |
| `ukeys` | `List[int]` | List of security keys |
| `periods` | `List[DateTime]` | Specific reporting periods as DateTime objects |

```python
df = cd.get_financial_statement_raw_metric_for_periods(
    as_on_date=sdate,
    report_type=FinancialReportType.INCOME_STATEMENT,
    report_period=FinancialReportPeriod.QUARTERLY,
    report_metric=FinancialReportMetric.REVENUE,
    ukeys=ukeys,
    periods=[DateTime("20231231"), DateTime("20221231")],
)
# returns pd.DataFrame -> [col.MSYMBOL_UKEY, col.PERIOD, col.METRIC, col.VALUE, col.SOURCE]
```

---

#### `get_share_holding_aggregate_data_as_on_date(as_on_date, ukeys, lookback_periods)`

| Parameter | Type | Description |
|---|---|---|
| `as_on_date` | `DateTime` | Reference date |
| `ukeys` | `List[int]` | List of security keys |
| `lookback_periods` | `int` | How many periods to look back (default: `2`) |

```python
df = cd.get_share_holding_aggregate_data_as_on_date(
    as_on_date=sdate,
    ukeys=ukeys,
    lookback_periods=2
)
# returns pd.DataFrame -> [col.MSYMBOL_UKEY, col.DATETIME, col.PERIOD, col.DATA_AVAILABILITY_DATE, col.PROMOTER_SHAREHOLDING_PCT, col.RETAIL_SHAREHOLDING_PCT, col.FII_SHAREHOLDING_PCT, col.MF_SHAREHOLDING_PCT, col.OTHER_DOMESTIC_SHAREHOLDING_PCT, col.OTHERS_SHAREHOLDING_PCT, col.DII_SHAREHOLDING_PCT]
```

---

#### `get_share_holding_aggregate_data_for_periods(as_on_date, ukeys, periods)`

| Parameter | Type | Description |
|---|---|---|
| `as_on_date` | `DateTime` | Reference date |
| `ukeys` | `List[int]` | List of security keys |
| `periods` | `List[DateTime]` | Specific reporting periods as DateTime objects |

```python
df = cd.get_share_holding_aggregate_data_for_periods(
    as_on_date=sdate,
    ukeys=ukeys,
    periods=[DateTime("20231231"), DateTime("20221231")],
)
# returns pd.DataFrame -> [col.DATETIME, col.PERIOD, col.DATA_AVAILABILITY_DATE, col.MSYMBOL_UKEY, col.PROMOTER_SHAREHOLDING_PCT, col.RETAIL_SHAREHOLDING_PCT, col.FII_SHAREHOLDING_PCT, col.MF_SHAREHOLDING_PCT, col.OTHER_DOMESTIC_SHAREHOLDING_PCT, col.OTHERS_SHAREHOLDING_PCT, col.DII_SHAREHOLDING_PCT]
```

---

## SecurityInfo

Look up securities, map identifiers, and retrieve metadata.

```python
from mtech import SecurityInfo
from mtech import Universe
from mtech import DateTime
from mtech import Region
from mtech import columns as col
from mtech.enums import UniverseType
from mtech.enums import FinancialType

region = Region("IN")
sdate  = DateTime("20240101")

univ   = Universe(region).get_universe(univ_type=UniverseType.NIFTY500, date=sdate)
ukeys  = univ[col.MSYMBOL_UKEY].tolist()

si = SecurityInfo()
```

### Methods

#### `get_sec_data(as_on_date, msymbols, ukeys, exchange_symbols)`

| Parameter | Type | Description |
|---|---|---|
| `as_on_date` | `DateTime` | Reference date |
| `msymbols` | `List[str]` | List of master symbols |
| `ukeys` | `List[int]` | List of security keys |
| `exchange_symbols` | `List[str]` | List of exchange symbols |

```python
df = si.get_sec_data(
    as_on_date=sdate,
    ukeys=ukeys,
)
# returns pd.DataFrame -> [col.EXCHANGE_SYMBOL, col.EXCHANGE_NAME, col.FINANCIAL_TYPE_NAME, col.MSYMBOL, col.MSYMBOL_UKEY, col.UNDERLYING_EXCHANGE_SYMBOL, col.UNDERLYING_MSYMBOL_UKEY, col.UNDERLYING_MSYMBOL, col.DATETIME_FORMATTED, col.EFFECTIVE_DATE, col.EXPIRATION_DATE]
```

---

#### `get_exchange_symbol_to_ukey_map(exchange_symbols)`

| Parameter | Type | Description |
|---|---|---|
| `exchange_symbols` | `pd.DataFrame` | DataFrame with columns `[col.EXCHANGE_SYMBOL, col.FINANCIAL_TYPE_NAME]` |

```python
df = si.get_exchange_symbol_to_ukey_map(
    exchange_symbols=df_exchange_symbols
)
```

---

#### `get_isin_to_exchange_symbol_map(isins, exchange_names)`

| Parameter | Type | Description |
|---|---|---|
| `isins` | `List[str]` | List of ISIN strings |
| `exchange_names` | `List[str]` | Filter by exchange names (optional) |

```python
df = si.get_isin_to_exchange_symbol_map(
    isins=["INE002A01018"],
    exchange_names=["NSE"]
)
# Index(['datetime', 'exchange_name', 'exchange_symbol', 'isin', 'datetime_formatted'], dtype='object')
```

---

#### `get_ukey_to_isin_map(ukeys, exchange_names)`

| Parameter | Type | Description |
|---|---|---|
| `ukeys` | `List[int]` | List of security keys |
| `exchange_names` | `List[str]` | Filter by exchange names (optional) |

```python
df = si.get_ukey_to_isin_map(ukeys=ukeys)
# Index(['msymbol_ukey', 'exchange_name', 'isin'], dtype='object')
```

---

#### `get_all_issues_for_underlying(as_on_date, underlying_msymbols, underlying_ukeys, underlying_exchange_symbols, financial_types)`

| Parameter | Type | Description |
|---|---|---|
| `as_on_date` | `DateTime` | Reference date (optional) |
| `underlying_msymbols` | `List[str]` | Underlying master symbols (optional) |
| `underlying_ukeys` | `List[int]` | Underlying security keys (optional) |
| `underlying_exchange_symbols` | `List[str]` | Underlying exchange symbols (optional) |
| `financial_types` | `List[FinancialType]` | Filter by instrument type e.g. `[FinancialType.EQ, FinancialType.FUT]` (optional) |

```python
df = si.get_all_issues_for_underlying(
    as_on_date=sdate,
    underlying_ukeys=ukeys,
)
# Index(['exchange_symbol', 'exchange_name', 'financial_type_name', 'msymbol',
#        'msymbol_ukey', 'underlying_exchange_symbol', 'underlying_msymbol_ukey',
#        'underlying_msymbol', 'datetime_formatted', 'effective_date',
#        'expiration_date'], dtype='object')
```

---

#### `map_ukey_to_underlying_ukeys(data, as_on_date, financial_types)`

| Parameter | Type | Description |
|---|---|---|
| `data` | `pd.DataFrame` | DataFrame containing ukeys to map |
| `as_on_date` | `DateTime` | Reference date |
| `financial_types` | `List[FinancialType]` | Filter by instrument type (optional) |

```python
df = si.map_ukey_to_underlying_ukeys(
    data=univ,
    as_on_date=sdate,
    financial_types=[FinancialType.EQ]
)
```

---

#### `get_ipo_dates(ukeys)`

| Parameter | Type | Description |
|---|---|---|
| `ukeys` | `List[int]` | List of security keys |

```python
df = si.get_ipo_dates(ukeys=ukeys)
# Index(['msymbol_ukey', 'ipo_date'], dtype='object')
```

---

#### `get_company_metadata(ukeys)`

| Parameter | Type | Description |
|---|---|---|
| `ukeys` | `List[int]` | List of security keys |

```python
df = si.get_company_metadata(ukeys=ukeys)
# Index(['msymbol_ukey', 'company_name', 'gics_sector', 'gics_group',
#        'gics_industry', 'gics_sub_industry'], dtype='object')
```

---

#### `closest_match_to_underlying_ukeys(date, names, derivatives)`

| Parameter | Type | Description |
|---|---|---|
| `date` | `DateTime` | Reference date |
| `names` | `List[str]` | Company names to fuzzy-match |
| `derivatives` | `bool` | Include derivative instruments (default: `False`) |

```python
df = si.closest_match_to_underlying_ukeys(
    date=sdate,
    names=["Reliance Industries", "Infosys"],
    derivatives=False
)
# Index(['company_name', 'underlying_msymbol_ukey'], dtype='object')
```

---

#### `get_active_futures_contracts_for_underlying(as_on_date, underlying_ukeys)`

| Parameter | Type | Description |
|---|---|---|
| `as_on_date` | `DateTime` | Reference date |
| `underlying_ukeys` | `List[int]` | List of underlying security keys |

```python
df = si.get_active_futures_contracts_for_underlying(
    as_on_date=sdate,
    underlying_ukeys=ukeys
)
# Index(['datetime', 'exchange_symbol', 'exchange_name', 'msymbol',
#        'msymbol_ukey', 'underlying_exchange_symbol', 'underlying_msymbol',
#        'underlying_msymbol_ukey', 'effective_date', 'expiration_date',
#        'lot_size', 'datetime_formatted'], dtype='object')
```

---

#### `get_margin_pct(as_on_date, ukeys)`

| Parameter | Type | Description |
|---|---|---|
| `as_on_date` | `DateTime` | Reference date |
| `ukeys` | `List[int]` | List of security keys |

```python
df = si.get_margin_pct(
    as_on_date=sdate,
    ukeys=ukeys
)
# Index(['msymbol_ukey', 'financial_type_name', 'margin_pct'], dtype='object')
```

---

## Returns

Compute forward, daily, cumulative, category-level returns.

```python
from mtech import Returns
from mtech import DateTime
from mtech import Region
from mtech import Universe
from mtech import columns as col
from mtech import constants as cns
from mtech.enums import UniverseType
from mtech.enums import ReturnType
from mtech.enums import ForwardReturnHorizon
from mtech.enums import PortfolioWeights

returns = Returns(Region("IN"))
sdate = DateTime("20240101")
edate = DateTime("20240630")

univ = Universe(Region("IN")).get_universe(
    univ_type=UniverseType.NIFTY500,
    date=sdate,
)
ukeys = univ[col.MSYMBOL_UKEY].tolist()
```

### Constructor

```python
Returns(region: str, base_url: str = None)
```

| Parameter | Type | Description |
|---|---|---|
| `region` | `Region` | Region code used for business-date calendars, e.g. `"IN"` |
| `base_url` | `str` | Optional API base URL override |

### Accepted Calculation Values

`ReturnType` supports `"TOTAL"` and `"RESIDUAL"`. A `risk_model` must be supplied for residual returns.

`horizon` supports ForwardReturnHorizon from enums:

```textA
ForwardReturnHorizon.FWD_1D,
ForwardReturnHorizon.FWD_1D_2D,
ForwardReturnHorizon.FWD_2D_3D,
ForwardReturnHorizon.FWD_3D_5D,
ForwardReturnHorizon.FWD_5D_21D,
ForwardReturnHorizon.FWD_21D_63D,
ForwardReturnHorizon.FWD_63D_126D,
ForwardReturnHorizon.FWD_126D_252D,
ForwardReturnHorizon.FWD_1D_21D,
ForwardReturnHorizon.FWD_1D_63D,
ForwardReturnHorizon.FWD_1D_126D,
ForwardReturnHorizon.FWD_1D_252D,
```

### Methods

#### `forward_total_returns(date_times, horizon, ukeys=None)`

Compounds daily total returns over the requested forward business-day horizon.

| Parameter | Type | Description |
|---|---|---|
| `date_times` | `List[DateTime]` | Dates queried for forward return.  |
| `horizon` | `ForwardReturnHorizon` | One of the supported forward-horizon values above |
| `ukeys` | `List[int]` | Optional security filter; `None` or an empty list means no explicit ukey filter |

```python
df = returns.forward_total_returns(
    date_times=[sdate],
    horizon=ForwardReturnHorizon.FWD_5D_21D,
    ukeys=ukeys,
)
# returns pd.DataFrame -> [col.DATETIME, col.HORIZON_START_DATE, col.HORIZON_END_DATE, col.MSYMBOL_UKEY, col.RETURN]

```

---

#### `forward_residual_returns(date_times, horizon, risk_model, ukeys=None)`

Compounds security-level residual returns from a risk model over the requested business days and horizon.

| Parameter | Type | Description |
|---|---|---|
| `date_times` | `List[DateTime]` | Dates queried for forward return. |
| `horizon` | `ForwardReturnHorizon` | One of the supported forward-horizon values above |
| `risk_model` | `str` | Risk model , e.g. `"INEC1"` |
| `ukeys` | `List[int]` | Optional security filter |

```python
df = returns.forward_residual_returns(
    date_times=[sdate],
    horizon=ForwardReturnHorizon.FWD_5D_21D,
    risk_model="INEC1",
    ukeys=ukeys,
)
# returns pd.DataFrame -> [col.DATETIME, col.HORIZON_START_DATE, col.HORIZON_END_DATE, col.MSYMBOL_UKEY, col.RESIDUAL_RETURN]

```

---

#### `daily_returns(date_times, return_type, ukeys=None, filter_for_fin_types=None, risk_model=None)`

Returns daily total or residual returns.

| Parameter | Type | Description |
|---|---|---|
| `date_times` | `List[DateTime]` | Dates to query |
| `return_type` | `ReturnType` | `ReturnType.TOTAL or ReturnType.RESIDUAL` |
| `ukeys` | `List[int]` | Optional security filter |
| `filter_for_fin_types` | `List[str]` | Optional financial-type filter, e.g. `[cns.COMMON_STOCK]` |
| `risk_model` | `str` | Required when `return_type=ReturnType.RESIDUAL` |

```python
df = returns.daily_returns(
    date_times=[sdate],
    return_type= ReturnType.TOTAL,
    ukeys=ukeys,
    filter_for_fin_types = None,
    risk_model="INEC1",
)
# returns pd.DataFrame -> [col.DATETIME, col.MSYMBOL_UKEY, col.RETURN]
```

---

#### `cumulative_returns(start_date, end_date, return_type, ukeys=None, filter_for_fin_types=None, risk_model=None)`

Compounds the available daily returns for each security across the business-date range using `prod(1 + return) - 1`.

| Parameter | Type | Description |
|---|---|---|
| `start_date` | `DateTime` | Start of the date range |
| `end_date` | `DateTime` | End of the date range |
| `return_type` | `ReturnType` | ``ReturnType.TOTAL or ReturnType.RESIDUAL`` |
| `ukeys` | `List[int]` | Optional security filter |
| `filter_for_fin_types` | `List[str]` | Optional financial-type filter |
| `risk_model` | `str` | Required when `return_type="residual"` |

```python
df = returns.cumulative_returns(
    start_date=sdate,
    end_date=edate,
    return_type=ReturnType.TOTAL,
    ukeys=ukeys,
)
# returns pd.DataFrame -> [col.MSYMBOL_UKEY, col.RETURN]
```

---

#### `category_cumulative_returns(start_date, end_date, return_type, category_col, weight_type, ukeys=None, filter_for_fin_types=None, risk_model=None)`

Calculates daily weighted returns within a company-metadata category, compounds them over the date range, and maps each category result back to its securities.
| Parameter | Type | Description |
|---|---|---|
| `start_date` | `DateTime` | Start of the date range |
| `end_date` | `DateTime` | End of the date range |
| `return_type` | `ReturnType` | `ReturnType.TOTAL` or `ReturnType.RESIDUAL` |
| `category_col` | `str` | Company-metadata column used for grouping, e.g. `col.GICS_SECTOR` |
| `weight_type` | `PortfolioWeights` | `PortfolioWeights.EQUAL` or `PortfolioWeights.MARKET_CAP` |
| `ukeys` | `List[int]` | Optional security filter |
| `filter_for_fin_types` | `List[str]` | Optional financial-type filter |
| `risk_model` | `str` | Required when `return_type="residual"` |

```python
df = returns.category_cumulative_returns(
    start_date=sdate,
    end_date=edate,
    return_type=ReturnType.TOTAL,
    category_col=col.GICS_SECTOR,
    weight_type=PortfolioWeights.MARKET_CAP,
    ukeys=ukeys,
)
# returns pd.DataFrame -> [col.MSYMBOL_UKEY, col.GICS_SECTOR, col.RETURN]
```

---

#### `returns_rsquared(date_times, return_type, ukeys=None, filter_for_fin_types=None, risk_model=None)`

| Parameter | Type | Description |
|---|---|---|
| `date_times` | `List[DateTime]` | Dates used to construct the return path |
| `return_type` | `ReturnType` | `ReturnType.TOTAL` or `ReturnType.RESIDUAL` |
| `ukeys` | `List[int]` | Optional security filter |
| `filter_for_fin_types` | `List[str]` | Optional financial-type filter |
| `risk_model` | `str` | Required when `return_type="residual"` |

```python
df = returns.returns_rsquared(
    date_times=[sdate],
    return_type=ReturnType.TOTAL,
    ukeys=ukeys,
)
# returns pd.DataFrame -> [col.MSYMBOL_UKEY, col.RSQUARED]
```

---

## RiskDecomposition

Access risk-model data and calculate portfolio exposures, volatility, variance contributions, model P&L, event sensitivity, and equal-risk weights.

```python
from mtech import RiskDecomposition
from mtech import DateTime
from mtech import columns as col

risk = RiskDecomposition(model_name="INEC1")
date = DateTime("20240131")
univ = Universe(Region("IN")).get_universe(
    univ_type=UniverseType.NIFTY500,
    date=sdate,
)
ukeys = univ[col.MSYMBOL_UKEY].tolist()
```

The current implementation supports the `"INEC1"` model.

### Constructor

```python
RiskDecomposition(model_name: str, base_url: str = None)
```

| Parameter | Type | Description |
|---|---|---|
| `model_name` | `str` | Risk-model name, currently `"INEC1"` |
| `base_url` | `str` | Optional API base URL override |

Common date parameters use the following public types:

| Parameter | Type | Description |
|---|---|---|
| `date_times` | `List[DateTime]` | One or more business dates |
| `date` | `DateTime` | single business date |
| `wide_format` | `bool` | Return matrix-like factor columns instead of long-form records (default: `False`) |

### Model Data Methods

All methods in this table return a `pd.DataFrame`.

| Method | Description | Output |
|---|---|---|
| `get_universe(date_times)` | Get model securities and estimation-universe membership | `[col.DATETIME, col.MSYMBOL_UKEY, col.IN_ESTU]` |
| `get_factor_map()` | Map each factor to its Market, Style, or Industry factor type | `[col.FACTOR_TYPE, col.FACTOR_NAME]` |
| `get_factor_loadings(date_times, wide_format=False)` | Get security factor loadings; pivot to one column per factor when `wide_format=True` | Long form: `[col.DATETIME, col.FACTOR_NAME, col.IN_ESTU, col.MSYMBOL_UKEY, col.FACTOR_LOADING]` |
| `get_factor_returns(date_times)` | Get daily factor returns and model-fit statistics | `[col.DATETIME, col.FACTOR_NAME, col.FACTOR_RETURN, col.TSTAT, col.RSQUARED, col.ADJ_RSQUARED]` |
| `get_residual_returns(date_times)` | Get the security-level return unexplained by the model | `[col.DATETIME, col.MSYMBOL_UKEY, col.RETURN, col.FACTOR_RETURN, col.RESIDUAL_RETURN]` |
| `get_factor_vol(date_times)` | Get annualized factor volatility | `[col.DATETIME, col.FACTOR_NAME, col.FACTOR_VOL]` |
| `get_factor_covariance(date_times)` | Get factor covariance in long or matrix-like wide form | Long form: `[col.DATETIME, col.FACTOR_NAME_1, col.FACTOR_NAME_2, col.FACTOR_COVARIANCE]` |
| `get_srisk(date_times)` | Get security-specific risk used as idiosyncratic volatility | `[col.DATETIME, col.MSYMBOL_UKEY, col.SRISK]` |
| `get_trisk(date_times)` | Get security-level total risk | `[col.DATETIME, col.MSYMBOL_UKEY, col.TRISK]` |
| `get_beta(date_times)` | Get security-level model beta | `[col.DATETIME, col.MSYMBOL_UKEY, col.BETA]` |

`wide_format=True` produces:

- factor loadings: `[col.DATETIME, col.MSYMBOL_UKEY, col.IN_ESTU, <one column per factor>]`
- factor covariance: `[col.DATETIME, col.FACTOR_NAME_1, <one column per factor>]`

```python
factor_map = risk.get_factor_map()
loadings = risk.get_factor_loadings(
    date_times=[date],
    wide_format=False,
)
covariance = risk.get_factor_covariance(
    date_times=[date],
    wide_format=True,
)
```

### Portfolio Input

Portfolio methods accept a DataFrame which has relevant columns. Each weight record requires `col.MSYMBOL_UKEY` and `col.WEIGHT`. Calls can be more optimized by using groupby_cols which allow unique portfolios to be analyzed at once. eg:- groupby_cols=[col.DATETIME,col.PORTFOLIO_TYPE]

| Parameter | Type | Description |
|---|---|---|
| `date` | `DateTime` | Portfolio analysis date |
| `weights` | `pd.DataFrame` | Security weight records |
| `groupby_cols` | `List[str]` | Optional record fields used to calculate separate portfolios (default: `[]`) |
| `aggregate` | `bool` | Aggregate factor exposures to portfolio/group level (default: `True`) |

### Portfolio Exposure and Volatility Methods

The output of each grouped calculation begins with the requested `groupby_cols`.

| Method | Calculation | Output after `groupby_cols` |
|---|---|---|
| `get_portfolio_beta(date, weights, groupby_cols=[])` | Sum of `weight * beta` | `[col.BETA]` |
| `get_portfolio_stock_level_beta(date, weights, groupby_cols=[])` | Per-security | `[col.MSYMBOL_UKEY, col.BETA_EXP]` |
| `get_portfolio_factor_exposures(date, weights, groupby_cols=[], aggregate=True)` | Weighted factor loadings,  | `[col.FACTOR_NAME, col.FACTOR_EXPOSURE]` when aggregated |
| `get_portfolio_factor_vol(date, weights, groupby_cols=[])` | Factor volatility, | `[col.FACTOR_VOL]` |
| `get_portfolio_factor_group_vol(date, weights, groupby_cols=[])` | Separate Market, Style, and Industry factor-block volatility | `[col.MARKET_VOL, col.STYLE_VOL, col.INDUSTRY_VOL]` |
| `get_portfolio_idio_vol(date, weights, groupby_cols=[])` | Idiosyncratic volatility, | `[col.IDIO_VOL]` |
| `get_portfolio_total_vol(date, weights, groupby_cols=[])` | Factor, factor-group, idiosyncratic, and total volatility | `[col.FACTOR_VOL, col.MARKET_VOL, col.STYLE_VOL, col.INDUSTRY_VOL, col.IDIO_VOL, col.TOTAL_VOL]` |

```python
portfolio_risk = risk.get_portfolio_total_vol(
    date=date,
    weights=weights,
    groupby_cols=[col.PORTFOLIO_TYPE],
)
# returns pd.DataFrame -> [col.PORTFOLIO_TYPE, col.FACTOR_VOL, col.MARKET_VOL,
#                          col.STYLE_VOL, col.INDUSTRY_VOL,
#                          col.IDIO_VOL, col.TOTAL_VOL]
```

### Variance Attribution and P&L Methods

| Method | Description | Output after `groupby_cols` |
|---|---|---|
| `get_portfolio_marginal_idio_var_contribution(date, weights, groupby_cols=[])` | Per-security idiosyncratic variance and its share of group idiosyncratic variance | `[col.MSYMBOL_UKEY, col.WEIGHT, col.MARGINAL_IDIO_VAR, col.MARGINAL_IDIO_VAR_CONTRIB]` |
| `get_portfolio_marginal_factor_var_contribution(date, weights, groupby_cols=[])` | Per-factor marginal variance and its share of total factor variance | `[col.FACTOR_NAME, col.MARGINAL_FACTOR_VAR, col.MARGINAL_FACTOR_VAR_CONTRIB]` |
| `get_portfolio_marginal_stock_level_factor_var_contribution(date, weights, groupby_cols=[])` | Per-security, per-factor marginal factor variance | `[col.MSYMBOL_UKEY, col.FACTOR_NAME, col.MARGINAL_FACTOR_VAR]` |
| `get_portfolio_marginal_total_var_contribution(date, weights, groupby_cols=[])` | Per-security factor-group, idiosyncratic, and total variance attribution | See the expanded schema below |
| `get_portfolio_stock_level_risk_model_pnl(date, weights, groupby_cols=[])` | Same-date weighted residual and factor P&L, with factor P&L split by type | `[col.MSYMBOL_UKEY, col.RESIDUAL_PNL, col.FACTOR_PNL, col.MARKET_PNL, col.STYLE_PNL, col.INDUSTRY_PNL]` |

`get_portfolio_marginal_total_var_contribution` returns:

```text
groupby_cols
+ [col.MSYMBOL_UKEY,
   col.MARGINAL_FACTOR_VAR,   col.MARGINAL_FACTOR_VAR_CONTRIB,
   col.MARGINAL_MARKET_VAR,   col.MARGINAL_MARKET_VAR_CONTRIB,
   col.MARGINAL_STYLE_VAR,    col.MARGINAL_STYLE_VAR_CONTRIB,
   col.MARGINAL_INDUSTRY_VAR, col.MARGINAL_INDUSTRY_VAR_CONTRIB,
   col.MARGINAL_IDIO_VAR,     col.MARGINAL_IDIO_VAR_CONTRIB,
   col.MARGINAL_TOTAL_VAR,    col.MARGINAL_TOTAL_VAR_CONTRIB]
```

```python
contributions = risk.get_portfolio_marginal_total_var_contribution(
    date=date,
    weights=weights,
    groupby_cols=groupby_cols,
)
```

### Equal-Risk Portfolio

#### `build_equal_risk_portfolio(date, ukeys, risk_type="total")`

Builds a long-only, fully invested portfolio whose securities have approximately equal total-risk contributions.

| Parameter | Type | Description |
|---|---|---|
| `date` | `DateTime` | Portfolio construction date |
| `ukeys` | `List[int]` | Candidate security keys |
| `risk_type` | `str` | Risk objective; `"total"`|

```python
equal_risk_weights = risk.build_equal_risk_portfolio(
    date=date,
    ukeys=ukeys,
    risk_type="total",
)
# returns pd.DataFrame -> [col.MSYMBOL_UKEY, col.WEIGHT]
```

## Constants & Columns

Two pre-instantiated objects expose defined constants and standard column names as attributes.

```python
from mtech import constants as cns
from mtech import columns as col

print(cns.IST_TZ)  # "Asia/Kolkata"
print(col.UKEY)    # "ukey"
print(col.DATE)    # "date"
```

These are loaded automatically on import.

---

## Enums

Enum types are used as typed parameters across several classes. Import them from `mtech.enums`:

```python
from mtech.enums import VOLUME_TYPE
from mtech.enums import FinancialReportType
from mtech.enums import FinancialReportPeriod
from mtech.enums import FinancialReportMetric
from mtech.enums import FinancialType
from mtech.enums import UniverseType
```

### `VOLUME_TYPE`

Used in `MarketData` volume methods.

| Value | Description |
|---|---|
| `VOLUME_TYPE.MULTI_EXCHANGE_VOLUME` | Combined volume across all exchanges (default) |
| `VOLUME_TYPE.EXCHANGE_VOLUME` | Volume on the primary exchange only |

---

### `FinancialReportType`

Used in `CorporateData` financial statement methods.

| Value | Description |
|---|---|
| `FinancialReportType.INCOME_STATEMENT` | Profit & Loss statement |
| `FinancialReportType.BALANCE_SHEET` | Balance sheet |
| `FinancialReportType.CASH_FLOW` | Cash flow statement |

---

### `FinancialReportPeriod`

Used in `CorporateData` financial statement methods.

| Value | Description |
|---|---|
| `FinancialReportPeriod.QUARTERLY` | Quarterly report |
| `FinancialReportPeriod.ANNUAL` | Annual report |

---

### `FinancialReportMetric`

Used in `CorporateData` financial statement methods.

---

### `FinancialType`

Used in `SecurityInfo` methods to filter by instrument type.

| Value | Description |
|---|---|
| `FinancialType.EQ` | Equity / common stock |
| `FinancialType.FUT` | Futures contract |
| `FinancialType.OPT` | Options contract |

---

### `UniverseType`

Used in `Universe.get_universe()`.
