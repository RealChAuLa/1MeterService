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

# New models for payment and billing
class PaymentRecord(BaseModel):
    month: str  # YYYY-MM format
    amount: float

class PaymentHistoryResponse(BaseModel):
    username: str
    payments: List[PaymentRecord]
    email: Optional[str] = None

class BillCalculationRequest(BaseModel):
    username: str

# Update the BillResponse model to include a message field
class BillResponse(BaseModel):
    username: str
    year_month: str  # YYYY-MM format
    total_kwh: float
    amount: float
    is_paid: bool
    payment_date: Optional[str] = None
    message: str = ""  # Add this field for status messages

class ConnectionStatusRequest(BaseModel):
    product_id: str
    status: bool

class ConnectionStatusResponse(BaseModel):
    product_id: str
    status: bool
    updated_at: str
    message: str

class UserProductStatus(BaseModel):
    username: str
    product_id: str
    email: Optional[str] = None
    connection_status: bool
    last_active: Optional[str] = None  # Will show the latest timestamp from data if available

class AllConnectionStatusResponse(BaseModel):
    timestamp: str  # Current UTC time when the request was made
    users: List[UserProductStatus]
    total_count: int