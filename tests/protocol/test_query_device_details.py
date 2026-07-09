"""Spec: docs/protocol/query_device_details.md"""

from __future__ import annotations

from custom_components.ha_moorgen_home.core.protocol.codec import (
    build_protocol_packet,
    parse_protocol_packet,
    route,
)
from custom_components.ha_moorgen_home.core.protocol.commands import query_device_details

# 抓包样本请求（query device details）
REQ_DEVICE_HEX = "231600646f6f7961736863700103070c0005000f0001000123"
EXPECTED_REQ_JSON = {
    "action": "query_device_details",
    "proto_type": 3,
    "link_code": 7,
    "serial_num": 12,
    "datareq_type": 1,
}

# 抓包样本响应（device details response）
RSP_DEVICE_HEX = (
    "237815646f6f796173686370010308000067150f00010004110002002f0004000800f000ffffffff00ff600001000198"
    "000100009c00010000720001000086000100015f0001000001020100023100020010f130000500723035303006000c00"
    "e5ba8ae5a4b4e5b084e781af040008000200ffffffff00ff600001000198000100489c00010000720001000086000100"
    "015f00010000a700010005010201000205001000646f6f796172303530306c313130103006000c00e58fb3e99885e8af"
    "bbe781af0b000100000a000200ffff040008000200ffffffff01ff600001000198000100489c00010000720001000086"
    "000100015f00010001a700010005010201000205001000646f6f796172303530306c313130103006000600e781afe5b8"
    "a60b000100000a000200ffff040008000200ffffffff02ff600001000198000100489c00010000720001000086000100"
    "015f00010002a700010005010201000205001000646f6f796172303530306c313130103006000c00e9a398e7aa97e5b0"
    "84e781af0b000100000a000200ffff040008000200ffffffff03ff600001000198000100489c00010000720001000086"
    "000100015f00010003a700010005010201000205001000646f6f796172303530306c313130103006000c00e5b7a6e998"
    "85e8afbbe781af0b000100000a000200ffff040008000200ffffffff04ff600001000198000100489c00010000720001"
    "000086000100015f00010004a700010005010201000205001000646f6f796172303730306c313130103006000300322d"
    "340b000100000a000200ffff040008000200ffffffff05ff600001000198000100489c00010000720001000086000100"
    "015f00010005a700010005010201000205001000646f6f796172303730306c313130103006000300322d350b00010000"
    "0a000200ffff040008000200ffffffff06ff600001000198000100489c00010000720001000086000100015f00010006"
    "a700010005010201000205001000646f6f796172303730306c313130103006000400322d36300b000100000a000200ff"
    "ff040008000200ffffffff07ff600001000198000100489c00010000720001000086000100015f00010007a700010005"
    "010201000205001000646f6f796172303630306c313130103006000c00e4b880e994aee696ade794b50b000100010a00"
    "0200ffff040008000100ffffffff00ff600001000198000100489c00010000720001000086000100015f00010000a700"
    "010005010201000205001000646f6f796172303630306c313130103006000c00e78e84e585b3e781afe5b8a60b000100"
    "000a000200ffff040008000100ffffffff01ff600001000198000100489c00010000720001000086000100015f000100"
    "01a700010005010201000205001000646f6f796172303630306c313130103006000c00e5a4a9e88ab1e781afe5b8a60b"
    "000100000a000200ffff040008000100ffffffff02ff600001000198000100489c00010000720001000086000100015f"
    "00010002a700010005010201000205001000646f6f796172303630306c313130103006000c00e5aea2e9a490e5b084e7"
    "81af0b000100000a000200ffff040008000100ffffffff03ff600001000198000100489c000100007200010000860001"
    "00015f00010003a700010005010201000205001000646f6f796172303630306c313130103006000c00e5aea2e58e85e4"
    "b8bbe781af0b000100010a000200ffff040008000100ffffffff04ff600001000198000100489c000100007200010000"
    "86000100015f00010004a700010005010201000205001000646f6f796172303630306c313130103006000c00e9a490e5"
    "8e85e4b8bbe781af0b000100010a000200ffff040008000100ffffffff05ff600001000198000100489c000100007200"
    "01000086000100015f00010005a700010005010201000205001000646f6f796172303530306c313130103006000c00e8"
    "bf87e98193e5b084e781af0b000100000a000200ffff040008000100ffffffff06ff600001000198000100489c000100"
    "00720001000086000100015f00010006a700010005010201000205001000646f6f796172303530306c31313010300600"
    "0600e4b8bbe781af0b000100000a000200ffff040008000100ffffffff07ff600001000198000100489c000100007200"
    "01000086000100015f00010007a700010005010201000205001000646f6f796172303530306c313130103006000c00e8"
    "838ce699afe5b084e781af0b000100000a000200ffff040008001100ffffffff00ff600001000198000100409c000100"
    "00720001000086000100085f00010000a700010002010201000205001000646f6f796172303130307231353380300600"
    "0c00e78e84e585b3e99da2e69dbf0b000100010a009000010504303130300500030201000002010100ffffffff04ff11"
    "6c696768742d726576657273652d6578650003010100ffffffff00ff116c696768742d726576657273652d6578650007"
    "010100ffffffff01ff116c696768742d726576657273652d6578650006010100ffffffff03ff116c696768742d726576"
    "657273652d6578650005050430323030050003020100009700020040ff040008001200ffffffff00ff60000100019800"
    "0100409c00010000720001000086000100085f00010000a700010002010201000205001000646f6f7961723031303072"
    "313533803006000c00e5aea2e58e85e99da2e69dbf0b000100010a00bb00010504303330300500030201000002050430"
    "3530300500030201000003010100ffffffff04ff116c696768742d726576657273652d65786500050504303430300500"
    "030201000006010100ffffffff01ff116c696768742d726576657273652d6578650007010100ffffffff03ff116c6967"
    "68742d726576657273652d6578650008010100ffffffff02ff116c696768742d726576657273652d6578650004010100"
    "ffffffff00ff116c696768742d726576657273652d657865009700020064ff040008001300ffffffff00ff6000010001"
    "98000100409c00010000720001000086000100085f00010000a700010002010201000205001000646f6f796172303130"
    "3072313533803006001200e4b8bbe58da7e8bf9be997a8e99da2e69dbf0b000100000a00900001050430363030050003"
    "0201000003010100ffffffff06ff116c696768742d726576657273652d6578650004010100ffffffff05ff116c696768"
    "742d726576657273652d65786500050504303730300500030201000007010200ffffffff01ff116c696768742d726576"
    "657273652d6578650008010100ffffffff07ff116c696768742d726576657273652d657865009700020000ff04000800"
    "1400ffffffff00ff600001000198000100409c00010000720001000086000100085f00010000a7000100020102010002"
    "05001000646f6f7961723031303072313533803006000f00e4b8bbe58da7e5ba8ae5a4b4e5b7a60b000100000a007200"
    "010504303630300500030201000003010100ffffffff06ff116c696768742d726576657273652d657865000505043037"
    "30300500030201000007010200ffffffff01ff116c696768742d726576657273652d6578650002050430633030050003"
    "0201000006050430623030050003020100009700020000ff040008001500ffffffff00ff600001000198000100409c00"
    "010000720001000086000100085f00010000a700010002010201000205001000646f6f79617230313030723135338030"
    "06000f00e4b8bbe58da7e5ba8ae5a4b4e58fb30b000100000a009c000105043037303005000302010000020504303830"
    "30050003020100000301f000ffffffff00ff01550004010200ffffffff02ff116c696768742d726576657273652d6578"
    "65000505043036303005000302010000060504306330300500030201000007010100ffffffff07ff116c696768742d72"
    "6576657273652d6578650008010100ffffffff05ff116c696768742d726576657273652d657865009700020000ff0400"
    "08002100ffffffff00ff6000010001980001006f9c00010000720001000086000100015f000100000102010002050010"
    "00646f6f7961723034303068313130103006000c00e5aea2e58e85e59cb0e69a960b000100000a00040000241d010400"
    "08002100ffffffff01ff6000010001980001006f9c00010000720001000086000100015f000100010102010002050010"
    "00646f6f7961723033303061313630103006000c00e5aea2e58e85e696b0e9a38e0b000100000a000a0030ffffffff1d"
    "01ffff00040008002100ffffffff02ff6000010001980001006f9c00010000720001000086000100015f000100020102"
    "01000205001000646f6f7961723032303061313730103006000c00e5aea2e58e85e7a9bae8b0830b000100000a000a00"
    "28361d01010111ffff00040008002200ffffffff00ff6000010001980001006f9c00010000720001000086000100015f"
    "00010000010201000205001000646f6f7961723034303068313130103006000c00e9a490e58e85e59cb0e69a960b0001"
    "00000a000400003c1801040008002200ffffffff01ff6000010001980001006f9c00010000720001000086000100015f"
    "00010001010201000205001000646f6f7961723033303061313630103006000c00e9a490e58e85e696b0e9a38e0b0001"
    "00000a000a0030ffffffff1801ffff00040008002200ffffffff02ff6000010001980001006f9c000100007200010000"
    "86000100015f00010002010201000205001000646f6f7961723032303061313730103006000c00e9a490e58e85e7a9ba"
    "e8b0830b000100000a000a0028361801010111ffff00040008002300ffffffff00ff6000010001980001006f9c000100"
    "00720001000086000100015f00010000010201000205001000646f6f7961723034303068313130103006000c00e4b8bb"
    "e58da7e59cb0e69a960b000100000a000400002a0e01040008002300ffffffff01ff6000010001980001006f9c000100"
    "00720001000086000100015f00010001010201000205001000646f6f7961723033303061313630103006000c00e4b8bb"
    "e58da7e696b0e9a38e0b000100000a000a0030ffffffff0e01ffff00040008002300ffffffff02ff6000010001980001"
    "006f9c00010000720001000086000100015f00010002010201000205001000646f6f7961723032303061313730103006"
    "000c00e4b8bbe58da7e7a9bae8b0830b000100000a000a0028380e01010111ffff00040008002400ffffffff00ff6000"
    "010001980001006f9c00010000720001000086000100015f00010000010201000205001000646f6f7961723034303068"
    "313130103006001000e58c97e6aca1e58da731e59cb0e69a960b000100000a000400003c1301040008002400ffffffff"
    "01ff6000010001980001006f9c00010000720001000086000100015f00010001010201000205001000646f6f79617230"
    "33303061313630103006001000e58c97e6aca1e58da731e696b0e9a38e0b000100000a000a0010ffffffff1301ffff00"
    "040008002400ffffffff02ff6000010001980001006f9c00010000720001000086000100015f00010002010201000205"
    "001000646f6f7961723032303061313730103006001000e58c97e6aca1e58da731e7a9bae8b0830b000100000a000a00"
    "38361301010311ffff00040008002500ffffffff00ff6000010001980001006f9c00010000720001000086000100015f"
    "00010000010201000205001000646f6f7961723034303068313130103006001000e58c97e6aca1e58da732e59cb0e69a"
    "960b000100000a000400003c0901040008002500ffffffff01ff6000010001980001006f9c0001000072000100008600"
    "0100015f00010001010201000205001000646f6f7961723033303061313630103006001000e58c97e6aca1e58da732e6"
    "96b0e9a38e0b000100000a000a0000ffffffff0901ffff00040008002500ffffffff02ff6000010001980001006f9c00"
    "010000720001000086000100015f00010002010201000205001000646f6f7961723032303061313730103006001000e5"
    "8c97e6aca1e58da732e7a9bae8b0830b000100000a000a0038370901010311ffff00040008002600ffffffff00ff6000"
    "010001980001006f9c00010000720001000086000100015f00010000010201000205001000646f6f7961723034303068"
    "313130103006000f00e58d97e6aca1e58da7e59cb0e69a960b000100000a000400003c1301040008002600ffffffff01"
    "ff6000010001980001006f9c00010000720001000086000100015f00010001010201000205001000646f6f7961723033"
    "303061313630103006000f00e58d97e6aca1e58da7e696b0e9a38e0b000100000a000a0010ffffffff1301ffff000400"
    "08002600ffffffff02ff6000010001980001006f9c00010000720001000086000100015f000100020102010002050010"
    "00646f6f7961723032303061313730103006000f00e58d97e6aca1e58da7e7a9bae8b0830b000100000a000a00283613"
    "01010111ffff00040008000300ffffffff01ff600001000198000100009c00010000720001000086000100015f000100"
    "010102010002750008000300ffffffff00ff05001000646f6f7961723033303061313630103006000800e696b0e9a38e"
    "2d310b000100000a00070030000000000000040008000400ffffffff00ff600001000198000100009c00010000720001"
    "000086000100015f000100000102010002750008000400ffffffff00ff05001000646f6f796172303230306131313010"
    "3006000a00e5aea2e9a490e58e85310b000100000a000400011b0100040008000400ffffffff01ff6000010001980001"
    "00009c00010000720001000086000100015f000100010102010002750008000400ffffffff00ff05001000646f6f7961"
    "723032303061313130103006000a00e58c97e6aca1e58da7320b000100000a000400011b0300040008000400ffffffff"
    "02ff600001000198000100009c00010000720001000086000100015f000100020102010002750008000400ffffffff00"
    "ff05001000646f6f7961723032303061313130103006000a00e5aea2e9a490e58e85320b000100000a000400011b0100"
    "040008000400ffffffff03ff600001000198000100009c00010000720001000086000100015f00010003010201000275"
    "0008000400ffffffff00ff05001000646f6f7961723032303061313130103006000600e4b8bbe58da70b000100000a00"
    "0400011c0100040008000400ffffffff04ff600001000198000100009c00010000720001000086000100015f00010004"
    "0102010002750008000400ffffffff00ff05001000646f6f7961723032303061313130103006000600e4b9a6e688bf0b"
    "000100000a000400011b0300040008000400ffffffff05ff600001000198000100009c00010000720001000086000100"
    "015f000100050102010002750008000400ffffffff00ff05001000646f6f7961723032303061313130103006000900e5"
    "8d97e6aca1e58da70b000100000a000400011b0100940001000123"
)

