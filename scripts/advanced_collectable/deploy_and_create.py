from scripts.helpers import get_account,OPENSEA_URL
from brownie import AdvancedCollectable


def deploy_and_create():
    account = get_account()
    adv_collectable = AdvancedCollectable.deploy({"from": account})
   


def main():
    deploy_and_create()