from scripts.helpers import get_account, OPENSEA_URL, get_contract,fund_with_link
from brownie import AdvancedCollectable, config, network


def deploy_and_create():
    account = get_account()
    adv_collectable = AdvancedCollectable.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["key_hash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
    )
    fund_with_link(adv_collectable.address)
    creating_tx = adv_collectable.createCollectable({"from":account})
    creating_tx.wait(1)
    print("New Token has been Created!")


def main():
    deploy_and_create()
