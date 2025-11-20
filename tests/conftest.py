import copy as _copy
import pytest

from httpx import AsyncClient

import src.app as app_module


# Keep an original deep copy to restore before each test to avoid state bleed
_ORIGINAL_ACTIVITIES = _copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    # Restore the module-level `activities` before each test
    app_module.activities = _copy.deepcopy(_ORIGINAL_ACTIVITIES)
    yield


@pytest.fixture
async def async_client():
    async with AsyncClient(app=app_module.app, base_url="http://testserver") as ac:
        yield ac
