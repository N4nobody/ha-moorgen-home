import logging

from homeassistant.components.light import ColorMode, LightEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import COORDINATOR, DOMAIN
from .core.protocol.codec import infer_device_type

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinator = hass.data[DOMAIN][COORDINATOR]
    entities = []

    for device in coordinator.data["devices"]:
        if infer_device_type(device) != "light":
            continue

        device_mac = device.get("Device_Mac")
        device_name = device.get("Device_Name")
        if device_mac is None or not device_name:
            continue

        entities.append(MoorgenLightEntity(coordinator, device_mac, device_name))

    async_add_entities(entities)
    _LOGGER.info("%s lights initialized", len(entities))


class MoorgenLightEntity(CoordinatorEntity, LightEntity):
    _attr_supported_color_modes = {ColorMode.ONOFF}
    _attr_color_mode = ColorMode.ONOFF

    def __init__(self, coordinator, device_mac: int, name: str):
        super().__init__(coordinator, context=str(device_mac))
        self._device_mac = device_mac
        self._attr_unique_id = f"moorgen_light_{device_mac}"
        self._attr_name = name

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
    def available(self) -> bool:
        device = self._device
        if not device:
            return False
        return device.get("Device_is_online", 1) == 1

    async def async_turn_on(self, **kwargs):
        await self.coordinator.turn_device_on(self._device_mac)

    async def async_turn_off(self, **kwargs):
        await self.coordinator.turn_device_off(self._device_mac)
