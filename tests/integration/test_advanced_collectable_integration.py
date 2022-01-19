from scripts.helpers import LOCAL_BLOCKCHAIN_ENV, get_account, get_contract
from scripts.advanced_collectable.deploy_and_create import deploy_and_create
import pytest
from brownie import network
import time


def test_can_create_simple_collectable_integration():
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip("Only for Integration testing")
    account = get_account()
    # Act
    adv_collectable, creation_tx = deploy_and_create()
    time.sleep(60)
    # Assert
    assert adv_collectable.tokenCounter() == 1