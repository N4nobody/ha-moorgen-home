
import json
import logging
from dataclasses import dataclass, field
from typing import List

_LOGGER = logging.getLogger(__name__)

data_types = [
    {'id': 792, 'name': 'ALIAS', 'type': 'number'},
    {'id': 531, 'name': 'APPID', 'type': 'string'},
    {'id': 137, 'name': 'APP_APPID', 'type': 'number'},
    {'id': 3079, 'name': 'APP_HOST_CONN_STATE', 'type': 'number'},
    {'id': 119, 'name': 'APP_PUSHID', 'type': 'number'},
    {'id': 120, 'name': 'APP_PUSHID_STATE', 'type': 'number'},
    {'id': 868, 'name': 'AP_DATA_TYPE', 'type': 'number'},
    {'id': 865, 'name': 'AP_WIFI_ACCESS_NUMBER', 'type': 'number'},
    {'id': 863, 'name': 'AP_WIFI_AP_PWD', 'type': 'number'},
    {'id': 860, 'name': 'AP_WIFI_AUTH_MODE', 'type': 'number'},
    {'id': 864, 'name': 'AP_WIFI_CHANNEL', 'type': 'number'},
    {'id': 861, 'name': 'AP_WIFI_ENCRYPTION_MODE', 'type': 'number'},
    {'id': 862, 'name': 'AP_WIFI_HIDE_SWITCH', 'type': 'number'},
    {'id': 858, 'name': 'AP_WIFI_NAME', 'type': 'number'},
    {'id': 866, 'name': 'AP_WIFI_POWER_MODE', 'type': 'number'},
    {'id': 857, 'name': 'AP_WIFI_SWITCH', 'type': 'number'},
    {'id': 867, 'name': 'AP_WIFI_TYPE', 'type': 'number'},
    {'id': 859, 'name': 'AP_WIFI_WIRELESS_MODE', 'type': 'number'},
    {'id': 856, 'name': 'AREA_TRIGGER_COND', 'type': 'number'},
    {'id': 772, 'name': 'AUTH_CODE', 'type': 'number'},
    {'id': 159, 'name': 'AUTOMATE_LOGIC_TYPE', 'type': 'number'},
    {'id': 14, 'name': 'Auth_Info', 'type': 'number'},
    {'id': 822, 'name': 'BACKUP_RESTORE_STATE_INFO', 'type': 'number'},
    {'id': 819, 'name': 'BACKUP_RESTORE_TYPE', 'type': 'number'},
    {'id': 820, 'name': 'BACKUP_STATE', 'type': 'number'},
    {'id': 799, 'name': 'BK_TYPE', 'type': 'number'},
    {'id': 174, 'name': 'BUTTON_FUNC', 'type': 'number'},
    {'id': 173, 'name': 'BUTTON_ICO', 'type': 'number'},
    {'id': 169, 'name': 'BUTTON_NAME', 'type': 'number'},
    {'id': 540, 'name': 'BUTTON_NO', 'type': 'number'},
    {'id': 524, 'name': 'CAMERA_CONFIG_JSON', 'type': 'number'},
    {'id': 520, 'name': 'CD_DEVICE_MAC', 'type': 'number'},
    {'id': 519, 'name': 'CD_SCENE_ID', 'type': 'number'},
    {'id': 769, 'name': 'CLIENT_ID', 'type': 'number'},
    {'id': 165, 'name': 'CLOUDDATA_SYNCED', 'type': 'number'},
    {'id': 166, 'name': 'CLOUDDATA_SYNC_ENABLED', 'type': 'number'},
    {'id': 771, 'name': 'CODE_VERIFIER', 'type': 'number'},
    {'id': 870, 'name': 'CONNECT_MODE', 'type': 'number'},
    {'id': 848, 'name': 'CRM_CHECK_CODE', 'type': 'number'},
    {'id': 849, 'name': 'CRM_CHECK_STATUS', 'type': 'number'},
    {'id': 847, 'name': 'CRM_CHECK_URL', 'type': 'number'},
    {'id': 790, 'name': 'CUR_DOWNLOAD_SIZE', 'type': 'number'},
    {'id': 56, 'name': 'Create_Time', 'type': 'number'},
    {'id': 811, 'name': 'DATA_SAVE_STATE', 'type': 'number'},
    {'id': 529, 'name': 'DATA_SHARED_TO_THIRD_PARTY', 'type': 'number'},
    {'id': 518, 'name': 'DATA_SHARING_ACK', 'type': 'number'},
    {'id': 834, 'name': 'DEFAULT_PWD_VERIFY', 'type': 'number'},
    {'id': 541, 'name': 'DEVICE_ALIAS', 'type': 'number'},
    {'id': 183, 'name': 'DEVICE_BUS_TYPE', 'type': 'number'},
    {'id': 776, 'name': 'DEVICE_CONFIG_CMD', 'type': 'number'},
    {'id': 777, 'name': 'DEVICE_CONFIG_CMD_DATA', 'type': 'number'},
    {'id': 842, 'name': 'DEVICE_CONFIG_JSON', 'type': 'number'},
    {'id': 824, 'name': 'DEVICE_DATA_STATE', 'type': 'number'},
    {'id': 803, 'name': 'DEVICE_EXT_CMD', 'type': 'number'},
    {'id': 804, 'name': 'DEVICE_EXT_CMD_DATA', 'type': 'number'},
    {'id': 802, 'name': 'DEVICE_EXT_CMD_OPT_CODE', 'type': 'number'},
    {'id': 810, 'name': 'DEVICE_FAULT_CODE', 'type': 'number'},
    {'id': 156, 'name': 'DEVICE_FORBID_BY_LOCK', 'type': 'number'},
    {'id': 809, 'name': 'DEVICE_FW_VER', 'type': 'number'},
    {'id': 854, 'name': 'DEVICE_PUSH_CAP', 'type': 'number'},
    {'id': 851, 'name': 'DEVICE_PUSH_CONFIG', 'type': 'number'},
    {'id': 833, 'name': 'DEVICE_SN', 'type': 'number'},
    {'id': 144, 'name': 'DEVICE_UDN', 'type': 'number'},
    {'id': 170, 'name': 'DEVICE_UI_CODE', 'type': 'number'},
    {'id': 152, 'name': 'DEVICE_VERSION', 'type': 'number'},
    {'id': 161, 'name': 'DOMAIN_NAME', 'type': 'string'},
    {'id': 15, 'name': 'Datareq_Type', 'type': 'number'},
    {'id': 134, 'name': 'Dev_ChannelSum', 'type': 'number'},
    {'id': 17, 'name': 'DeviceCount', 'type': 'number'},
    {'id': 49, 'name': 'DeviceFunc', 'type': 'number'},
    {'id': 52, 'name': 'DeviceMulti', 'type': 'number'},
    {'id': 51, 'name': 'DeviceNumber', 'type': 'number'},
    {'id': 50, 'name': 'DeviceSeries', 'type': 'number'},
    {'id': 105, 'name': 'Device_AIRCON_BRAND', 'type': 'number'},
    {'id': 112, 'name': 'Device_AIRCON_CODE', 'type': 'number'},
    {'id': 9, 'name': 'Device_Cmd', 'type': 'number'},
    {'id': 10, 'name': 'Device_CmdData', 'type': 'string'},
    {'id': 60, 'name': 'Device_Congif_data', 'type': 'number'},
    {'id': 5, 'name': 'Device_Desc', 'type': 'string'},
    {'id': 98, 'name': 'Device_GroupBtn_cmd', 'type': 'number'},
    {'id': 100, 'name': 'Device_GroupBtn_data', 'type': 'number'},
    {'id': 99, 'name': 'Device_GroupBtn_name', 'type': 'number'},
    {'id': 102, 'name': 'Device_GroupBtn_operate', 'type': 'number'},
    {'id': 101, 'name': 'Device_GroupBtn_value', 'type': 'number'},
    {'id': 167, 'name': 'Device_Icon', 'type': 'number'},
    {'id': 4, 'name': 'Device_Mac', 'type': 'number'},
    {'id': 104, 'name': 'Device_Media_multy_func', 'type': 'number'},
    {'id': 6, 'name': 'Device_Name', 'type': 'string'},
    {'id': 11, 'name': 'Device_State', 'type': 'number'},
    {'id': 8, 'name': 'Device_Type', 'type': 'number'},
    {'id': 95, 'name': 'Device_channel', 'type': 'number'},
    {'id': 96, 'name': 'Device_is_online', 'type': 'number'},
    {'id': 97, 'name': 'Device_max_channel', 'type': 'number'},
    {'id': 31, 'name': 'Device_power', 'type': 'number'},
    {'id': 33, 'name': 'Device_powerCount', 'type': 'number'},
    {'id': 198, 'name': 'Device_real_mac', 'type': 'number'},
    {'id': 32, 'name': 'Device_runTime', 'type': 'number'},
    {'id': 114, 'name': 'Device_virtual_flag', 'type': 'number'},
    {'id': 871, 'name': 'EMAIL', 'type': 'number'},
    {'id': 93, 'name': 'ENCRYPT_RANDOM', 'type': 'number'},
    {'id': 160, 'name': 'ENCRYPT_TYPE', 'type': 'number'},
    {'id': 1, 'name': 'ENCRYPT_TYPE_AES', 'type': 'string'},
    {'id': 3, 'name': 'ENCRYPT_TYPE_AES2', 'type': 'string'},
    {'id': 0, 'name': 'ENCRYPT_TYPE_NONT', 'type': 'string'},
    {'id': 2, 'name': 'ENCRYPT_TYPE_RSA', 'type': 'string'},
    {'id': 513, 'name': 'ENTITY_HIDDEN', 'type': 'number'},
    {'id': 147, 'name': 'EVENT_NAME', 'type': 'number'},
    {'id': 238, 'name': 'EXE_ERROR_RESP', 'type': 'number'},
    {'id': 29, 'name': 'Excute_faile', 'type': 'number'},
    {'id': 855, 'name': 'FAMILY_AREA_MAP', 'type': 'number'},
    {'id': 786, 'name': 'FILE_ATTR', 'type': 'number'},
    {'id': 787, 'name': 'FILE_CRC32', 'type': 'number'},
    {'id': 780, 'name': 'FILE_FORMAT', 'type': 'number'},
    {'id': 779, 'name': 'FILE_LENGTH', 'type': 'number'},
    {'id': 789, 'name': 'FILE_MD5', 'type': 'number'},
    {'id': 778, 'name': 'FILE_NAME', 'type': 'number'},
    {'id': 791, 'name': 'FILE_SIZE', 'type': 'number'},
    {'id': 788, 'name': 'FILE_URL', 'type': 'number'},
    {'id': 177, 'name': 'FIRMWARE_UPDATE_PROGRESS', 'type': 'number'},
    {'id': 178, 'name': 'FIRMWARE_UPDATE_STATE', 'type': 'number'},
    {'id': 153, 'name': 'FLOOR_DESCRIP', 'type': 'number'},
    {'id': 154, 'name': 'FLOOR_NAME', 'type': 'number'},
    {'id': 155, 'name': 'FLOOR_PIC', 'type': 'number'},
    {'id': 839, 'name': 'FW_LOGIC_VERSION', 'type': 'number'},
    {'id': 544, 'name': 'GATEWAY_485_ADDRESS', 'type': 'number'},
    {'id': 532, 'name': 'GATEWAY_DEBUGGABLE', 'type': 'number'},
    {'id': 533, 'name': 'GATEWAY_DEBUGGABLE_TIME', 'type': 'number'},
    {'id': 535, 'name': 'GATEWAY_FW_MODEL', 'type': 'number'},
    {'id': 534, 'name': 'GATEWAY_IP', 'type': 'number'},
    {'id': 528, 'name': 'GATEWAY_MAC_ADDRESS', 'type': 'number'},
    {'id': 168, 'name': 'GP_DEV_DELAY', 'type': 'number'},
    {'id': 852, 'name': 'HA_AUTH_SWITCH', 'type': 'number'},
    {'id': 149, 'name': 'HOSTTIME_MODE', 'type': 'number'},
    {'id': 526, 'name': 'HOST_ACTIVATE_STATE', 'type': 'number'},
    {'id': 527, 'name': 'HOST_ACTIVATE_TIME_LEFT', 'type': 'number'},
    {'id': 542, 'name': 'HOST_AREA_NAME', 'type': 'number'},
    {'id': 536, 'name': 'HOST_AUTH_CODE', 'type': 'number'},
    {'id': 512, 'name': 'HOST_CLOUD_SYNC_METHOD', 'type': 'number'},
    {'id': 193, 'name': 'HOST_CLOUD_SYNC_METHOD_1', 'type': 'number'},
    {'id': 813, 'name': 'HOST_MODULE_FW_VER', 'type': 'number'},
    {'id': 815, 'name': 'HOST_MODULE_OTA_MD5', 'type': 'number'},
    {'id': 814, 'name': 'HOST_MODULE_OTA_URL', 'type': 'number'},
    {'id': 816, 'name': 'HOST_MODULE_TYPE', 'type': 'number'},
    {'id': 817, 'name': 'HOST_SCENE_CAPTURE_SWITCH', 'type': 'number'},
    {'id': 514, 'name': 'HOST_TYPE_CODE', 'type': 'number'},
    {'id': 58, 'name': 'Hearting_powerPin', 'type': 'number'},
    {'id': 57, 'name': 'Hearting_timePin', 'type': 'number'},
    {'id': 28, 'name': 'Hosttime', 'type': 'string'},
    {'id': 841, 'name': 'IP_CONFIG_MTD', 'type': 'number'},
    {'id': 146, 'name': 'LANGUAGE', 'type': 'number'},
    {'id': 825, 'name': 'LAST_BACKUP_TIME', 'type': 'number'},
    {'id': 826, 'name': 'LAST_RESTORE_TIME', 'type': 'number'},
    {'id': 853, 'name': 'LHOST_AUTH_SWITCH', 'type': 'number'},
    {'id': 188, 'name': 'LOCK_OPT_CODE', 'type': 'number'},
    {'id': 186, 'name': 'LOCK_USER_CUSTOMER_INFO', 'type': 'number'},
    {'id': 185, 'name': 'LOCK_USER_ID', 'type': 'number'},
    {'id': 189, 'name': 'LOCK_USER_NUMBER', 'type': 'number'},
    {'id': 191, 'name': 'LOCK_USER_TYPE', 'type': 'number'},
    {'id': 794, 'name': 'LOGIN_AUTH_CODE', 'type': 'number'},
    {'id': 840, 'name': 'LOGIN_ERR_LEFT_TIME', 'type': 'number'},
    {'id': 163, 'name': 'LONGTI_LANTI', 'type': 'string'},
    {'id': 163, 'name': 'LONLANTITUDE', 'type': 'number'},
    {'id': 184, 'name': 'MODEL_TYPE', 'type': 'number'},
    {'id': 546, 'name': 'MODULE_ADDRESS', 'type': 'number'},
    {'id': 774, 'name': 'MODULE_FW_VER', 'type': 'number'},
    {'id': 835, 'name': 'MODULE_OTA_PROGRESS', 'type': 'number'},
    {'id': 836, 'name': 'MODULE_OTA_STATE', 'type': 'number'},
    {'id': 775, 'name': 'MODULE_OTA_TYPE', 'type': 'number'},
    {'id': 143, 'name': 'MOVIE', 'type': 'number'},
    {'id': 795, 'name': 'MSG_CHECK_CODE', 'type': 'number'},
    {'id': 545, 'name': 'MUDULE_FW_VERSION', 'type': 'number'},
    {'id': 61, 'name': 'Media_learn_Key', 'type': 'number'},
    {'id': 62, 'name': 'Media_learn_KeyId', 'type': 'number'},
    {'id': 180, 'name': 'OFFLINE_DEVICE_HIDDEN_FUNC', 'type': 'number'},
    {'id': 773, 'name': 'OTA_PRODUCTION_CODE', 'type': 'number'},
    {'id': 16, 'name': 'Operate_Type', 'type': 'number'},
    {'id': 3076, 'name': 'PANEL_HOST_CONN_STATE', 'type': 'number'},
    {'id': 543, 'name': 'PANEL_PRESS_MODE', 'type': 'number'},
    {'id': 151, 'name': 'PANEL_STATE', 'type': 'number'},
    {'id': 3078, 'name': 'PANEL_TRIGGER_ACTION', 'type': 'number'},
    {'id': 3077, 'name': 'PANEL_TRIGGER_BT_NO', 'type': 'number'},
    {'id': 793, 'name': 'PHONE_NO', 'type': 'number'},
    {'id': 823, 'name': 'POWER_CONSUMPTION_TYPE', 'type': 'number'},
    {'id': 831, 'name': 'PROJECT_INFO', 'type': 'number'},
    {'id': 827, 'name': 'PROJECT_UAT_STATE', 'type': 'number'},
    {'id': 179, 'name': 'PUBLIC_ROOM_HIDDEN_FUNC', 'type': 'number'},
    {'id': 850, 'name': 'REMOTER_ID_LIST', 'type': 'number'},
    {'id': 148, 'name': 'REQUEST_DATA_OVER', 'type': 'number'},
    {'id': 157, 'name': 'RESOURCE_TYPE', 'type': 'number'},
    {'id': 821, 'name': 'RESTORE_STATE', 'type': 'number'},
    {'id': 796, 'name': 'RESULT_CODE', 'type': 'number'},
    {'id': 190, 'name': 'RSA_PUBLIC_KEY', 'type': 'number'},
    {'id': 249, 'name': 'RTSP_EXEC', 'type': 'number'},
    {'id': 53, 'name': 'RoomCount', 'type': 'number'},
    {'id': 48, 'name': 'RoomDesc', 'type': 'string'},
    {'id': 55, 'name': 'RoomImage', 'type': 'number'},
    {'id': 54, 'name': 'RoomName', 'type': 'string'},
    {'id': 538, 'name': 'SAS_CONDITION', 'type': 'number'},
    {'id': 539, 'name': 'SAS_TIME_OFFSET', 'type': 'number'},
    {'id': 515, 'name': 'SCENE_EXECUTE_MODE', 'type': 'number'},
    {'id': 808, 'name': 'SCENE_SAVE_PROCESS', 'type': 'number'},
    {'id': 799, 'name': 'SCENE_TYPE', 'type': 'number'},
    {'id': 92, 'name': 'SECURITY_COUNT_INIT', 'type': 'number'},
    {'id': 85, 'name': 'SECURITY_COUNT_NEED', 'type': 'number'},
    {'id': 82, 'name': 'SECURITY_DESCRIB', 'type': 'number'},
    {'id': 83, 'name': 'SECURITY_NAME', 'type': 'number'},
    {'id': 84, 'name': 'SECURITY_ONOFF_FLAG', 'type': 'number'},
    {'id': 135, 'name': 'SECURITY_PUSH_DATA', 'type': 'number'},
    {'id': 122, 'name': 'SECURITY_PUSH_LANGUAGE', 'type': 'number'},
    {'id': 121, 'name': 'SECURITY_PUSH_SWITCH', 'type': 'number'},
    {'id': 145, 'name': 'SECURITY_REPEAT', 'type': 'number'},
    {'id': 86, 'name': 'SENSOR_PARAM_EQUAL', 'type': 'number'},
    {'id': 87, 'name': 'SENSOR_PARAM_LARGER', 'type': 'number'},
    {'id': 517, 'name': 'SENSOR_PARAM_NOT_EQUAL', 'type': 'number'},
    {'id': 88, 'name': 'SENSOR_PARAM_SMALLER', 'type': 'number'},
    {'id': 89, 'name': 'SENSOR_REPEAT_MODE', 'type': 'number'},
    {'id': 797, 'name': 'SESSION_CODE', 'type': 'number'},
    {'id': 158, 'name': 'STATE_POS', 'type': 'number'},
    {'id': 131, 'name': 'SYSTEM_GATEWAY', 'type': 'number'},
    {'id': 130, 'name': 'SYSTEM_IPADDR', 'type': 'number'},
    {'id': 136, 'name': 'SYSTEM_MAC', 'type': 'number'},
    {'id': 132, 'name': 'SYSTEM_NETMASK', 'type': 'number'},
    {'id': 129, 'name': 'SYSTEM_OTA_MD5', 'type': 'number'},
    {'id': 128, 'name': 'SYSTEM_OTA_URL', 'type': 'number'},
    {'id': 133, 'name': 'SYSTEM_PORT', 'type': 'number'},
    {'id': 530, 'name': 'SYSTEM_RSA_PUBLIC_KEY', 'type': 'number'},
    {'id': 244, 'name': 'SYS_HOST_F4', 'type': 'number'},
    {'id': 243, 'name': 'SYS_PORT_F3', 'type': 'number'},
    {'id': 81, 'name': 'SYS_VERSION', 'type': 'number'},
    {'id': 18, 'name': 'SceneCount', 'type': 'number'},
    {'id': 2, 'name': 'Scene_Desc', 'type': 'string'},
    {'id': 80, 'name': 'Scene_Device_Delay', 'type': 'number'},
    {'id': 94, 'name': 'Scene_Icon', 'type': 'number'},
    {'id': 38, 'name': 'Scene_Mode', 'type': 'number'},
    {'id': 1, 'name': 'Scene_Name', 'type': 'number'},
    {'id': 141, 'name': 'Sequence_Delay', 'type': 'number'},
    {'id': 138, 'name': 'Sequence_Desc', 'type': 'number'},
    {'id': 139, 'name': 'Sequence_Name', 'type': 'number'},
    {'id': 140, 'name': 'Sequence_Pic', 'type': 'number'},
    {'id': 164, 'name': 'TAMPERATURE_UNIT', 'type': 'number'},
    {'id': 830, 'name': 'TEMP_ACCOUNT_KEY', 'type': 'number'},
    {'id': 828, 'name': 'TEMP_ACCOUNT_SITUATION', 'type': 'number'},
    {'id': 829, 'name': 'TEMP_ACCOUNT_TIME_LIMIT', 'type': 'number'},
    {'id': 537, 'name': 'TIMER_SAS_STATE', 'type': 'number'},
    {'id': 162, 'name': 'TIMEZONE', 'type': 'number'},
    {'id': 844, 'name': 'TRANS_ADDRESS', 'type': 'number'},
    {'id': 843, 'name': 'TRANS_DATA', 'type': 'number'},
    {'id': 846, 'name': 'TRANS_DST_PORT', 'type': 'number'},
    {'id': 845, 'name': 'TRANS_SRC_PORT', 'type': 'number'},
    {'id': 785, 'name': 'TRANS_STATE', 'type': 'number'},
    {'id': 784, 'name': 'TRANS_TYPE', 'type': 'number'},
    {'id': 818, 'name': 'TUYA_DEVICE_PID', 'type': 'number'},
    {'id': 25, 'name': 'TimerBegin', 'type': 'number'},
    {'id': 19, 'name': 'TimerCount', 'type': 'number'},
    {'id': 20, 'name': 'TimerDesc', 'type': 'number'},
    {'id': 26, 'name': 'TimerEnd', 'type': 'number'},
    {'id': 21, 'name': 'TimerName', 'type': 'number'},
    {'id': 22, 'name': 'TimerStartStop', 'type': 'number'},
    {'id': 23, 'name': 'TimerWeek', 'type': 'number'},
    {'id': 523, 'name': 'UI_DISPLAY_SPEC_1', 'type': 'number'},
    {'id': 770, 'name': 'USER_ID', 'type': 'number'},
    {'id': 12, 'name': 'USER_NAME', 'type': 'string'},
    {'id': 812, 'name': 'USER_NICK_NAME', 'type': 'string'},
    {'id': 13, 'name': 'USER_PSW', 'type': 'string'},
    {'id': 27, 'name': 'Update_proc', 'type': 'number'},
    {'id': 176, 'name': 'VOICE_PANEL_ACTIVATE_CODE', 'type': 'number'},
    {'id': 175, 'name': 'VOICE_PANEL_ACTIVATE_URL', 'type': 'number'},
    {'id': 181, 'name': 'VOICE_PANEL_DEVICE_ID', 'type': 'number'},
    {'id': 182, 'name': 'VOICE_PANEL_TOKEN_ID', 'type': 'number'},
    {'id': 832, 'name': 'WIFI_CHANEL_NO', 'type': 'number'},
    {'id': 3075, 'name': 'WIFI_CONN_STATE', 'type': 'number'},
    {'id': 3074, 'name': 'WIFI_PWD', 'type': 'number'},
    {'id': 3073, 'name': 'WIFI_SSID', 'type': 'number'},
    {'id': 869, 'name': 'ZIGBEE_CHANNEL', 'type': 'number'},
    {'id': 807, 'name': 'ZIGBEE_MODULE_FM_VER', 'type': 'number'},
    {'id': 806, 'name': 'ZIGBEE_MODULE_MAC', 'type': 'number'},
    {'id': 118, 'name': 'camera_token', 'type': 'number'},
    {'id': 117, 'name': 'device_father', 'type': 'string'},
    {'id': 115, 'name': 'isCloud_hostID', 'type': 'number'},
    {'id': 116, 'name': 'isCloud_hostName', 'type': 'number'},
    {'id': 197, 'name': 'smallHost_ID', 'type': 'number'},
    {'id': 196, 'name': 'smallHost_name', 'type': 'string'}
]


