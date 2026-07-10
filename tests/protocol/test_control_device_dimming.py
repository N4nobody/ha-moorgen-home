"""Spec: docs/protocol/control_device_dimming.md"""

from __future__ import annotations

from custom_components.ha_moorgen_home.core.protocol.codec import (
    build_protocol_packet,
    parse_protocol_packet,
)

from tests.protocol._shared import extract_tlv_value_bytes
from tests.protocol.fixtures.control_device_dimming_assets import (
    EXPECTED_PUSH_0_JSON,
    EXPECTED_PUSH_100_JSON,
    EXPECTED_REQ_0_JSON,
    EXPECTED_REQ_100_JSON,
    PUSH_DIM_0_HEX,
    PUSH_DIM_100_HEX,
    PUSH_DIM_30_HEX,
    PUSH_DIM_67_HEX,
    PUSH_DIM_71_HEX,
    PUSH_DIM_8_HEX,
    PUSH_DIM_83_HEX,
    REQ_DIM_0_HEX,
    REQ_DIM_100_HEX,
    REQ_DIM_30_HEX,
    REQ_DIM_67_DUP_HEX,
    REQ_DIM_67_HEX,
    REQ_DIM_71_HEX,
    REQ_DIM_8_HEX,
    REQ_DIM_83_HEX,
)


def _request_json_to_hex(payload: dict) -> str:
    cmd_numeric = int.from_bytes(payload["device_cmd"].encode("utf-8"), "little")

    # NOTE:
    # models.py 将 type=10(Device_CmdData) 标为 string。
    # 抓包实际是 1-byte 原始值（0~100），这里用单字符 string 来对齐原样 hex。
    raw_level_as_one_char = chr(payload["device_cmd_data"])

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
            {"type": 10, "value": raw_level_as_one_char},
        ],
    )
    return packet.hex()


def _request_hex_to_json(packet_hex: str) -> dict:
    packet = parse_protocol_packet(bytes.fromhex(packet_hex))
    field_map = {f.id: f.value for f in packet.fields}

    cmd_raw = extract_tlv_value_bytes(packet_hex, 9) or b""
    level_raw = extract_tlv_value_bytes(packet_hex, 10) or b"\x00"

    return {
        "action": "control_device_dimming",
        "proto_type": packet.proto_type,
        "link_code": packet.link_code,
        "serial_num": packet.serial_num,
        "operate_type": field_map.get(16),
        "device_mac": field_map.get(4),
        "device_cmd": cmd_raw.decode("utf-8"),
        "device_cmd_data": level_raw[0],
    }


def _response_hex_to_json(packet_hex: str) -> dict:
    packet = parse_protocol_packet(bytes.fromhex(packet_hex))
    field_map = {f.id: f.value for f in packet.fields}

    return {
        "action": "control_device_dimming_push",
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
            "device_desc_hex": (field_map.get(5) or b"").hex(),
            "device_name": field_map.get(6),
            "device_state": field_map.get(11),
            "device_cmd_data_hex": (field_map.get(10) or b"").hex(),
            "panel_state_raw": field_map.get(151),
            "brightness": (field_map.get(151) or 0) & 0xFF,
        },
    }


def test_control_device_dimming_request_encode_decode_matches_expected():
    assert _request_json_to_hex(EXPECTED_REQ_100_JSON) == REQ_DIM_100_HEX
    assert _request_json_to_hex(EXPECTED_REQ_0_JSON) == REQ_DIM_0_HEX

    assert _request_hex_to_json(REQ_DIM_100_HEX) == EXPECTED_REQ_100_JSON
    assert _request_hex_to_json(REQ_DIM_0_HEX) == EXPECTED_REQ_0_JSON


def test_control_device_dimming_request_level_sequence_matches_expected():
    req_hex_list = [
        REQ_DIM_30_HEX,
        REQ_DIM_67_HEX,
        REQ_DIM_67_DUP_HEX,
        REQ_DIM_83_HEX,
        REQ_DIM_100_HEX,
        REQ_DIM_71_HEX,
        REQ_DIM_8_HEX,
        REQ_DIM_0_HEX,
    ]
    levels = [_request_hex_to_json(h)["device_cmd_data"] for h in req_hex_list]
    cmds = [_request_hex_to_json(h)["device_cmd"] for h in req_hex_list]

    assert levels == [30, 67, 67, 83, 100, 71, 8, 0]
    assert cmds == ["random-light-dimming"] * len(req_hex_list)


def test_control_device_dimming_push_decode_matches_expected_json():
    assert _response_hex_to_json(PUSH_DIM_100_HEX) == EXPECTED_PUSH_100_JSON
    assert _response_hex_to_json(PUSH_DIM_0_HEX) == EXPECTED_PUSH_0_JSON


def test_control_device_dimming_push_brightness_track_matches_expected():
    push_hex_list = [
        PUSH_DIM_30_HEX,
        PUSH_DIM_67_HEX,
        PUSH_DIM_83_HEX,
        PUSH_DIM_100_HEX,
        PUSH_DIM_71_HEX,
        PUSH_DIM_8_HEX,
        PUSH_DIM_0_HEX,
    ]

    brightness = [_response_hex_to_json(h)["device"]["brightness"] for h in push_hex_list]
    states = [_response_hex_to_json(h)["device"]["device_state"] for h in push_hex_list]

    assert brightness == [30, 67, 83, 100, 71, 8, 0]
    assert states == [1, 1, 1, 1, 1, 1, 0]
