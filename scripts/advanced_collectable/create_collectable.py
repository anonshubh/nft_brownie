import imp
from webbrowser import get
from brownie import AdvancedCollectable, config, network
from scripts.helpers import get_account, OPENSEA_URL, get_contract, fund_with_link
from web3 import Web3


def main():
    account = get_account()
    advanced_collectable = AdvancedCollectable[-1]
    fund_with_link(advanced_collectable.address, amount=Web3.toWei(0.1, "ether"))
    creation_transaction = advanced_collectable.createCollectable({"from":account})
    creation_transaction.wait(1)
    print("Collectable created!")