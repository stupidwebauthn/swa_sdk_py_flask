from flask import Request, Response
from werkzeug.exceptions import HTTPException
import requests


class AuthResponse:
    user_id: int
    user_email: str
    user_created_at: int

    @staticmethod
    def FromJson(json: any):
        a = AuthResponse()
        a.user_id = json["user_id"]
        a.user_email = json["user_email"]
        a.user_created_at = json["user_created_at"]
        return a


class StupidWebauthnSdk:
    url: str

    def __init__(self, url: str):
        self.url = url

    def middleware(self, req: Request, res: Response):
        cookies = req.headers.get("Cookie")
        headers = dict()
        headers["Cookie"] = cookies
        newRes = requests.get(
            self.url,
            headers=headers,
            timeout=5000,
        )
        if newRes.status_code != 200:
            try:
                json = newRes.json()
                raise HTTPException(json["message"])
            except Exception as exc:
                raise HTTPException(newRes.status_code + ": " + newRes.text) from exc

        json = newRes.json()

        res.headers.set("Set-Cookie", newRes.headers.get("Set-Cookie"))
        return AuthResponse.FromJson(json)
