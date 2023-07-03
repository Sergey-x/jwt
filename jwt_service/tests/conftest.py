import pytest

import jwt_service.services as serv
from jwt_service.schemas import Credentials

from .mocks import mock_validate_credentials


serv.validate_credentials = mock_validate_credentials


@pytest.fixture
def credentials() -> Credentials:
    credentials: Credentials = Credentials(email='a@a.a', password='password')
    return credentials
