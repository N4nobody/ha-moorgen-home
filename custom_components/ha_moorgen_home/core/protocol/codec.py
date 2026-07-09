import logging

from .models import DataField, DataPacket, RoomInfo, SceneInfo, get_type_by_id

_LOGGER = logging.getLogger(__name__)


def parse_protocol_packet(data) -> DataPacket:
    if len(data) < 19:
        raise ValueError("Packet is too short to parse")

    packet = DataPacket()

    packet.msg_flag = data[0]
    packet.length = data[1] + (data[2] << 8)
    packet.proto_name = data[3:12].decode()
    packet.proto_num = data[12]
    packet.proto_type = data[13]
    packet.link_code = data[14]
    packet.serial_num = data[15] + (data[16] << 8)
    packet.data_len = data[17] + (data[18] << 8)
    packet.fields = []

    datafield_offset = 19
    ptr = datafield_offset
    limit = datafield_offset + packet.data_len
    while ptr < limit and ptr + 4 <= len(data):
        dtype = data[ptr] + (data[ptr + 1] << 8)
        vlen = data[ptr + 2] + (data[ptr + 3] << 8)
        val = data[ptr + 4 : ptr + 4 + vlen]

        field = DataField()
        field.id = dtype

        tdesc = get_type_by_id(dtype)
        field.name = tdesc["name"] if tdesc else f"unknown_{dtype}"
        try:
            if tdesc and tdesc["type"] == "string":
                field.value = val.decode("utf-8")
            elif tdesc:
                field.value = int.from_bytes(val, "little")
            else:
                field.value = val
        except Exception:
            field.value = val

        packet.fields.append(field)
        ptr += 4 + vlen

    return packet


def build_protocol_packet(msgFlag, protoName, protoNum, protoType, linkCode, serialNum, fields):
    """
    Build a protocol packet from the given fields.

    Args:
        msgFlag (int): Message flag (1 byte)
        length (int): Length (2 byte)
        protoName (str): Protocol name (9 bytes)
        protoNum (int): Protocol number (1 byte)
        protoType (int): Protocol type (1 byte)
        linkCode (int): Link code (1 byte)
        serialNum (int): Serial number (2 bytes)
        dataLen (int): Data length (2 bytes)
        fields (list): List of field dictionaries, each containing:
            - 'type': Field ID (2 bytes)
            - 'value': Field value (variable length, converted based on type)
        msgFlag (int): Message flag (1 byte)
    Returns:
        bytes: The constructed protocol packet
    """
    # Convert protoName to bytes and ensure it's exactly 9 bytes
    protoName_bytes = protoName.encode("ascii")
    if len(protoName_bytes) != 9:
        raise ValueError("protoName must be exactly 9 ASCII characters")

    # Prepare the data fields
    data_fields = bytearray()
    for item in fields:
        # Get field type information
        tdesc = get_type_by_id(item["type"])
        if not tdesc:
            raise ValueError(f"Unknown field type ID: {item['type']}")

        # Convert value based on type
        value = item["value"]
        if tdesc["type"] == "string":
            if not isinstance(value, str):
                value = str(value)
            value_bytes = value.encode("utf-8")
        else:  # number type
            if isinstance(value, str):
                value = int(value)
            if not isinstance(value, int):
                raise ValueError(f"Field {tdesc['name']} expects a numeric value")
            # Determine minimum bytes needed to represent the number
            byte_count = (value.bit_length() + 7) // 8 or 1
            value_bytes = value.to_bytes(byte_count, "little")

        # Append field header (type + length) and value
        data_fields.extend(item["type"].to_bytes(2, "little"))
        data_fields.extend(len(value_bytes).to_bytes(2, "little"))
        data_fields.extend(value_bytes)

    # Calculate lengths
    dataLen = len(data_fields)
    total_length = 17 + dataLen  # 19 bytes for header + data fields

    # Build the packet
    packet = bytearray()
    packet.append(msgFlag)  # 1 byte
    packet.extend(total_length.to_bytes(2, "little"))  # 2 bytes
    packet.extend(protoName_bytes)  # 9 bytes
    packet.append(protoNum)  # 1 byte
    packet.append(protoType)  # 1 byte
    packet.append(linkCode)  # 1 byte
    packet.extend(serialNum.to_bytes(2, "little"))  # 2 bytes
    packet.extend(dataLen.to_bytes(2, "little"))  # 2 bytes
    packet.extend(data_fields)  # variable length
    packet.append(0x23)
    return bytes(packet)


