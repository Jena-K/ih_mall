from app.users import fastapi_users
from auth.kakao.client import KakaoOAuth2
from .backend import auth_backend
import os
from dotenv import load_dotenv

load_dotenv()
environment = os.environ.get('ENVIRONMENT')
client_id = os.environ.get('KAKAO_CLIENT_ID')
client_secret = os.environ.get('KAKAO_CLIENT_SECRET')
state_secret = os.environ.get('KAKAO_CLIENT_SECRET')
login_method="kakao"
if environment == 'production':
    redirect_url= f"https://quiet-dawn-85341.herokuapp.com/auth/{login_method}/callback"
else:
    redirect_url= f"http://127.0.0.1:8000/auth/{login_method}/callback"

kakao_oauth_client = KakaoOAuth2(
    client_id=client_id,
    client_secret=client_secret,
    scopes=[
    	# https://developers.kakao.com/docs/latest/ko/kakaologin/common#user-info-kakao-account
        "account_email"
    ]
)

kakao_oauth_router = fastapi_users.get_oauth_router(
    oauth_client=kakao_oauth_client,
    backend=auth_backend,
    state_secret="abcdefg1234",
    redirect_url="http://127.0.0.1:8000/auth/kakao/callback",
    associate_by_email=True,
)