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
        univ = Universe(self._region).get_universe(univ_type=UniverseType.NIFTY,date=date)
        ukeys = univ[col.MSYMBOL_UKEY].tolist()

        df_21 = MarketData().get_adjusted_price(
            date_times=[DateUtils().shift_busdate(date, self._region, -cns.DAYS_IN_MONTH)],
            ukeys=ukeys
        )[[col.MSYMBOL_UKEY, col.CLOSE_PRICE]].rename(columns={col.CLOSE_PRICE: "price_21"})

        df_252 = MarketData().get_adjusted_price(
            date_times=[DateUtils().shift_busdate(date, self._region, -cns.DAYS_IN_YEAR)],
            ukeys=ukeys
        )[[col.MSYMBOL_UKEY, col.CLOSE_PRICE]].rename(columns={col.CLOSE_PRICE: "price_252"})

        df = (
            univ.merge(df_21, on=col.MSYMBOL_UKEY)
                .merge(df_252, on=col.MSYMBOL_UKEY)
        )

        df[col.SCORE] = df["price_21"]/df["price_252"] - 1

        df = df[[col.DATETIME,col.MSYMBOL_UKEY,col.SCORE]]

        return df


if __name__ == "__main__":
    factor = SampleFactor(Region("IN"))
    df = factor.compute(DateTime("20200101"))
    print(df)

    factor.backfill(DateTime("20200101"),DateTime("20200105"))
