from datetime import datetime
import calendar
from typing import Dict, List, Any, Union, Optional
import logging

from app.db.firebase import database

from app.electricity.models import ChartDataPoint, ChartDataResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ElectricityUsageService:
    @staticmethod
    def get_minutely_usage(product_id: str, date_str: str, hour: str) -> ChartDataResponse:
        """Get minutely average electricity usage for a specific hour in a day."""
        try:
            # Access the Firebase path for the specific product, date, and hour
            ref_path = f"electricity_usage/{product_id}/{date_str}/{hour}"
            minute_data = database.child(ref_path).get() or {}

            # Convert to chart data points sorted by minute
            data_points = []

            # Handle both object format and array format data
            if isinstance(minute_data, dict):
                # Process dictionary-style data (minute: value)
                for minute, value in sorted(minute_data.items()):
                    # Skip null values and ensure we have a valid float
                    if value is not None:
                        try:
                            watt_value = float(value)
                            data_points.append(ChartDataPoint(
                                label=minute,
                                value=round(watt_value, 2)
                            ))
                        except (ValueError, TypeError):
                            # Skip invalid values
                            logger.warning(f"Invalid value for minute {minute}: {value}")
            elif isinstance(minute_data, list):
                # Process array-style data where index is the minute
                for index, value in enumerate(minute_data):
                    # Skip null values
                    if value is not None:
                        try:
                            watt_value = float(value)
                            minute_str = f"{index:02d}"
                            data_points.append(ChartDataPoint(
                                label=minute_str,
                                value=round(watt_value, 2)
                            ))
                        except (ValueError, TypeError):
                            # Skip invalid values
                            logger.warning(f"Invalid value for minute {index}: {value}")

            return ChartDataResponse(
                data_points=data_points,
                chart_title=f"Minute-by-Minute Usage on {date_str} at {hour}:00",
                x_axis_label="Minute"
            )
        except Exception as e:
            logger.error(f"Error retrieving minutely data: {str(e)}")
            return ChartDataResponse(
                data_points=[],
                chart_title=f"No data available for {date_str} at {hour}:00",
                x_axis_label="Minute"
            )

    @staticmethod
    def get_hourly_usage(product_id: str, date_str: str) -> ChartDataResponse:
        """Get hourly average electricity usage for a specific day."""
        try:
            # Access the Firebase path for the specific product and date
            ref_path = f"electricity_usage/{product_id}/{date_str}"
            day_data = database.child(ref_path).get() or {}

            data_points = []

            # Process each hour in the day
            for hour in sorted(day_data.keys()):
                # Skip non-hour keys like "connection_status"
                if not hour.isdigit():
                    continue

                hour_data = day_data.get(hour, {})
                hour_values = []

                # Handle both object format and array format data
                if isinstance(hour_data, dict):
                    # Dictionary format (minute: value)
                    for minute, value in hour_data.items():
                        if value is not None:
                            try:
                                hour_values.append(float(value))
                            except (ValueError, TypeError):
                                continue
                elif isinstance(hour_data, list):
                    # Array format where index is the minute
                    for value in hour_data:
                        if value is not None:
                            try:
                                hour_values.append(float(value))
                            except (ValueError, TypeError):
                                continue

                # Calculate the hour's average if we have values
                if hour_values:
                    hour_avg = sum(hour_values) / len(hour_values)
                    data_points.append(ChartDataPoint(
                        label=f"{hour}:00",
                        value=round(hour_avg, 2)
                    ))

            return ChartDataResponse(
                data_points=data_points,
                chart_title=f"Hourly Usage on {date_str}",
                x_axis_label="Hour"
            )
        except Exception as e:
            logger.error(f"Error retrieving hourly data: {str(e)}")
            return ChartDataResponse(
                data_points=[],
                chart_title=f"No data available for {date_str}",
                x_axis_label="Hour"
            )

    @staticmethod
    def get_daily_usage(product_id: str, year_month: str) -> ChartDataResponse:
        """Get daily average electricity usage for a specific month."""
        try:
            # Extract year and month from input
            year, month = year_month.split('-')

            # Calculate the number of days in the month
            _, days_in_month = calendar.monthrange(int(year), int(month))

            data_points = []

            # For each day in the month
            for day in range(1, days_in_month + 1):
                # Format the date string for Firebase
                date_str = f"{year_month}-{day:02d}"

                try:
                    # Get data for the day
                    day_ref_path = f"electricity_usage/{product_id}/{date_str}"
                    day_data = database.child(day_ref_path).get()

                    if not day_data:
                        continue  # Skip if no data for this day

                    # Calculate the daily average across all hours and minutes
                    all_values = []

                    for hour, hour_data in day_data.items():
                        # Skip non-hour keys
                        if not hour.isdigit():
                            continue

                        # Process each minute in the hour
                        if isinstance(hour_data, dict):
                            for minute, value in hour_data.items():
                                if value is not None:
                                    try:
                                        all_values.append(float(value))
                                    except (ValueError, TypeError):
                                        continue
                        elif isinstance(hour_data, list):
                            for value in hour_data:
                                if value is not None:
                                    try:
                                        all_values.append(float(value))
                                    except (ValueError, TypeError):
                                        continue

                    # Add data point if we have values
                    if all_values:
                        daily_avg = sum(all_values) / len(all_values)
                        data_points.append(ChartDataPoint(
                            label=f"{day:02d}",
                            value=round(daily_avg, 2)
                        ))
                except Exception as e:
                    logger.warning(f"Error processing day {date_str}: {str(e)}")
                    continue  # Skip this day if there's an error

            # Get month name for the chart title
            month_name = datetime.strptime(month, "%m").strftime("%B")

            return ChartDataResponse(
                data_points=data_points,
                chart_title=f"Daily Usage in {month_name} {year}",
                x_axis_label="Day"
            )
        except Exception as e:
            logger.error(f"Error retrieving daily data: {str(e)}")
            return ChartDataResponse(
                data_points=[],
                chart_title=f"No data available for {year_month}",
                x_axis_label="Day"
            )

    @staticmethod
    def get_monthly_usage(product_id: str, year: str) -> ChartDataResponse:
        """Get monthly average electricity usage for a specific year."""
        try:
            data_points = []

            # For each month in the year
            for month in range(1, 13):
                month_str = f"{month:02d}"

                try:
                    # Get all data for the month
                    month_ref_path = f"electricity_usage/{product_id}"
                    year_month = f"{year}-{month_str}"

                    # Get all days for this month
                    all_month_values = []

                    # For each day in the month
                    _, days_in_month = calendar.monthrange(int(year), int(month))
                    for day in range(1, days_in_month + 1):
                        date_str = f"{year_month}-{day:02d}"
                        day_ref_path = f"{month_ref_path}/{date_str}"
                        day_data = database.child(day_ref_path).get()

                        if not day_data:
                            continue  # Skip if no data for this day

                        # Process each hour in the day
                        for hour, hour_data in day_data.items():
                            # Skip non-hour keys
                            if not hour.isdigit():
                                continue

                            # Process each minute in the hour
                            if isinstance(hour_data, dict):
                                for minute, value in hour_data.items():
                                    if value is not None:
                                        try:
                                            all_month_values.append(float(value))
                                        except (ValueError, TypeError):
                                            continue
                            elif isinstance(hour_data, list):
                                for value in hour_data:
                                    if value is not None:
                                        try:
                                            all_month_values.append(float(value))
                                        except (ValueError, TypeError):
                                            continue

                    # Calculate monthly average if we have values
                    if all_month_values:
                        monthly_avg = sum(all_month_values) / len(all_month_values)

                        # Get month name for the label
                        month_name = datetime.strptime(month_str, "%m").strftime("%b")
                        data_points.append(ChartDataPoint(
                            label=month_name,
                            value=round(monthly_avg, 2)
                        ))
                except Exception as e:
                    logger.warning(f"Error processing month {year_month}: {str(e)}")
                    continue  # Skip this month if there's an error

            return ChartDataResponse(
                data_points=data_points,
                chart_title=f"Monthly Usage in {year}",
                x_axis_label="Month"
            )
        except Exception as e:
            logger.error(f"Error retrieving monthly data: {str(e)}")
            return ChartDataResponse(
                data_points=[],
                chart_title=f"No data available for {year}",
                x_axis_label="Month"
            )