from ic.canister import Canister
from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent
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


def get_common_holders(*lists):
    common_holders = []
    if len(lists) == 0:
        return common_holders
    btcflower_copy = lists[0].copy()
    for holder in btcflower_copy:
        if all(holder in lst for lst in lists):
            common_holders.append(holder)
            for lst in lists:
                lst.remove(holder)

    return common_holders, lists


def main():
    # read governance candid from file
    ext_did = open(os.path.dirname(__file__) + "/../production.did").read()

    print("getting holders...")
    btcflower = get_holders("pk6rk-6aaaa-aaaae-qaazq-cai", ext_did)
    ethflower = get_holders("dhiaa-ryaaa-aaaae-qabva-cai", ext_did)
    icpflower = get_holders("4ggk4-mqaaa-aaaae-qad6q-cai", ext_did)

    result = get_common_holders(btcflower, ethflower, icpflower)
    print(len(result[0]))
    print(len(result[1][0]))
    print(len(result[1][1]))
    print(len(result[1][2]))

    # dump addresses with random indices to file
    dump(result[0], "triology")
    dump(result[1][0], "btcflower")
    dump(result[1][1], "ethflower")
    dump(result[1][2], "icpflower")
