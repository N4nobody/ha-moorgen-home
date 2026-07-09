"""Spec: docs/protocol/control_device_dimming.md"""

from __future__ import annotations

from custom_components.ha_moorgen_home.core.protocol.codec import (
    build_protocol_packet,
    parse_protocol_packet,
)

REQ_DIM_30_HEX = (
    "233f00646f6f79617368637001040978012e001000010001040008001500ffffffff00ff"
    "0900140072616e646f6d2d6c696768742d64696d6d696e670a0001001e23"
)
REQ_DIM_67_HEX = (
    "233f00646f6f7961736863700104097a012e001000010001040008001500ffffffff00ff"
    "0900140072616e646f6d2d6c696768742d64696d6d696e670a0001004323"
)
REQ_DIM_67_DUP_HEX = (
    "233f00646f6f7961736863700104097c012e001000010001040008001500ffffffff00ff"
    "0900140072616e646f6d2d6c696768742d64696d6d696e670a0001004323"
)
REQ_DIM_83_HEX = (
    "233f00646f6f7961736863700104097e012e001000010001040008001500ffffffff00ff"
    "0900140072616e646f6d2d6c696768742d64696d6d696e670a0001005323"
)
REQ_DIM_100_HEX = (
    "233f00646f6f79617368637001040980012e001000010001040008001500ffffffff00ff"
    "0900140072616e646f6d2d6c696768742d64696d6d696e670a0001006423"
)
REQ_DIM_71_HEX = (
    "233f00646f6f79617368637001040982012e001000010001040008001500ffffffff00ff"
    "0900140072616e646f6d2d6c696768742d64696d6d696e670a0001004723"
)
REQ_DIM_8_HEX = (
    "233f00646f6f79617368637001040984012e001000010001040008001500ffffffff00ff"
    "0900140072616e646f6d2d6c696768742d64696d6d696e670a0001000823"
)
REQ_DIM_0_HEX = (
    "233f00646f6f79617368637001040986012e001000010001040008001500ffffffff00ff"
    "0900140072616e646f6d2d6c696768742d64696d6d696e670a0001000023"
)

