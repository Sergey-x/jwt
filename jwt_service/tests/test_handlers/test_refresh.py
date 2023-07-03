import fastapi as fa
import freezegun

from jwt_service.schemas import Credentials, RefreshToken

from ...services import JWTRefresh
from ..client import client


class TestRefreshTokenPair:
    valid_time: str = "2022-10-06 21:45:00"
    expired_time: str = "2022-11-16 21:45:00"

    @staticmethod
    @freezegun.freeze_time(valid_time)
    def get_refresh_token() -> dict:
        refresh = RefreshToken(token=JWTRefresh.gen_token({}))
        return refresh.dict()

    @staticmethod
    def get_url() -> str:
        return '/jwt/refresh'

    @freezegun.freeze_time(valid_time)
    def test_200(self):
        response = client.post(url=self.get_url(), json=self.get_refresh_token())
        assert response.status_code == fa.status.HTTP_200_OK

    @freezegun.freeze_time(expired_time)
    def test_expired_token(self):
        response = client.post(url=self.get_url(), json=self.get_refresh_token())
        assert response.status_code == fa.status.HTTP_400_BAD_REQUEST

    @freezegun.freeze_time(valid_time)
    def test_has_jwt_keys(self, credentials: Credentials):
        response = client.post(url=self.get_url(), json=self.get_refresh_token())
        response_body = response.json()
        assert 'access' in response_body
        assert 'refresh' in response_body

    @freezegun.freeze_time(valid_time)
    def test_tokens_are_not_the_same(self, credentials: Credentials):
        response = client.post(url=self.get_url(), json=self.get_refresh_token())
        response_body = response.json()
        assert response_body.get('access') != response_body.get('refresh')

    def test_empty_cred(self, credentials: Credentials):
        response = client.post(url=self.get_url(), json={})
        assert response.status_code == fa.status.HTTP_422_UNPROCESSABLE_ENTITY

    # TODO: check 401 status
