from typing import Any, Dict, List, Optional, Tuple, cast

import json
from httpx_oauth.errors import GetIdEmailError
from httpx_oauth.oauth2 import BaseOAuth2
from httpx_oauth.typing import TypedDict
from fastapi_users.authentication import AuthenticationBackend
from app.users import bearer_transport, get_jwt_strategy
from app.users import fastapi_users
    

NAVER_USERINFO_URL = 'https://openapi.naver.com/v1/nid/me'
AUTHORIZE_ENDPOINT = "https://nid.naver.com/oauth2.0/authorize"
ACCESS_TOKEN_ENDPOINT = "https://nid.naver.com/oauth2.0/token"
REFRESH_TOKEN_ENDPOINT = ACCESS_TOKEN_ENDPOINT
REVOKE_TOKEN_ENDPOINT = ACCESS_TOKEN_ENDPOINT
PROFILE_ENDPOINT = "https://openapi.naver.com/v1/nid/me"
BASE_SCOPES = []


# 네이버로그인 시작
class NaverOAuth2(BaseOAuth2[Dict[str, Any]]):
    display_name = "Naver"

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        scopes: Optional[List[str]] = BASE_SCOPES,
        name: str = "naver",
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
                headers={**self.request_headers,
                         "Authorization": f"Bearer {token}"},
            )

            if response.status_code >= 400:
                raise GetIdEmailError(response.json())

            account_info = cast(Dict[str, Any], response.json())
            account_info = account_info.get('response')
            return account_info.get('id'), account_info.get('email')
# 카카오로그인 끝



auth_backend = AuthenticationBackend(
    name="jwt-naver",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# 인증 클라이언트
naver_oauth_client = NaverOAuth2(
    client_id="y7_z4EK7BYMajOfzIhTb",
    client_secret="_f1oxB2vty"
)

naver_oauth_router = fastapi_users.get_oauth_router(
    oauth_client=naver_oauth_client,
    backend=auth_backend,
    state_secret="abcdefg1234",
    redirect_url="http://127.0.0.1:8000/auth/naver/callback",
    associate_by_email=True,
)