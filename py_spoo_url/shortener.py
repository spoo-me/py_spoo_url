import requests
import json
from typing import Optional


class Shortener:
    def __init__(self):
        self.short_code: Optional[str] = None
        self._url = "https://spoo.me"

    def shorten(
        self,
        long_url: str,
        password: Optional[str] = None,
        max_clicks: Optional[int] = None,
        alias: Optional[str] = None,
    ) -> Optional[str]:
        payload = {"url": long_url}

        if password:
            payload["password"] = password
        if max_clicks is not None:
            payload["max-clicks"] = str(max_clicks)
        if alias:
            payload["alias"] = alias

        headers = {"Accept": "application/json"}

        r = requests.post(self._url, data=payload, headers=headers)

        if r.status_code == 200:
            response = json.loads(r.text)
            self.short_code = str(response["short_url"])
            return self.short_code
        else:
            raise Exception(f"Error {r.status_code}: {r.text}")

    def emojify(
        self,
        long_url: str,
        emoji_alias: Optional[str] = None,
        max_clicks: Optional[int] = None,
        password: Optional[str] = None,
    ) -> Optional[str]:
        payload = {"url": long_url}

        if password:
            payload["password"] = password
        if max_clicks is not None:
            payload["max-clicks"] = str(max_clicks)
        if emoji_alias:
            payload["emojies"] = emoji_alias

        headers = {"Accept": "application/json"}

        r = requests.post(f"{self._url}/emoji", data=payload, headers=headers)

        if r.status_code == 200:
            response = json.loads(r.text)
            self.short_code = str(response["short_url"])
            return self.short_code
        else:
            raise Exception(f"Error {r.status_code}: {r.text}")