EXPECTED_RSP_JSON = {
    "action": "query_device_details",
    "proto_type": 3,
    "link_code": 8,
    "serial_num": 0,
    "datareq_type": 4,
    "device_count": 47,
    "request_data_over": 1,
    "devices": [{'Device_Mac': 18374967954648269040,
  'Device_is_online': 1,
  'DEVICE_VERSION': 0,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 0,
  'ENTITY_HIDDEN': 2,
  'DeviceFunc': 61712,
  'RoomDesc': 'r0500',
  'Device_Name': '床头射灯'},
 {'Device_Mac': 18374967954648268802,
  'Device_is_online': 1,
  'DEVICE_VERSION': 72,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 0,
  'Device_Icon': 5,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0500l110\x100',
  'Device_Name': '右阅读灯',
  'Device_State': 0,
  'Device_CmdData': b'\xff\xff'},
 {'Device_Mac': 18375249429624979458,
  'Device_is_online': 1,
  'DEVICE_VERSION': 72,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 1,
  'Device_Icon': 5,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0500l110\x100',
  'Device_Name': '灯带',
  'Device_State': 0,
  'Device_CmdData': b'\xff\xff'},
 {'Device_Mac': 18375530904601690114,
  'Device_is_online': 1,
  'DEVICE_VERSION': 72,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 2,
  'Device_Icon': 5,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0500l110\x100',
  'Device_Name': '飘窗射灯',
  'Device_State': 0,
  'Device_CmdData': b'\xff\xff'},
 {'Device_Mac': 18375812379578400770,
  'Device_is_online': 1,
  'DEVICE_VERSION': 72,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 3,
  'Device_Icon': 5,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0500l110\x100',
  'Device_Name': '左阅读灯',
  'Device_State': 0,
  'Device_CmdData': b'\xff\xff'},
 {'Device_Mac': 18376093854555111426,
  'Device_is_online': 1,
  'DEVICE_VERSION': 72,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 4,
  'Device_Icon': 5,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0700l110\x100',
  'Device_Name': '2-4',
  'Device_State': 0,
  'Device_CmdData': b'\xff\xff'},
 {'Device_Mac': 18376375329531822082,
  'Device_is_online': 1,
  'DEVICE_VERSION': 72,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 5,
  'Device_Icon': 5,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0700l110\x100',
  'Device_Name': '2-5',
  'Device_State': 0,
  'Device_CmdData': b'\xff\xff'},
 {'Device_Mac': 18376656804508532738,
  'Device_is_online': 1,
  'DEVICE_VERSION': 72,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 6,
  'Device_Icon': 5,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0700l110\x100',
  'Device_Name': '2-60',
  'Device_State': 0,
  'Device_CmdData': b'\xff\xff'},
 {'Device_Mac': 18376938279485243394,
  'Device_is_online': 1,
  'DEVICE_VERSION': 72,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 7,
  'Device_Icon': 5,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0600l110\x100',
  'Device_Name': '一键断电',
  'Device_State': 1,
  'Device_CmdData': b'\xff\xff'},
 {'Device_Mac': 18374967954648268801,
  'Device_is_online': 1,
  'DEVICE_VERSION': 72,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 0,
  'Device_Icon': 5,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0600l110\x100',
  'Device_Name': '玄关灯带',
  'Device_State': 0,
  'Device_CmdData': b'\xff\xff'},
 {'Device_Mac': 18375249429624979457,
  'Device_is_online': 1,
  'DEVICE_VERSION': 72,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 1,
  'Device_Icon': 5,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0600l110\x100',
  'Device_Name': '天花灯带',
  'Device_State': 0,
  'Device_CmdData': b'\xff\xff'},
 {'Device_Mac': 18375530904601690113,
  'Device_is_online': 1,
  'DEVICE_VERSION': 72,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 2,
  'Device_Icon': 5,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0600l110\x100',
  'Device_Name': '客餐射灯',
  'Device_State': 0,
  'Device_CmdData': b'\xff\xff'},
 {'Device_Mac': 18375812379578400769,
  'Device_is_online': 1,
  'DEVICE_VERSION': 72,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 3,
  'Device_Icon': 5,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0600l110\x100',
  'Device_Name': '客厅主灯',
  'Device_State': 1,
  'Device_CmdData': b'\xff\xff'},
 {'Device_Mac': 18376093854555111425,
  'Device_is_online': 1,
  'DEVICE_VERSION': 72,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 4,
  'Device_Icon': 5,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0600l110\x100',
  'Device_Name': '餐厅主灯',
  'Device_State': 1,
  'Device_CmdData': b'\xff\xff'},
 {'Device_Mac': 18376375329531822081,
  'Device_is_online': 1,
  'DEVICE_VERSION': 72,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 5,
  'Device_Icon': 5,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0500l110\x100',
  'Device_Name': '过道射灯',
  'Device_State': 0,
  'Device_CmdData': b'\xff\xff'},
 {'Device_Mac': 18376656804508532737,
  'Device_is_online': 1,
  'DEVICE_VERSION': 72,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 6,
  'Device_Icon': 5,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0500l110\x100',
  'Device_Name': '主灯',
  'Device_State': 0,
  'Device_CmdData': b'\xff\xff'},
 {'Device_Mac': 18376938279485243393,
  'Device_is_online': 1,
  'DEVICE_VERSION': 72,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 7,
  'Device_Icon': 5,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0500l110\x100',
  'Device_Name': '背景射灯',
  'Device_State': 0,
  'Device_CmdData': b'\xff\xff'},
 {'Device_Mac': 18374967954648268817,
  'Device_is_online': 1,
  'DEVICE_VERSION': 64,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 8,
  'Device_channel': 0,
  'Device_Icon': 2,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': b'dooyar0100r153\x800',
  'Device_Name': '玄关面板',
  'Device_State': 1,
  'Device_CmdData': b'\x01\x05\x040100\x05\x00\x03\x02\x01\x00\x00\x02\x01\x01\x00\xff\xff\xff\xff\x04\xff\x11light-reverse-exe\x00\x03'
                    b'\x01\x01\x00\xff\xff\xff\xff\x00\xff\x11light-reverse-exe\x00\x07\x01\x01\x00\xff\xff\xff\xff\x01\xff\x11light-rev'
                    b'erse-exe\x00\x06\x01\x01\x00\xff\xff\xff\xff\x03\xff\x11light-reverse-exe\x00\x05\x05\x040200\x05\x00\x03'
                    b'\x02\x01\x00\x00',
  'PANEL_STATE': 65344},
 {'Device_Mac': 18374967954648268818,
  'Device_is_online': 1,
  'DEVICE_VERSION': 64,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 8,
  'Device_channel': 0,
  'Device_Icon': 2,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': b'dooyar0100r153\x800',
  'Device_Name': '客厅面板',
  'Device_State': 1,
  'Device_CmdData': b'\x01\x05\x040300\x05\x00\x03\x02\x01\x00\x00\x02\x05\x040500\x05\x00\x03\x02\x01\x00\x00\x03\x01\x01\x00'
                    b'\xff\xff\xff\xff\x04\xff\x11light-reverse-exe\x00\x05\x05\x040400\x05\x00\x03\x02\x01\x00\x00\x06\x01\x01\x00\xff'
                    b'\xff\xff\xff\x01\xff\x11light-reverse-exe\x00\x07\x01\x01\x00\xff\xff\xff\xff\x03\xff\x11light-reverse-exe'
                    b'\x00\x08\x01\x01\x00\xff\xff\xff\xff\x02\xff\x11light-reverse-exe\x00\x04\x01\x01\x00\xff\xff\xff\xff\x00\xff\x11lig'
                    b'ht-reverse-exe\x00',
  'PANEL_STATE': 65380},
 {'Device_Mac': 18374967954648268819,
  'Device_is_online': 1,
  'DEVICE_VERSION': 64,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 8,
  'Device_channel': 0,
  'Device_Icon': 2,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': b'dooyar0100r153\x800',
  'Device_Name': '主卧进门面板',
  'Device_State': 0,
  'Device_CmdData': b'\x01\x05\x040600\x05\x00\x03\x02\x01\x00\x00\x03\x01\x01\x00\xff\xff\xff\xff\x06\xff\x11light-reverse-exe\x00\x04'
                    b'\x01\x01\x00\xff\xff\xff\xff\x05\xff\x11light-reverse-exe\x00\x05\x05\x040700\x05\x00\x03\x02\x01\x00\x00\x07\x01'
                    b'\x02\x00\xff\xff\xff\xff\x01\xff\x11light-reverse-exe\x00\x08\x01\x01\x00\xff\xff\xff\xff\x07\xff\x11light-reverse-'
                    b'exe\x00',
  'PANEL_STATE': 65280},
 {'Device_Mac': 18374967954648268820,
  'Device_is_online': 1,
  'DEVICE_VERSION': 64,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 8,
  'Device_channel': 0,
  'Device_Icon': 2,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': b'dooyar0100r153\x800',
  'Device_Name': '主卧床头左',
  'Device_State': 0,
  'Device_CmdData': b'\x01\x05\x040600\x05\x00\x03\x02\x01\x00\x00\x03\x01\x01\x00\xff\xff\xff\xff\x06\xff\x11light-reverse-exe\x00\x05'
                    b'\x05\x040700\x05\x00\x03\x02\x01\x00\x00\x07\x01\x02\x00\xff\xff\xff\xff\x01\xff\x11light-reverse-exe\x00\x02\x05'
                    b'\x040c00\x05\x00\x03\x02\x01\x00\x00\x06\x05\x040b00\x05\x00\x03\x02\x01\x00\x00',
  'PANEL_STATE': 65280},
 {'Device_Mac': 18374967954648268821,
  'Device_is_online': 1,
  'DEVICE_VERSION': 64,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 8,
  'Device_channel': 0,
  'Device_Icon': 2,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': b'dooyar0100r153\x800',
  'Device_Name': '主卧床头右',
  'Device_State': 0,
  'Device_CmdData': b'\x01\x05\x040700\x05\x00\x03\x02\x01\x00\x00\x02\x05\x040800\x05\x00\x03\x02\x01\x00\x00\x03\x01\xf0\x00'
                    b'\xff\xff\xff\xff\x00\xff\x01U\x00\x04\x01\x02\x00\xff\xff\xff\xff\x02\xff\x11light-reverse-exe\x00\x05\x05\x04060'
                    b'0\x05\x00\x03\x02\x01\x00\x00\x06\x05\x040c00\x05\x00\x03\x02\x01\x00\x00\x07\x01\x01\x00\xff\xff\xff\xff\x07\xff'
                    b'\x11light-reverse-exe\x00\x08\x01\x01\x00\xff\xff\xff\xff\x05\xff\x11light-reverse-exe\x00',
  'PANEL_STATE': 65280},
 {'Device_Mac': 18374967954648268833,
  'Device_is_online': 1,
  'DEVICE_VERSION': 111,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 0,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0400h110\x100',
  'Device_Name': '客厅地暖',
  'Device_State': 0,
  'Device_CmdData': '\x00$\x1d\x01'},
 {'Device_Mac': 18375249429624979489,
  'Device_is_online': 1,
  'DEVICE_VERSION': 111,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 1,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0300a160\x100',
  'Device_Name': '客厅新风',
  'Device_State': 0,
  'Device_CmdData': b'0\xff\xff\xff\xff\x1d\x01\xff\xff\x00'},
 {'Device_Mac': 18375530904601690145,
  'Device_is_online': 1,
  'DEVICE_VERSION': 111,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 2,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0200a170\x100',
  'Device_Name': '客厅空调',
  'Device_State': 0,
  'Device_CmdData': b'(6\x1d\x01\x01\x01\x11\xff\xff\x00'},
 {'Device_Mac': 18374967954648268834,
  'Device_is_online': 1,
  'DEVICE_VERSION': 111,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 0,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0400h110\x100',
  'Device_Name': '餐厅地暖',
  'Device_State': 0,
  'Device_CmdData': '\x00<\x18\x01'},
 {'Device_Mac': 18375249429624979490,
  'Device_is_online': 1,
  'DEVICE_VERSION': 111,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 1,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0300a160\x100',
  'Device_Name': '餐厅新风',
  'Device_State': 0,
  'Device_CmdData': b'0\xff\xff\xff\xff\x18\x01\xff\xff\x00'},
 {'Device_Mac': 18375530904601690146,
  'Device_is_online': 1,
  'DEVICE_VERSION': 111,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 2,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0200a170\x100',
  'Device_Name': '餐厅空调',
  'Device_State': 0,
  'Device_CmdData': b'(6\x18\x01\x01\x01\x11\xff\xff\x00'},
 {'Device_Mac': 18374967954648268835,
  'Device_is_online': 1,
  'DEVICE_VERSION': 111,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 0,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0400h110\x100',
  'Device_Name': '主卧地暖',
  'Device_State': 0,
  'Device_CmdData': '\x00*\x0e\x01'},
 {'Device_Mac': 18375249429624979491,
  'Device_is_online': 1,
  'DEVICE_VERSION': 111,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 1,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0300a160\x100',
  'Device_Name': '主卧新风',
  'Device_State': 0,
  'Device_CmdData': b'0\xff\xff\xff\xff\x0e\x01\xff\xff\x00'},
 {'Device_Mac': 18375530904601690147,
  'Device_is_online': 1,
  'DEVICE_VERSION': 111,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 2,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0200a170\x100',
  'Device_Name': '主卧空调',
  'Device_State': 0,
  'Device_CmdData': b'(8\x0e\x01\x01\x01\x11\xff\xff\x00'},
 {'Device_Mac': 18374967954648268836,
  'Device_is_online': 1,
  'DEVICE_VERSION': 111,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 0,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0400h110\x100',
  'Device_Name': '北次卧1地暖',
  'Device_State': 0,
  'Device_CmdData': '\x00<\x13\x01'},
 {'Device_Mac': 18375249429624979492,
  'Device_is_online': 1,
  'DEVICE_VERSION': 111,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 1,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0300a160\x100',
  'Device_Name': '北次卧1新风',
  'Device_State': 0,
  'Device_CmdData': b'\x10\xff\xff\xff\xff\x13\x01\xff\xff\x00'},
 {'Device_Mac': 18375530904601690148,
  'Device_is_online': 1,
  'DEVICE_VERSION': 111,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 2,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0200a170\x100',
  'Device_Name': '北次卧1空调',
  'Device_State': 0,
  'Device_CmdData': b'86\x13\x01\x01\x03\x11\xff\xff\x00'},
 {'Device_Mac': 18374967954648268837,
  'Device_is_online': 1,
  'DEVICE_VERSION': 111,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 0,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0400h110\x100',
  'Device_Name': '北次卧2地暖',
  'Device_State': 0,
  'Device_CmdData': '\x00<\t\x01'},
 {'Device_Mac': 18375249429624979493,
  'Device_is_online': 1,
  'DEVICE_VERSION': 111,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 1,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0300a160\x100',
  'Device_Name': '北次卧2新风',
  'Device_State': 0,
  'Device_CmdData': b'\x00\xff\xff\xff\xff\t\x01\xff\xff\x00'},
 {'Device_Mac': 18375530904601690149,
  'Device_is_online': 1,
  'DEVICE_VERSION': 111,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 2,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0200a170\x100',
  'Device_Name': '北次卧2空调',
  'Device_State': 0,
  'Device_CmdData': b'87\t\x01\x01\x03\x11\xff\xff\x00'},
 {'Device_Mac': 18374967954648268838,
  'Device_is_online': 1,
  'DEVICE_VERSION': 111,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 0,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0400h110\x100',
  'Device_Name': '南次卧地暖',
  'Device_State': 0,
  'Device_CmdData': '\x00<\x13\x01'},
 {'Device_Mac': 18375249429624979494,
  'Device_is_online': 1,
  'DEVICE_VERSION': 111,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 1,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0300a160\x100',
  'Device_Name': '南次卧新风',
  'Device_State': 0,
  'Device_CmdData': b'\x10\xff\xff\xff\xff\x13\x01\xff\xff\x00'},
 {'Device_Mac': 18375530904601690150,
  'Device_is_online': 1,
  'DEVICE_VERSION': 111,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 2,
  'ENTITY_HIDDEN': 2,
  'Device_Desc': 'dooyar0200a170\x100',
  'Device_Name': '南次卧空调',
  'Device_State': 0,
  'Device_CmdData': b'(6\x13\x01\x01\x01\x11\xff\xff\x00'},
 {'Device_Mac': 18375249429624979459,
  'Device_is_online': 1,
  'DEVICE_VERSION': 0,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 1,
  'ENTITY_HIDDEN': 2,
  'device_father': b'\x03\x00\xff\xff\xff\xff\x00\xff',
  'Device_Desc': 'dooyar0300a160\x100',
  'Device_Name': '新风-1',
  'Device_State': 0,
  'Device_CmdData': '0\x00\x00\x00\x00\x00\x00'},
 {'Device_Mac': 18374967954648268804,
  'Device_is_online': 1,
  'DEVICE_VERSION': 0,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 0,
  'ENTITY_HIDDEN': 2,
  'device_father': b'\x04\x00\xff\xff\xff\xff\x00\xff',
  'Device_Desc': 'dooyar0200a110\x100',
  'Device_Name': '客餐厅1',
  'Device_State': 0,
  'Device_CmdData': '\x01\x1b\x01\x00'},
 {'Device_Mac': 18375249429624979460,
  'Device_is_online': 1,
  'DEVICE_VERSION': 0,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 1,
  'ENTITY_HIDDEN': 2,
  'device_father': b'\x04\x00\xff\xff\xff\xff\x00\xff',
  'Device_Desc': 'dooyar0200a110\x100',
  'Device_Name': '北次卧2',
  'Device_State': 0,
  'Device_CmdData': '\x01\x1b\x03\x00'},
 {'Device_Mac': 18375530904601690116,
  'Device_is_online': 1,
  'DEVICE_VERSION': 0,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 2,
  'ENTITY_HIDDEN': 2,
  'device_father': b'\x04\x00\xff\xff\xff\xff\x00\xff',
  'Device_Desc': 'dooyar0200a110\x100',
  'Device_Name': '客餐厅2',
  'Device_State': 0,
  'Device_CmdData': '\x01\x1b\x01\x00'},
 {'Device_Mac': 18375812379578400772,
  'Device_is_online': 1,
  'DEVICE_VERSION': 0,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 3,
  'ENTITY_HIDDEN': 2,
  'device_father': b'\x04\x00\xff\xff\xff\xff\x00\xff',
  'Device_Desc': 'dooyar0200a110\x100',
  'Device_Name': '主卧',
  'Device_State': 0,
  'Device_CmdData': '\x01\x1c\x01\x00'},
 {'Device_Mac': 18376093854555111428,
  'Device_is_online': 1,
  'DEVICE_VERSION': 0,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 4,
  'ENTITY_HIDDEN': 2,
  'device_father': b'\x04\x00\xff\xff\xff\xff\x00\xff',
  'Device_Desc': 'dooyar0200a110\x100',
  'Device_Name': '书房',
  'Device_State': 0,
  'Device_CmdData': '\x01\x1b\x03\x00'},
 {'Device_Mac': 18376375329531822084,
  'Device_is_online': 1,
  'DEVICE_VERSION': 0,
  'DEVICE_FORBID_BY_LOCK': 0,
  'Device_virtual_flag': 0,
  'Dev_ChannelSum': 1,
  'Device_channel': 5,
  'ENTITY_HIDDEN': 2,
  'device_father': b'\x04\x00\xff\xff\xff\xff\x00\xff',
  'Device_Desc': 'dooyar0200a110\x100',
  'Device_Name': '南次卧',
  'Device_State': 0,
  'Device_CmdData': '\x01\x1b\x01\x00'}],
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
        "action": "query_device_details",
        "proto_type": packet.proto_type,
        "link_code": packet.link_code,
        "serial_num": packet.serial_num,
        "datareq_type": datareq_type,
    }


