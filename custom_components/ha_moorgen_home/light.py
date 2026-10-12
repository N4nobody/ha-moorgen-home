import logging

from homeassistant.components.light import ATTR_BRIGHTNESS, ColorMode, LightEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import COORDINATOR, DOMAIN
from .core.protocol.codec import device_room_id, infer_device_type

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinator = hass.data[DOMAIN][COORDINATOR]
    entities = []
    room_names = {room.id: room.name for room in coordinator.data.get("rooms", [])}

    for device in coordinator.data["devices"]:
        dtype = infer_device_type(device)
        if dtype not in ("light", "light_dimmer"):
            continue

        device_mac = device.get("Device_Mac")
        device_name = device.get("Device_Name")
        if device_mac is None or not device_name:
            continue

        entities.append(
            MoorgenLightEntity(
                coordinator,
                device_mac,
                device_name,
                supports_brightness=dtype == "light_dimmer",
                area=room_names.get(device_room_id(device)),
            )
        )

    async_add_entities(entities)
    _LOGGER.info("%s lights initialized", len(entities))


class MoorgenLightEntity(CoordinatorEntity, LightEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(
        self,
        coordinator,
        device_mac: int,
        name: str,
        supports_brightness: bool,
        area: str | None = None,
    ):
        super().__init__(coordinator, context=str(device_mac))
        self._device_mac = device_mac
        self._supports_brightness = supports_brightness
        self._attr_supported_color_modes = (
            {ColorMode.BRIGHTNESS} if supports_brightness else {ColorMode.ONOFF}
        )
        self._attr_color_mode = ColorMode.BRIGHTNESS if supports_brightness else ColorMode.ONOFF
        self._attr_unique_id = f"moorgen_light_{device_mac}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, str(device_mac))},
            name=name,
            manufacturer="Moorgen",
            model="Dimmer" if supports_brightness else "Light",
            suggested_area=area,
        )

    @property
    def _device(self) -> dict | None:
        for device in self.coordinator.data.get("devices", []):
            if device.get("Device_Mac") == self._device_mac:
                return device
        return None

    @property
    def is_on(self) -> bool:
        device = self._device
        if not device:
            return False
        return device.get("Device_State") == 1

    @property
    def brightness(self) -> int | None:
        if not self._supports_brightness:
            return None

        device = self._device
        if not device:
            return None

        raw = device.get("PANEL_STATE")
        if not isinstance(raw, int):
            return None

        level_100 = max(0, min(100, raw & 0xFF))
        return round(level_100 * 255 / 100)

    @property
    def available(self) -> bool:
        device = self._device
        if not device:
            return False
        return device.get("Device_is_online", 1) == 1

    async def async_turn_on(self, **kwargs):
        if not self._supports_brightness:
            await self.coordinator.turn_device_on(self._device_mac)
            return

        if ATTR_BRIGHTNESS in kwargs:
            ha_level = kwargs[ATTR_BRIGHTNESS] or 0
            level_100 = round(max(0, min(255, ha_level)) * 100 / 255)
        else:
            current = self.brightness
            if current is None:
                level_100 = 100
            else:
                level_100 = round(max(0, min(255, current)) * 100 / 255)
                if level_100 == 0:
                    level_100 = 100

        await self.coordinator.set_device_brightness(self._device_mac, level_100)

    async def async_turn_off(self, **kwargs):
        if self._supports_brightness:
            await self.coordinator.set_device_brightness(self._device_mac, 0)
            return

        await self.coordinator.turn_device_off(self._device_mac)
