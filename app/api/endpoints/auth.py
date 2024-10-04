from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.db import SessionDep
from app.schemas.token import Token
from app.schemas.user import UserIn, UserOut
from app.services.user import CurrentUserDep, UserService

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserIn,
    session: SessionDep,
):
    return await UserService.register_user(user_data, session)


@router.post("/token", status_code=status.HTTP_200_OK)
async def token(
    session: SessionDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    return await UserService.login(form_data, session)


@router.get("/login", status_code=status.HTTP_200_OK)
async def login(current_user: CurrentUserDep) -> UserOut:
    return UserOut.model_validate(current_user)
