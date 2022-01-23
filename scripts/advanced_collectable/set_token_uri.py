from brownie import AdvancedCollectable, config, network
from scripts.helpers import OPENSEA_URL, get_account, get_type

meta_data_dic = {
    "CHARACTER": "https://ipfs.io/ipfs/Qme37KzMvBc6Y7rtRKJ5rgRmk2DmUF93HpE7Lfim32RuH2?filename=0-CHARACTER.json",
    "SCENE": "https://ipfs.io/ipfs/QmbbAwfEq7o63k8imXaq1qLMDzf4JURE3wUu4zEtTMQpLj?filename=1-SCENE.json",
}


def main():
    print(f"Working on {network.show_active()}")
    adv_collectable = AdvancedCollectable[-1]
    number_of_adv_collectable = adv_collectable.tokenCounter()
    print(f"Total {number_of_adv_collectable} collectables are available")

    for token_id in range(number_of_adv_collectable):
        type_ = get_type(adv_collectable.tokenIdToType(token_id))
        if not adv_collectable.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            set_tokenURI(token_id,adv_collectable,meta_data_dic[type_])


def set_tokenURI(token_id, ntf_contract, tokenURI):
    account = get_account()
    tx = ntf_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"You can view your NFT at {OPENSEA_URL.format(ntf_contract.address,token_id)}"
    )
    print("Please wait for 20 minutes and then hit the refresh metadata button!")
