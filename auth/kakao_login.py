from typing import Any, Dict, List, Optional, Tuple, cast

import json
from httpx_oauth.errors import GetIdEmailError
from httpx_oauth.oauth2 import BaseOAuth2
from httpx_oauth.typing import TypedDict
from fastapi_users.authentication import AuthenticationBackend
from auth.users import bearer_transport, get_jwt_strategy
from auth.users import fastapi_users
import os
from dotenv import load_dotenv


load_dotenv()

environment = os.environ.get('ENVIRONMENT')

redirect_url = None

if environment == 'production':
    redirect_url = "https://ieunghieut-frontend.pages.dev/login/kakao"
else:
    redirect_url = f"http://127.0.0.1:8000/auth/kakao/callback"

AUTHORIZE_ENDPOINT = "https://kauth.kakao.com/oauth/authorize"
ACCESS_TOKEN_ENDPOINT = "https://kauth.kakao.com/oauth/token"
PROFILE_ENDPOINT = "https://kapi.kakao.com/v2/user/me"
BASE_SCOPES = ["account_email"]
BASE_PROFILE_SCOPES = ["kakao_account.email"]


# 카카오로그인 시작
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
            name=name,
            base_scopes=scopes,
        )

    async def get_id_email(self, token: str) -> Tuple[str, Optional[str]]:
        async with self.get_httpx_client() as client:
            response = await client.post(
                PROFILE_ENDPOINT,
                params={"property_keys": json.dumps(BASE_PROFILE_SCOPES)},
                headers={**self.request_headers,
                         "Authorization": f"Bearer {token}"},
            )

            if response.status_code >= 400:
                raise GetIdEmailError(response.json())

            account_info = cast(Dict[str, Any], response.json())
            kakao_account = account_info.get('kakao_account')
            print(kakao_account)

            return str(account_info.get('id')), kakao_account.get('email')

# 카카오로그인 끝



auth_backend_kakao = AuthenticationBackend(
    name="jwt-kakao",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy
)

# 인증 클라이언트
kakao_oauth_client = KakaoOAuth2(
    client_id="136400062f784e6bf58615cfab6cd7d9",
    client_secret="zffq0z1BWKVyAhxYTbgqHYD3X2mxknc7",
    scopes=[
    	# https://developers.kakao.com/docs/latest/ko/kakaologin/common#user-info-kakao-account
        "account_email"
    ]
)

# 카카오 로그인 JWT 라우터
kakao_oauth_router = fastapi_users.get_oauth_router(
    oauth_client=kakao_oauth_client,
    backend=auth_backend_kakao,
    state_secret="abcdefg1234",
    redirect_url=redirect_url,
    associate_by_email=True,
)