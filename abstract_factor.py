from abc import ABC, abstractmethod

from mtech import Region
from mtech import DateTime
from mtech import CorporateActions
from mtech import CorporateData
from mtech import Universe
from mtech import DateUtils
from mtech import MarketData
from mtech import constants as cns
from mtech import columns as col
from mtech import SecurityInfo

import pandas as pd

from mtech.enums import UniverseType
from mtech.enums import FinancialReportType
from mtech.enums import FinancialReportMetric
from mtech.enums import FinancialReportPeriod

from mtech.ParallelUtils import loop_parallel
from multiprocessing import cpu_count
from functools import partial

import boto3
import os
import io


class AbstractFactor(ABC):

    def __init__(self, region: Region):
        self._region = region

    @abstractmethod
    def compute(self, date: DateTime) -> float:
        pass

    def _process_single_date(self, date):
        import io
        import boto3
        import os

        s3 = boto3.client('s3')
        USER_ID = os.environ.get('USER_ID')
        BUCKET = os.environ.get('S3_BUCKET')
        CLASS_NAME = self.__class__.__name__

        df = self.compute(date)

        if df is None or df.empty:
            print(f"Skipping {date} (empty df)")
            return

        ukey_exch_sym_map = SecurityInfo().get_sec_data(
            as_on_date=date,
            ukeys=df[col.MSYMBOL_UKEY].unique().tolist()
        )[[col.MSYMBOL_UKEY, col.EXCHANGE_SYMBOL]]

        df[col.MSYMBOL_UKEY] = pd.to_numeric(df[col.MSYMBOL_UKEY], errors="coerce")
        ukey_exch_sym_map[col.MSYMBOL_UKEY] = pd.to_numeric(ukey_exch_sym_map[col.MSYMBOL_UKEY], errors="coerce")

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

    def backfill(self, sdate: DateTime, edate: DateTime, force_query: bool = True):
        dates = DateUtils().get_busdate_range(sdate, edate, self._region)

        s3 = boto3.client('s3')
        USER_ID = os.environ.get('USER_ID')
        BUCKET = os.environ.get('S3_BUCKET')
        CLASS_NAME = self.__class__.__name__

        prefix = f"{USER_ID}/data/{CLASS_NAME}/"

        if force_query == False:
            existing_dates = set()
            continuation_token = None

            while True:
                params = {
                    "Bucket": BUCKET,
                    "Prefix": prefix
                }

                if continuation_token:
                    params["ContinuationToken"] = continuation_token

                response = s3.list_objects_v2(**params)

                for obj in response.get("Contents", []):
                    key = obj["Key"]
                    filename = key.split("/")[-1]
                    date_str = filename.replace(".csv", "")

                    existing_dates.add(DateTime(date_str))

                continuation_token = response.get("NextContinuationToken")
                if not continuation_token:
                    break

            dates = [d for d in dates if d not in existing_dates]

        loop_parallel(
            iter_list=dates,
            func=partial(self._process_single_date),
            processes=cpu_count(),   
            use_threads=True,
        )

        meta_content = f"""ALPHA_KEY = {CLASS_NAME}
    ALPHA_DESCRIPTION = From Code editor
    START_DATE = {sdate}
    END_DATE = {edate}
    PRODUCTION_UPLOADED = FALSE
    """

        meta_key = f"{USER_ID}/meta_data/{CLASS_NAME}/meta.txt"

        s3.put_object(
            Bucket=BUCKET,
            Key=meta_key,
            Body=meta_content.encode("utf-8")
        )

        print(f"Metadata uploaded: s3://{BUCKET}/{meta_key}")