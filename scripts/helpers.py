from brownie import (
    network,
    config,
    accounts,
    interface,
    Contract,
    VRFCoordinatorMock,
    LinkToken
)
from web3 import Web3


FORKED_LOCAL_ENV = ["mainnet-fork"]
LOCAL_BLOCKCHAIN_ENV = ["development", "ganache-local"]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"

contract_to_mock = {
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}

TYPE_MAPPING = {0:"CHARACTER",1:"SCENE"}

def get_type(type_):
    return TYPE_MAPPING[type_]

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


def get_contract(contract_name):
    """
    This function will grab the contract address from the brownie config
    if defined, otherwise it will deploy a mock version of that contract and
    return that mock contract
    Args:
        contract_name(string)
    Returns:
        brownie.network.contract.ProjectContract: this most recently deployed
        version of this contract
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENV:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks():
    account = get_account()
    link_token = LinkToken.deploy({'from':account})
    VRFCoordinatorMock.deploy(link_token.address,{'from':account})
    print("Deployed Mocks")


def fund_with_link(contract_address,account=None,link_token=None,amount=100000000000000000): #0.1 Link
    if(account==None):
        account = get_account()
    if(link_token==None):
        link_token = get_contract("link_token")
    tx = link_token.transfer(contract_address,amount,{'from':account})
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address,amount,{'from':account})
    tx.wait(1)
    print("Funded Contract")
    return tx