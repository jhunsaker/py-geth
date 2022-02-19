import struct

HEADER_PREFIX = b"h"
HEADER_HASH_SUFFIX = b"n"
BLOCK_BODY_PREFIX = b"b"


def encode_block_number(number: int) -> bytes:

    return struct.pack(">Q", number)


def header_key(number: int, hash: bytes) -> bytes:

    num = encode_block_number(number)
    return b"".join([HEADER_PREFIX, num, hash])


def header_hash_key(number: int) -> bytes:

    num = encode_block_number(number)
    return b"".join([HEADER_PREFIX, num, HEADER_HASH_SUFFIX])


def block_body_key(number: int, hash: bytes) -> bytes:

    num = encode_block_number(number)
    return b"".join([BLOCK_BODY_PREFIX, num, hash])
