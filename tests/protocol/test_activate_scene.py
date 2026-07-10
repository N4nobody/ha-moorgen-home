"""Spec: docs/protocol/activate_scene.md"""

from __future__ import annotations

from custom_components.ha_moorgen_home.core.protocol.codec import (
    build_protocol_packet,
    parse_protocol_packet,
)
from custom_components.ha_moorgen_home.core.protocol.commands import activate_scene

# 抓包样本请求（执行场景：餐厅开灯/关灯）
REQ_SCENE_ON_HEX = "231e00646f6f79617368637001040978000d001000010005020004003064303023"
REQ_SCENE_OFF_HEX = "231e00646f6f7961736863700104097a000d001000010005020004003065303023"

EXPECTED_REQ_ON_JSON = {
    "action": "activate_scene",
    "proto_type": 4,
    "link_code": 9,
    "serial_num": 120,
    "operate_type": 5,
    "scene_id": "0d00",
}
EXPECTED_REQ_OFF_JSON = {
    "action": "activate_scene",
    "proto_type": 4,
    "link_code": 9,
    "serial_num": 122,
    "operate_type": 5,
    "scene_id": "0e00",
}


# 抓包样本推送（执行后设备状态变化）
PUSH_SCENE_ON_HEX = (
    "237e00646f6f79617368637001050c00006d001b000100031100010001040008000100ffffffff"
    "04ff600001000198000100489c00010000720001000086000100015f00010004a7000100050102"
    "01000205001000646f6f796172303630306c313130103006000c00e9a490e58e85e4b8bbe781af"
    "0b000100010a000200ffff23"
)
PUSH_SCENE_OFF_HEX = (
    "237e00646f6f79617368637001050c00006d001b000100031100010001040008000100ffffffff"
    "04ff600001000198000100489c00010000720001000086000100015f00010004a7000100050102"
    "01000205001000646f6f796172303630306c313130103006000c00e9a490e58e85e4b8bbe781af"
    "0b000100000a000200ffff23"
)



def _request_json_to_hex(payload: dict) -> str:
    packet = build_protocol_packet(
        msgFlag=0x23,
        protoName="dooyashcp",
        protoNum=1,
        protoType=payload["proto_type"],
        linkCode=payload["link_code"],
        serialNum=payload.get("serial_num", 0),
        fields=[
            {"type": 16, "value": payload["operate_type"]},
            {"type": 2, "value": payload["scene_id"]},
        ],
    )
    return packet.hex()



def _request_hex_to_json(packet_hex: str) -> dict:
    packet = parse_protocol_packet(bytes.fromhex(packet_hex))
    operate_type = next((f.value for f in packet.fields if f.id == 16), None)
    scene_id = next((f.value for f in packet.fields if f.id == 2), None)
    return {
        "action": "activate_scene",
        "proto_type": packet.proto_type,
        "link_code": packet.link_code,
        "serial_num": packet.serial_num,
        "operate_type": operate_type,
        "scene_id": scene_id,
    }



def _push_hex_to_json(packet_hex: str) -> dict:
    packet = parse_protocol_packet(bytes.fromhex(packet_hex))

    field_map = {f.id: f.value for f in packet.fields}

    return {
        "action": "scene_effect_push",
        "proto_type": packet.proto_type,
        "link_code": packet.link_code,
        "serial_num": packet.serial_num,
        "update_proc": field_map.get(27),
        "device_count": field_map.get(17),
        "device_mac": field_map.get(4),
        "device_name": field_map.get(6),
        "device_state": field_map.get(11),
    }



def test_activate_scene_request_encode_decode_and_command_default_serial():
    # JSON -> HEX（与抓包原样一致）
    req_on_hex = _request_json_to_hex(EXPECTED_REQ_ON_JSON)
    req_off_hex = _request_json_to_hex(EXPECTED_REQ_OFF_JSON)
    assert req_on_hex == REQ_SCENE_ON_HEX
    assert req_off_hex == REQ_SCENE_OFF_HEX

    # 对比现有 commands 默认 serial=0 的固定构包
    assert activate_scene("0d00").hex() == "231e00646f6f79617368637001040900000d001000010005020004003064303023"

    # HEX -> JSON（抓包样本）
    req_on_json_back = _request_hex_to_json(REQ_SCENE_ON_HEX)
    req_off_json_back = _request_hex_to_json(REQ_SCENE_OFF_HEX)
    assert req_on_json_back == EXPECTED_REQ_ON_JSON
    assert req_off_json_back == EXPECTED_REQ_OFF_JSON



def test_activate_scene_push_decode_matches_expected_json():
    on_push_json = _push_hex_to_json(PUSH_SCENE_ON_HEX)
    off_push_json = _push_hex_to_json(PUSH_SCENE_OFF_HEX)

    assert on_push_json == {
        "action": "scene_effect_push",
        "proto_type": 5,
        "link_code": 12,
        "serial_num": 0,
        "update_proc": 3,
        "device_count": 1,
        "device_mac": 18376093854555111425,
        "device_name": "餐厅主灯",
        "device_state": 1,
    }
    assert off_push_json == {
        "action": "scene_effect_push",
        "proto_type": 5,
        "link_code": 12,
        "serial_num": 0,
        "update_proc": 3,
        "device_count": 1,
        "device_mac": 18376093854555111425,
        "device_name": "餐厅主灯",
        "device_state": 0,
    }
