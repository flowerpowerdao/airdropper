from audioop import add
import random
from ic.canister import Canister
from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent
from ic.candid import Types

iden = Identity()
client = Client()
agent = Agent(iden, client)


def get_registry(canister: Canister):
    return canister.getRegistry()   # type: ignore


def extract_addresses(registry):
    addresses = []
    for entry in registry[0]:
        addresses.append(entry[1])
    return addresses


def dump(addresses, random_indices):
    with open('addresses.txt', 'w') as f:
        for index, address in enumerate(addresses):
            f.write(f'(\"{address}\", {random_indices[index]})')


def main():
    # create pool of random numbers
    random_indices = random.sample(range(4024), 4024)

    # read governance candid from file
    ext_did = open("production.did").read()

    # create a governance canister instance
    btcflower = Canister(
        agent=agent, canister_id="pk6rk-6aaaa-aaaae-qaazq-cai", candid=ext_did)

    # create a governance canister instance
    ethflower = Canister(
        agent=agent, canister_id="dhiaa-ryaaa-aaaae-qabva-cai", candid=ext_did)

    btcflower_registry = get_registry(btcflower)
    ethflower_registry = get_registry(ethflower)

    btcflower_addresses = extract_addresses(btcflower_registry)
    ethflower_addresses = extract_addresses(ethflower_registry)

    addresses = btcflower_addresses + ethflower_addresses

    dump(addresses, random_indices)


if __name__ == "__main__":
    main()
