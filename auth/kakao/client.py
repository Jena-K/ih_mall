from typing import Any, Dict, List, Optional, Tuple, cast

import json
from httpx_oauth.errors import GetIdEmailError
from httpx_oauth.oauth2 import BaseOAuth2

AUTHORIZE_ENDPOINT = "https://kauth.kakao.com/oauth/authorize"
ACCESS_TOKEN_ENDPOINT = "https://kauth.kakao.com/oauth/token"
REFRESH_TOKEN_ENDPOINT = ACCESS_TOKEN_ENDPOINT
REVOKE_TOKEN_ENDPOINT = "https://kapi.kakao.com/v1/user/unlink"
PROFILE_ENDPOINT = "https://kapi.kakao.com/v2/user/me"
BASE_SCOPES = ["account_email"]
PROFILE_PROPERTIES = ["kakao_account.email"]


class KakaoOAuth2(BaseOAuth2[Dict[str, Any]]):
    display_name = "Kakao"

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        scopes: Optional[List[str]] = BASE_SCOPES,
        name: str = "kakao",
    ):
        super().__init__(
            client_id,
            client_secret,
            AUTHORIZE_ENDPOINT,
            ACCESS_TOKEN_ENDPOINT,
            refresh_token_endpoint=REFRESH_TOKEN_ENDPOINT,
            revoke_token_endpoint=REVOKE_TOKEN_ENDPOINT,
            name=name,
            base_scopes=scopes,
        )

    async def get_id_email(self, token: str) -> Tuple[str, Optional[str]]:
        async with self.get_httpx_client() as client:
            response = await client.post(
                PROFILE_ENDPOINT,
                params={"property_keys": json.dumps(PROFILE_PROPERTIES)},
                headers={**self.request_headers,
                         "Authorization": f"Bearer {token}"},
            )

            if response.status_code >= 400:
                raise GetIdEmailError(response.json())

            account_info = cast(Dict[str, Any], response.json())
            kakao_account = account_info.get('kakao_account')

            if kakao_account is None or kakao_account.get('email') is None:
                raise GetIdEmailError(response.json())

            return str(account_info.get('id')), kakao_account.get('email')