import logging

from .const import COORDINATOR, DOMAIN
from .core.coordinator import FurnitureLightsCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry):
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    _LOGGER.info(f"config entry is {config_entry.data}")
    coordinator = FurnitureLightsCoordinator(hass, config_entry)

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][COORDINATOR] = coordinator
    await hass.config_entries.async_forward_entry_setups(config_entry, ["button"])

    _LOGGER.info("main initialized")
    return True


async def async_unload_entry(hass, entry):
    """Unload handler for a config entry."""
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "button")
    if not unload_ok:
        return False

    coordinator = hass.data.get(DOMAIN, {}).pop(COORDINATOR, None)
    if coordinator:
        await coordinator.async_shutdown()

    return True
