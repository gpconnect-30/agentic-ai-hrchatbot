from data.employees import company_holidays
from datetime import datetime

def get_holidays(month: str = None, upcoming_only: bool = False, current_date: str = None):
    if month:
        target_month = f"-{month.zfill(2)}-"
        return [h for h in company_holidays if target_month in h["date"]]

    if upcoming_only:
        ref_date = current_date or datetime.now().strftime("%Y-%m-%d")
        return [h for h in company_holidays if h["date"] >= ref_date]

    return company_holidays