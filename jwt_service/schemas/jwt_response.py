import pydantic as pd


class TokenPair(pd.BaseModel):
    access: str = pd.Field(description="Access token")
    refresh: str = pd.Field(description="Refresh token")
