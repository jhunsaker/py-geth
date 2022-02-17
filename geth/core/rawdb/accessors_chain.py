from geth.core.rawdb.schema import header_hash_key


def read_canonical_hash(db, number: int):

    key = header_hash_key(number)
    hash = db.get(key)
    return hash
