import fastapi as fa

from jwt_service.schemas import Credentials

from ..client import client


class TestObtainTokenPair:
    @staticmethod
    def get_url() -> str:
        return '/jwt/obtain'

    def test_200(self, credentials: Credentials):
        response = client.post(url=self.get_url(), json=credentials.dict())
        assert response.status_code == fa.status.HTTP_200_OK

    def test_has_jwt_keys(self, credentials: Credentials):
        response = client.post(url=self.get_url(), json=credentials.dict())
        response_body = response.json()
        assert 'access' in response_body
        assert 'refresh' in response_body

    def test_tokens_are_not_the_same(self, credentials: Credentials):
        response = client.post(url=self.get_url(), json=credentials.dict())
        response_body = response.json()
        assert response_body.get('access') != response_body.get('refresh')

    def test_empty_cred(self, credentials: Credentials):
        response = client.post(url=self.get_url(), json={})
        assert response.status_code == fa.status.HTTP_422_UNPROCESSABLE_ENTITY

    # TODO: check 401 status
