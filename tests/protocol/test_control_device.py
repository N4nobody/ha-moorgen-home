"""Spec: docs/protocol/control_device.md"""

from __future__ import annotations

from custom_components.ha_moorgen_home.core.protocol.codec import (
    build_protocol_packet,
    parse_protocol_packet,
)
from custom_components.ha_moorgen_home.core.protocol.commands import control_device

from tests.protocol._shared import extract_tlv_value_bytes
from tests.protocol.fixtures.control_device_assets import (
    EXPECTED_PUSH_OFF_JSON,
    EXPECTED_PUSH_ON_JSON,
    EXPECTED_REQ_OFF_JSON,
    EXPECTED_REQ_ON_JSON,
    PUSH_OFF_HEX,
    PUSH_ON_HEX,
    REQ_DEVICE_CMD_OFF_HEX,
    REQ_DEVICE_CMD_ON_HEX,
)


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

    cmd_raw = extract_tlv_value_bytes(packet_hex, 9) or b""
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


def test_control_device_request_encode_decode_and_command_default_serial():
    assert _request_json_to_hex(EXPECTED_REQ_ON_JSON) == REQ_DEVICE_CMD_ON_HEX
    assert _request_json_to_hex(EXPECTED_REQ_OFF_JSON) == REQ_DEVICE_CMD_OFF_HEX

    assert control_device(18376093854555111425, "light-on").hex() == (
        "232e00646f6f79617368637001040900001d001000010001040008000100ffffffff04ff"
        "090008006c696768742d6f6e23"
    )

    assert _request_hex_to_json(REQ_DEVICE_CMD_ON_HEX) == EXPECTED_REQ_ON_JSON
    assert _request_hex_to_json(REQ_DEVICE_CMD_OFF_HEX) == EXPECTED_REQ_OFF_JSON


def test_control_device_push_decode_matches_expected_json():
    assert _response_hex_to_json(PUSH_ON_HEX) == EXPECTED_PUSH_ON_JSON
    assert _response_hex_to_json(PUSH_OFF_HEX) == EXPECTED_PUSH_OFF_JSON
