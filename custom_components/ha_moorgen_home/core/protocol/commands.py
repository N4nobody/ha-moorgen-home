from .codec import build_protocol_packet


def query_room_info():
    return build_protocol_packet(
        msgFlag=0x23,
        protoName="dooyashcp",
        protoNum=1,
        protoType=3,
        linkCode=7,
        serialNum=0,
        fields=[{"type": 15, "value": 11}],
    )


def query_user_info():
    return build_protocol_packet(
        msgFlag=0x23,
        protoName="dooyashcp",
        protoNum=1,
        protoType=3,
        linkCode=7,
        serialNum=0,
        fields=[{"type": 15, "value": 9}],
    )


def query_device_details():
    return build_protocol_packet(
        msgFlag=0x23,
        protoName="dooyashcp",
        protoNum=1,
        protoType=3,
        linkCode=7,
        serialNum=0,
        fields=[{"type": 15, "value": 1}],
    )


def query_scene_details():
    return build_protocol_packet(
        msgFlag=0x23,
        protoName="dooyashcp",
        protoNum=1,
        protoType=3,
        linkCode=7,
        serialNum=0,
        fields=[{"type": 15, "value": 17}],
    )


def activate_scene(scene_name):
    return build_protocol_packet(
        msgFlag=0x23,
        protoName="dooyashcp",
        protoNum=1,
        protoType=4,
        linkCode=9,
        serialNum=0,
        fields=[{"type": 16, "value": 5}, {"type": 2, "value": scene_name}],
    )


def control_device(device_mac: int, device_cmd: str):
    cmd_numeric = int.from_bytes(device_cmd.encode("utf-8"), "little")
    return build_protocol_packet(
        msgFlag=0x23,
        protoName="dooyashcp",
        protoNum=1,
        protoType=4,
        linkCode=9,
        serialNum=0,
        fields=[
            {"type": 16, "value": 1},
            {"type": 4, "value": device_mac},
            {"type": 9, "value": cmd_numeric},
        ],
    )