PUSH_DIM_30_HEX = (
    "232101646f6f79617368637001050c000010011b000100031100010001040008001500ffffffff00ff"
    "600001000198000100409c00010000720001000086000100085f00010000a7000100020102010002"
    "05001000646f6f7961723031303072313533803006000f00e4b8bbe58da7e5ba8ae5a4b4e58fb30b00"
    "0100010a009c00010504303730300500030201000002050430383030050003020100000301f000ffff"
    "ffff00ff01550004010200ffffffff02ff116c696768742d726576657273652d657865000505043036"
    "303005000302010000060504306330300500030201000007010100ffffffff07ff116c696768742d72"
    "6576657273652d6578650008010100ffffffff05ff116c696768742d726576657273652d6578650097"
    "0002001eff23"
)
PUSH_DIM_67_HEX = (
    "232101646f6f79617368637001050c000010011b000100031100010001040008001500ffffffff00ff"
    "600001000198000100409c00010000720001000086000100085f00010000a7000100020102010002"
    "05001000646f6f7961723031303072313533803006000f00e4b8bbe58da7e5ba8ae5a4b4e58fb30b00"
    "0100010a009c00010504303730300500030201000002050430383030050003020100000301f000ffff"
    "ffff00ff01550004010200ffffffff02ff116c696768742d726576657273652d657865000505043036"
    "303005000302010000060504306330300500030201000007010100ffffffff07ff116c696768742d72"
    "6576657273652d6578650008010100ffffffff05ff116c696768742d726576657273652d6578650097"
    "00020043ff23"
)
PUSH_DIM_83_HEX = (
    "232101646f6f79617368637001050c000010011b000100031100010001040008001500ffffffff00ff"
    "600001000198000100409c00010000720001000086000100085f00010000a7000100020102010002"
    "05001000646f6f7961723031303072313533803006000f00e4b8bbe58da7e5ba8ae5a4b4e58fb30b00"
    "0100010a009c00010504303730300500030201000002050430383030050003020100000301f000ffff"
    "ffff00ff01550004010200ffffffff02ff116c696768742d726576657273652d657865000505043036"
    "303005000302010000060504306330300500030201000007010100ffffffff07ff116c696768742d72"
    "6576657273652d6578650008010100ffffffff05ff116c696768742d726576657273652d6578650097"
    "00020053ff23"
)
PUSH_DIM_100_HEX = (
    "232101646f6f79617368637001050c000010011b000100031100010001040008001500ffffffff00ff"
    "600001000198000100409c00010000720001000086000100085f00010000a7000100020102010002"
    "05001000646f6f7961723031303072313533803006000f00e4b8bbe58da7e5ba8ae5a4b4e58fb30b00"
    "0100010a009c00010504303730300500030201000002050430383030050003020100000301f000ffff"
    "ffff00ff01550004010200ffffffff02ff116c696768742d726576657273652d657865000505043036"
    "303005000302010000060504306330300500030201000007010100ffffffff07ff116c696768742d72"
    "6576657273652d6578650008010100ffffffff05ff116c696768742d726576657273652d6578650097"
    "00020064ff23"
)
PUSH_DIM_71_HEX = (
    "232101646f6f79617368637001050c000010011b000100031100010001040008001500ffffffff00ff"
    "600001000198000100409c00010000720001000086000100085f00010000a7000100020102010002"
    "05001000646f6f7961723031303072313533803006000f00e4b8bbe58da7e5ba8ae5a4b4e58fb30b00"
    "0100010a009c00010504303730300500030201000002050430383030050003020100000301f000ffff"
    "ffff00ff01550004010200ffffffff02ff116c696768742d726576657273652d657865000505043036"
    "303005000302010000060504306330300500030201000007010100ffffffff07ff116c696768742d72"
    "6576657273652d6578650008010100ffffffff05ff116c696768742d726576657273652d6578650097"
    "00020047ff23"
)
PUSH_DIM_8_HEX = (
    "232101646f6f79617368637001050c000010011b000100031100010001040008001500ffffffff00ff"
    "600001000198000100409c00010000720001000086000100085f00010000a7000100020102010002"
    "05001000646f6f7961723031303072313533803006000f00e4b8bbe58da7e5ba8ae5a4b4e58fb30b00"
    "0100010a009c00010504303730300500030201000002050430383030050003020100000301f000ffff"
    "ffff00ff01550004010200ffffffff02ff116c696768742d726576657273652d657865000505043036"
    "303005000302010000060504306330300500030201000007010100ffffffff07ff116c696768742d72"
    "6576657273652d6578650008010100ffffffff05ff116c696768742d726576657273652d6578650097"
    "00020008ff23"
)
PUSH_DIM_0_HEX = (
    "232101646f6f79617368637001050c000010011b000100031100010001040008001500ffffffff00ff"
    "600001000198000100409c00010000720001000086000100085f00010000a7000100020102010002"
    "05001000646f6f7961723031303072313533803006000f00e4b8bbe58da7e5ba8ae5a4b4e58fb30b00"
    "0100000a009c00010504303730300500030201000002050430383030050003020100000301f000ffff"
    "ffff00ff01550004010200ffffffff02ff116c696768742d726576657273652d657865000505043036"
    "303005000302010000060504306330300500030201000007010100ffffffff07ff116c696768742d72"
    "6576657273652d6578650008010100ffffffff05ff116c696768742d726576657273652d6578650097"
    "00020000ff23"
)