def get_type_by_id(idx):
    return next((x for x in data_types if x['id'] == idx), None)


@dataclass
class DataField:
    id: int = 0
    name: str = ""
    value: any = ""


@dataclass
class DataPacket:
    msg_flag: str = ""
    length: int = 0
    proto_name: str = ""
    proto_num: int = 0
    proto_type: int = 0
    link_code: int = 0
    serial_num: int = 0
    data_len: int = 0
    fields: List[DataField] = field(default_factory=list)


@dataclass
class RoomInfo:
    id: str = ""
    name: str = ""
    image: int = 0


@dataclass
class SceneInfo:
    id: str = ""
    name: str = ""
    image: int = 0


@dataclass
class DeviceInfo:
    id: str = ""


def parse_protocol_packet(data) -> DataPacket:
    if len(data) < 19:
        return "数据包太短，无法解析"

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
    fields = []
    ptr = datafield_offset
    limit = datafield_offset + packet.data_len
    while ptr < limit and ptr + 4 <= len(data):
        dtype = data[ptr] + (data[ptr + 1] << 8)
        vlen = data[ptr + 2] + (data[ptr + 3] << 8)
        val = data[ptr + 4:ptr + 4 + vlen]
        fields.append({'type': dtype, 'vlen': vlen, 'value': val})

        field = DataField()
        field.id = dtype
        field.name = get_type_by_id(dtype)['name']
        try:
            if get_type_by_id(dtype)['type'] == 'string':
                try:
                    field.value = val.decode('utf-8')
                except Exception:
                    field.value = val
            else:
                field.value = int.from_bytes(val, 'little')
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
    protoName_bytes = protoName.encode('ascii')
    if len(protoName_bytes) != 9:
        raise ValueError("protoName must be exactly 9 ASCII characters")

    # Prepare the data fields
    data_fields = bytearray()
    for field in fields:
        # Get field type information
        tdesc = get_type_by_id(field['type'])
        if not tdesc:
            raise ValueError(f"Unknown field type ID: {field['type']}")

        # Convert value based on type
        value = field['value']
        if tdesc['type'] == 'string':
            if not isinstance(value, str):
                value = str(value)
            value_bytes = value.encode('utf-8')
        else:  # number type
            if isinstance(value, str):
                value = int(value)
            if not isinstance(value, int):
                raise ValueError(
                    f"Field {tdesc['name']} expects a numeric value")
            # Determine minimum bytes needed to represent the number
            byte_count = (value.bit_length() + 7) // 8 or 1
            value_bytes = value.to_bytes(byte_count, 'little')

        # Append field header (type + length) and value
        data_fields.extend(field['type'].to_bytes(2, 'little'))
        data_fields.extend(len(value_bytes).to_bytes(2, 'little'))
        data_fields.extend(value_bytes)

    # Calculate lengths
    dataLen = len(data_fields)
    total_length = 17 + dataLen  # 19 bytes for header + data fields

    # Build the packet
    packet = bytearray()
    packet.append(msgFlag)  # 1 byte
    packet.extend(total_length.to_bytes(2, 'little'))  # 2 bytes
    packet.extend(protoName_bytes)  # 9 bytes
    packet.append(protoNum)  # 1 byte
    packet.append(protoType)  # 1 byte
    packet.append(linkCode)  # 1 byte
    packet.extend(serialNum.to_bytes(2, 'little'))  # 2 bytes
    packet.extend(dataLen.to_bytes(2, 'little'))  # 2 bytes
    packet.extend(data_fields)  # variable length
    packet.append(0x23)
    return bytes(packet)


