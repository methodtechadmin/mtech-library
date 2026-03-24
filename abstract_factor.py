
from abc import ABC, abstractmethod
from mtech import Region,DateTime,CorporateActions,Universe,DateUtils,MarketData,constants as cns,columns as col
import pandas as pd

class AbstractFactor(ABC):

    def __init__(self, region: Region):
        self._region = region

    @abstractmethod
    def compute(self, date: DateTime) -> float:
        pass

class SampleFactor(AbstractFactor):

    def __init__(self, region: Region):
        super().__init__(region)

    def compute(self, date: DateTime) -> pd.DataFrame:
        univ = Universe(self._region).get_universe(univ_type="nifty",date=date)
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
        print(df)

        df[col.SCORE] = df["price_21"]/df["price_252"] - 1

        df = df[[col.DATETIME,col.MSYMBOL_UKEY,col.SCORE]]

        return df


if __name__ == "__main__":
    factor = SampleFactor(Region("IN"))
    print(factor.compute(DateTime("20200101")))
