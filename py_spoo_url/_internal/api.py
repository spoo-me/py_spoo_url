import requests
import json
from typing import Optional, Any


def fetch_statistics(short_code: str, password: Optional[str] = None) -> Any:
    url = f"https://spoo.me/stats/{short_code}"
    params = {"password": password} if password else None
    r = requests.post(url, data=params)
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        raise Exception(f"Error {r.status_code}: {r.text}")
