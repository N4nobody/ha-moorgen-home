import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import COORDINATOR, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinator = hass.data[DOMAIN][COORDINATOR]
    scene_buttons = []

    for scene in coordinator.data["scenes"]:
        scene_buttons.append(VirtualSceneButton(coordinator, scene.name, scene.id))
    async_add_entities(scene_buttons)
    _LOGGER.info(f"{len(scene_buttons)} buttons initialized")


class VirtualSceneButton(CoordinatorEntity, ButtonEntity):
    def __init__(self, coordinator, name, unique_id):
        super().__init__(coordinator, context=unique_id)
        self._attr_name = name
        self._attr_unique_id = unique_id

    async def async_press(self):
        await self.coordinator.activate_scene(self._attr_unique_id)
        _LOGGER.info(f"Scene '{self._attr_name}' triggered")

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        super()._handle_coordinator_update()
