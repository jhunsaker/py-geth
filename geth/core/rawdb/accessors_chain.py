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


def read_header(db, hash: bytes, number: int) -> dict:

    data = read_header_rlp(db, hash=hash, number=number)
    header_data = rlp.decode_raw(data, strict=True, preserve_cache_info=False)
    header_data = header_data[0]

    # names translated from go code:
    # https://github.com/ethereum/go-ethereum/blob/master/core/types/block.go#L70-L95
    # https://ethereum.github.io/yellowpaper/paper.pdf
    header = {
        "parent_hash": HexBytes(header_data[0]),         # 256-bit hash; `json:"parentHash"       gencodec:"required"`
        "uncle_hash": HexBytes(header_data[1]),          # 256-bit hash; `json:"sha3Uncles"       gencodec:"required"`
        "coinbase": HexBytes(header_data[2]),            # 160-bit addr; `json:"miner"            gencodec:"required"`
        "root": HexBytes(header_data[3]),                # 256-bit hash; `json:"stateRoot"        gencodec:"required"`
        "tx_hash": HexBytes(header_data[4]),             # 256-bit hash; `json:"transactionsRoot" gencodec:"required"`
        "receipt_hash": HexBytes(header_data[5]),        # 256-bit hash; `json:"receiptsRoot"     gencodec:"required"`
        "bloom": HexBytes(header_data[6]),               # 2048-bit val; `json:"logsBloom"        gencodec:"required"`
        "difficulty": _decode_unsigned(header_data[7]),  # bigint;       `json:"difficulty"       gencodec:"required"`
        "number": _decode_unsigned(header_data[8]),      # bigint;       `json:"number"           gencodec:"required"`
        "gas_limit": _decode_unsigned(header_data[9]),   # uint64;       `json:"gasLimit"         gencodec:"required"`
        "gas_used": _decode_unsigned(header_data[10]),   # uint64;       `json:"gasUsed"          gencodec:"required"`
        "time": _decode_unsigned(header_data[11]),       # uint64;       `json:"timestamp"        gencodec:"required"`
        "extra": header_data[12],                        # 32 bytes;     `json:"extraData"        gencodec:"required"`
        "mix_digest": HexBytes(header_data[13]),         # 256-bit hash; `json:"mixHash"`
        "nonce": _decode_unsigned(header_data[14]),      # 64-bit val;   `json:"nonce"`
    }
    return header
