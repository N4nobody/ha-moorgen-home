import logging

from .const import API_INSTANCE, COORDINATOR, DOMAIN
from .coordinator import FurnitureLightsCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry):
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    _LOGGER.info(f"config entry is {config_entry.data}")
    coordinator = FurnitureLightsCoordinator(
        hass, config_entry)

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][COORDINATOR] = coordinator
    await hass.config_entries.async_forward_entry_setups(config_entry, ["button"])

    coordinator.async_add_listener(lambda: None)
    _LOGGER.info(f"main initialized")
    return True


async def async_unload_entry(hass, entry):
    """卸载 config entry 时调用"""
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "button")
    if unload_ok:
        hass.data[DOMAIN].pop(COORDINATOR)
    return unload_ok
