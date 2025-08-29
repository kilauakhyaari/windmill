import requests
import datetime
from typing import Optional

def main(record_limit: Optional[int] = None):
    """
    Extract job listings from NYC Open Data API.
    record_limit: Optional limit for number of records (default = 5).
    """
    limit = record_limit if record_limit is not None else 5
    api_url = f"https://data.cityofnewyork.us/resource/kpav-sd4t.json?$limit={limit}"
    
    start_time = datetime.datetime.now()
    try:
        response = requests.get(api_url, timeout=10)
        data = response.json()
        jobs = [{
            "timestamp": datetime.datetime.now().isoformat(),
            "agency": item.get("agency"),
            "title": item.get("business_title"),
            "salary_range": f"{item.get('salary_range_from')} - {item.get('salary_range_to')}",
            "posting_date": item.get("posting_date")
        } for item in data]
    except Exception as e:
        print("Error:", e)
        jobs = []

    end_time = datetime.datetime.now()
    execution_time_ms = (end_time - start_time).total_seconds() * 1000

    return {
        "status": "success",
        "records": jobs,
        "record_count": len(jobs),
        "source": "NYC Open Data",
        "execution_time_ms": execution_time_ms,
        "timestamp": datetime.datetime.now().isoformat()
    }
