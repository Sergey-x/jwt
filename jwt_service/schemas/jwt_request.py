import pydantic as pd


class Credentials(pd.BaseModel):
    email: str = pd.Field(min_length=4)
    password: str = pd.Field(min_length=6)


class RefreshToken(pd.BaseModel):
    token: str
