
from abc import ABC, abstractmethod
from mtech import Region,DateTime,CorporateActions,CorporateData,Universe,DateUtils,MarketData,constants as cns,columns as col
import pandas as pd
from mtech.enums import UniverseType, FinancialReportType, FinancialReportMetric,FinancialReportPeriod

class AbstractFactor(ABC):

    def __init__(self, region: Region):
        self._region = region

    @abstractmethod
    def compute(self, date: DateTime) -> float:
        pass
