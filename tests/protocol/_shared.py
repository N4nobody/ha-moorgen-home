from __future__ import annotations


def extract_tlv_value_bytes(packet_hex: str, field_id: int) -> bytes | None:
    """Extract raw TLV value bytes by field id from a protocol hex packet."""
    data = bytes.fromhex(packet_hex)
    data_len = data[17] + (data[18] << 8)
    ptr = 19
    limit = ptr + data_len
    while ptr < limit and ptr + 4 <= len(data):
        dtype = data[ptr] + (data[ptr + 1] << 8)
        vlen = data[ptr + 2] + (data[ptr + 3] << 8)
        value = data[ptr + 4 : ptr + 4 + vlen]
        if dtype == field_id:
            return value
        ptr += 4 + vlen
    return None
