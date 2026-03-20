from fastapi import APIRouter

from app.schemas.auth import LoginRequest, LoginResponse

router = APIRouter(prefix='/auth')


@router.post('/login', response_model=LoginResponse)
def fake_login(payload: LoginRequest) -> LoginResponse:
    token = f'demo-token-{payload.username}'
    return LoginResponse(token=token, username=payload.username)