def query_room_info():
    return build_protocol_packet(
        msgFlag=0x23,
        protoName="dooyashcp",
        protoNum=1,
        protoType=3,
        linkCode=7,
        serialNum=0,
        fields=[
            {'type': 15, 'value': 11}
        ]
    )


def query_user_info():
    return build_protocol_packet(
        msgFlag=0x23,
        protoName="dooyashcp",
        protoNum=1,
        protoType=3,
        linkCode=7,
        serialNum=0,
        fields=[
            {'type': 15, 'value': 9}
        ]
    )


def query_device_details():
    return build_protocol_packet(
        msgFlag=0x23,
        protoName="dooyashcp",
        protoNum=1,
        protoType=3,
        linkCode=7,
        serialNum=0,
        fields=[
            {'type': 15, 'value': 1}
        ]
    )


def query_scene_details():
    return build_protocol_packet(
        msgFlag=0x23,
        protoName="dooyashcp",
        protoNum=1,
        protoType=3,
        linkCode=7,
        serialNum=0,
        fields=[
            {'type': 15, 'value': 17}
        ]
    )


def activate_scene(scene_name):
    return build_protocol_packet(
        msgFlag=0x23,
        protoName="dooyashcp",
        protoNum=1,
        protoType=4,
        linkCode=9,
        serialNum=0,
        fields=[
            {'type': 16, 'value': 5},
            {'type': 2, 'value': scene_name}
        ]
    )


