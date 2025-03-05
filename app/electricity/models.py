from pydantic import BaseModel
from typing import List, Dict, Optional, Union

class MinutelyUsageRequest(BaseModel):
    product_id: str
    date: str  # YYYY-MM-DD format
    hour: str  # HH format (00-23)

class HourlyUsageRequest(BaseModel):
    product_id: str
    date: str  # YYYY-MM-DD format

class DailyUsageRequest(BaseModel):
    product_id: str
    year_month: str  # YYYY-MM format

class MonthlyUsageRequest(BaseModel):
    product_id: str
    year: str  # YYYY format

class ChartDataPoint(BaseModel):
    label: str
    value: float

class ChartDataResponse(BaseModel):
    data_points: List[ChartDataPoint]
    chart_title: str
    x_axis_label: str
    y_axis_label: str = "Power Consumption (W)"