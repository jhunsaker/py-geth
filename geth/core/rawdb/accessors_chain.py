import rusty_rlp as rlp
from hexbytes import HexBytes

from geth.core.rawdb.schema import header_hash_key, header_key


def _decode_signed(n: bytes) -> int:

    return int.from_bytes(n, byteorder="big", signed=True)


def _decode_unsigned(n: bytes) -> int:

    return int.from_bytes(n, byteorder="big", signed=False)


def read_canonical_hash(db, number: int) -> bytes:

    key = header_hash_key(number)
    hash = db.get(key)
    return hash


def read_header_rlp(db, hash: bytes, number: int) -> bytes:

    key = header_key(number, hash)
    data = db.get(key)
    return data


def read_header(db, hash: bytes, number: int):

    data = read_header_rlp(db, hash=hash, number=number)
    header_data = rlp.decode_raw(data, strict=True, preserve_cache_info=False)
    header_data = header_data[0]
    header = {
        "parent_hash": HexBytes(header_data[0]),
        "uncle_hash": HexBytes(header_data[1]),
        "coinbase": HexBytes(header_data[2]),
        "root": HexBytes(header_data[3]),
        "tx_hash": HexBytes(header_data[4]),
        "receipt_hash": HexBytes(header_data[5]),
        "bloom": HexBytes(header_data[6]),
        "difficulty": _decode_unsigned(header_data[7]),
        "number": _decode_unsigned(header_data[8]),
        "gas_limit": _decode_unsigned(header_data[9]),
        "gas_used": _decode_unsigned(header_data[10]),
        "time": _decode_unsigned(header_data[11]),
        "extra": header_data[12],
        "mix_digest": HexBytes(header_data[13]),
        "nonce": HexBytes(header_data[14]),
    }
    return header
