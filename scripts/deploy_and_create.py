from scripts.helpers import get_account
from brownie import SimpleCollectable


simple_token_uri = ""
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"

def deploy_and_create():
    account = get_account()
    simple_collectable = SimpleCollectable.deploy({"from": account})
    tx = simple_collectable.createCollectable(simple_token_uri,{"from":account})
    tx.wait(1)
    print(f"NFT Deployed at {OPENSEA_URL.format(simple_collectable.address,simple_collectable.tokenCounter() - 1)}")
    return simple_collectable


def main():
    deploy_and_create()