EXPECTED_REQ_100_JSON = {
    "action": "control_device_dimming",
    "proto_type": 4,
    "link_code": 9,
    "serial_num": 384,
    "operate_type": 1,
    "device_mac": 18374967954648268821,
    "device_cmd": "random-light-dimming",
    "device_cmd_data": 100,
}
EXPECTED_REQ_0_JSON = {
    "action": "control_device_dimming",
    "proto_type": 4,
    "link_code": 9,
    "serial_num": 390,
    "operate_type": 1,
    "device_mac": 18374967954648268821,
    "device_cmd": "random-light-dimming",
    "device_cmd_data": 0,
}

EXPECTED_PUSH_100_JSON = {
    "action": "control_device_dimming_push",
    "proto_type": 5,
    "link_code": 12,
    "serial_num": 0,
    "update_proc": 3,
    "device_count": 1,
    "device": {
        "device_mac": 18374967954648268821,
        "device_is_online": 1,
        "device_version": 64,
        "device_forbid_by_lock": 0,
        "device_virtual_flag": 0,
        "dev_channel_sum": 8,
        "device_channel": 0,
        "device_icon": 2,
        "entity_hidden": 2,
        "device_desc_hex": "646f6f79617230313030723135338030",
        "device_name": "主卧床头右",
        "device_state": 1,
        "device_cmd_data_hex": (
            "010504303730300500030201000002050430383030050003020100000301f000ffffffff00ff"
            "01550004010200ffffffff02ff116c696768742d726576657273652d65786500050504303630"
            "3005000302010000060504306330300500030201000007010100ffffffff07ff116c69676874"
            "2d726576657273652d6578650008010100ffffffff05ff116c696768742d726576657273652d"
            "65786500"
        ),
        "panel_state_raw": 65380,
        "brightness": 100,
    },
}
EXPECTED_PUSH_0_JSON = {
    "action": "control_device_dimming_push",
    "proto_type": 5,
    "link_code": 12,
    "serial_num": 0,
    "update_proc": 3,
    "device_count": 1,
    "device": {
        "device_mac": 18374967954648268821,
        "device_is_online": 1,
        "device_version": 64,
        "device_forbid_by_lock": 0,
        "device_virtual_flag": 0,
        "dev_channel_sum": 8,
        "device_channel": 0,
        "device_icon": 2,
        "entity_hidden": 2,
        "device_desc_hex": "646f6f79617230313030723135338030",
        "device_name": "主卧床头右",
        "device_state": 0,
        "device_cmd_data_hex": (
            "010504303730300500030201000002050430383030050003020100000301f000ffffffff00ff"
            "01550004010200ffffffff02ff116c696768742d726576657273652d65786500050504303630"
            "3005000302010000060504306330300500030201000007010100ffffffff07ff116c69676874"
            "2d726576657273652d6578650008010100ffffffff05ff116c696768742d726576657273652d"
            "65786500"
        ),
        "panel_state_raw": 65280,
        "brightness": 0,
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

    cmd_raw = _extract_tlv_value_bytes(packet_hex, 9) or b""
    level_raw = _extract_tlv_value_bytes(packet_hex, 10) or b"\x00"

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


def test_control_device_dimming_request_json_hex_roundtrip():
    assert _request_json_to_hex(EXPECTED_REQ_100_JSON) == REQ_DIM_100_HEX
    assert _request_json_to_hex(EXPECTED_REQ_0_JSON) == REQ_DIM_0_HEX

    assert _request_hex_to_json(REQ_DIM_100_HEX) == EXPECTED_REQ_100_JSON
    assert _request_hex_to_json(REQ_DIM_0_HEX) == EXPECTED_REQ_0_JSON


def test_control_device_dimming_request_level_sequence():
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


def test_control_device_dimming_push_hex_to_json():
    assert _response_hex_to_json(PUSH_DIM_100_HEX) == EXPECTED_PUSH_100_JSON
    assert _response_hex_to_json(PUSH_DIM_0_HEX) == EXPECTED_PUSH_0_JSON


def test_control_device_dimming_push_brightness_track():
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
