from authlib.integrations.httpx_client import AsyncOAuth2Client

from careermatch_ai.core.settings import get_settings


class GoogleOAuthService:
    def __init__(self) -> None:
        settings = get_settings()
        self._client = AsyncOAuth2Client(
            client_id=settings.google_client_id,
            client_secret=settings.google_client_secret,
        )

    async def verify_id_token(self, id_token: str) -> dict:
        response = await self._client.get(
            "https://oauth2.googleapis.com/tokeninfo",
            params={"id_token": id_token},
        )
        response.raise_for_status()
        return response.json()
