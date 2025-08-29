import requests
import datetime
from typing import Optional

def main(
    record_limit: Optional[int] = 10
):
    """
    Fetch random user data using RandomUser.me public API.
    - record_limit: Number of user records to return (max 5000 per request).
    """
    start_time = datetime.datetime.now()
    limit = min(record_limit, 5000)

    try:
        url = f"https://randomuser.me/api/?results={limit}"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            users = response.json().get("results", [])
            formatted_users = [
                {
                    "name": f"{user['name']['first']} {user['name']['last']}",
                    "email": user["email"],
                    "gender": user["gender"],
                    "country": user["location"]["country"],
                    "phone": user["phone"],
                    "username": user["login"]["username"],
                    "dob": user["dob"]["date"],
                    "registered": user["registered"]["date"]
                }
                for user in users
            ]
        else:
            formatted_users = []

    except Exception as e:
        formatted_users = []
        print(f"Error fetching data: {e}")

    end_time = datetime.datetime.now()
    execution_time = (end_time - start_time).total_seconds() * 1000

    return {
        "status": "success" if formatted_users else "error",
        "source": "https://randomuser.me/",
        "records": formatted_users,
        "record_count": len(formatted_users),
        "execution_time_ms": execution_time,
        "timestamp": datetime.datetime.now().isoformat()
    }
