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
import shutil
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

        date_str = str(date)
        dir_path = os.path.join("temp", CLASS_NAME)
        os.makedirs(dir_path, exist_ok=True)

        file_path = os.path.join(dir_path, f"{date_str}.csv")
        df.to_csv(file_path, index=False)

        print(f"Saved locally: {file_path}")


    def backfill(self, sdate: DateTime, edate: DateTime):
        dates = DateUtils().get_busdate_range(sdate, edate, self._region)

        USER_ID = os.environ.get('USER_ID')
        BUCKET = os.environ.get('S3_BUCKET')
        CLASS_NAME = self.__class__.__name__

        dir_path = os.path.join("temp", CLASS_NAME)
        os.makedirs(dir_path, exist_ok=True)

        loop_parallel(
            iter_list=dates,
            func=partial(self._process_single_date),
            processes=cpu_count(),
            use_threads=False,
        )

        zip_base_path = os.path.join("temp", CLASS_NAME)
        zip_file_path = shutil.make_archive(zip_base_path, 'zip', dir_path)

        print(f"Zipped files at: {zip_file_path}")

        s3 = boto3.client('s3')
        zip_key = f"{USER_ID}/data/{CLASS_NAME}/{CLASS_NAME}_{sdate}_{edate}.zip"

        with open(zip_file_path, "rb") as f:
            s3.upload_fileobj(f, BUCKET, zip_key)

        print(f"Uploaded zip: s3://{BUCKET}/{zip_key}")

        meta_content = f"""ALPHA_KEY = {CLASS_NAME}
    ALPHA_DESCRIPTION = From Code editor
    START_DATE = {sdate}
    END_DATE = {edate}
    PRODUCTION_UPLOADED = FALSE
    PRODUCTION_FILE_NAME = {CLASS_NAME}_{sdate}_{edate}.zip
    """

        meta_key = f"{USER_ID}/meta_data/{CLASS_NAME}/meta.txt"

        s3.put_object(
            Bucket=BUCKET,
            Key=meta_key,
            Body=meta_content.encode("utf-8")
        )

        print(f"Metadata uploaded: s3://{BUCKET}/{meta_key}")