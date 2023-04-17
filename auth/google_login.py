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
    redirect_url = "https://ieunghieut-frontend.pages.dev/login/google"
else:
    redirect_url = f"http://127.0.0.1:8000/auth/google/callback"

GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
GOOGLE_SCOPE_PROFILE = "https://www.googleapis.com/auth/userinfo.profile"
GOOGLE_SCOPE_EMAIL = "https://www.googleapis.com/auth/userinfo.email"
BASE_PROFILE_SCOPES = [GOOGLE_SCOPE_PROFILE, GOOGLE_SCOPE_EMAIL, "openid"]


# 카카오로그인 시작
class GoogleOAuth2(BaseOAuth2[Dict[str, Any]]):
    display_name = "Google"

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        scopes: Optional[List[str]] = [GOOGLE_SCOPE_PROFILE, GOOGLE_SCOPE_EMAIL, "openid"],
        name: str = "google",
    ):
        super().__init__(
            client_id,
            client_secret,
            "https://accounts.google.com/o/oauth2/v2/auth",
            "https://oauth2.googleapis.com/token",
            name=name,
            base_scopes=scopes,
        )

    async def get_id_email(self, token: str) -> Tuple[str, Optional[str]]:
        async with self.get_httpx_client() as client:
            response = await client.post(
                GOOGLE_USERINFO_URL,
                params={"property_keys": json.dumps(BASE_PROFILE_SCOPES)},
                headers={**self.request_headers,
                         "Authorization": f"Bearer {token}"},
            )

            if response.status_code >= 400:
                raise GetIdEmailError(response.json())

            account_info = cast(Dict[str, Any], response.json())
            print(f"account_info : {account_info}")
            google_account = account_info.get('google_account')
            print(f"google_account: {google_account}")

            return str(account_info.get('id')), account_info.get('email')


# 카카오로그인 끝
auth_backend_google = AuthenticationBackend(
    name="jwt-google",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy
)

# 인증 클라이언트
google_oauth_client = GoogleOAuth2(
    client_id="227870507429-7pvpqe2tk9392fs7p4r14pb4sr9j4ghb.apps.googleusercontent.com",
    client_secret="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",
    scopes=[
        GOOGLE_SCOPE_PROFILE, GOOGLE_SCOPE_EMAIL, "openid"
    ]
)


# 카카오 로그인 JWT 라우터
google_oauth_router = fastapi_users.get_oauth_router(
    oauth_client=google_oauth_client,
    backend=auth_backend_google,
    state_secret="abcdefg1234",
    redirect_url=redirect_url,
    associate_by_email=True,
)
# redirect_url=f"{redirect_url}/auth/google/callback",
