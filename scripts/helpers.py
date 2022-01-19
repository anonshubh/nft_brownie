from brownie import accounts,network,config


FORKED_LOCAL_ENV = ["mainnet-fork"]
LOCAL_BLOCKCHAIN_ENV = ["development", "ganache-local"]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (network.show_active() in LOCAL_BLOCKCHAIN_ENV) or (
        network.show_active() in FORKED_LOCAL_ENV
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])