def route(packet: DataPacket, data_dict: dict):
    _LOGGER.info(f"packet come {packet.proto_num} {packet.proto_type} {packet.link_code}")

    if packet.proto_num == 1 and packet.proto_type == 3 and packet.link_code == 8:
        datareq_field = next((f for f in packet.fields if f.id == 15), None)
        if datareq_field is not None:
            datareq_type = datareq_field.value
            if datareq_type == 12:
                _LOGGER.info("room info come")
                data_dict["rooms"] = parse_room_info(packet)
                return "rooms"
            if datareq_type == 4:
                _LOGGER.info("device info come")
                data_dict["devices"] = parse_device_info(packet)
                return "devices"
            if datareq_type == 18:
                _LOGGER.info("scene info come")
                data_dict["scenes"] = parse_scene_info(packet)
                return "scenes"

    return None


def parse_room_info(packet: DataPacket) -> list[RoomInfo]:
    result = []

    i = 2
    while i + 2 < len(packet.fields):
        room = RoomInfo()
        room.id = packet.fields[i].value
        room.name = packet.fields[i + 1].value
        room.image = packet.fields[i + 2].value
        i += 3
        result.append(room)
    return result


def _normalize_desc_text(value) -> str:
    if isinstance(value, (bytes, bytearray)):
        try:
            return value.decode("utf-8", errors="ignore")
        except Exception:
            return ""
    if isinstance(value, str):
        return value
    return ""


def infer_device_type(device: dict) -> str:
    """Infer high-level device type from parsed fields.

    NOTE: current DATA_RSP_DEVICE sample does not always carry explicit Device_Type(8),
    so this inference relies on Device_Desc pattern and name fallback.
    """

    desc = _normalize_desc_text(device.get("Device_Desc", ""))
    name = str(device.get("Device_Name", ""))

    if "r153" in desc:
        return "panel"
    if "l110" in desc:
        return "light"
    if "h110" in desc:
        return "floor_heating"
    if "a160" in desc:
        return "fresh_air"
    if "a170" in desc:
        return "air_conditioner"
    if "a110" in desc:
        return "hvac_group"

    return "unknown"


def parse_device_info(packet: DataPacket):
    devices = []
    current = {}
    for item in packet.fields:
        if item.id in (15, 17, 148):
            continue
        if item.id == 4 and current:
            devices.append(current)
            current = {}
        t = get_type_by_id(item.id)
        key = t["name"] if t else (item.name or f"unknown_{item.id}")
        current[key] = item.value
    if current:
        devices.append(current)

    _LOGGER.info(devices)
    return devices


def parse_scene_info(packet: DataPacket) -> list[SceneInfo]:
    scenes = []
    current = {}
    for item in packet.fields:
        if item.id in (15, 18, 148):
            continue
        if item.id == 2 and current:
            scenes.append(current)
            current = {}
        t = get_type_by_id(item.id)
        key = t["name"] if t else (item.name or f"unknown_{item.id}")
        current[key] = item.value
    if current:
        scenes.append(current)

    result = []
    for scene in scenes:
        info = SceneInfo()
        info.id = scene["ENCRYPT_TYPE_RSA"]
        info.name = scene["ENCRYPT_TYPE_AES"]
        info.image = scene["Scene_Icon"]
        result.append(info)

    _LOGGER.info(result)
    return result
