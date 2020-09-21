"""Definition and setup of the Welland Canal Bridges Sensors for Home Assistant."""

import logging
import json

from datetime import timedelta

from homeassistant.components.sensor import ENTITY_ID_FORMAT
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.const import ATTR_NAME
import homeassistant.helpers.config_validation as cv
import homeassistant.util.dt as dt_util
from homeassistant.helpers.entity import Entity
from . import WellandCanalBridgeUpdater

from .const import COORDINATOR, DOMAIN, ATTR_IDENTIFIERS, ATTR_MANUFACTURER, ATTR_MODEL

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
        self._unique_id = ENTITY_ID_FORMAT.format("wellandcanalbridge_" + str(bridge.get("id")))
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
        return False

    @property
    def unique_id(self):
        """Return the unique Home Assistant friendly identifier for this entity."""
        return self._unique_id

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
        coordinator_data = json.loads(str(self.coordinator.data))
        bridge_list = coordinator_data.get("bridges")

        for bridge in bridge_list:
            if str(bridge.get("id")) == str(self._id):
                self.attrs["last_updated"] = bridge["status"].get("updated_at")

        return self.attrs

    @property
    def device_info(self):
        """Define the device based on device_identifier."""

        device_name = "Welland Canal Bridges"
        device_model = "Bridges"

        return {
            ATTR_IDENTIFIERS: {(DOMAIN, "wellandcanalbridges")},
            ATTR_NAME: device_name,
            ATTR_MANUFACTURER: "Saint Lawrence Seaway",
            ATTR_MODEL: device_model,
        }


    @property
    def is_on(self) -> bool:
        """Return the state."""
        coordinator_data = json.loads(str(self.coordinator.data))
        bridge_list = coordinator_data.get("bridges")

        for bridge in bridge_list:
            if str(bridge.get("id")) == str(self._id):
                self._state = self.bridge_state(int(bridge["status"].get("status_type")))

        return self._state

    def bridge_state(self, status_type):
        return status_type == 1

    async def async_update(self):
        """Update Welland Canal Bridge Entity."""
        await self.coordinator.async_request_refresh()
                
    async def async_added_to_hass(self):
        """Subscribe to updates."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
