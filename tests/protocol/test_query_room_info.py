"""Spec: docs/protocol/query_room_info.md"""

from __future__ import annotations

from custom_components.ha_moorgen_home.core.protocol.codec import (
    build_protocol_packet,
    parse_protocol_packet,
    route,
)
from custom_components.ha_moorgen_home.core.protocol.commands import query_room_info

# 抓包样本请求（query room info）
REQ_ROOM_INFO_HEX = "231600646f6f796173686370010307080005000f0001000b23"
EXPECTED_REQ_JSON = {
    "action": "query_room_info",
    "proto_type": 3,
    "link_code": 7,
    "serial_num": 8,
    "datareq_type": 11,
}

# 抓包样本响应（room info response）
RSP_ROOM_INFO_HEX = (
    "23d100646f6f7961736863700103080000c0000f0001000c350002000700300005007230313030"
    "36000c00e585ace585b1e58cbae59f9f3700000030000500723032303036000600e7a9bae8b083"
    "370001003130000500723033303036000600e696b0e9a38e370001003130000500723034303036"
    "000600e59cb0e69a96370001003130000500723035303036000600e4b8bbe58da7370001003130"
    "000500723036303036000900e5aea2e9a490e58e85370001003130000500723037303036000600"
    "e5a487e794a83700010031940001000123"
)
EXPECTED_RSP_JSON = {
    "action": "query_room_info",
    "proto_type": 3,
    "link_code": 8,
    "serial_num": 0,
    "datareq_type": 12,
    "room_count": 7,
    "request_data_over": 1,
    "rooms": [
        {"id": "r0100", "name": "公共区域", "image": 0},
        {"id": "r0200", "name": "空调", "image": 49},
        {"id": "r0300", "name": "新风", "image": 49},
        {"id": "r0400", "name": "地暖", "image": 49},
        {"id": "r0500", "name": "主卧", "image": 49},
        {"id": "r0600", "name": "客餐厅", "image": 49},
        {"id": "r0700", "name": "备用", "image": 49},
    ],
}


def _request_json_to_hex(payload: dict) -> str:
    packet = build_protocol_packet(
        msgFlag=0x23,
        protoName="dooyashcp",
        protoNum=1,
        protoType=payload["proto_type"],
        linkCode=payload["link_code"],
        serialNum=payload.get("serial_num", 0),
        fields=[{"type": 15, "value": payload["datareq_type"]}],
    )
    return packet.hex()


def _request_hex_to_json(packet_hex: str) -> dict:
    packet = parse_protocol_packet(bytes.fromhex(packet_hex))
    datareq_type = next((f.value for f in packet.fields if f.id == 15), None)
    return {
        "action": "query_room_info",
        "proto_type": packet.proto_type,
        "link_code": packet.link_code,
        "serial_num": packet.serial_num,
        "datareq_type": datareq_type,
    }


def _response_hex_to_json(packet_hex: str) -> dict:
    packet = parse_protocol_packet(bytes.fromhex(packet_hex))

    datareq_type = next((f.value for f in packet.fields if f.id == 15), None)
    room_count = next((f.value for f in packet.fields if f.id == 53), None)
    request_data_over = next((f.value for f in packet.fields if f.id == 148), None)

    data = {}
    routed = route(packet, data)
    assert routed == "rooms"

    rooms = [
        {"id": room.id, "name": room.name, "image": room.image}
        for room in data.get("rooms", [])
    ]

    return {
        "action": "query_room_info",
        "proto_type": packet.proto_type,
        "link_code": packet.link_code,
        "serial_num": packet.serial_num,
        "datareq_type": datareq_type,
        "room_count": room_count,
        "request_data_over": request_data_over,
        "rooms": rooms,
    }


def test_query_room_info_request_encode_decode_and_command_default_serial():
    # JSON -> HEX（与抓包原样一致）
    req_hex = _request_json_to_hex(EXPECTED_REQ_JSON)
    assert req_hex == REQ_ROOM_INFO_HEX

    # 对比现有 commands 默认 serial=0 的固定构包
    assert query_room_info().hex() == "231600646f6f796173686370010307000005000f0001000b23"

    # HEX -> JSON（抓包样本）
    req_json_back = _request_hex_to_json(REQ_ROOM_INFO_HEX)
    assert req_json_back == EXPECTED_REQ_JSON


def test_query_room_info_response_decode_matches_expected_json():
    rsp_json = _response_hex_to_json(RSP_ROOM_INFO_HEX)
    assert rsp_json == EXPECTED_RSP_JSON
