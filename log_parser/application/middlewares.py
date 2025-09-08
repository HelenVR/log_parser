from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import status

security = HTTPBasic()


def auth(login: str, password: str):
    if not (login and password):
        raise Exception("Login and/or password are missing")

    def auth_check(creds: HTTPBasicCredentials = Depends(security)):
        if not (creds.username == login and creds.password == password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect login or password",
                headers={"WWW-Authenticate": "Basic"},
            )
        return creds.username
    return auth_check
