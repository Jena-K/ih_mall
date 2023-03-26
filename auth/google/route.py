from httpx_oauth.clients.google import GoogleOAuth2
from app.users import fastapi_users

from auth.google.backend import auth_backend

GOOGLE_SCOPE_PROFILE = "https://www.googleapis.com/auth/userinfo.profile"
GOOGLE_SCOPE_EMAIL = "https://www.googleapis.com/auth/userinfo.email"

google_oauth_client = GoogleOAuth2(
    client_id="227870507429-7pvpqe2tk9392fs7p4r14pb4sr9j4ghb.apps.googleusercontent.com",
    client_secret="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"
)

google_oauth_router = fastapi_users.get_oauth_router(
    oauth_client=google_oauth_client,
    backend=auth_backend,
    state_secret="abcdefg1234",
    redirect_url="http://127.0.0.1:8000/auth/google/callback",
    associate_by_email=True,
)