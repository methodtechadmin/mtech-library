from abstract_factor import AbstractFactor

from mtech import Region
from mtech import DateTime
from mtech import CorporateActions
from mtech import CorporateData
from mtech import Universe
from mtech import DateUtils
from mtech import MarketData
from mtech import constants as cns
from mtech import columns as col

import pandas as pd

from mtech.enums import UniverseType
from mtech.enums import FinancialReportType
from mtech.enums import FinancialReportMetric
from mtech.enums import FinancialReportPeriod

class SampleFactor(AbstractFactor):

    def __init__(self, region: Region):
        super().__init__(region)

    def compute(self, date: DateTime) -> pd.DataFrame:
        
        omit_days = cns.DAYS_IN_WEEK
        lookback_days = 3 * cns.DAYS_IN_MONTH 

        edate = DateUtils().shift_busdate(date, self._region, -omit_days)
        sdate = DateUtils().shift_busdate(date, self._region, -lookback_days)

        # universe
        univ = Universe(self._region).get_universe(
            univ_type=UniverseType.NIFTY,
            date=date
        )
        ukeys = univ[col.MSYMBOL_UKEY].tolist()

        # prices
        df_edate = MarketData().get_adjusted_price(
            date_times=[edate],
            ukeys=ukeys
        )[[col.MSYMBOL_UKEY, col.CLOSE_PRICE]] \
         .rename(columns={col.CLOSE_PRICE: "price_edate"})

        df_sdate = MarketData().get_adjusted_price(
            date_times=[sdate],
            ukeys=ukeys
        )[[col.MSYMBOL_UKEY, col.CLOSE_PRICE]] \
         .rename(columns={col.CLOSE_PRICE: "price_sdate"})

        # merge
        df = (
            univ
            .merge(df_edate, on=col.MSYMBOL_UKEY, how="inner")
            .merge(df_sdate, on=col.MSYMBOL_UKEY, how="inner")
        )

        df[col.SCORE] = df["price_edate"] / df["price_sdate"] - 1

        return df[[col.DATETIME, col.MSYMBOL_UKEY, col.SCORE]]


if __name__ == "__main__":
    factor = SampleFactor(Region("IN"))
    df = factor.compute(DateTime("20200101"))
    print(df)

    factor.backfill(DateTime("20200101"),DateTime("20200105"))
