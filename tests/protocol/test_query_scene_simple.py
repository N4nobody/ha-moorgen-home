"""Spec: docs/protocol/query_scene_simple.md"""

from __future__ import annotations

from custom_components.ha_moorgen_home.core.protocol.codec import (
    build_protocol_packet,
    parse_protocol_packet,
    route,
)
from custom_components.ha_moorgen_home.core.protocol.commands import query_scene_details

# 抓包样本请求（query scene simple info）
REQ_SCENE_SIMPLE_HEX = "231600646f6f7961736863700103070e0005000f0001001123"
EXPECTED_REQ_JSON = {
    "action": "query_scene_simple",
    "proto_type": 3,
    "link_code": 7,
    "serial_num": 14,
    "datareq_type": 17,
}

# 抓包样本响应（scene simple info response）
RSP_SCENE_SIMPLE_HEX = (
    "231a02646f6f796173686370010308000009020f00010012120002000e000200040030313030"
    "01000c00e59b9ee5aeb6e6a8a1e5bc8f5e00010031110002000200020004003032303001000c00"
    "e7a6bbe5aeb6e6a8a1e5bc8f5e00010031110002000c00020004003033303001000c00e4bc9ae5"
    "aea2e6a8a1e5bc8f5e00010031110002000500020004003034303001000c00e4bc91e997b2e6a8"
    "a1e5bc8f5e00010031110002000500020004003035303001000c00e5b0b1e9a490e6a8a1e5bc8f"
    "5e00010031110002000400020004003036303001000c00e4b8bbe58da7e585a8e5bc805e000100"
    "31110002000700020004003037303001000c00e4b8bbe58da7e585a8e585b35e00010031110002"
    "000700020004003038303001000f00e4b8bbe58da7e4bc91e997b2e58fb35e0001003111000200"
    "0700020004003062303001000f00e4b8bbe58da7e4bc91e997b2e5b7a65e000100311100020007"
    "00020004003063303001000c00e99885e8afbbe6a8a1e5bc8f5e00010037110002000600300005"
    "007230353030020004003039303001000c00e5aea2e58e85e5bc80e781af5e0001003711000200"
    "0100020004003061303001000c00e5aea2e58e85e585b3e781af5e000100371100020003000200"
    "04003064303001000c00e9a490e58e85e5bc80e781af5e00010037110002000100020004003065"
    "303001000c00e9a490e58e85e585b3e781af5e00010037110002000100940001000123"
)
EXPECTED_RSP_JSON = {
    "action": "query_scene_simple",
    "proto_type": 3,
    "link_code": 8,
    "serial_num": 0,
    "datareq_type": 18,
    "scene_count": 14,
    "request_data_over": 1,
    "scenes": [
        {"id": "0100", "name": "回家模式", "icon": 49},
        {"id": "0200", "name": "离家模式", "icon": 49},
        {"id": "0300", "name": "会客模式", "icon": 49},
        {"id": "0400", "name": "休闲模式", "icon": 49},
        {"id": "0500", "name": "就餐模式", "icon": 49},
        {"id": "0600", "name": "主卧全开", "icon": 49},
        {"id": "0700", "name": "主卧全关", "icon": 49},
        {"id": "0800", "name": "主卧休闲右", "icon": 49},
        {"id": "0b00", "name": "主卧休闲左", "icon": 49},
        {"id": "0c00", "name": "阅读模式", "icon": 55},
        {"id": "0900", "name": "客厅开灯", "icon": 55},
        {"id": "0a00", "name": "客厅关灯", "icon": 55},
        {"id": "0d00", "name": "餐厅开灯", "icon": 55},
        {"id": "0e00", "name": "餐厅关灯", "icon": 55},
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
        "action": "query_scene_simple",
        "proto_type": packet.proto_type,
        "link_code": packet.link_code,
        "serial_num": packet.serial_num,
        "datareq_type": datareq_type,
    }


def _response_hex_to_json(packet_hex: str) -> dict:
    packet = parse_protocol_packet(bytes.fromhex(packet_hex))

    datareq_type = next((f.value for f in packet.fields if f.id == 15), None)
    request_data_over = next((f.value for f in packet.fields if f.id == 148), None)
    scene_count = next((f.value for f in packet.fields if f.id == 18), None)

    data = {}
    routed = route(packet, data)
    assert routed == "scenes"

    scenes = [
        {"id": scene.id, "name": scene.name, "icon": scene.image}
        for scene in data.get("scenes", [])
    ]

    return {
        "action": "query_scene_simple",
        "proto_type": packet.proto_type,
        "link_code": packet.link_code,
        "serial_num": packet.serial_num,
        "datareq_type": datareq_type,
        "scene_count": scene_count,
        "request_data_over": request_data_over,
        "scenes": scenes,
    }


def test_request_json_to_hex_uses_capture_raw_sample():
    # JSON -> HEX（与抓包原样一致）
    req_hex = _request_json_to_hex(EXPECTED_REQ_JSON)
    assert req_hex == REQ_SCENE_SIMPLE_HEX

    # 对比现有 commands 默认 serial=0 的固定构包
    assert query_scene_details().hex() == "231600646f6f796173686370010307000005000f0001001123"

    # HEX -> JSON（抓包样本）
    req_json_back = _request_hex_to_json(REQ_SCENE_SIMPLE_HEX)
    assert req_json_back == EXPECTED_REQ_JSON


def test_response_capture_hex_to_business_json():
    rsp_json = _response_hex_to_json(RSP_SCENE_SIMPLE_HEX)
    assert rsp_json == EXPECTED_RSP_JSON
