"""Definition and setup of the Welland Canal Bridges Sensors for Home Assistant."""

import logging
import json

from datetime import timedelta

from homeassistant.components.sensor import ENTITY_ID_FORMAT
from homeassistant.components.binary_sensor import BinarySensorEntity
import homeassistant.helpers.config_validation as cv
import homeassistant.util.dt as dt_util
from homeassistant.helpers.entity import Entity

from .const import COORDINATOR, DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities, discovery_info=None):
    """Set up the binary sensor platforms."""

    coordinator = hass.data[DOMAIN][entry.entry_id][COORDINATOR]
    bridges = []
    
    coordinator_data = json.loads(str(coordinator.data))
    bridge_list = coordinator_data.get("bridges")

    for bridge in bridge_list:
        bridges.append(WellandCanalBridge(coordinator, bridge))
    
    async_add_entities(bridges, update_before_add=True)

class WellandCanalBridge(BinarySensorEntity):
    """Defines a Welland Canal Bridge sensor."""

    def __init__(self, coordinator, bridge):
        """Initialize Entities."""

        bridgename = bridge.get("name") + " - " + bridge.get("location")
        if bridge.get("nickname") != "":
            bridgename = bridgename + " (" + bridge.get("nickname") + ")"
        
        self._name = bridgename
        self.entity_id = ENTITY_ID_FORMAT.format("wellandcanalbridge_" + str(bridge.get("id")))
        self._state = self.bridge_state(int(bridge["status"].get("status_type")))
        self._device_class = "door"
        self._icon = "mdi:bridge"
        self._id = str(bridge.get("id"))
        self.coordinator = coordinator
        self.attrs = {}
        self.attrs["bridge_id"] = str(bridge.get("id"))
        
    @property
    def should_poll(self):
        """Return the polling requirement of an entity."""
        return True

    @property
    def unique_id(self):
        """Return the unique Home Assistant friendly identifier for this entity."""
        return self.entity_id

    @property
    def name(self):
        """Return the friendly name of this entity."""
        return self._name

    @property
    def device_class(self):
        """Return the device class for this entity."""
        return self._device_class

    @property
    def icon(self):
        """Return the icon for this entity."""
        return self._icon

    @property
    def device_state_attributes(self):
        """Return the attributes."""
        return self.attrs

    @property
    def is_on(self) -> bool:
        """Return the state."""
        return self._state

    @property
    def device_info(self):
        """Define the device for the entity registry."""
        return {
            "identifiers": {DOMAIN, "wellandcanalniagara"},
            "name": "Welland Canal Bridges",
            "manufacturer": "St. Lawrence Seaway",
            "model": "Welland Canal",
        }

    def bridge_state(self, status_type):
        return status_type == 1

    async def async_update(self):
        """Update Welland Canal Bridge Entity."""
        await self.coordinator.async_request_refresh()
        _LOGGER.debug("Updating state of the sensors.")
        coordinator_data = json.loads(str(self.coordinator.data))
        bridge_list = coordinator_data.get("bridges")

        for bridge in bridge_list:
            if str(bridge.get("id")) == str(self._id):
                self.attrs["last_updated"] = bridge["status"].get("updated_at")
                self._state = self.bridge_state(int(bridge["status"].get("status_type")))
                
    async def async_added_to_hass(self):
        """Subscribe to updates."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
