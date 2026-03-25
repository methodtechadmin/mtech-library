
from abc import ABC, abstractmethod
from mtech import Region,DateTime,CorporateActions,CorporateData,Universe,DateUtils,MarketData,constants as cns,columns as col, SecurityInfo
import pandas as pd
from mtech.enums import UniverseType, FinancialReportType, FinancialReportMetric,FinancialReportPeriod
import boto3
import os
import io

class AbstractFactor(ABC):

    def __init__(self, region: Region):
        self._region = region

    @abstractmethod
    def compute(self, date: DateTime) -> float:
        pass

    def backfill(self, sdate: DateTime, edate: DateTime):
        dates = DateUtils().get_busdate_range(sdate, edate)

        s3 = boto3.client('s3')
        USER_ID = os.environ.get('USER_ID')
        BUCKET = os.environ.get('S3_BUCKET')
        CLASS_NAME = self.__class__.__name__

        for date in dates:
            df = self.compute(date)

            if df is None or df.empty:
                print(f"Skipping {date} (empty df)")
                continue

            ukey_exch_sym_map = SecurityInfo().get_sec_data(as_on_date=date, ukeys=df[col.MSYMBOL_UKEY].unique().tolist())[[col.MSYMBOL_UKEY, col.EXCHANGE_SYMBOL]]
            df = df.merge(
                ukey_exch_sym_map,
                on=col.MSYMBOL_UKEY,
                how="left"
            )
                df = df.rename(columns={
                col.DATETIME: "Date",
                col.EXCHANGE_SYMBOL: "ExchangeSymbol",
                col.SCORE: "Alpha"
            })

            df = df[["Date", "ExchangeSymbol", "Alpha"]]
            buffer = io.BytesIO()

            df.to_csv(buffer, index=False)

            buffer.seek(0)

            date_str = str(date)
            key = f"{USER_ID}/data/{CLASS_NAME}/{date_str}.csv"

            s3.upload_fileobj(buffer, BUCKET, key)

            print(f"Uploaded: s3://{BUCKET}/{key}")
                
        meta_content = f"""ALPHA_KEY = {CLASS_NAME}
        ALPHA_DESCRIPTION = From Code editor
        START_DATE = {sdate}
        END_DATE = {edate}
        """

        meta_key = f"{USER_ID}/meta_data/{CLASS_NAME}/meta.txt"

        s3.put_object(
            Bucket=BUCKET,
            Key=meta_key,
            Body=meta_content.encode("utf-8")
        )

        print(f"Metadata uploaded: s3://{BUCKET}/{meta_key}")