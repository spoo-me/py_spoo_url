import requests
import json

class Shortener:
    def __init__(self):
        self.short_code = None
        self.url = "https://spoo.me"

    def shorten(
        self,
        long_url: str,
        password: str = None,
        max_clicks: int = None,
        alias: str = None,
    ):

        payload = {"url": long_url}

        if password:
            payload["password"] = password
        if max_clicks:
            payload["max_clicks"] = max_clicks
        if alias:
            payload["alias"] = alias

        headers = {"Accept": "application/json"}

        r = requests.post(self.url, data=payload, headers=headers)

        if r.status_code == 200:
            response = json.loads(r.text)
            self.short_code = response["short_url"]
            return self.short_code
        else:
            raise Exception(f"Error {r.status_code}: {r.text}")

    def emojify(
        self,
        long_url: str,
        emoji_alias=None,
        max_clicks: int= None,
        password: str=None
    ):

        payload = {"url": long_url}

        if password:
            payload["password"] = password
        if max_clicks:
            payload["max_clicks"] = max_clicks
        if emoji_alias:
            payload["emojies"] = emoji_alias

        headers = {"Accept": "application/json"}

        r = requests.post(f"{self.url}/emoji", data=payload, headers=headers)

        if r.status_code == 200:
            response = json.loads(r.text)
            self.short_code = response["short_url"]
            return self.short_code
        else:
            raise Exception(f"Error {r.status_code}: {r.text}")
