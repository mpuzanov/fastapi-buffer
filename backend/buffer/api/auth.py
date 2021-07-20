from fastapi import (
    APIRouter,
    Depends,
)
# from fastapi.security import OAuth2PasswordRequestForm
from .. import models
from ..services.auth_basic import (
    get_current_user,
)

router = APIRouter(
    prefix='/auth',
    tags=["Авторизация"],
)


# @router.post(
#     '/sign-in/',
#     response_model=models.Token,
#     description='Авторизация',
#     tags=["Авторизация"],
#     summary="Авторизация"
# )
# def sign_in(
#         auth_data: OAuth2PasswordRequestForm = Depends(),
#         auth_service: AuthService = Depends(),
# ):
#     return auth_service.authenticate_user(
#         auth_data.username,
#         auth_data.password,
#     )


@router.get(
    '/user/',
    response_model=models.User,
    tags=["Авторизация"],
)
def get_user(user: models.User = Depends(get_current_user)):
    return user
