import logging

import pytest

import ldclient
from ldclient import Config
from testing import sdk_key
from testing.sync_util import wait_until

logging.basicConfig(level=logging.DEBUG)


@pytest.mark.skipif(sdk_key is None, reason="requires LD_SDK_KEY environment variable to be set")
def test_set_sdk_key_before_init():
    ldclient.set_config(Config.default())

    ldclient.set_sdk_key(sdk_key)
    wait_until(ldclient.get().is_initialized, timeout=30)

    ldclient.get().close()


@pytest.mark.skipif(sdk_key is None, reason="requires LD_SDK_KEY environment variable to be set")
def test_set_sdk_key_after_init():
    ldclient.set_config(Config.default())
    assert ldclient.get().is_initialized() is False
    ldclient.set_sdk_key(sdk_key)
    wait_until(ldclient.get().is_initialized, timeout=30)

    ldclient.get().close()


@pytest.mark.skipif(sdk_key is None, reason="requires LD_SDK_KEY environment variable to be set")
def test_set_config():
    offline_config = ldclient.Config(offline=True)
    online_config = ldclient.Config(sdk_key=sdk_key, offline=False)

    ldclient.set_config(offline_config)
    assert ldclient.get().is_offline() is True

    ldclient.set_config(online_config)
    assert ldclient.get().is_offline() is False
    wait_until(ldclient.get().is_initialized, timeout=30)

    ldclient.get().close()

