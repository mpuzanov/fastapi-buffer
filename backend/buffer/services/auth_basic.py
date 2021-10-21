import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from backend.buffer.database import Session, get_session
from .. import (
    models,
    tables,
)

security_basic = HTTPBasic()


class AuthService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    @classmethod
    def verify_password(cls, password: str, password2: str) -> bool:
        return secrets.compare_digest(password, password2)

    def authenticate_user(
            self,
            credentials: HTTPBasicCredentials
    ) -> models.User:

        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Basic'},
        )

        user = (
            self.session
                .query(tables.User)
                .filter(tables.User.login == credentials.username)
                .first()
        )

        if not user or user.pswd is None:
            raise exception

        if not self.verify_password(credentials.password, user.pswd):
            raise exception

        return user


def get_current_user(credentials: HTTPBasicCredentials = Depends(security_basic),
                     auth_service: AuthService = Depends()) -> models.User:
    return auth_service.authenticate_user(credentials)
