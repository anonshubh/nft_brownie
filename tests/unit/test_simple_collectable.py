from scripts.helpers import LOCAL_BLOCKCHAIN_ENV,get_account
from scripts.simple_collectable.deploy_and_create import deploy_and_create
import pytest
from brownie import network

def test_can_create_simple_collectable():
    if(network.show_active() not in LOCAL_BLOCKCHAIN_ENV):
        pytest.skip()

    simple_collectable = deploy_and_create()
    assert simple_collectable.ownerOf(0) == get_account()