def route(packet: DataPacket, data_dict: dict):
    _LOGGER.info(
        f"packet come {packet.proto_num} {packet.proto_type} {packet.link_code}")

    if packet.proto_num == 1 and packet.proto_type == 3 and packet.link_code == 8:
        if (len(packet.fields) > 0 and packet.fields[0].id == 12):
            _LOGGER.info("room info come")
            data_dict['rooms'] = parse_room_info(packet)
            return
        if (len(packet.fields) > 0 and packet.fields[0].id == 4):
            _LOGGER.info("device info come")
            data_dict['devices'] = parse_device_info(packet)
            return
        if (len(packet.fields) > 0 and packet.fields[0].id == 15):
            _LOGGER.info("scene info come")
            data_dict['scenes'] = parse_scene_info(packet)
            return


def parse_room_info(packet: DataPacket) -> List[RoomInfo]:
    result = []

    i = 2
    while i+2 < len(packet.fields):
        room = RoomInfo()
        room.id = packet.fields[i].value
        room.name = packet.fields[i+1].value
        room.image = packet.fields[i+2].value
        i += 3
        result.append(room)
    return result


def parse_device_info(packet: DataPacket):
    devices = []
    current = {}
    for field in packet.fields:
        if field.id in (15, 17, 148):
            continue
        if field.id == 4 and current:
            devices.append(current)
            current = {}
        t = get_type_by_id(field.id)
        current[t['name']] = field.value
    if current:
        devices.append(current)

    _LOGGER.info(devices)
    return devices


