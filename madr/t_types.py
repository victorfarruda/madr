from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from madr.database import get_session

T_FormData = Annotated[OAuth2PasswordRequestForm, Depends()]
T_Session = Annotated[Session, Depends(get_session)]
T_OAuthSchema = Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl='auth/token'))]
