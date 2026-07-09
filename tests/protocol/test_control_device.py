"""Spec: docs/protocol/control_device.md"""

from __future__ import annotations

from custom_components.ha_moorgen_home.core.protocol.codec import (
    build_protocol_packet,
    parse_protocol_packet,
)
from custom_components.ha_moorgen_home.core.protocol.commands import control_device

REQ_DEVICE_CMD_ON_HEX = (
    "232e00646f6f796173686370010409e2001d001000010001040008000100ffffffff04ff"
    "090008006c696768742d6f6e23"
)
REQ_DEVICE_CMD_OFF_HEX = (
    "232f00646f6f796173686370010409e4001e001000010001040008000100ffffffff04ff"
    "090009006c696768742d6f666623"
)

EXPECTED_REQ_ON_JSON = {
    "action": "control_device",
    "proto_type": 4,
    "link_code": 9,
    "serial_num": 226,
    "operate_type": 1,
    "device_mac": 18376093854555111425,
    "device_cmd": "light-on",
}
EXPECTED_REQ_OFF_JSON = {
    "action": "control_device",
    "proto_type": 4,
    "link_code": 9,
    "serial_num": 228,
    "operate_type": 1,
    "device_mac": 18376093854555111425,
    "device_cmd": "light-off",
}

PUSH_ON_HEX = (
    "237e00646f6f79617368637001050c00006d001b000100031100010001040008000100ffffffff"
    "04ff600001000198000100489c00010000720001000086000100015f00010004a7000100050102"
    "01000205001000646f6f796172303630306c313130103006000c00e9a490e58e85e4b8bbe781af"
    "0b000100010a000200ffff23"
)
PUSH_OFF_HEX = (
    "237e00646f6f79617368637001050c00006d001b000100031100010001040008000100ffffffff"
    "04ff600001000198000100489c00010000720001000086000100015f00010004a7000100050102"
    "01000205001000646f6f796172303630306c313130103006000c00e9a490e58e85e4b8bbe781af"
    "0b000100000a000200ffff23"
)

EXPECTED_PUSH_ON_JSON = {
    "action": "control_device_push",
    "proto_type": 5,
    "link_code": 12,
    "serial_num": 0,
    "update_proc": 3,
    "device_count": 1,
    "device": {
        "device_mac": 18376093854555111425,
        "device_is_online": 1,
        "device_version": 72,
        "device_forbid_by_lock": 0,
        "device_virtual_flag": 0,
        "dev_channel_sum": 1,
        "device_channel": 4,
        "device_icon": 5,
        "entity_hidden": 2,
        "device_desc": "dooyar0600l110\x100",
        "device_name": "餐厅主灯",
        "device_state": 1,
        "device_cmd_data": "ffff",
    },
}
EXPECTED_PUSH_OFF_JSON = {
    "action": "control_device_push",
    "proto_type": 5,
    "link_code": 12,
    "serial_num": 0,
    "update_proc": 3,
    "device_count": 1,
    "device": {
        "device_mac": 18376093854555111425,
        "device_is_online": 1,
        "device_version": 72,
        "device_forbid_by_lock": 0,
        "device_virtual_flag": 0,
        "dev_channel_sum": 1,
        "device_channel": 4,
        "device_icon": 5,
        "entity_hidden": 2,
        "device_desc": "dooyar0600l110\x100",
        "device_name": "餐厅主灯",
        "device_state": 0,
        "device_cmd_data": "ffff",
    },
}


def _extract_tlv_value_bytes(packet_hex: str, field_id: int) -> bytes | None:
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


def _request_json_to_hex(payload: dict) -> str:
    cmd_numeric = int.from_bytes(payload["device_cmd"].encode("utf-8"), "little")
    packet = build_protocol_packet(
        msgFlag=0x23,
        protoName="dooyashcp",
        protoNum=1,
        protoType=payload["proto_type"],
        linkCode=payload["link_code"],
        serialNum=payload.get("serial_num", 0),
        fields=[
            {"type": 16, "value": payload["operate_type"]},
            {"type": 4, "value": payload["device_mac"]},
            {"type": 9, "value": cmd_numeric},
        ],
    )
    return packet.hex()


def _request_hex_to_json(packet_hex: str) -> dict:
    packet = parse_protocol_packet(bytes.fromhex(packet_hex))
    field_map = {f.id: f.value for f in packet.fields}

    cmd_raw = _extract_tlv_value_bytes(packet_hex, 9) or b""
    cmd_text = cmd_raw.decode("utf-8")

    return {
        "action": "control_device",
        "proto_type": packet.proto_type,
        "link_code": packet.link_code,
        "serial_num": packet.serial_num,
        "operate_type": field_map.get(16),
        "device_mac": field_map.get(4),
        "device_cmd": cmd_text,
    }


def _response_hex_to_json(packet_hex: str) -> dict:
    packet = parse_protocol_packet(bytes.fromhex(packet_hex))
    field_map = {f.id: f.value for f in packet.fields}

    return {
        "action": "control_device_push",
        "proto_type": packet.proto_type,
        "link_code": packet.link_code,
        "serial_num": packet.serial_num,
        "update_proc": field_map.get(27),
        "device_count": field_map.get(17),
        "device": {
            "device_mac": field_map.get(4),
            "device_is_online": field_map.get(96),
            "device_version": field_map.get(152),
            "device_forbid_by_lock": field_map.get(156),
            "device_virtual_flag": field_map.get(114),
            "dev_channel_sum": field_map.get(134),
            "device_channel": field_map.get(95),
            "device_icon": field_map.get(167),
            "entity_hidden": field_map.get(513),
            "device_desc": field_map.get(5),
            "device_name": field_map.get(6),
            "device_state": field_map.get(11),
            "device_cmd_data": (field_map.get(10) or b"").hex(),
        },
    }


def test_control_device_request_json_hex_roundtrip():
    assert _request_json_to_hex(EXPECTED_REQ_ON_JSON) == REQ_DEVICE_CMD_ON_HEX
    assert _request_json_to_hex(EXPECTED_REQ_OFF_JSON) == REQ_DEVICE_CMD_OFF_HEX

    assert control_device(18376093854555111425, "light-on").hex() == (
        "232e00646f6f79617368637001040900001d001000010001040008000100ffffffff04ff"
        "090008006c696768742d6f6e23"
    )

    assert _request_hex_to_json(REQ_DEVICE_CMD_ON_HEX) == EXPECTED_REQ_ON_JSON
    assert _request_hex_to_json(REQ_DEVICE_CMD_OFF_HEX) == EXPECTED_REQ_OFF_JSON


def test_control_device_push_hex_to_json():
    assert _response_hex_to_json(PUSH_ON_HEX) == EXPECTED_PUSH_ON_JSON
    assert _response_hex_to_json(PUSH_OFF_HEX) == EXPECTED_PUSH_OFF_JSON