def parse_scene_info(packet: DataPacket) -> List[SceneInfo]:
    scenes = []
    current = {}
    for field in packet.fields:
        if field.id in (15, 18, 148):
            continue
        if field.id == 2 and current:
            scenes.append(current)
            current = {}
        t = get_type_by_id(field.id)
        current[t['name']] = field.value
    if current:
        scenes.append(current)

    result = []
    for scene in scenes:
        info = SceneInfo()
        info.id = scene['ENCRYPT_TYPE_RSA']
        info.name = scene['ENCRYPT_TYPE_AES']
        info.image = scene['Scene_Icon']
        result.append(info)
        
    _LOGGER.info(result)
    return result


# parse_device_info(parse_protocol_packet(bytes.fromhex("237815646f6f796173686370010308000067150f00010004110002002f0004000800f000ffffffff00ff600001000198000100009c00010000720001000086000100015f0001000001020100023100020010f130000500723035303006000c00e5ba8ae5a4b4e5b084e781af040008000200ffffffff00ff600001000198000100489c00010000720001000086000100015f00010000a700010005010201000205001000646f6f796172303530306c313130103006000c00e58fb3e99885e8afbbe781af0b000100000a000200ffff040008000200ffffffff01ff600001000198000100489c00010000720001000086000100015f00010001a700010005010201000205001000646f6f796172303530306c313130103006000600e781afe5b8a60b000100000a000200ffff040008000200ffffffff02ff600001000198000100489c00010000720001000086000100015f00010002a700010005010201000205001000646f6f796172303530306c313130103006000c00e9a398e7aa97e5b084e781af0b000100000a000200ffff040008000200ffffffff03ff600001000198000100489c00010000720001000086000100015f00010003a700010005010201000205001000646f6f796172303530306c313130103006000c00e5b7a6e99885e8afbbe781af0b000100000a000200ffff040008000200ffffffff04ff600001000198000100489c00010000720001000086000100015f00010004a700010005010201000205001000646f6f796172303730306c313130103006000300322d340b000100000a000200ffff040008000200ffffffff05ff600001000198000100489c00010000720001000086000100015f00010005a700010005010201000205001000646f6f796172303730306c313130103006000300322d350b000100000a000200ffff040008000200ffffffff06ff600001000198000100489c00010000720001000086000100015f00010006a700010005010201000205001000646f6f796172303730306c313130103006000400322d36300b000100000a000200ffff040008000200ffffffff07ff600001000198000100489c00010000720001000086000100015f00010007a700010005010201000205001000646f6f796172303630306c313130103006000c00e4b880e994aee696ade794b50b000100000a000200ffff040008000100ffffffff00ff600001000198000100489c00010000720001000086000100015f00010000a700010005010201000205001000646f6f796172303630306c313130103006000c00e78e84e585b3e781afe5b8a60b000100000a000200ffff040008000100ffffffff01ff600001000198000100489c00010000720001000086000100015f00010001a700010005010201000205001000646f6f796172303630306c313130103006000c00e5a4a9e88ab1e781afe5b8a60b000100000a000200ffff040008000100ffffffff02ff600001000198000100489c00010000720001000086000100015f00010002a700010005010201000205001000646f6f796172303630306c313130103006000c00e5aea2e9a490e5b084e781af0b000100000a000200ffff040008000100ffffffff03ff600001000198000100489c00010000720001000086000100015f00010003a700010005010201000205001000646f6f796172303630306c313130103006000c00e5aea2e58e85e4b8bbe781af0b000100000a000200ffff040008000100ffffffff04ff600001000198000100489c00010000720001000086000100015f00010004a700010005010201000205001000646f6f796172303630306c313130103006000c00e9a490e58e85e4b8bbe781af0b000100000a000200ffff040008000100ffffffff05ff600001000198000100489c00010000720001000086000100015f00010005a700010005010201000205001000646f6f796172303530306c313130103006000c00e8bf87e98193e5b084e781af0b000100000a000200ffff040008000100ffffffff06ff600001000198000100489c00010000720001000086000100015f00010006a700010005010201000205001000646f6f796172303530306c313130103006000600e4b8bbe781af0b000100000a000200ffff040008000100ffffffff07ff600001000198000100489c00010000720001000086000100015f00010007a700010005010201000205001000646f6f796172303530306c313130103006000c00e8838ce699afe5b084e781af0b000100000a000200ffff040008001100ffffffff00ff600001000198000100409c00010000720001000086000100085f00010000a700010002010201000205001000646f6f7961723031303072313533803006000c00e78e84e585b3e99da2e69dbf0b000100010a009000010504303130300500030201000002010100ffffffff04ff116c696768742d726576657273652d6578650003010100ffffffff00ff116c696768742d726576657273652d6578650007010100ffffffff01ff116c696768742d726576657273652d6578650006010100ffffffff03ff116c696768742d726576657273652d6578650005050430323030050003020100009700020064ff040008001200ffffffff00ff600001000198000100409c00010000720001000086000100085f00010000a700010002010201000205001000646f6f7961723031303072313533803006000c00e5aea2e58e85e99da2e69dbf0b000100010a00bb000105043033303005000302010000020504303530300500030201000003010100ffffffff04ff116c696768742d726576657273652d65786500050504303430300500030201000006010100ffffffff01ff116c696768742d726576657273652d6578650007010100ffffffff03ff116c696768742d726576657273652d6578650008010100ffffffff02ff116c696768742d726576657273652d6578650004010100ffffffff00ff116c696768742d726576657273652d657865009700020064ff040008001300ffffffff00ff600001000198000100409c00010000720001000086000100085f00010000a700010002010201000205001000646f6f7961723031303072313533803006001200e4b8bbe58da7e8bf9be997a8e99da2e69dbf0b000100010a009000010504303630300500030201000003010100ffffffff06ff116c696768742d726576657273652d6578650004010100ffffffff05ff116c696768742d726576657273652d65786500050504303730300500030201000007010200ffffffff01ff116c696768742d726576657273652d6578650008010100ffffffff07ff116c696768742d726576657273652d657865009700020064ff040008001400ffffffff00ff600001000198000100409c00010000720001000086000100085f00010000a700010002010201000205001000646f6f7961723031303072313533803006000f00e4b8bbe58da7e5ba8ae5a4b4e5b7a60b000100010a007200010504303630300500030201000003010100ffffffff06ff116c696768742d726576657273652d65786500050504303730300500030201000007010200ffffffff01ff116c696768742d726576657273652d65786500020504306330300500030201000006050430623030050003020100009700020064ff040008001500ffffffff00ff600001000198000100409c00010000720001000086000100085f00010000a700010002010201000205001000646f6f7961723031303072313533803006000f00e4b8bbe58da7e5ba8ae5a4b4e58fb30b000100010a009c00010504303730300500030201000002050430383030050003020100000301f000ffffffff00ff01550004010200ffffffff02ff116c696768742d726576657273652d657865000505043036303005000302010000060504306330300500030201000007010100ffffffff07ff116c696768742d726576657273652d6578650008010100ffffffff05ff116c696768742d726576657273652d657865009700020038ff040008002100ffffffff00ff6000010001980001006f9c00010000720001000086000100015f00010000010201000205001000646f6f7961723034303068313130103006000c00e5aea2e58e85e59cb0e69a960b000100000a000400003c1301040008002100ffffffff01ff6000010001980001006f9c00010000720001000086000100015f00010001010201000205001000646f6f7961723033303061313630103006000c00e5aea2e58e85e696b0e9a38e0b000100000a000a0030ffffffff1301ffff00040008002100ffffffff02ff6000010001980001006f9c00010000720001000086000100015f00010002010201000205001000646f6f7961723032303061313730103006000c00e5aea2e58e85e7a9bae8b0830b000100000a000a00783b1301030311ffff00040008002200ffffffff00ff6000010001980001006f9c00010000720001000086000100015f00010000010201000205001000646f6f7961723034303068313130103006000c00e9a490e58e85e59cb0e69a960b000100000a000400003c0e01040008002200ffffffff01ff6000010001980001006f9c00010000720001000086000100015f00010001010201000205001000646f6f7961723033303061313630103006000c00e9a490e58e85e696b0e9a38e0b000100000a000a0030ffffffff0e01ffff00040008002200ffffffff02ff6000010001980001006f9c00010000720001000086000100015f00010002010201000205001000646f6f7961723032303061313730103006000c00e9a490e58e85e7a9bae8b0830b000100000a000a00983c0e01040311ffff00040008002300ffffffff00ff6000010001980001006f9c00010000720001000086000100015f00010000010201000205001000646f6f7961723034303068313130103006000c00e4b8bbe58da7e59cb0e69a960b000100000a000400003c1301040008002300ffffffff01ff6000010001980001006f9c00010000720001000086000100015f00010001010201000205001000646f6f7961723033303061313630103006000c00e4b8bbe58da7e696b0e9a38e0b000100000a000a0030ffffffff1301ffff00040008002300ffffffff02ff6000010001980001006f9c00010000720001000086000100015f00010002010201000205001000646f6f7961723032303061313730103006000c00e4b8bbe58da7e7a9bae8b0830b000100000a000a00883e1301040111ffff00040008002400ffffffff00ff6000010001980001006f9c00010000720001000086000100015f00010000010201000205001000646f6f7961723034303068313130103006001000e58c97e6aca1e58da731e59cb0e69a960b000100000a000400003c1801040008002400ffffffff01ff6000010001980001006f9c00010000720001000086000100015f00010001010201000205001000646f6f7961723033303061313630103006001000e58c97e6aca1e58da731e696b0e9a38e0b000100000a000a0010ffffffff1801ffff00040008002400ffffffff02ff6000010001980001006f9c00010000720001000086000100015f00010002010201000205001000646f6f7961723032303061313730103006001000e58c97e6aca1e58da731e7a9bae8b0830b000100000a000a00983d1801040311ffff00040008002500ffffffff00ff6000010001980001006f9c00010000720001000086000100015f00010000010201000205001000646f6f7961723034303068313130103006001000e58c97e6aca1e58da732e59cb0e69a960b000100000a000400003c0e01040008002500ffffffff01ff6000010001980001006f9c00010000720001000086000100015f00010001010201000205001000646f6f7961723033303061313630103006001000e58c97e6aca1e58da732e696b0e9a38e0b000100000a000a0000ffffffff0e01ffff00040008002500ffffffff02ff6000010001980001006f9c00010000720001000086000100015f00010002010201000205001000646f6f7961723032303061313730103006001000e58c97e6aca1e58da732e7a9bae8b0830b000100000a000a00983e0e01040311ffff00040008002600ffffffff00ff6000010001980001006f9c00010000720001000086000100015f00010000010201000205001000646f6f7961723034303068313130103006000f00e58d97e6aca1e58da7e59cb0e69a960b000100000a000400003c1301040008002600ffffffff01ff6000010001980001006f9c00010000720001000086000100015f00010001010201000205001000646f6f7961723033303061313630103006000f00e58d97e6aca1e58da7e696b0e9a38e0b000100000a000a0010ffffffff1301ffff00040008002600ffffffff02ff6000010001980001006f9c00010000720001000086000100015f00010002010201000205001000646f6f7961723032303061313730103006000f00e58d97e6aca1e58da7e7a9bae8b0830b000100000a000a00883e1301040111ffff00040008000300ffffffff01ff600001000198000100009c00010000720001000086000100015f000100010102010002750008000300ffffffff00ff05001000646f6f7961723033303061313630103006000800e696b0e9a38e2d310b000100000a00070010000000000000040008000400ffffffff00ff600001000198000100009c00010000720001000086000100015f000100000102010002750008000400ffffffff00ff05001000646f6f7961723032303061313130103006000a00e5aea2e9a490e58e85310b000100000a000000040008000400ffffffff01ff600001000198000100009c00010000720001000086000100015f000100010102010002750008000400ffffffff00ff05001000646f6f7961723032303061313130103006000a00e58c97e6aca1e58da7320b000100000a00040000000000040008000400ffffffff02ff600001000198000100009c00010000720001000086000100015f000100020102010002750008000400ffffffff00ff05001000646f6f7961723032303061313130103006000a00e5aea2e9a490e58e85320b000100000a00040000000000040008000400ffffffff03ff600001000198000100009c00010000720001000086000100015f000100030102010002750008000400ffffffff00ff05001000646f6f7961723032303061313130103006000600e4b8bbe58da70b000100000a00040000000000040008000400ffffffff04ff600001000198000100009c00010000720001000086000100015f000100040102010002750008000400ffffffff00ff05001000646f6f7961723032303061313130103006000a00e58c97e6aca1e58da7310b000100000a00040000000000040008000400ffffffff05ff600001000198000100009c00010000720001000086000100015f000100050102010002750008000400ffffffff00ff05001000646f6f7961723032303061313130103006000900e58d97e6aca1e58da70b000100000a00040000000000940001000123")))
# parse_scene_info(parse_protocol_packet(bytes.fromhex("238501646f6f796173686370010308000074010f00010012120002000a00020004003031303001000c00e59b9ee5aeb6e6a8a1e5bc8f5e00010031110002000600020004003032303001000c00e7a6bbe5aeb6e6a8a1e5bc8f5e00010031110002000d00020004003033303001000c00e4bc9ae5aea2e6a8a1e5bc8f5e00010031110002000500020004003034303001000c00e4bc91e997b2e6a8a1e5bc8f5e00010031110002000500020004003035303001000c00e5b0b1e9a490e6a8a1e5bc8f5e00010031110002000400020004003036303001000c00e4b8bbe58da7e585a8e5bc805e00010031110002000700020004003037303001000c00e4b8bbe58da7e585a8e585b35e00010031110002000700020004003038303001000f00e4b8bbe58da7e4bc91e997b2e58fb35e00010031110002000700020004003062303001000f00e4b8bbe58da7e4bc91e997b2e5b7a65e00010031110002000700020004003063303001000c00e99885e8afbbe6a8a1e5bc8f5e00010031110002000700940001000123")))


# _LOGGER.info(query_scene_details().hex())

# packet = parse_protocol_packet(bytes.fromhex(
#     "231e00646f6f79617368637001040924000d001000010005020004003031303023"))

# _LOGGER.info(packet)
# _LOGGER.info("==========")

# packet = build_protocol_packet(
#     msgFlag=0x23,
#     protoName="dooyashcp",
#     protoNum=1,
#     protoType=4,
#     linkCode=9,
#     serialNum=34,
#     fields=[
#         {'type': 16, 'value': 1},
#         {'type': 4, 'value': 18376093854555111425},
#         {'type': 9, 'value': 7957629044578019692}
#     ]
# )

# result_hex = packet.hex()
# _LOGGER.info(result_hex)
