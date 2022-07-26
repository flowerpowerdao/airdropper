import json


def get_registry():
    with open('pk6rk-6aaaa-aaaae-qaazq-cai.json', 'r') as f:
        return json.load(f)


def extract_addresses(registry):
    addresses = []
    for entry in registry:
        # filter for addressses that should be removed here
        if entry[1] == '04986920ad70b5e959851d8ac323a4cf3c0e164311cdd2b7da815c9b9553ba96':
            continue
        addresses.append(entry[1])
    return addresses


def dump(addresses):
    with open('addresses.txt', 'w') as f:
        for index, address in enumerate(addresses):
            f.write(f'\"{address}\",')


def main():

    # holds concatenation of all addresses
    all_addresses = []

    registry = get_registry()
    # extract the addresses
    addresses = extract_addresses(registry)
    all_addresses += addresses
    print(len(all_addresses))

    # dump addresses with random indices to file
    dump(all_addresses)
