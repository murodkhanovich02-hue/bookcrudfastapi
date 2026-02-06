from pydantic import BaseModel
from datetime import datetime

# for Register
class RegisterModel(BaseModel):
    username: str
    password: str
    confirm_password: str

    class Config:
        orm_mode = True

# for login
class LoginModel(BaseModel):
    username: str
    password: str

# for Logout
class LogoutModel(BaseModel):
    refresh_token: str

# for Refresh
class RefreshTokenModel(BaseModel):
    refresh_token: str
