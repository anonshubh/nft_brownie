from scripts.helpers import LOCAL_BLOCKCHAIN_ENV, get_account, get_contract
from scripts.advanced_collectable.deploy_and_create import deploy_and_create
import pytest
from brownie import network


def test_can_create_simple_collectable():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()
    account = get_account()
    # Act
    adv_collectable, creation_tx = deploy_and_create()
    requestId = creation_tx.events["requestedCollectable"]["requestId"]
    random_number = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, random_number, adv_collectable.address, {"from": account}
    )
    # Assert
    assert adv_collectable.tokenCounter() == 1
    assert adv_collectable.tokenIdToType(0) == random_number % 2
