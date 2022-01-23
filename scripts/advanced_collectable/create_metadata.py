from brownie import AdvancedCollectable, config, network
from scripts.helpers import get_type
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests, json
from scripts.upload_to_pinata import upload_to_pinata


def main():
    adv_collectable = AdvancedCollectable[-1]
    number_of_adv_collectable = adv_collectable.tokenCounter()
    print(f"Total {number_of_adv_collectable} collectables are available")

    for token_id in range(number_of_adv_collectable):
        type_ = get_type(adv_collectable.tokenIdToType(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{type_}.json"
        )
        collectable_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists!, Delete it to Overwrite...")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            collectable_metadata["name"] = type_
            collectable_metadata["description"] = f"An Nice {type_}"
            image_path = "./img/" + type_.lower() + ".jpg"
            # image_uri = upload_to_ipfs(image_path)
            image_uri = upload_to_pinata(image_path)

            collectable_metadata["image"] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(collectable_metadata, file)
            meta_data_uri = upload_to_pinata(metadata_file_name)
            print(meta_data_uri)


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        return image_uri
