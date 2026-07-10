"""Protocol test assets extracted from corresponding test module."""

from __future__ import annotations

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
