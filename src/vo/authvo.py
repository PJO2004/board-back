from typing import List
from pydantic import BaseModel
import os
import sys
import base64

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from config import envconfig

envsetting = envconfig.setting


class Settings(BaseModel):
    authjwt_algorithm: str = envsetting.JWT_ALGORITHM
    authjwt_decode_algorithms: List[str] = [envsetting.JWT_ALGORITHM]
    authjwt_token_location: set = {"cookies", "headers"}
    authjwt_access_cookie_key: str = "access_token"
    authjwt_refresh_cookie_key: str = "refresh_token"
    authjwt_cookie_csrf_protect: bool = False
    authjwt_public_key: str = (
        base64.b64decode(envsetting.JWT_PUBLIC_KEY).decode("utf-8").replace("\r", "")
    )
    authjwt_private_key: str = (
        base64.b64decode(envsetting.JWT_PRIVATE_KEY).decode("utf-8").replace("\r", "")
    )

    class Config:
        orm_mode: bool = True
