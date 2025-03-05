from fastapi import APIRouter, HTTPException, status

from app.electricity.models import (
    MinutelyUsageRequest,
    HourlyUsageRequest,
    DailyUsageRequest,
    MonthlyUsageRequest,
    ChartDataResponse
)
from app.electricity.service import ElectricityUsageService

router = APIRouter()


@router.post("/minutely", response_model=ChartDataResponse)
async def get_minutely_usage(request: MinutelyUsageRequest):
    """
    Get minute-by-minute electricity usage for a specific hour in a day.

    Returns data for chart where:
    - X-axis shows minutes (00-59)
    - Y-axis shows average watt values

    This endpoint is publicly accessible.
    """
    return ElectricityUsageService.get_minutely_usage(
        request.product_id,
        request.date,
        request.hour
    )


@router.post("/hourly", response_model=ChartDataResponse)
async def get_hourly_usage(request: HourlyUsageRequest):
    """
    Get hourly electricity usage for a specific day.

    Returns data for chart where:
    - X-axis shows hours (00-23)
    - Y-axis shows average watt values

    This endpoint is publicly accessible.
    """
    return ElectricityUsageService.get_hourly_usage(
        request.product_id,
        request.date
    )


@router.post("/daily", response_model=ChartDataResponse)
async def get_daily_usage(request: DailyUsageRequest):
    """
    Get daily electricity usage for a specific month.

    Returns data for chart where:
    - X-axis shows days (01-31)
    - Y-axis shows average watt values

    This endpoint is publicly accessible.
    """
    return ElectricityUsageService.get_daily_usage(
        request.product_id,
        request.year_month
    )


@router.post("/monthly", response_model=ChartDataResponse)
async def get_monthly_usage(request: MonthlyUsageRequest):
    """
    Get monthly electricity usage for a specific year.

    Returns data for chart where:
    - X-axis shows months (01-12)
    - Y-axis shows average watt values

    This endpoint is publicly accessible.
    """
    return ElectricityUsageService.get_monthly_usage(
        request.product_id,
        request.year
    )


# Add GET endpoints for more flexibility
@router.get("/minutely/{product_id}/{date}/{hour}", response_model=ChartDataResponse)
async def get_minutely_usage_get(product_id: str, date: str, hour: str):
    """
    Get minute-by-minute electricity usage for a specific hour in a day using GET.

    - product_id: The product identifier
    - date: Date in YYYY-MM-DD format
    - hour: Hour in HH format (00-23)

    Returns data for chart where:
    - X-axis shows minutes (00-59)
    - Y-axis shows average watt values

    This endpoint is publicly accessible.
    """
    return ElectricityUsageService.get_minutely_usage(product_id, date, hour)


@router.get("/hourly/{product_id}/{date}", response_model=ChartDataResponse)
async def get_hourly_usage_get(product_id: str, date: str):
    """
    Get hourly electricity usage for a specific day using GET.

    - product_id: The product identifier
    - date: Date in YYYY-MM-DD format

    Returns data for chart where:
    - X-axis shows hours (00-23)
    - Y-axis shows average watt values

    This endpoint is publicly accessible.
    """
    return ElectricityUsageService.get_hourly_usage(product_id, date)


@router.get("/daily/{product_id}/{year_month}", response_model=ChartDataResponse)
async def get_daily_usage_get(product_id: str, year_month: str):
    """
    Get daily electricity usage for a specific month using GET.

    - product_id: The product identifier
    - year_month: Year and month in YYYY-MM format

    Returns data for chart where:
    - X-axis shows days (01-31)
    - Y-axis shows average watt values

    This endpoint is publicly accessible.
    """
    return ElectricityUsageService.get_daily_usage(product_id, year_month)


@router.get("/monthly/{product_id}/{year}", response_model=ChartDataResponse)
async def get_monthly_usage_get(product_id: str, year: str):
    """
    Get monthly electricity usage for a specific year using GET.

    - product_id: The product identifier
    - year: Year in YYYY format

    Returns data for chart where:
    - X-axis shows months (01-12)
    - Y-axis shows average watt values

    This endpoint is publicly accessible.
    """
    return ElectricityUsageService.get_monthly_usage(product_id, year)