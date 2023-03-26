from typing import Any, Dict, List, Optional, Tuple, cast
import requests
from httpx_oauth.errors import GetIdEmailError
from httpx_oauth.oauth2 import BaseOAuth2
from httpx_oauth.typing import TypedDict
from fastapi_users.authentication import AuthenticationBackend
from infrastructure.database import User
from auth.users import bearer_transport, get_jwt_strategy
from auth.users import fastapi_users
from app.exceptions import BadCredentialException
from httpx_oauth.clients.google import GoogleOAuth2
    
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
GOOGLE_SCOPE_PROFILE = "https://www.googleapis.com/auth/userinfo.profile"
GOOGLE_SCOPE_EMAIL = "https://www.googleapis.com/auth/userinfo.email"



class GoogleAuthBackend(BaseOAuth2[Dict[str, Any]]):
    def get_profile(self, access_token: str) -> dict:
        response = requests.get(url=GOOGLE_USERINFO_URL,
                                params={'access_token': access_token})
        if not response.ok:
            raise BadCredentialException(
                'Failed to get user information from Google.')
        return response.json()

    def update_profile(self, user: User, profile: dict) -> User:
        user = super().update_profile(user, profile)
        if user.first_name == None:
            user.first_name = profile.get('given_name')
        if user.last_name == None:
            user.last_name = profile.get('family_name')
        if user.picture == None:
            user.picture = profile.get('picture')
        return user


auth_backend = GoogleAuthBackend(
    name="jwt-google",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

google_oauth_client = GoogleOAuth2(
    client_id="227870507429-7pvpqe2tk9392fs7p4r14pb4sr9j4ghb.apps.googleusercontent.com",
    client_secret="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",
    scope=[
        GOOGLE_SCOPE_PROFILE, GOOGLE_SCOPE_EMAIL, "openid"
    ],
)

google_oauth_router = fastapi_users.get_oauth_router(
    oauth_client=google_oauth_client,
    backend=auth_backend,
    state_secret="abcdefg1234",
    redirect_url="http://127.0.0.1:8000/auth/google/callback",
    associate_by_email=True,
)