def _response_hex_to_json(packet_hex: str) -> dict:
    packet = parse_protocol_packet(bytes.fromhex(packet_hex))

    datareq_type = next((f.value for f in packet.fields if f.id == 15), None)
    device_count = next((f.value for f in packet.fields if f.id == 17), None)
    request_data_over = next((f.value for f in packet.fields if f.id == 148), None)

    data = {}
    routed = route(packet, data)
    assert routed == "devices"

    return {
        "action": "query_device_details",
        "proto_type": packet.proto_type,
        "link_code": packet.link_code,
        "serial_num": packet.serial_num,
        "datareq_type": datareq_type,
        "device_count": device_count,
        "request_data_over": request_data_over,
        "devices": data.get("devices", []),
    }


def test_request_json_to_hex_uses_capture_raw_sample():
    # JSON -> HEX（与抓包原样一致）
    req_hex = _request_json_to_hex(EXPECTED_REQ_JSON)
    assert req_hex == REQ_DEVICE_HEX

    # 对比现有 commands 默认 serial=0 的固定构包
    assert query_device_details().hex() == "231600646f6f796173686370010307000005000f0001000123"

    # HEX -> JSON（抓包样本）
    req_json_back = _request_hex_to_json(REQ_DEVICE_HEX)
    assert req_json_back == EXPECTED_REQ_JSON


def test_response_capture_hex_to_business_json():
    rsp_json = _response_hex_to_json(RSP_DEVICE_HEX)
    assert rsp_json == EXPECTED_RSP_JSON
