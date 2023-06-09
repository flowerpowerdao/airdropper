from ic.canister import Canister
from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent
from collections import Counter
import os

iden = Identity()
client = Client()
agent = Agent(iden, client)


def get_registry(canister: Canister):
    print("getting registry...")
    return canister.getRegistry()  # type: ignore


def extract_addresses(registry):
    print("extracting addresses...")
    addresses = []
    for entry in registry[0]:
        # filter for addressses that should be removed here
        if (
            entry[1]
            == "04986920ad70b5e959851d8ac323a4cf3c0e164311cdd2b7da815c9b9553ba96"
        ):  # toniq earn address
            continue
        addresses.append(entry[1])
    return addresses


def dump(addresses, filename):
    with open(f"{filename}.txt", "w") as f:
        for address in addresses:
            f.write(f'"{address}";')


def get_holders(canister_id: str, ext_did: str):
    canister = Canister(agent=agent, canister_id=canister_id, candid=ext_did)
    # get registry
    registry = get_registry(canister)
    # extract the addresses
    addresses = extract_addresses(registry)
    return addresses


def get_pair_holders(holders):
    counter = Counter(holders)
    pair_holders = [item for item, count in counter.items() for _ in range(count // 2)]
    return pair_holders


def main():
    # read governance candid from file
    ext_did = open(os.path.dirname(__file__) + "/../production.did").read()

    print("getting holders...")
    punks = get_holders("skjpp-haaaa-aaaae-qac7q-cai", ext_did)
    result = get_pair_holders(punks)

    print(len(result))

    # dump addresses with random indices to file
    dump(result, "double_punks")
