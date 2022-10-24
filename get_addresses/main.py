import random
from ic.canister import Canister
from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent

iden = Identity()
client = Client()
agent = Agent(iden, client)


def get_registry(canister: Canister):
    return canister.getRegistry()  # type: ignore


def extract_addresses(registry):
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


def dump(addresses):
    with open("addresses.txt", "w") as f:
        for index, address in enumerate(addresses):
            f.write(f'"{address}",')


def get_holders(canister_id: str, ext_did: str):
    canister = Canister(agent=agent, canister_id=canister_id, candid=ext_did)
    # get registry
    registry = get_registry(canister)
    # extract the addresses
    addresses = extract_addresses(registry)
    return addresses


def get_common_holders(btcflower, ethflower):
    common_holders = list()
    for address in btcflower:
        if address in ethflower:
            ethflower.remove(address)
            common_holders.append(address)

    return common_holders


def main():
    # read governance candid from file
    ext_did = open("production.did").read()

    btcflower = get_holders("pk6rk-6aaaa-aaaae-qaazq-cai", ext_did)
    ethflower = get_holders("dhiaa-ryaaa-aaaae-qabva-cai", ext_did)

    common_holders = get_common_holders(btcflower, ethflower)
    print(2021 - len(common_holders))

    # dump addresses with random indices to file
    dump(common_holders)


main()
