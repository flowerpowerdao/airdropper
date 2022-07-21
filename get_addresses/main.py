import random
from ic.canister import Canister
from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent
import sys

iden = Identity()
client = Client()
agent = Agent(iden, client)


def get_registry(canister: Canister):
    return canister.getRegistry()   # type: ignore


def extract_addresses(registry):
    addresses = []
    for entry in registry[0]:
        # # filter for addressses that should be removed here
        # if entry[1] == '04986920ad70b5e959851d8ac323a4cf3c0e164311cdd2b7da815c9b9553ba96':
        #     continue
        addresses.append(entry[1])
    return addresses


def dump(addresses, random_indices, total_size):
    with open('addresses.txt', 'w') as f:
        for index, address in enumerate(addresses):
            f.write(f'(\"{address}\", {random_indices[index]}),')

    difference = list(
        set(random_indices).symmetric_difference(range(total_size)))

    with open('for_sale.txt', 'w') as f:
        for index in random.sample(difference, len(difference)):
            f.write(f'{index},')


def main():
    # read governance candid from file
    ext_did = open("production.did").read()

    # holds concatenation of all addresses
    all_addresses = []

    # get total collection size
    total_size = int(sys.argv[1])

    # loop over canister
    for canister_id in sys.argv[2:]:
        # create a canister instance
        canister = Canister(
            agent=agent, canister_id=canister_id, candid=ext_did)
        # get registry
        registry = get_registry(canister)
        # extract the addresses
        addresses = extract_addresses(registry)
        all_addresses += addresses

    # create pool of random numbers
    random_indices = random.sample(
        range(total_size), len(all_addresses))

    # dump addresses with random indices to file
    dump(all_addresses, random_indices, total_size)
